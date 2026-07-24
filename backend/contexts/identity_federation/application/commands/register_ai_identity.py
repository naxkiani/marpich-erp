"""RegisterAIIdentity command (P200-B4)."""
from __future__ import annotations

from dataclasses import dataclass, field

from contexts.identity_federation.domain.factories import AiFederatedAgentFactory


@dataclass(frozen=True, slots=True)
class RegisterAIIdentityCommand:
    tenant_id: str
    agent_ref: str
    owner_principal_id: str
    display_name: str
    capabilities: list[str] = field(default_factory=list)
    correlation_id: str = ""


async def handle_register_ai_identity(command: RegisterAIIdentityCommand) -> dict:
    agent = AiFederatedAgentFactory.create(
        tenant_id=command.tenant_id,
        agent_ref=command.agent_ref,
        owner_principal_id=command.owner_principal_id,
        display_name=command.display_name,
        capabilities=command.capabilities,
        correlation_id=command.correlation_id,
    )
    events = [e.event_name for e in agent.domain_events]
    return {**agent.to_dict(), "domain_events": events}
