from __future__ import annotations

from typing import Any

from django.forms.models import model_to_dict

from contracts.models import Contract, ContractAuditAction, ContractAuditLog


def log_contract_audit(
    *,
    contract: Contract,
    action: str,
    actor,
    before: dict[str, Any] | None = None,
    after: dict[str, Any] | None = None,
) -> ContractAuditLog:
    payload: dict[str, Any] = {}
    if before is not None:
        payload["before"] = before
    if after is not None:
        payload["after"] = after
    return ContractAuditLog.objects.create(
        contract_ref=contract.contract_id,
        contract_pk=contract.pk,
        action=action,
        actor=actor if getattr(actor, "is_authenticated", False) else None,
        payload=payload,
    )


def snapshot_contract(contract: Contract) -> dict[str, Any]:
    data = model_to_dict(
        contract,
        fields=[
            "contract_id",
            "title",
            "vendor",
            "value_usd",
            "risk",
            "risk_reason",
            "clearance_required",
        ],
    )
    data["value_usd"] = str(data["value_usd"])
    return data
