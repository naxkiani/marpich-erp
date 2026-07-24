"""Factories for federation aggregates (P200-B4)."""
from __future__ import annotations

from contexts.identity_federation.domain.aggregates.ai_federated_agent import AiFederatedAgent
from contexts.identity_federation.domain.aggregates.federation_platform import (
    IdentityLink,
    IdentityProvider,
    TrustRelationship,
)
from shared.domain.value_objects.unique_id import UniqueId


class IdentityProviderFactory:
    @staticmethod
    def create(
        *,
        tenant_id: str,
        provider_ref: str,
        protocol: str,
        name: str,
        config: dict | None = None,
    ) -> IdentityProvider:
        return IdentityProvider.register(
            tenant_id=tenant_id,
            provider_ref=provider_ref,
            protocol=protocol,
            name=name,
            config=config,
        )


class TrustRelationshipFactory:
    @staticmethod
    def create_pending(
        *,
        tenant_id: str,
        trust_ref: str,
        source_entity_type: str,
        source_entity_id: str,
        target_entity_type: str,
        target_entity_id: str,
        trust_score: int = 50,
    ) -> TrustRelationship:
        return TrustRelationship(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            trust_ref=trust_ref,
            source_entity_type=source_entity_type,
            source_entity_id=source_entity_id,
            target_entity_type=target_entity_type,
            target_entity_id=target_entity_id,
            trust_score=trust_score,
            status="pending",
        )


class IdentityLinkFactory:
    @staticmethod
    def create(
        *,
        tenant_id: str,
        link_ref: str,
        user_id: str,
        provider_id: str,
        external_subject: str,
    ) -> IdentityLink:
        return IdentityLink(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            link_ref=link_ref,
            user_id=user_id,
            provider_id=provider_id,
            external_subject=external_subject,
            link_status="active",
        )


class AiFederatedAgentFactory:
    @staticmethod
    def create(
        *,
        tenant_id: str,
        agent_ref: str,
        owner_principal_id: str,
        display_name: str,
        capabilities: list[str] | None = None,
        correlation_id: str = "",
    ) -> AiFederatedAgent:
        return AiFederatedAgent.register(
            tenant_id=tenant_id,
            agent_ref=agent_ref,
            owner_principal_id=owner_principal_id,
            display_name=display_name,
            capabilities=capabilities or [],
            correlation_id=correlation_id,
        )
