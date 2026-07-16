"""Lifecycle workflow engine — state machine and transition rules."""
from __future__ import annotations

from contexts.identity_lifecycle.domain.aggregates.identity_lifecycle_platform import (
    LifecycleAction,
    LifecycleState,
)

# Valid transitions: action -> (from_states, to_state)
WORKFLOW_RULES: dict[str, tuple[frozenset[str], str]] = {
    LifecycleAction.REGISTRATION.value: (frozenset({LifecycleState.DRAFT.value}), LifecycleState.REGISTERED.value),
    LifecycleAction.INVITATION.value: (frozenset({LifecycleState.DRAFT.value, LifecycleState.REGISTERED.value}), LifecycleState.INVITED.value),
    LifecycleAction.EMAIL_VERIFICATION.value: (
        frozenset({LifecycleState.REGISTERED.value, LifecycleState.INVITED.value, LifecycleState.PENDING_VERIFICATION.value}),
        LifecycleState.PENDING_VERIFICATION.value,
    ),
    LifecycleAction.PHONE_VERIFICATION.value: (
        frozenset({LifecycleState.PENDING_VERIFICATION.value}),
        LifecycleState.PENDING_VERIFICATION.value,
    ),
    LifecycleAction.GOVERNMENT_ID_VERIFICATION.value: (
        frozenset({LifecycleState.PENDING_VERIFICATION.value}),
        LifecycleState.PENDING_VERIFICATION.value,
    ),
    LifecycleAction.KYC.value: (
        frozenset({LifecycleState.PENDING_VERIFICATION.value}),
        LifecycleState.PENDING_VERIFICATION.value,
    ),
    LifecycleAction.AML.value: (
        frozenset({LifecycleState.PENDING_VERIFICATION.value, LifecycleState.VERIFIED.value}),
        LifecycleState.PENDING_VERIFICATION.value,
    ),
    LifecycleAction.BACKGROUND_VERIFICATION.value: (
        frozenset({LifecycleState.PENDING_VERIFICATION.value}),
        LifecycleState.PENDING_VERIFICATION.value,
    ),
    LifecycleAction.IDENTITY_VERIFICATION.value: (
        frozenset({LifecycleState.PENDING_VERIFICATION.value}),
        LifecycleState.VERIFIED.value,
    ),
    LifecycleAction.ACCOUNT_ACTIVATION.value: (
        frozenset({LifecycleState.VERIFIED.value, LifecycleState.REGISTERED.value}),
        LifecycleState.ACTIVE.value,
    ),
    LifecycleAction.SUSPENSION.value: (
        frozenset({LifecycleState.ACTIVE.value}),
        LifecycleState.SUSPENDED.value,
    ),
    LifecycleAction.TEMPORARY_DISABLE.value: (
        frozenset({LifecycleState.ACTIVE.value}),
        LifecycleState.TEMPORARILY_DISABLED.value,
    ),
    LifecycleAction.REACTIVATION.value: (
        frozenset({
            LifecycleState.SUSPENDED.value,
            LifecycleState.TEMPORARILY_DISABLED.value,
            LifecycleState.RECOVERY_PENDING.value,
        }),
        LifecycleState.ACTIVE.value,
    ),
    LifecycleAction.MERGE_IDENTITIES.value: (
        frozenset({LifecycleState.ACTIVE.value, LifecycleState.VERIFIED.value}),
        LifecycleState.MERGED.value,
    ),
    LifecycleAction.SPLIT_IDENTITY.value: (
        frozenset({LifecycleState.MERGED.value, LifecycleState.ACTIVE.value}),
        LifecycleState.ACTIVE.value,
    ),
    LifecycleAction.IDENTITY_ARCHIVE.value: (
        frozenset({LifecycleState.ACTIVE.value, LifecycleState.SUSPENDED.value, LifecycleState.TEMPORARILY_DISABLED.value}),
        LifecycleState.ARCHIVED.value,
    ),
    LifecycleAction.IDENTITY_RECOVERY.value: (
        frozenset({LifecycleState.ARCHIVED.value, LifecycleState.SOFT_DELETED.value}),
        LifecycleState.RECOVERY_PENDING.value,
    ),
    LifecycleAction.SOFT_DELETE.value: (
        frozenset({LifecycleState.ACTIVE.value, LifecycleState.SUSPENDED.value, LifecycleState.ARCHIVED.value, LifecycleState.RECOVERY_PENDING.value}),
        LifecycleState.SOFT_DELETED.value,
    ),
    LifecycleAction.HARD_DELETE.value: (
        frozenset({LifecycleState.SOFT_DELETED.value, LifecycleState.ARCHIVED.value}),
        LifecycleState.HARD_DELETED.value,
    ),
    LifecycleAction.IDENTITY_DELETION.value: (
        frozenset({LifecycleState.ACTIVE.value, LifecycleState.SUSPENDED.value}),
        LifecycleState.SOFT_DELETED.value,
    ),
    LifecycleAction.CONSENT_MANAGEMENT.value: (
        frozenset({
            LifecycleState.REGISTERED.value,
            LifecycleState.PENDING_VERIFICATION.value,
            LifecycleState.VERIFIED.value,
            LifecycleState.ACTIVE.value,
        }),
        LifecycleState.PENDING_VERIFICATION.value,
    ),
}


def list_workflow_actions() -> list[dict]:
    return [{"action": a.value, "label": a.name.replace("_", " ").title()} for a in LifecycleAction]


def list_lifecycle_states() -> list[dict]:
    return [{"state": s.value, "label": s.name.replace("_", " ").title()} for s in LifecycleState]


def can_transition(current_state: str, action: str) -> bool:
    rule = WORKFLOW_RULES.get(action)
    if not rule:
        return False
    allowed_from, _ = rule
    return current_state in allowed_from


def resolve_transition(current_state: str, action: str) -> str | None:
    rule = WORKFLOW_RULES.get(action)
    if not rule:
        return None
    allowed_from, to_state = rule
    if current_state not in allowed_from:
        return None
    return to_state


def build_workflow_graph() -> dict:
    nodes = [{"id": s.value, "label": s.name.replace("_", " ").title()} for s in LifecycleState]
    edges = []
    for action, (from_states, to_state) in WORKFLOW_RULES.items():
        for from_state in from_states:
            if from_state != to_state:
                edges.append({"from": from_state, "to": to_state, "action": action})
    return {"nodes": nodes, "edges": edges}


def required_verifications_for_activation(kyc_required: bool, aml_required: bool) -> list[str]:
    base = ["email_verification"]
    if kyc_required:
        base.append("kyc")
    if aml_required:
        base.append("aml")
    return base
