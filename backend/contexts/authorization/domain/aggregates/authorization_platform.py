"""Authorization PDP aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class AuthorizationCapability(StrEnum):
    RBAC_EVALUATION = "rbac_evaluation"
    ABAC_EVALUATION = "abac_evaluation"
    PBAC_EVALUATION = "pbac_evaluation"
    BATCH_CHECK = "batch_check"
    DECISION_SIMULATION = "decision_simulation"
    DECISION_AUDIT = "decision_audit"
    POLICY_DRIVEN_PDP = "policy_driven_pdp"
    AUTHORIZATION_DASHBOARD = "authorization_dashboard"


class DecisionEffect(StrEnum):
    ALLOW = "allow"
    DENY = "deny"


class AbacEffect(StrEnum):
    ALLOW = "allow"
    DENY = "deny"


@dataclass(eq=False, kw_only=True)
class AuthorizationProfile(AggregateRoot):
    tenant_id: str
    profile_ref: str
    rbac_enabled: bool = True
    abac_enabled: bool = True
    pbac_enabled: bool = True
    default_decision: str = "deny"
    decision_cache_ttl_seconds: int = 30
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(cls, *, tenant_id: str, profile_ref: str) -> AuthorizationProfile:
        return cls(id=UniqueId.generate(), tenant_id=tenant_id, profile_ref=profile_ref)

    def to_dict(self) -> dict:
        return {
            "profile_ref": self.profile_ref,
            "tenant_id": self.tenant_id,
            "rbac_enabled": self.rbac_enabled,
            "abac_enabled": self.abac_enabled,
            "pbac_enabled": self.pbac_enabled,
            "default_decision": self.default_decision,
            "decision_cache_ttl_seconds": self.decision_cache_ttl_seconds,
        }


@dataclass(eq=False, kw_only=True)
class AbacPolicy(AggregateRoot):
    tenant_id: str
    policy_ref: str
    name: str
    effect: str
    permission_pattern: str
    conditions: list[dict]
    priority: int = 100
    active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        policy_ref: str,
        name: str,
        effect: str,
        permission_pattern: str,
        conditions: list[dict],
        priority: int = 100,
    ) -> AbacPolicy:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            policy_ref=policy_ref,
            name=name,
            effect=effect,
            permission_pattern=permission_pattern,
            conditions=conditions,
            priority=priority,
        )

    def to_dict(self) -> dict:
        return {
            "policy_ref": self.policy_ref,
            "tenant_id": self.tenant_id,
            "name": self.name,
            "effect": self.effect,
            "permission_pattern": self.permission_pattern,
            "conditions": self.conditions,
            "priority": self.priority,
            "active": self.active,
        }


@dataclass(eq=False, kw_only=True)
class AccessDecision(AggregateRoot):
    tenant_id: str
    decision_ref: str
    principal_id: str
    permission_code: str
    resource: str
    action: str
    decision: str
    model: str
    reason_codes: list[str]
    policy_keys: list[str]
    obligations: list[str]
    facts: dict
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def record(
        cls,
        *,
        tenant_id: str,
        decision_ref: str,
        principal_id: str,
        permission_code: str,
        resource: str,
        action: str,
        decision: str,
        model: str,
        reason_codes: list[str],
        policy_keys: list[str],
        obligations: list[str],
        facts: dict,
    ) -> AccessDecision:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            decision_ref=decision_ref,
            principal_id=principal_id,
            permission_code=permission_code,
            resource=resource,
            action=action,
            decision=decision,
            model=model,
            reason_codes=reason_codes,
            policy_keys=policy_keys,
            obligations=obligations,
            facts=facts,
        )

    def to_dict(self) -> dict:
        return {
            "decision_ref": self.decision_ref,
            "tenant_id": self.tenant_id,
            "principal_id": self.principal_id,
            "permission_code": self.permission_code,
            "resource": self.resource,
            "action": self.action,
            "decision": self.decision,
            "model": self.model,
            "reason_codes": self.reason_codes,
            "policy_keys": self.policy_keys,
            "obligations": self.obligations,
            "facts": self.facts,
            "created_at": self.created_at.isoformat(),
        }
