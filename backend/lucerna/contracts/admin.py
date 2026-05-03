from django.contrib import admin

from contracts.models import (
    ComplianceMetric,
    Contract,
    ContractAuditLog,
    ContractDeadline,
    OrganizationKpi,
    SpendSnapshot,
)


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ("contract_id", "title", "vendor", "value_usd", "risk", "clearance_required")
    search_fields = ("contract_id", "title", "vendor")


@admin.register(ContractDeadline)
class ContractDeadlineAdmin(admin.ModelAdmin):
    list_display = ("title", "contract", "due_date", "clearance_required")


@admin.register(ContractAuditLog)
class ContractAuditLogAdmin(admin.ModelAdmin):
    list_display = ("created_at", "action", "contract_ref", "actor")
    readonly_fields = ("created_at", "payload")


@admin.register(ComplianceMetric)
class ComplianceMetricAdmin(admin.ModelAdmin):
    list_display = ("category", "rate_pct")


@admin.register(SpendSnapshot)
class SpendSnapshotAdmin(admin.ModelAdmin):
    list_display = ("period", "obligated_usd", "sort_order")


@admin.register(OrganizationKpi)
class OrganizationKpiAdmin(admin.ModelAdmin):
    list_display = ("id", "compliance_rate_pct", "contractor_performance_score")
