"""Enterprise Identity Governance Platform engine."""
from __future__ import annotations

from collections import defaultdict
from datetime import UTC, datetime, timedelta

from contexts.identity_governance.domain.aggregates.identity_governance_platform import (
    AccessGrantStatus,
    CertificationStatus,
    IdentityGovernanceCapability,
    RequestStatus,
    ReviewStatus,
)

PLATFORM_CATALOG: dict[str, dict] = {
    IdentityGovernanceCapability.USER_LIFECYCLE.value: {
        "label": "User Lifecycle",
        "delegates_to": "identity",
        "no_duplication": True,
    },
    IdentityGovernanceCapability.ROLE_LIFECYCLE.value: {
        "label": "Role Lifecycle",
        "delegates_to": "identity",
        "no_duplication": True,
    },
    IdentityGovernanceCapability.ACCESS_REQUEST.value: {"label": "Access Request", "approval_required": True},
    IdentityGovernanceCapability.ACCESS_REVIEW.value: {"label": "Access Review", "periodic": True},
    IdentityGovernanceCapability.PRIVILEGE_REVIEW.value: {"label": "Privilege Review"},
    IdentityGovernanceCapability.SEGREGATION_OF_DUTIES.value: {
        "label": "Segregation of Duties",
        "enforcement": True,
    },
    IdentityGovernanceCapability.TEMPORARY_ACCESS.value: {
        "label": "Temporary Access",
        "time_limited": True,
    },
    IdentityGovernanceCapability.EMERGENCY_ACCESS.value: {
        "label": "Emergency Access",
        "delegates_to": "security_incident",
        "break_glass": True,
    },
    IdentityGovernanceCapability.CERTIFICATION.value: {"label": "Certification", "attestation": True},
    IdentityGovernanceCapability.APPROVAL.value: {
        "label": "Approval",
        "delegates_to": "workflow",
    },
    IdentityGovernanceCapability.AUDIT.value: {
        "label": "Audit",
        "delegates_to": "audit",
        "no_duplication": True,
    },
    IdentityGovernanceCapability.IDENTITY_DASHBOARD.value: {"label": "Identity Dashboard"},
}

POLICY_KEYS = [
    "identity_governance.access_review.frequency_days",
    "identity_governance.certification.required",
    "identity_governance.sod.enforcement",
    "identity_governance.temporary_access.max_hours",
    "identity_governance.emergency_access.max_hours",
]

SOD_CONFLICT_RULES: list[dict] = [
    {"roles": ["finance_approver", "finance_poster"], "reason": "Cannot approve and post transactions"},
    {"roles": ["treasury_operator", "treasury_approver"], "reason": "Cannot operate and approve treasury"},
    {"roles": ["audit_reviewer", "finance_poster"], "reason": "Cannot audit and post financial entries"},
    {"roles": ["admin", "audit_reviewer"], "reason": "Admin and audit reviewer separation"},
]

DEFAULT_SEED_ACCESS_REQUESTS: list[dict] = [
    {
        "target_user_id": "user-finance-1",
        "requested_roles": ["finance_viewer"],
        "justification": "Quarterly reporting access",
    },
    {
        "target_user_id": "user-treasury-1",
        "requested_roles": ["treasury_viewer"],
        "justification": "Treasury dashboard access",
    },
]


def list_capability_catalog() -> list[dict]:
    return [{"capability": k, **v} for k, v in PLATFORM_CATALOG.items()]


def list_policy_keys() -> list[str]:
    return list(POLICY_KEYS)


def list_sod_rules() -> list[dict]:
    return [{"rule_id": f"sod-{i+1}", **rule} for i, rule in enumerate(SOD_CONFLICT_RULES)]


def dependency_map() -> dict:
    nodes = [{"id": "identity_governance", "type": "platform", "label": "Identity Governance Platform"}]
    edges = []
    for mod in ("identity", "workflow", "audit", "security_incident", "security"):
        nodes.append({"id": mod, "type": "module", "label": mod})
        edges.append({"from": mod, "to": "identity_governance", "type": "supports_governance"})
    nodes.append({"id": "policy", "type": "shared_service", "label": "policy"})
    edges.append({"from": "identity_governance", "to": "policy", "type": "delegates"})
    return {"nodes": nodes, "edges": edges, "no_identity_duplication": True}


def check_segregation_of_duties(*, existing_roles: list[str], requested_roles: list[str]) -> dict:
    all_roles = set(existing_roles + requested_roles)
    conflicts = []
    for rule in SOD_CONFLICT_RULES:
        rule_roles = set(rule["roles"])
        if rule_roles.issubset(all_roles):
            conflicts.append({
                "roles": list(rule_roles),
                "reason": rule["reason"],
            })
    return {
        "valid": len(conflicts) == 0,
        "conflicts": conflicts,
        "roles_checked": list(all_roles),
    }


def compute_expiry(*, hours: int, from_time: datetime | None = None) -> str:
    base = from_time or datetime.now(UTC)
    return (base + timedelta(hours=hours)).isoformat()


def build_dashboard(
    *,
    profile: dict | None,
    access_requests: list[dict],
    access_reviews: list[dict],
    certifications: list[dict],
    temporary_grants: list[dict],
    emergency_grants: list[dict],
    audit_entries: list[dict],
) -> dict:
    pending_requests = [r for r in access_requests if r.get("status") == RequestStatus.PENDING.value]
    active_temp = [g for g in temporary_grants if g.get("status") == AccessGrantStatus.ACTIVE.value]
    active_emergency = [g for g in emergency_grants if g.get("status") == AccessGrantStatus.ACTIVE.value]
    pending_certs = [c for c in certifications if c.get("status") == CertificationStatus.PENDING.value]

    by_request_status: dict[str, int] = defaultdict(int)
    for req in access_requests:
        by_request_status[req.get("status", "unknown")] += 1

    return {
        "summary": {
            "capabilities": len(PLATFORM_CATALOG),
            "pending_access_requests": len(pending_requests),
            "active_access_reviews": len([r for r in access_reviews if r.get("status") == ReviewStatus.IN_PROGRESS.value]),
            "pending_certifications": len(pending_certs),
            "active_temporary_grants": len(active_temp),
            "active_emergency_grants": len(active_emergency),
            "audit_entries": len(audit_entries),
            "sod_enforcement": profile.get("sod_enforcement", True) if profile else True,
        },
        "by_request_status": dict(by_request_status),
        "recent_requests": sorted(access_requests, key=lambda r: r.get("created_at", ""), reverse=True)[:5],
        "recent_audit": sorted(audit_entries, key=lambda e: e.get("created_at", ""), reverse=True)[:5],
        "delegation": {
            "identity_user_role_management": True,
            "workflow_approval": True,
            "audit_trail": True,
            "local_identity_duplication": False,
        },
        "generated_at": datetime.now(UTC).isoformat(),
    }
