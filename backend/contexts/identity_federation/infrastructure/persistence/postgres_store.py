"""PostgreSQL repositories — Identity Federation SoR (EIFTP core path)."""
from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select

from contexts.identity_federation.domain.aggregates.federation_platform import (
    ClaimsMapping,
    FederationSession,
    IdentityLink,
    IdentityProvider,
    TrustRelationship,
)
from contexts.identity_federation.domain.ports.federation_repositories import (
    IClaimsMappingRepository,
    IFederationSessionRepository,
    IIdentityLinkRepository,
    IIdentityProviderRepository,
    ITrustRelationshipRepository,
)
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.database.engine import session_scope
from shared.infrastructure.database.orm import (
    FederationClaimsMappingRow,
    FederationIdentityLinkRow,
    FederationIdentityProviderRow,
    FederationRefCounterRow,
    FederationSessionRow,
    FederationTrustRelationshipRow,
)


def _uuid(value: UniqueId | str | UUID) -> UUID:
    if isinstance(value, UUID):
        return value
    return UUID(str(value))


def _provider_from_row(row: FederationIdentityProviderRow) -> IdentityProvider:
    return IdentityProvider(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        provider_ref=row.provider_ref,
        protocol=row.protocol,
        name=row.name,
        config=dict(row.config or {}),
        enabled=bool(row.enabled),
        plugin_id=row.plugin_id,
        created_at=row.created_at or datetime.now(UTC),
    )


def _trust_from_row(row: FederationTrustRelationshipRow) -> TrustRelationship:
    return TrustRelationship(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        trust_ref=row.trust_ref,
        source_entity_type=row.source_entity_type,
        source_entity_id=row.source_entity_id,
        target_entity_type=row.target_entity_type,
        target_entity_id=row.target_entity_id,
        trust_score=int(row.trust_score),
        trust_level=row.trust_level,
        status=row.status,
        metadata=dict(row.metadata_json or {}),
        valid_from=row.valid_from or datetime.now(UTC),
        valid_until=row.valid_until,
        created_at=row.created_at or datetime.now(UTC),
    )


def _claims_from_row(row: FederationClaimsMappingRow) -> ClaimsMapping:
    return ClaimsMapping(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        mapping_ref=row.mapping_ref,
        provider_id=str(row.provider_id),
        source_claim=row.source_claim,
        target_claim=row.target_claim,
        transform_type=row.transform_type,
        transform_config=dict(row.transform_config or {}),
        enabled=bool(row.enabled),
        priority=int(row.priority),
    )


def _link_from_row(row: FederationIdentityLinkRow) -> IdentityLink:
    return IdentityLink(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        link_ref=row.link_ref,
        user_id=str(row.user_id),
        provider_id=str(row.provider_id),
        external_subject=row.external_subject,
        link_status=row.link_status,
        linked_at=row.linked_at or datetime.now(UTC),
        metadata=dict(row.metadata_json or {}),
    )


def _session_from_row(row: FederationSessionRow) -> FederationSession:
    return FederationSession(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        session_ref=row.session_ref,
        provider_id=str(row.provider_id),
        protocol=row.protocol,
        user_id=str(row.user_id) if row.user_id else None,
        idp_session_id=row.idp_session_id,
        status=row.status,
        expires_at=row.expires_at,
        created_at=row.created_at or datetime.now(UTC),
    )


class _RefCounterMixin:
    _local_counters: dict[str, int] = {}

    def _local_next(self, tenant_id: str, prefix: str) -> str:
        key = f"{tenant_id}:{prefix}"
        n = self._local_counters.get(key, 0) + 1
        self._local_counters[key] = n
        return f"{prefix}-{tenant_id}-{n:04d}"

    @classmethod
    def reset_counters(cls) -> None:
        cls._local_counters = {}

    async def _next_ref(self, tenant_id: str, prefix: str) -> str:
        try:
            async with session_scope(tenant_id=tenant_id) as session:
                row = await session.get(FederationRefCounterRow, (tenant_id, prefix))
                if row is None:
                    row = FederationRefCounterRow(
                        tenant_id=tenant_id, prefix=prefix, next_value=2
                    )
                    session.add(row)
                    n = 1
                else:
                    n = row.next_value
                    row.next_value = n + 1
                return f"{prefix}-{tenant_id}-{n:04d}"
        except Exception:
            return self._local_next(tenant_id, prefix)


