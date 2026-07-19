"""Implements IFederationTrustFacts for MEOS peer modules (P200-B2)."""
from __future__ import annotations

from contexts.identity_federation.application.commands.evaluate_trust import (
    EvaluateTrustCommand,
    handle_evaluate_trust,
)
from contexts.identity_federation.application.queries.get_trust_facts import (
    GetTrustFactsQuery,
    handle_get_trust_facts,
)
from contexts.identity_federation.domain.ports.federation_repositories import (
    IFederationSessionRepository,
)
from shared.application.ports.identity_federation import (
    FederationTrustFacts,
    IFederationTrustFacts,
)


class FederationTrustFactsClient(IFederationTrustFacts):
    def __init__(self, sessions: IFederationSessionRepository | None = None) -> None:
        self._sessions = sessions

    async def get_trust_facts(
        self,
        tenant_id: str,
        *,
        subject_id: str,
        federation_session_id: str | None = None,
    ) -> FederationTrustFacts:
        dto = await handle_get_trust_facts(
            GetTrustFactsQuery(
                tenant_id=tenant_id,
                subject_id=subject_id,
                federation_session_id=federation_session_id,
            ),
            sessions=self._sessions,
        )
        return dto.to_port()

    async def evaluate_trust(
        self,
        tenant_id: str,
        *,
        subject_id: str,
        subject_kind: str = "human",
        context: dict | None = None,
    ) -> FederationTrustFacts:
        ctx = context or {}
        dto = await handle_evaluate_trust(
            EvaluateTrustCommand(
                tenant_id=tenant_id,
                subject_id=subject_id,
                subject_kind=subject_kind,
                organization_trust=int(ctx.get("organization_trust", 50)),
                partner_trust=int(ctx.get("partner_trust", 50)),
                identity_trust=int(ctx.get("identity_trust", 50)),
                device_trust=int(ctx.get("device_trust", 50)),
                context=ctx,
            )
        )
        return dto.to_port()
