"""Enterprise journal engine — types, rules, workflow, versioning."""
from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from contexts.financial_kernel.domain.aggregates.journal import JournalStatus
from contexts.financial_kernel.domain.aggregates.journal_types import (
    JOURNAL_TYPE_RULES,
    JournalTypeRules,
)
from contexts.financial_kernel.domain.services.financial_workflow_engine import (
    generate_ai_recommendation,
    sign_workflow,
)


def get_journal_type_rules(journal_type: str) -> JournalTypeRules:
    rule = JOURNAL_TYPE_RULES.get(journal_type)
    if not rule:
        raise KeyError(f"unknown_journal_type:{journal_type}")
    return rule


def list_journal_types() -> list[dict]:
    return [
        {
            "journal_type": rule.journal_type,
            "label": rule.label,
            "journal_entry_type": rule.journal_entry_type,
            "approval_workflow_required": rule.approval_workflow_required,
            "digital_signature_required": rule.digital_signature_required,
            "ai_review_enabled": rule.ai_review_enabled,
            "automatic_posting_allowed": rule.automatic_posting_allowed,
            "batch_posting_allowed": rule.batch_posting_allowed,
            "rollback_allowed": rule.rollback_allowed,
            "lock_on_post": rule.lock_on_post,
            "versioning_enabled": rule.versioning_enabled,
            "default_posting_mode": rule.default_posting_mode,
            "description": rule.description,
        }
        for rule in JOURNAL_TYPE_RULES.values()
    ]


def resolve_journal_type(journal_type: str | None) -> str:
    if not journal_type:
        return "general"
    get_journal_type_rules(journal_type)
    return journal_type


def apply_type_posting_defaults(
    journal_type: str,
    *,
    require_approval: bool | None = None,
    posting_mode: str | None = None,
    journal_entry_type: str | None = None,
) -> dict:
    rules = get_journal_type_rules(journal_type)
    resolved_approval = (
        require_approval
        if require_approval is not None
        else rules.approval_workflow_required
    )
    resolved_mode = posting_mode or rules.default_posting_mode
    if not rules.automatic_posting_allowed and resolved_mode == "automatic":
        resolved_mode = "manual"
        if require_approval is None:
            resolved_approval = True
    return {
        "journal_type": journal_type,
        "require_approval": resolved_approval,
        "posting_mode": resolved_mode,
        "journal_entry_type": journal_entry_type or rules.journal_entry_type,
        "lock_on_post": rules.lock_on_post,
    }


def validate_journal_modifiable(*, status: str, is_locked: bool) -> tuple[bool, str]:
    if is_locked:
        return False, "journal_locked"
    if status in (JournalStatus.POSTED.value, JournalStatus.REVERSED.value):
        return False, "journal_immutable"
    return True, ""


def validate_rollback_allowed(journal_type: str) -> tuple[bool, str]:
    rules = get_journal_type_rules(journal_type)
    if not rules.rollback_allowed:
        return False, "rollback_not_allowed_for_type"
    return True, ""


def validate_batch_entry(journal_type: str) -> tuple[bool, str]:
    rules = get_journal_type_rules(journal_type)
    if not rules.batch_posting_allowed:
        return False, f"batch_not_allowed:{journal_type}"
    return True, ""


def validate_versioning_enabled(journal_type: str) -> tuple[bool, str]:
    rules = get_journal_type_rules(journal_type)
    if not rules.versioning_enabled:
        return False, "versioning_not_enabled"
    return True, ""


def validate_signature_required(*, journal_type: str, has_signature: bool) -> tuple[bool, str]:
    rules = get_journal_type_rules(journal_type)
    if rules.digital_signature_required and not has_signature:
        return False, "digital_signature_required"
    return True, ""


def review_journal_with_ai(*, journal: dict) -> dict:
    total = max(journal.get("total_debits", 0), journal.get("total_credits", 0))
    review = generate_ai_recommendation(
        workflow_type=journal.get("journal_type", "general"),
        amount=total,
        currency=journal.get("currency", "USD"),
        metadata={
            "journal_id": journal.get("id"),
            "line_count": len(journal.get("lines", [])),
            "status": journal.get("status"),
        },
    )
    review["journal_id"] = journal.get("id")
    review["journal_type"] = journal.get("journal_type", "general")
    review["review_type"] = "journal_ai_review"
    return review


def sign_journal_entry(*, journal_id: str, journal_type: str, signer_id: str) -> dict:
    return sign_workflow(
        workflow_id=journal_id,
        workflow_type=f"journal:{journal_type}",
        signer_id=signer_id,
    )


def build_batch_id() -> str:
    return f"batch-{uuid4().hex[:12]}"


def enrich_journal_dict(journal_dict: dict, rules: JournalTypeRules) -> dict:
    enriched = dict(journal_dict)
    enriched["journal_type_rules"] = {
        "approval_workflow_required": rules.approval_workflow_required,
        "digital_signature_required": rules.digital_signature_required,
        "ai_review_enabled": rules.ai_review_enabled,
        "automatic_posting_allowed": rules.automatic_posting_allowed,
        "batch_posting_allowed": rules.batch_posting_allowed,
        "rollback_allowed": rules.rollback_allowed,
        "lock_on_post": rules.lock_on_post,
        "versioning_enabled": rules.versioning_enabled,
    }
    return enriched


def lock_timestamp() -> datetime:
    return datetime.now(UTC)
