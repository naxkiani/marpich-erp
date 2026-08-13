"""Unit — Identity Federation SoR postgres row reconstruction (no live DB)."""
from __future__ import annotations

from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from uuid import UUID

from contexts.identity_federation.domain.aggregates.federation_platform import (
    ClaimsMapping,
    FederationSession,
    IdentityLink,
    IdentityProvider,
    TrustRelationship,
)
from contexts.identity_federation.infrastructure.persistence import postgres_store as pg
from shared.domain.value_objects.unique_id import UniqueId


def test_provider_and_trust_from_row():
    provider = IdentityProvider.register(
        tenant_id="t1",
        provider_ref="idp-t1-0001",
        protocol="oidc",
        name="Corp IdP",
        config={"issuer": "https://idp.example"},
        plugin_id="plugin.oidc",
    )
    row = SimpleNamespace(
        id=UUID(str(provider.id)),
        tenant_id=provider.tenant_id,
        provider_ref=provider.provider_ref,
        protocol=provider.protocol,
        name=provider.name,
        config=provider.config,
        enabled=provider.enabled,
        plugin_id=provider.plugin_id,
        created_at=provider.created_at,
    )
    restored = pg._provider_from_row(row)
    assert restored.provider_ref == "idp-t1-0001"
    assert restored.plugin_id == "plugin.oidc"

    trust = TrustRelationship(
        id=UniqueId.generate(),
        tenant_id="t1",
        trust_ref="trust-t1-0001",
        source_entity_type="provider",
        source_entity_id=str(provider.id),
        target_entity_type="tenant",
        target_entity_id="t1",
        trust_score=80,
        trust_level="high",
        status="active",
        metadata={"note": "ok"},
    )
    trow = SimpleNamespace(
        id=UUID(str(trust.id)),
        tenant_id=trust.tenant_id,
        trust_ref=trust.trust_ref,
        source_entity_type=trust.source_entity_type,
        source_entity_id=trust.source_entity_id,
        target_entity_type=trust.target_entity_type,
        target_entity_id=trust.target_entity_id,
        trust_score=trust.trust_score,
        trust_level=trust.trust_level,
        status=trust.status,
        metadata_json=trust.metadata,
        valid_from=trust.valid_from,
        valid_until=None,
        created_at=trust.created_at,
    )
    assert pg._trust_from_row(trow).trust_score == 80


def test_claims_link_session_from_row():
    provider_id = UniqueId.generate()
    user_id = UniqueId.generate()
    mapping = ClaimsMapping(
        id=UniqueId.generate(),
        tenant_id="t1",
        mapping_ref="claim-map-t1-0001",
        provider_id=str(provider_id),
        source_claim="email",
        target_claim="user.email",
    )
    mrow = SimpleNamespace(
        id=UUID(str(mapping.id)),
        tenant_id=mapping.tenant_id,
        mapping_ref=mapping.mapping_ref,
        provider_id=UUID(mapping.provider_id),
        source_claim=mapping.source_claim,
        target_claim=mapping.target_claim,
        transform_type=mapping.transform_type,
        transform_config=mapping.transform_config,
        enabled=mapping.enabled,
        priority=mapping.priority,
    )
    assert pg._claims_from_row(mrow).source_claim == "email"

    link = IdentityLink(
        id=UniqueId.generate(),
        tenant_id="t1",
        link_ref="link-t1-0001",
        user_id=str(user_id),
        provider_id=str(provider_id),
        external_subject="ext-sub-1",
    )
    lrow = SimpleNamespace(
        id=UUID(str(link.id)),
        tenant_id=link.tenant_id,
        link_ref=link.link_ref,
        user_id=UUID(link.user_id),
        provider_id=UUID(link.provider_id),
        external_subject=link.external_subject,
        link_status=link.link_status,
        linked_at=link.linked_at,
        metadata_json={},
    )
    assert pg._link_from_row(lrow).external_subject == "ext-sub-1"

    now = datetime.now(UTC)
    sess = FederationSession(
        id=UniqueId.generate(),
        tenant_id="t1",
        session_ref="fed-sess-t1-0001",
        provider_id=str(provider_id),
        protocol="oidc",
        user_id=str(user_id),
        expires_at=now + timedelta(hours=1),
        created_at=now,
    )
    srow = SimpleNamespace(
        id=UUID(str(sess.id)),
        tenant_id=sess.tenant_id,
        session_ref=sess.session_ref,
        provider_id=UUID(sess.provider_id),
        protocol=sess.protocol,
        user_id=UUID(sess.user_id),
        idp_session_id=None,
        status=sess.status,
        expires_at=sess.expires_at,
        created_at=sess.created_at,
    )
    assert pg._session_from_row(srow).session_ref == "fed-sess-t1-0001"
