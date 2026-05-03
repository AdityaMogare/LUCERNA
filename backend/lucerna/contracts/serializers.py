from __future__ import annotations

from datetime import date

from rest_framework import serializers

from contracts.audit import log_contract_audit, snapshot_contract
from contracts.clearance import clearance_label
from contracts.models import (
    ComplianceMetric,
    Contract,
    ContractAuditAction,
    ContractDeadline,
    OrganizationKpi,
    SpendSnapshot,
)


class ContractSerializer(serializers.ModelSerializer):
    clearance_required_label = serializers.SerializerMethodField()

    class Meta:
        model = Contract
        fields = [
            "id",
            "contract_id",
            "title",
            "vendor",
            "value_usd",
            "risk",
            "risk_reason",
            "clearance_required",
            "clearance_required_label",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "clearance_required_label"]

    def get_clearance_required_label(self, obj: Contract) -> str:
        return clearance_label(int(obj.clearance_required))


class ContractWriteSerializer(ContractSerializer):
    def validate(self, attrs):
        request = self.context.get("request")
        level = int(getattr(request, "clearance_level", 0))
        new_clearance = attrs.get("clearance_required")
        if new_clearance is None and getattr(self, "instance", None):
            new_clearance = self.instance.clearance_required
        if new_clearance is not None and int(new_clearance) > level:
            raise serializers.ValidationError(
                {"clearance_required": "Cannot exceed session clearance."}
            )
        return attrs

    def create(self, validated_data):
        request = self.context.get("request")
        actor = getattr(request, "user", None)
        instance = super().create(validated_data)
        log_contract_audit(
            contract=instance,
            action=ContractAuditAction.CREATE,
            actor=actor,
            after=snapshot_contract(instance),
        )
        return instance

    def update(self, instance, validated_data):
        request = self.context.get("request")
        actor = getattr(request, "user", None)
        before = snapshot_contract(instance)
        instance = super().update(instance, validated_data)
        after = snapshot_contract(instance)
        log_contract_audit(
            contract=instance,
            action=ContractAuditAction.UPDATE,
            actor=actor,
            before=before,
            after=after,
        )
        return instance


class DeadlineSerializer(serializers.ModelSerializer):
    days_remaining = serializers.SerializerMethodField()
    clearance_required_label = serializers.SerializerMethodField()
    contract_id = serializers.CharField(source="contract.contract_id", read_only=True)

    class Meta:
        model = ContractDeadline
        fields = [
            "id",
            "contract",
            "contract_id",
            "title",
            "due_date",
            "days_remaining",
            "clearance_required",
            "clearance_required_label",
        ]
        read_only_fields = ["id", "clearance_required", "days_remaining", "clearance_required_label"]

    def get_days_remaining(self, obj: ContractDeadline) -> int:
        today = date.today()
        return (obj.due_date - today).days

    def get_clearance_required_label(self, obj: ContractDeadline) -> str:
        return clearance_label(int(obj.clearance_required))


class SpendSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpendSnapshot
        fields = ["period", "obligated_usd"]


class ComplianceMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplianceMetric
        fields = ["category", "rate_pct"]
