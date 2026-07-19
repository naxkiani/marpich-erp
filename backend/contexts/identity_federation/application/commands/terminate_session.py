"""TerminateSession command (P200-B4)."""
from __future__ import annotations

from dataclasses import dataclass

from contexts.identity_federation.domain.ports.federation_repositories import (
    IFederationSessionRepository,
)


@dataclass(frozen=True, slots=True)
class TerminateSessionCommand:
    tenant_id: str
    session_ref: str
    reason: str = "terminated"
    correlation_id: str = ""


async def handle_terminate_session(
    command: TerminateSessionCommand,
    *,
    sessions: IFederationSessionRepository,
) -> dict:
    session = await sessions.find_by_ref(command.tenant_id, command.session_ref)
    if session is None:
        raise ValueError("session.not_found")
    session.terminate(reason=command.reason, correlation_id=command.correlation_id)
    await sessions.save(session)
    events = [e.event_name for e in session.clear_events()]
    return {**session.to_dict(), "domain_events": events}