class PostgresIdentityProviderRepository(IIdentityProviderRepository, _RefCounterMixin):
    async def save(self, provider: IdentityProvider) -> None:
        async with session_scope(tenant_id=provider.tenant_id) as session:
            row = await session.get(
                FederationIdentityProviderRow, (provider.tenant_id, _uuid(provider.id))
            )
            if row is None:
                row = FederationIdentityProviderRow(
                    tenant_id=provider.tenant_id,
                    id=_uuid(provider.id),
                    provider_ref=provider.provider_ref,
                    protocol=provider.protocol,
                    name=provider.name,
                    config=dict(provider.config or {}),
                    enabled=provider.enabled,
                    plugin_id=provider.plugin_id,
                    created_at=provider.created_at,
                )
                session.add(row)
            else:
                row.provider_ref = provider.provider_ref
                row.protocol = provider.protocol
                row.name = provider.name
                row.config = dict(provider.config or {})
                row.enabled = provider.enabled
                row.plugin_id = provider.plugin_id

    async def find_by_ref(self, tenant_id: str, provider_ref: str) -> IdentityProvider | None:
        async with session_scope(tenant_id=tenant_id) as session:
            row = await session.scalar(
                select(FederationIdentityProviderRow).where(
                    FederationIdentityProviderRow.tenant_id == tenant_id,
                    FederationIdentityProviderRow.provider_ref == provider_ref,
                )
            )
            return _provider_from_row(row) if row else None

    async def list_by_tenant(self, tenant_id: str) -> list[IdentityProvider]:
        async with session_scope(tenant_id=tenant_id) as session:
            rows = (
                await session.scalars(
                    select(FederationIdentityProviderRow).where(
                        FederationIdentityProviderRow.tenant_id == tenant_id
                    )
                )
            ).all()
        return [_provider_from_row(r) for r in rows]

    def next_provider_ref(self, tenant_id: str) -> str:
        return self._local_next(tenant_id, "idp")


class PostgresTrustRelationshipRepository(ITrustRelationshipRepository, _RefCounterMixin):
    async def save(self, trust: TrustRelationship) -> None:
        async with session_scope(tenant_id=trust.tenant_id) as session:
            row = await session.get(
                FederationTrustRelationshipRow, (trust.tenant_id, _uuid(trust.id))
            )
            if row is None:
                session.add(
                    FederationTrustRelationshipRow(
                        tenant_id=trust.tenant_id,
                        id=_uuid(trust.id),
                        trust_ref=trust.trust_ref,
                        source_entity_type=trust.source_entity_type,
                        source_entity_id=trust.source_entity_id,
                        target_entity_type=trust.target_entity_type,
                        target_entity_id=trust.target_entity_id,
                        trust_score=trust.trust_score,
                        trust_level=trust.trust_level,
                        status=trust.status,
                        valid_from=trust.valid_from,
                        valid_until=trust.valid_until,
                        metadata_json=dict(trust.metadata or {}),
                        created_at=trust.created_at,
                    )
                )
            else:
                row.trust_ref = trust.trust_ref
                row.source_entity_type = trust.source_entity_type
                row.source_entity_id = trust.source_entity_id
                row.target_entity_type = trust.target_entity_type
                row.target_entity_id = trust.target_entity_id
                row.trust_score = trust.trust_score
                row.trust_level = trust.trust_level
                row.status = trust.status
                row.valid_from = trust.valid_from
                row.valid_until = trust.valid_until
                row.metadata_json = dict(trust.metadata or {})

    async def list_by_tenant(self, tenant_id: str) -> list[TrustRelationship]:
        async with session_scope(tenant_id=tenant_id) as session:
            rows = (
                await session.scalars(
                    select(FederationTrustRelationshipRow).where(
                        FederationTrustRelationshipRow.tenant_id == tenant_id
                    )
                )
            ).all()
        return [_trust_from_row(r) for r in rows]

    def next_trust_ref(self, tenant_id: str) -> str:
        return self._local_next(tenant_id, "trust")


class PostgresClaimsMappingRepository(IClaimsMappingRepository, _RefCounterMixin):
    async def save(self, mapping: ClaimsMapping) -> None:
        async with session_scope(tenant_id=mapping.tenant_id) as session:
            row = await session.get(
                FederationClaimsMappingRow, (mapping.tenant_id, _uuid(mapping.id))
            )
            if row is None:
                session.add(
                    FederationClaimsMappingRow(
                        tenant_id=mapping.tenant_id,
                        id=_uuid(mapping.id),
                        mapping_ref=mapping.mapping_ref,
                        provider_id=_uuid(mapping.provider_id),
                        source_claim=mapping.source_claim,
                        target_claim=mapping.target_claim,
                        transform_type=mapping.transform_type,
                        transform_config=dict(mapping.transform_config or {}),
                        enabled=mapping.enabled,
                        priority=mapping.priority,
                    )
                )
            else:
                row.mapping_ref = mapping.mapping_ref
                row.provider_id = _uuid(mapping.provider_id)
                row.source_claim = mapping.source_claim
                row.target_claim = mapping.target_claim
                row.transform_type = mapping.transform_type
                row.transform_config = dict(mapping.transform_config or {})
                row.enabled = mapping.enabled
                row.priority = mapping.priority

    async def list_by_provider(self, tenant_id: str, provider_id: str) -> list[ClaimsMapping]:
        async with session_scope(tenant_id=tenant_id) as session:
            rows = (
                await session.scalars(
                    select(FederationClaimsMappingRow).where(
                        FederationClaimsMappingRow.tenant_id == tenant_id,
                        FederationClaimsMappingRow.provider_id == _uuid(provider_id),
                    )
                )
            ).all()
        return [_claims_from_row(r) for r in rows]

    def next_mapping_ref(self, tenant_id: str) -> str:
        return self._local_next(tenant_id, "claim-map")


