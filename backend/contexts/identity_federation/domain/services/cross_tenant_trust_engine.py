"""Cross-Tenant Trust facade — governed collaboration facts (P200-B8)."""
from __future__ import annotations

from contexts.identity_federation.domain.policies.federation_policies import CrossTenantTrustPolicy
from contexts.identity_federation.domain.services.trust_fabric_engine import get_trust_fabric_engine
from contexts.identity_federation.domain.value_objects.cross_tenant_vos import (
    DelegationType,
    ExternalIdentityKind,
    TenantTrustStatus,
)


class CrossTenantTrustEngine:
    """Produces cross-tenant governance facts — never Permit/Deny."""

    def __init__(self) -> None:
        self._policy = CrossTenantTrustPolicy()

    def assess_trust_request(
        self,
        *,
        cross_tenant_enabled: bool = True,
        inputs: dict | None = None,
        zero_trust_ctx: dict | None = None,
    ) -> dict:
        if not cross_tenant_enabled:
            return {
                "allowed_to_proceed": False,
                "reason": "cross_tenant_disabled",
                "permit_deny": None,
            }
        evaluation = get_trust_fabric_engine().evaluate_continuous(
            inputs=inputs or {},
            zero_trust_ctx=zero_trust_ctx or {},
        )
        # Default-deny until approved+active — assessment only advances workflow
        policy_ok = self._policy.allows(
            cross_tenant_enabled=cross_tenant_enabled, trust_status="active"
        )
        proceed = evaluation["trust_score"] >= 20
        return {
            "assessment": evaluation,
            "trust_score": evaluation["trust_score"],
            "trust_level": evaluation["enterprise_level"],
            "policy_active_would_allow": policy_ok,
            "allowed_to_proceed": proceed,
            "reason": None if proceed else "trust_score_below_request_threshold",
            "never_implicit": True,
            "permit_deny": None,
        }

    def access_gate(
        self,
        *,
        trust_status: str,
        cross_tenant_enabled: bool = True,
        expired: bool = False,
    ) -> dict:
        if expired:
            return {"allowed": False, "reason": "expired", "permit_deny": None}
        ok = self._policy.allows(
            cross_tenant_enabled=cross_tenant_enabled, trust_status=trust_status
        )
        return {
            "allowed": ok,
            "reason": "active_trust" if ok else "trust_not_active",
            "status": trust_status,
            "permit_deny": None,
        }

    def catalog(self) -> dict:
        return {
            "prompt": "P200-B8",
            "adr": 222,
            "trust_statuses": [s.value for s in TenantTrustStatus],
            "delegation_types": [d.value for d in DelegationType],
            "external_kinds": [e.value for e in ExternalIdentityKind],
            "principles": [
                "no_implicit_cross_tenant_trust",
                "mandatory_expiration",
                "tenant_isolation",
                "least_privilege_delegation",
                "continuous_trust_evaluation",
                "transparent_audit_history",
            ],
            "knowledge_graph": {
                "tenant_trusts_tenant": True,
                "organization_delegates_to": True,
                "ai_agent_authorized_by": True,
            },
        }


_engine: CrossTenantTrustEngine | None = None


def get_cross_tenant_trust_engine() -> CrossTenantTrustEngine:
    global _engine
    if _engine is None:
        _engine = CrossTenantTrustEngine()
    return _engine
