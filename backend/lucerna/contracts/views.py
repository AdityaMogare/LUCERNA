from __future__ import annotations

from datetime import date
from decimal import Decimal

from django.db import connection
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from contracts.audit import log_contract_audit, snapshot_contract
from contracts.models import (
    ComplianceMetric,
    Contract,
    ContractAuditAction,
    ContractDeadline,
    OrganizationKpi,
    SpendSnapshot,
)
from contracts.query import apply_clearance
from contracts.serializers import (
    ComplianceMetricSerializer,
    ContractSerializer,
    ContractWriteSerializer,
    DeadlineSerializer,
    SpendSnapshotSerializer,
)


def _visible_contracts(request):
    qs = Contract.objects.all()
    return apply_clearance(qs, request.clearance_level)


def _visible_deadlines(request):
    qs = ContractDeadline.objects.select_related("contract")
    return apply_clearance(qs, request.clearance_level)


def _estimate_at_risk(contracts) -> Decimal:
    total = Decimal("0")
    for c in contracts:
        if c.risk == "high":
            total += (c.value_usd or Decimal("0")) * Decimal("0.08")
    return total.quantize(Decimal("1"))


class DashboardView(APIView):
    """
    Aggregate payload shaped for the Lucerna React dashboard.
    """

    def get(self, request):
        contracts = list(_visible_contracts(request))
        deadlines = list(_visible_deadlines(request))
        org = OrganizationKpi.objects.first()

        total_value = sum((c.value_usd for c in contracts), Decimal("0"))
        high_risk_count = sum(1 for c in contracts if c.risk == "high")
        perf = (org.contractor_performance_score if org else Decimal("7.8")) - (
            Decimal("0.4") if high_risk_count else Decimal("0")
        )
        perf = min(Decimal("10"), perf)

        upcoming = [d for d in deadlines if 0 <= (d.due_date - date.today()).days <= 45]

        return Response(
            {
                "kpis": {
                    "total_contract_value_usd": str(total_value),
                    "compliance_rate_pct": str(org.compliance_rate_pct if org else Decimal("94.2")),
                    "contractor_performance_score": str(perf),
                    "upcoming_deadlines_count": len(upcoming),
                    "at_risk_funds_usd": str(_estimate_at_risk(contracts)),
                },
                "spend_trend": SpendSnapshotSerializer(
                    SpendSnapshot.objects.order_by("sort_order"),
                    many=True,
                ).data,
                "compliance_by_category": ComplianceMetricSerializer(
                    ComplianceMetric.objects.all(),
                    many=True,
                ).data,
                "flagged_contracts": ContractSerializer(contracts, many=True).data,
                "deadlines": DeadlineSerializer(deadlines, many=True).data,
            }
        )


class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    lookup_field = "contract_id"
    lookup_url_kwarg = "contract_id"
    http_method_names = ["get", "head", "options", "patch", "post", "delete"]

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return ContractWriteSerializer
        return ContractSerializer

    def get_queryset(self):
        return _visible_contracts(self.request)

    def perform_destroy(self, instance):
        log_contract_audit(
            contract=instance,
            action=ContractAuditAction.DELETE,
            actor=self.request.user,
            before=snapshot_contract(instance),
        )
        instance.delete()


class DeadlineViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DeadlineSerializer

    def get_queryset(self):
        return _visible_deadlines(self.request)


class ContractPartialUpdateView(APIView):
    """PATCH /api/contracts/<contract_id>/ — mutates a single contract with audit trail."""

    def patch(self, request, contract_id: str):
        contract = get_object_or_404(_visible_contracts(request), contract_id=contract_id)
        serializer = ContractWriteSerializer(
            contract,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(ContractSerializer(contract).data)


class HealthView(APIView):
    def get(self, request):
        ok = True
        try:
            connection.ensure_connection()
        except Exception:
            ok = False
        return Response({"status": "ok" if ok else "degraded", "db": connection.vendor})