class PostgresIdentityLinkRepository(IIdentityLinkRepository, _RefCounterMixin):
    async def save(self, link: IdentityLink) -> None:
        async with session_scope(tenant_id=link.tenant_id) as session:
            row = await session.get(
                FederationIdentityLinkRow, (link.tenant_id, _uuid(link.id))
            )
            if row is None:
                session.add(
                    FederationIdentityLinkRow(
                        tenant_id=link.tenant_id,
                        id=_uuid(link.id),
                        link_ref=link.link_ref,
                        user_id=_uuid(link.user_id),
                        provider_id=_uuid(link.provider_id),
                        external_subject=link.external_subject,
                        link_status=link.link_status,
                        linked_at=link.linked_at,
                        metadata_json=dict(link.metadata or {}),
                    )
                )
            else:
                row.link_ref = link.link_ref
                row.user_id = _uuid(link.user_id)
                row.provider_id = _uuid(link.provider_id)
                row.external_subject = link.external_subject
                row.link_status = link.link_status
                row.linked_at = link.linked_at
                row.metadata_json = dict(link.metadata or {})

    async def find_by_external(
        self, tenant_id: str, provider_id: str, external_subject: str
    ) -> IdentityLink | None:
        async with session_scope(tenant_id=tenant_id) as session:
            row = await session.scalar(
                select(FederationIdentityLinkRow).where(
                    FederationIdentityLinkRow.tenant_id == tenant_id,
                    FederationIdentityLinkRow.provider_id == _uuid(provider_id),
                    FederationIdentityLinkRow.external_subject == external_subject,
                )
            )
            return _link_from_row(row) if row else None

    async def list_by_user(self, tenant_id: str, user_id: str) -> list[IdentityLink]:
        async with session_scope(tenant_id=tenant_id) as session:
            rows = (
                await session.scalars(
                    select(FederationIdentityLinkRow).where(
                        FederationIdentityLinkRow.tenant_id == tenant_id,
                        FederationIdentityLinkRow.user_id == _uuid(user_id),
                    )
                )
            ).all()
        return [_link_from_row(r) for r in rows]

    def next_link_ref(self, tenant_id: str) -> str:
        return self._local_next(tenant_id, "link")


class PostgresFederationSessionRepository(IFederationSessionRepository, _RefCounterMixin):
    async def save(self, session_agg: FederationSession) -> None:
        async with session_scope(tenant_id=session_agg.tenant_id) as session:
            row = await session.scalar(
                select(FederationSessionRow).where(
                    FederationSessionRow.tenant_id == session_agg.tenant_id,
                    FederationSessionRow.session_ref == session_agg.session_ref,
                )
            )
            if row is None:
                session.add(
                    FederationSessionRow(
                        tenant_id=session_agg.tenant_id,
                        id=_uuid(session_agg.id),
                        created_at=session_agg.created_at,
                        session_ref=session_agg.session_ref,
                        user_id=_uuid(session_agg.user_id) if session_agg.user_id else None,
                        provider_id=_uuid(session_agg.provider_id),
                        protocol=session_agg.protocol,
                        idp_session_id=session_agg.idp_session_id,
                        status=session_agg.status,
                        expires_at=session_agg.expires_at,
                    )
                )
            else:
                row.user_id = _uuid(session_agg.user_id) if session_agg.user_id else None
                row.provider_id = _uuid(session_agg.provider_id)
                row.protocol = session_agg.protocol
                row.idp_session_id = session_agg.idp_session_id
                row.status = session_agg.status
                row.expires_at = session_agg.expires_at

    async def find_by_ref(self, tenant_id: str, session_ref: str) -> FederationSession | None:
        async with session_scope(tenant_id=tenant_id) as session:
            row = await session.scalar(
                select(FederationSessionRow).where(
                    FederationSessionRow.tenant_id == tenant_id,
                    FederationSessionRow.session_ref == session_ref,
                )
            )
            return _session_from_row(row) if row else None

    def next_session_ref(self, tenant_id: str) -> str:
        return self._local_next(tenant_id, "fed-sess")
