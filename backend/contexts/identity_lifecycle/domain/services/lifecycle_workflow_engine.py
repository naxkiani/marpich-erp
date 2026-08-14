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
    # Joiner-Mover-Leaver (P201-A1)
    LifecycleAction.JOINER.value: (
        frozenset({
            LifecycleState.DRAFT.value,
            LifecycleState.REGISTERED.value,
            LifecycleState.VERIFIED.value,
        }),
        LifecycleState.ACTIVE.value,
    ),
    LifecycleAction.MOVER.value: (
        frozenset({LifecycleState.ACTIVE.value}),
        LifecycleState.ACTIVE.value,
    ),
    LifecycleAction.TRANSFER.value: (
        frozenset({LifecycleState.ACTIVE.value}),
        LifecycleState.ACTIVE.value,
    ),
    LifecycleAction.ROLE_CHANGE.value: (
        frozenset({LifecycleState.ACTIVE.value}),
        LifecycleState.ACTIVE.value,
    ),
    LifecycleAction.LEAVER.value: (
        frozenset({
            LifecycleState.ACTIVE.value,
            LifecycleState.SUSPENDED.value,
            LifecycleState.TEMPORARILY_DISABLED.value,
            LifecycleState.UNDER_INVESTIGATION.value,
        }),
        LifecycleState.SOFT_DELETED.value,
    ),
    LifecycleAction.REHIRE.value: (
        frozenset({
            LifecycleState.SOFT_DELETED.value,
            LifecycleState.ARCHIVED.value,
            LifecycleState.RECOVERY_PENDING.value,
        }),
        LifecycleState.ACTIVE.value,
    ),
    LifecycleAction.PLACE_UNDER_INVESTIGATION.value: (
        frozenset({LifecycleState.ACTIVE.value, LifecycleState.SUSPENDED.value}),
        LifecycleState.UNDER_INVESTIGATION.value,
    ),
    LifecycleAction.REACTIVATION.value: (
        frozenset({
            LifecycleState.SUSPENDED.value,
            LifecycleState.TEMPORARILY_DISABLED.value,
            LifecycleState.RECOVERY_PENDING.value,
            LifecycleState.UNDER_INVESTIGATION.value,
        }),
        LifecycleState.ACTIVE.value,
    ),
}


def canonicalize_state(state: str) -> str:
    from contexts.identity_lifecycle.domain.aggregates.identity_lifecycle_platform import (
        STATE_ALIASES,
    )

    return STATE_ALIASES.get(state, state)


def list_workflow_actions() -> list[dict]:
    return [{"action": a.value, "label": a.name.replace("_", " ").title()} for a in LifecycleAction]


def list_lifecycle_states() -> list[dict]:
    return [{"state": s.value, "label": s.name.replace("_", " ").title()} for s in LifecycleState]


def list_jml_actions() -> list[dict]:
    jml = [
        LifecycleAction.JOINER,
        LifecycleAction.MOVER,
        LifecycleAction.LEAVER,
        LifecycleAction.TRANSFER,
        LifecycleAction.ROLE_CHANGE,
        LifecycleAction.REHIRE,
        LifecycleAction.PLACE_UNDER_INVESTIGATION,
    ]
    return [{"action": a.value, "label": a.name.replace("_", " ").title()} for a in jml]


def state_machine_surface() -> dict:
    from contexts.identity_lifecycle.domain.aggregates.identity_lifecycle_platform import (
        STATE_ALIASES,
    )

    return {
        "canonical_states": list_lifecycle_states(),
        "aliases": dict(STATE_ALIASES),
        "jml_actions": list_jml_actions(),
        "workflow_graph": build_workflow_graph(),
    }


def can_transition(current_state: str, action: str) -> bool:
    rule = WORKFLOW_RULES.get(action)
    if not rule:
        return False
    allowed_from, _ = rule
    return canonicalize_state(current_state) in allowed_from


def resolve_transition(current_state: str, action: str) -> str | None:
    rule = WORKFLOW_RULES.get(action)
    if not rule:
        return None
    allowed_from, to_state = rule
    current = canonicalize_state(current_state)
    if current not in allowed_from:
        return None
    return to_state


def build_workflow_graph() -> dict:
    from contexts.identity_lifecycle.domain.aggregates.identity_lifecycle_platform import (
        STATE_ALIASES,
    )

    nodes = [{"id": s.value, "label": s.name.replace("_", " ").title()} for s in LifecycleState]
    edges = []
    for action, (from_states, to_state) in WORKFLOW_RULES.items():
        for from_state in from_states:
            if from_state != to_state:
                edges.append({"from": from_state, "to": to_state, "action": action})
    return {"nodes": nodes, "edges": edges, "aliases": dict(STATE_ALIASES)}


def required_verifications_for_activation(kyc_required: bool, aml_required: bool) -> list[str]:
    base = ["email_verification"]
    if kyc_required:
        base.append("kyc")
    if aml_required:
        base.append("aml")
    return base
