"""Enterprise financial audit engine — immutable history, tamper chain, lifecycle."""
from __future__ import annotations

import hashlib
import hmac
import json
from datetime import UTC, datetime

from contexts.financial_kernel.domain.aggregates.financial_audit import FinancialAuditAction

AUDIT_CATALOG: dict[str, dict] = {
    FinancialAuditAction.CREATED.value: {
        "label": "Who Created",
        "field": "created_by",
        "description": "Actor who created the financial record",
    },
    FinancialAuditAction.APPROVED.value: {
        "label": "Who Approved",
        "field": "approved_by",
        "description": "Actor who approved the transaction",
    },
    FinancialAuditAction.POSTED.value: {
        "label": "Who Posted",
        "field": "posted_by",
        "description": "Actor who posted to the general ledger",
    },
    FinancialAuditAction.MODIFIED.value: {
        "label": "Who Modified",
        "field": "modified_by",
        "description": "Actor who modified a draft or pending record",
    },
    FinancialAuditAction.REVERSED.value: {
        "label": "Who Reversed",
        "field": "reversed_by",
        "description": "Actor who reversed a posted transaction",
    },
}

TAMPER_SECRET = "marpich-fin-audit-tamper-v1"
DELETION_FORBIDDEN = True


def list_audit_catalog() -> list[dict]:
    tracked_fields = [
        "who_created",
        "who_approved",
        "who_posted",
        "who_modified",
        "who_reversed",
        "timestamp",
        "device",
        "ip",
        "tenant",
        "organization",
        "reason",
    ]
    return [
        {
            "actions": list(AUDIT_CATALOG.keys()),
            "tracked_fields": tracked_fields,
            "immutable": True,
            "deletion_allowed": False,
        }
    ]


def checksum_payload(payload: dict) -> str:
    data = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(data.encode()).hexdigest()


def compute_audit_tamper_hash(
    *,
    action: str,
    actor_id: str,
    resource_id: str,
    payload_checksum: str,
    previous_hash: str | None = None,
) -> str:
    chain = previous_hash or "genesis"
    payload = f"{chain}:{action}:{actor_id}:{resource_id}:{payload_checksum}"
    return hmac.new(TAMPER_SECRET.encode(), payload.encode(), hashlib.sha256).hexdigest()


def verify_audit_tamper(
    *,
    tamper_hash: str,
    action: str,
    actor_id: str,
    resource_id: str,
    payload_checksum: str,
    previous_hash: str | None = None,
) -> bool:
    expected = compute_audit_tamper_hash(
        action=action,
        actor_id=actor_id,
        resource_id=resource_id,
        payload_checksum=payload_checksum,
        previous_hash=previous_hash,
    )
    return hmac.compare_digest(tamper_hash, expected)


def assert_deletion_forbidden() -> None:
    if DELETION_FORBIDDEN:
        raise PermissionError("financial_audit_deletion_forbidden")


def build_lifecycle_history(entries: list[dict]) -> dict:
    sorted_entries = sorted(entries, key=lambda e: e.get("occurred_at", ""))
    lifecycle = {
        "who_created": None,
        "who_approved": None,
        "who_posted": None,
        "who_modified": None,
        "who_reversed": None,
        "created_at": None,
        "approved_at": None,
        "posted_at": None,
        "modified_at": None,
        "reversed_at": None,
        "tenant": None,
        "organization": None,
        "entries": sorted_entries,
    }
    action_map = {
        FinancialAuditAction.CREATED.value: ("who_created", "created_at"),
        FinancialAuditAction.APPROVED.value: ("who_approved", "approved_at"),
        FinancialAuditAction.POSTED.value: ("who_posted", "posted_at"),
        FinancialAuditAction.MODIFIED.value: ("who_modified", "modified_at"),
        FinancialAuditAction.REVERSED.value: ("who_reversed", "reversed_at"),
    }
    for entry in sorted_entries:
        action = entry.get("action", "")
        actor = entry.get("actor_id")
        ts = entry.get("occurred_at")
        if lifecycle["tenant"] is None:
            lifecycle["tenant"] = entry.get("tenant_id")
        if lifecycle["organization"] is None:
            lifecycle["organization"] = entry.get("organization_id")
        if action in action_map:
            who_field, when_field = action_map[action]
            if lifecycle[who_field] is None:
                lifecycle[who_field] = actor
                lifecycle[when_field] = ts
    return lifecycle


def build_immutable_audit_report(
    *,
    resource_type: str,
    resource_id: str,
    entries: list[dict],
    chain_valid: bool,
) -> dict:
    lifecycle = build_lifecycle_history(entries)
    return {
        "resource_type": resource_type,
        "resource_id": resource_id,
        "immutable": True,
        "deletion_allowed": False,
        "entry_count": len(entries),
        "chain_valid": chain_valid,
        "lifecycle": lifecycle,
        "tracked": {
            "who_created": lifecycle["who_created"],
            "who_approved": lifecycle["who_approved"],
            "who_posted": lifecycle["who_posted"],
            "who_modified": lifecycle["who_modified"],
            "who_reversed": lifecycle["who_reversed"],
            "tenant": lifecycle["tenant"],
            "organization": lifecycle["organization"],
        },
        "entries": entries,
        "generated_at": datetime.now(UTC).isoformat(),
    }


def verify_audit_chain(entries: list[dict]) -> tuple[bool, list[dict]]:
    sorted_entries = sorted(entries, key=lambda e: e.get("occurred_at", ""))
    previous_hash: str | None = None
    issues: list[dict] = []
    for entry in sorted_entries:
        valid = verify_audit_tamper(
            tamper_hash=entry["tamper_hash"],
            action=entry["action"],
            actor_id=entry["actor_id"],
            resource_id=entry["resource_id"],
            payload_checksum=entry["payload_checksum"],
            previous_hash=previous_hash,
        )
        if not valid:
            issues.append(
                {
                    "entry_id": entry.get("id"),
                    "error": "tamper_chain_broken",
                }
            )
        previous_hash = entry["tamper_hash"]
    return len(issues) == 0, issues
