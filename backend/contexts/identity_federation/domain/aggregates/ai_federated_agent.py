"""AI Federated Agent aggregate — first-class AI identity (P200-B4)."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from contexts.identity_federation.domain.events.federation_domain_events import (
    AIIdentityRegistered,
    AIIdentityRevoked,
)
from contexts.identity_federation.domain.policies.federation_policies import AiAgentMustHaveOwnerPolicy
from contexts.identity_federation.domain.value_objects.federation_vos import RiskLevel
from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class AiFederatedAgent(AggregateRoot):
    tenant_id: str
    agent_ref: str
    owner_principal_id: str
    display_name: str
    capabilities: list[str] = field(default_factory=list)
    execution_scopes: list[str] = field(default_factory=list)
    risk_level: str = RiskLevel.MEDIUM.value
    status: str = "active"
    trust_score: int = 50
    metadata: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    revoked_at: datetime | None = None

    @classmethod
    def register(
        cls,
        *,
        tenant_id: str,
        agent_ref: str,
        owner_principal_id: str,
        display_name: str,
        capabilities: list[str] | None = None,
        correlation_id: str = "",
    ) -> AiFederatedAgent:
        if not AiAgentMustHaveOwnerPolicy().allows(owner_principal_id):
            raise ValueError("ai_agent.owner_required")
        agent = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            agent_ref=agent_ref,
            owner_principal_id=owner_principal_id,
            display_name=display_name,
            capabilities=list(capabilities or []),
        )
        agent._raise(
            AIIdentityRegistered(
                aggregate_id=agent.id,
                tenant_id=TenantId(tenant_id),
                correlation_id=correlation_id or agent_ref,
                agent_ref=agent_ref,
                owner_principal_id=owner_principal_id,
            )
        )
        return agent

    def update_capabilities(self, capabilities: list[str]) -> None:
        if self.status != "active":
            raise ValueError("ai_agent.not_active")
        self.capabilities = list(dict.fromkeys(capabilities))

    def revoke(self, *, reason: str = "", correlation_id: str = "") -> None:
        if self.status == "revoked":
            return
        self.status = "revoked"
        self.revoked_at = datetime.now(UTC)
        self._raise(
            AIIdentityRevoked(
                aggregate_id=self.id,
                tenant_id=TenantId(self.tenant_id),
                correlation_id=correlation_id or self.agent_ref,
                agent_ref=self.agent_ref,
                reason=reason,
            )
        )

    def to_dict(self) -> dict:
        return {
            "agent_ref": self.agent_ref,
            "owner_principal_id": self.owner_principal_id,
            "display_name": self.display_name,
            "capabilities": self.capabilities,
            "execution_scopes": self.execution_scopes,
            "risk_level": self.risk_level,
            "status": self.status,
            "trust_score": self.trust_score,
            "metadata": self.metadata,
        }
