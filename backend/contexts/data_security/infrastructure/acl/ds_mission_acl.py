"""ACL: Data Security mission/scope ↔ peers (P211-B)."""
from __future__ import annotations

from typing import Any


def to_consent(*, tenant_id: str, subject_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "subject_ref": subject_ref,
        "via_consent": True,
        "privacy_responsibilities_clear_required": True,
        "consent_ledger_owned_by_consent": True,
        "peer_ids_only": True,
    }


def to_authorization(
    *, tenant_id: str, principal_ref: str, action: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "principal_ref": principal_ref,
        "action": action,
        "via_p208": True,
        "zero_trust_data_access": True,
        "peer_ids_only": True,
    }


def to_secrets(*, tenant_id: str, key_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "key_ref": key_ref,
        "via_p209": True,
        "crypto_owned_by_secrets": True,
        "peer_ids_only": True,
    }


def to_cyber_security(
    *, tenant_id: str, signal_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "signal_ref": signal_ref,
        "via_p210": True,
        "threat_defense_owned_by_cyber_security": True,
        "peer_ids_only": True,
    }


def to_identity_intelligence(
    *, tenant_id: str, identity_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "identity_ref": identity_ref,
        "via_p207": True,
        "peer_ids_only": True,
    }


def to_governance_board(
    *, tenant_id: str, board_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "board_ref": board_ref,
        "governance_model_complete_required": True,
        "ownership_model_required": True,
        "peer_ids_only": True,
    }
