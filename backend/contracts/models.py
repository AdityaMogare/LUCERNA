from __future__ import annotations

from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils import timezone

from accounts.models import Clearance


class Risk(models.TextChoices):
    HIGH = "high", "High"
    MEDIUM = "medium", "Medium"
    LOW = "low", "Low"


class Contract(models.Model):
    contract_id = models.CharField(max_length=32, unique=True, db_index=True)
    title = models.CharField(max_length=255)
    vendor = models.CharField(max_length=255)
    value_usd = models.DecimalField(max_digits=18, decimal_places=2)
    risk = models.CharField(max_length=16, choices=Risk.choices, default=Risk.MEDIUM)
    risk_reason = models.TextField(blank=True)
    clearance_required = models.PositiveSmallIntegerField(choices=Clearance.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "contracts_contract"
        ordering = ["-updated_at"]

    def __str__(self) -> str:
        return f"{self.contract_id} — {self.title}"


class ContractDeadline(models.Model):
    contract = models.ForeignKey(
        Contract,
        on_delete=models.CASCADE,
        related_name="deadlines",
    )
    title = models.CharField(max_length=255)
    due_date = models.DateField()
    clearance_required = models.PositiveSmallIntegerField(choices=Clearance.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "contracts_deadline"
        ordering = ["due_date"]

    def save(self, *args, **kwargs) -> None:
        if self.contract_id:
            self.clearance_required = self.contract.clearance_required
        super().save(*args, **kwargs)


class ContractAuditAction(models.TextChoices):
    CREATE = "create", "Create"
    UPDATE = "update", "Update"
    DELETE = "delete", "Delete"


class ContractAuditLog(models.Model):
    contract_ref = models.CharField(
        max_length=32,
        db_index=True,
        help_text="contract_id at time of event (row may be deleted).",
    )
    contract_pk = models.IntegerField(null=True, blank=True)
    action = models.CharField(max_length=16, choices=ContractAuditAction.choices)
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contract_audit_events",
    )
    payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        db_table = "contracts_auditlog"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.action} {self.contract_ref} @ {self.created_at:%Y-%m-%d %H:%M}"


class ComplianceMetric(models.Model):
    category = models.CharField(max_length=128, unique=True)
    rate_pct = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        db_table = "contracts_compliancemetric"
        ordering = ["category"]


class SpendSnapshot(models.Model):
    sort_order = models.PositiveSmallIntegerField(default=0)
    period = models.CharField(max_length=16)
    obligated_usd = models.DecimalField(max_digits=18, decimal_places=2)

    class Meta:
        db_table = "contracts_spendsnapshot"
        ordering = ["sort_order"]


class OrganizationKpi(models.Model):
    """Org rollup row for KPIs not derived from contracts (seed one row)."""

    compliance_rate_pct = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("0"))
    contractor_performance_score = models.DecimalField(
        max_digits=3, decimal_places=1, default=Decimal("0")
    )

    class Meta:
        db_table = "contracts_organizationkpi"
