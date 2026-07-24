"""Read trust facts for a subject/session — port-facing query."""
from __future__ import annotations

from dataclasses import dataclass

from contexts.identity_federation.application.commands.evaluate_trust import (
    EvaluateTrustCommand,
    handle_evaluate_trust,
)
from contexts.identity_federation.application.dto.trust_facts import TrustFactsDTO
from contexts.identity_federation.domain.ports.federation_repositories import (
    IFederationSessionRepository,
)


@dataclass(frozen=True, slots=True)
class GetTrustFactsQuery:
    tenant_id: str
    subject_id: str
    federation_session_id: str | None = None


async def handle_get_trust_facts(
    query: GetTrustFactsQuery,
    *,
    sessions: IFederationSessionRepository | None = None,
) -> TrustFactsDTO:
    ctx: dict = {"federation_session_id": query.federation_session_id}
    if sessions is not None and query.federation_session_id:
        session = await sessions.find_by_ref(query.tenant_id, query.federation_session_id)
        if session is not None:
            data = session.to_dict() if hasattr(session, "to_dict") else {}
            ctx["provider_id"] = data.get("provider_ref") or data.get("provider_id")
            ctx["identity_link_id"] = data.get("identity_link_id")
            subject_id = str(data.get("user_id") or query.subject_id)
            return await handle_evaluate_trust(
                EvaluateTrustCommand(
                    tenant_id=query.tenant_id,
                    subject_id=subject_id,
                    context=ctx,
                )
            )
    return await handle_evaluate_trust(
        EvaluateTrustCommand(
            tenant_id=query.tenant_id,
            subject_id=query.subject_id,
            context=ctx,
        )
    )
