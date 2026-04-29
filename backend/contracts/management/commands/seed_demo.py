from __future__ import annotations

from datetime import date
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from accounts.models import Clearance
from contracts.models import (
    ComplianceMetric,
    Contract,
    ContractDeadline,
    OrganizationKpi,
    Risk,
    SpendSnapshot,
)


class Command(BaseCommand):
    help = "Load demo contracts, deadlines, and dashboard reference data (idempotent)."

    @transaction.atomic
    def handle(self, *args, **options):
        kpi = OrganizationKpi.objects.first()
        if kpi is None:
            OrganizationKpi.objects.create(
                compliance_rate_pct=Decimal("94.20"),
                contractor_performance_score=Decimal("7.8"),
            )
        else:
            kpi.compliance_rate_pct = Decimal("94.20")
            kpi.contractor_performance_score = Decimal("7.8")
            kpi.save(update_fields=["compliance_rate_pct", "contractor_performance_score"])

        metrics = [
            ("FAR clauses", Decimal("97.00")),
            ("DFARS", Decimal("92.00")),
            ("Small business", Decimal("89.00")),
            ("Cyber (CMMC)", Decimal("96.00")),
            ("Environmental", Decimal("91.00")),
        ]
        for category, rate in metrics:
            ComplianceMetric.objects.update_or_create(
                category=category,
                defaults={"rate_pct": rate},
            )

        spend = [
            (0, "Oct", Decimal("42000000")),
            (1, "Nov", Decimal("48500000")),
            (2, "Dec", Decimal("51200000")),
            (3, "Jan", Decimal("55800000")),
            (4, "Feb", Decimal("61100000")),
            (5, "Mar", Decimal("67400000")),
        ]
        for order, period, amt in spend:
            SpendSnapshot.objects.update_or_create(
                period=period,
                defaults={"sort_order": order, "obligated_usd": amt},
            )

        demo_contracts = [
            {
                "contract_id": "c-1042",
                "title": "Aircraft sustainment — Lot 7",
                "vendor": "AeroDyne Systems",
                "value_usd": Decimal("22500000"),
                "risk": Risk.HIGH,
                "risk_reason": "Option period lapses in 18 days; funds uncommitted.",
                "clearance_required": Clearance.SECRET,
            },
            {
                "contract_id": "c-0891",
                "title": "Base IT modernization",
                "vendor": "Nexus Federal LLC",
                "value_usd": Decimal("8200000"),
                "risk": Risk.MEDIUM,
                "risk_reason": "Deliverable variance >15% vs. plan; CLIN re-alignment pending.",
                "clearance_required": Clearance.CONFIDENTIAL,
            },
            {
                "contract_id": "c-1203",
                "title": "Range operations support",
                "vendor": "Highland Logistics",
                "value_usd": Decimal("3100000"),
                "risk": Risk.LOW,
                "risk_reason": "Approaching funding ceiling; modification draft in review.",
                "clearance_required": Clearance.UNCLASSIFIED,
            },
            {
                "contract_id": "c-0777",
                "title": "Secure communications refresh",
                "vendor": "Cipher Ridge Corp",
                "value_usd": Decimal("41000000"),
                "risk": Risk.HIGH,
                "risk_reason": "CDRL overdue; COR escalation recommended.",
                "clearance_required": Clearance.TOP_SECRET,
            },
        ]

        for row in demo_contracts:
            Contract.objects.update_or_create(
                contract_id=row["contract_id"],
                defaults={k: v for k, v in row.items() if k != "contract_id"},
            )

        c1042 = Contract.objects.get(contract_id="c-1042")
        c0891 = Contract.objects.get(contract_id="c-0891")
        c1203 = Contract.objects.get(contract_id="c-1203")
        c0777 = Contract.objects.get(contract_id="c-0777")

        deadlines = [
            (c1042, "Option exercise decision", date(2026, 5, 17), Clearance.SECRET),
            (c0891, "Monthly progress report", date(2026, 5, 2), Clearance.CONFIDENTIAL),
            (c1203, "Funding realignment package", date(2026, 5, 28), Clearance.UNCLASSIFIED),
            (c0777, "CDRL A012 submission", date(2026, 4, 30), Clearance.TOP_SECRET),
        ]
        for contract, title, due, clr in deadlines:
            ContractDeadline.objects.update_or_create(
                contract=contract,
                title=title,
                defaults={"due_date": due, "clearance_required": clr},
            )

        self.stdout.write(self.style.SUCCESS("Demo data ready."))
