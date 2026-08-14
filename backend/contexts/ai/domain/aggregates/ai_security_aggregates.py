"""P214-I aggregates — quality-gate invariants."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


def _tid(tenant_id: str, code: str) -> str:
    if not tenant_id.strip():
        raise ValueError(code)
    return tenant_id.strip()


@dataclass(eq=False, kw_only=True)
class AiSecurityPlatformRoot(AggregateRoot):
    tenant_id: str
    platform_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, platform_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aisec.tenant_required")
        if not present:
            raise ValueError(
                "ai.aisec.enterprise_ai_security_platform_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            platform_ref=platform_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("AIAssetRegisteredEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class ModelSecurityRoot(AggregateRoot):
    tenant_id: str
    model_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, model_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aisec.model_tenant_required")
        if not present:
            raise ValueError("ai.aisec.ai_model_security_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            model_ref=model_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("ModelIntegrityVerifiedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class LlmSecurityRoot(AggregateRoot):
    tenant_id: str
    llm_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, llm_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aisec.llm_tenant_required")
        if not present:
            raise ValueError("ai.aisec.llm_security_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            llm_ref=llm_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("PromptAttackDetectedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class PromptSecurityRoot(AggregateRoot):
    tenant_id: str
    prompt_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, prompt_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aisec.prompt_tenant_required")
        if not present:
            raise ValueError("ai.aisec.prompt_security_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            prompt_ref=prompt_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("PromptAttackDetectedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class AgentSecurityRoot(AggregateRoot):
    tenant_id: str
    agent_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, agent_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aisec.agent_tenant_required")
        if not present:
            raise ValueError("ai.aisec.agent_security_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            agent_ref=agent_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("AgentBlockedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class AdversarialDefenseRoot(AggregateRoot):
    tenant_id: str
    defense_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, defense_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aisec.adversarial_tenant_required")
        if not present:
            raise ValueError("ai.aisec.adversarial_defense_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            defense_ref=defense_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("AIThreatDetectedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present
