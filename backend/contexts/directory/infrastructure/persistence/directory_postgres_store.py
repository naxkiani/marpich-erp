"""PostgreSQL repositories — Directory SoR."""
from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select

from contexts.directory.domain.aggregates.directory_platform import (
    DirectoryProfile,
    DirectorySyncJob,
    LdapConnector,
    SamlProvider,
    ScimProvider,
)
from contexts.directory.domain.ports.directory_repositories import (
    IDirectoryProfileRepository,
    IDirectorySyncJobRepository,
    ILdapConnectorRepository,
    ISamlProviderRepository,
    IScimProviderRepository,
)
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.database.engine import session_scope
from shared.infrastructure.database.orm import (
    DirectoryLdapConnectorRow,
    DirectoryProfileRow,
    DirectorySamlProviderRow,
    DirectoryScimProviderRow,
    DirectorySyncJobRow,
)


def _uuid(value: UniqueId | str | UUID) -> UUID:
    if isinstance(value, UUID):
        return value
    return UUID(str(value))


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


def _profile_from_row(row: object) -> DirectoryProfile:
    return DirectoryProfile(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        profile_ref=row.profile_ref,
        saml_enabled=bool(row.saml_enabled),
        ldap_enabled=bool(row.ldap_enabled),
        scim_enabled=bool(row.scim_enabled),
        auto_provision=bool(row.auto_provision),
        created_at=row.created_at or datetime.now(UTC),
    )


def _saml_from_row(row: object) -> SamlProvider:
    return SamlProvider(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        provider_ref=row.provider_ref,
        name=row.name,
        entity_id=row.entity_id,
        sso_url=row.sso_url,
        x509_cert=row.x509_cert or "",
        enabled=bool(row.enabled),
        created_at=row.created_at or datetime.now(UTC),
    )


def _ldap_from_row(row: object) -> LdapConnector:
    return LdapConnector(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        connector_ref=row.connector_ref,
        name=row.name,
        host=row.host,
        port=int(row.port),
        bind_dn=row.bind_dn,
        bind_password=row.bind_password,
        base_dn=row.base_dn,
        user_filter=row.user_filter,
        enabled=bool(row.enabled),
        created_at=row.created_at or datetime.now(UTC),
    )


def _scim_from_row(row: object) -> ScimProvider:
    return ScimProvider(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        provider_ref=row.provider_ref,
        name=row.name,
        bearer_token=row.bearer_token,
        enabled=bool(row.enabled),
        created_at=row.created_at or datetime.now(UTC),
    )


def _job_from_row(row: object) -> DirectorySyncJob:
    return DirectorySyncJob(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        job_ref=row.job_ref,
        source_type=row.source_type,
        source_ref=row.source_ref,
        status=row.status,
        users_synced=int(row.users_synced),
        users_created=int(row.users_created),
        error_message=row.error_message,
        created_at=row.created_at or datetime.now(UTC),
        completed_at=row.completed_at,
    )


class PostgresDirectoryProfileRepository(IDirectoryProfileRepository, _RefCounterMixin):
    async def find_by_tenant(self, tenant_id: str) -> DirectoryProfile | None:
        async with session_scope(tenant_id=tenant_id) as session:
            row = await session.scalar(
                select(DirectoryProfileRow).where(DirectoryProfileRow.tenant_id == tenant_id)
            )
            return _profile_from_row(row) if row else None

    async def save(self, profile: DirectoryProfile) -> None:
        async with session_scope(tenant_id=profile.tenant_id) as session:
            row = await session.get(DirectoryProfileRow, (profile.tenant_id, _uuid(profile.id)))
            if row is None:
                session.add(
                    DirectoryProfileRow(
                        tenant_id=profile.tenant_id,
                        id=_uuid(profile.id),
                        profile_ref=profile.profile_ref,
                        saml_enabled=profile.saml_enabled,
                        ldap_enabled=profile.ldap_enabled,
                        scim_enabled=profile.scim_enabled,
                        auto_provision=profile.auto_provision,
                        created_at=profile.created_at,
                    )
                )
            else:
                row.profile_ref = profile.profile_ref
                row.saml_enabled = profile.saml_enabled
                row.ldap_enabled = profile.ldap_enabled
                row.scim_enabled = profile.scim_enabled
                row.auto_provision = profile.auto_provision

    def next_profile_ref(self, tenant_id: str) -> str:
        return self._local_next(tenant_id, "dir-profile")


class PostgresSamlProviderRepository(ISamlProviderRepository, _RefCounterMixin):
    async def save(self, provider: SamlProvider) -> None:
        async with session_scope(tenant_id=provider.tenant_id) as session:
            row = await session.get(DirectorySamlProviderRow, (provider.tenant_id, _uuid(provider.id)))
            if row is None:
                session.add(
                    DirectorySamlProviderRow(
                        tenant_id=provider.tenant_id,
                        id=_uuid(provider.id),
                        provider_ref=provider.provider_ref,
                        name=provider.name,
                        entity_id=provider.entity_id,
                        sso_url=provider.sso_url,
                        x509_cert=provider.x509_cert,
                        enabled=provider.enabled,
                        created_at=provider.created_at,
                    )
                )
            else:
                row.provider_ref = provider.provider_ref
                row.name = provider.name
                row.entity_id = provider.entity_id
                row.sso_url = provider.sso_url
                row.x509_cert = provider.x509_cert
                row.enabled = provider.enabled

    async def list_by_tenant(self, tenant_id: str) -> list[SamlProvider]:
        async with session_scope(tenant_id=tenant_id) as session:
            rows = (
                await session.scalars(
                    select(DirectorySamlProviderRow).where(DirectorySamlProviderRow.tenant_id == tenant_id)
                )
            ).all()
        return [_saml_from_row(r) for r in rows]

    async def find_by_ref(self, tenant_id: str, provider_ref: str) -> SamlProvider | None:
        async with session_scope(tenant_id=tenant_id) as session:
            row = await session.scalar(
                select(DirectorySamlProviderRow).where(
                    DirectorySamlProviderRow.tenant_id == tenant_id,
                    DirectorySamlProviderRow.provider_ref == provider_ref,
                )
            )
            return _saml_from_row(row) if row else None

    def next_provider_ref(self, tenant_id: str) -> str:
        return self._local_next(tenant_id, "saml")


class PostgresLdapConnectorRepository(ILdapConnectorRepository, _RefCounterMixin):
    async def save(self, connector: LdapConnector) -> None:
        async with session_scope(tenant_id=connector.tenant_id) as session:
            row = await session.get(DirectoryLdapConnectorRow, (connector.tenant_id, _uuid(connector.id)))
            if row is None:
                session.add(
                    DirectoryLdapConnectorRow(
                        tenant_id=connector.tenant_id,
                        id=_uuid(connector.id),
                        connector_ref=connector.connector_ref,
                        name=connector.name,
                        host=connector.host,
                        port=connector.port,
                        bind_dn=connector.bind_dn,
                        bind_password=connector.bind_password,
                        base_dn=connector.base_dn,
                        user_filter=connector.user_filter,
                        enabled=connector.enabled,
                        created_at=connector.created_at,
                    )
                )
            else:
                row.connector_ref = connector.connector_ref
                row.name = connector.name
                row.host = connector.host
                row.port = connector.port
                row.bind_dn = connector.bind_dn
                row.bind_password = connector.bind_password
                row.base_dn = connector.base_dn
                row.user_filter = connector.user_filter
                row.enabled = connector.enabled

    async def list_by_tenant(self, tenant_id: str) -> list[LdapConnector]:
        async with session_scope(tenant_id=tenant_id) as session:
            rows = (
                await session.scalars(
                    select(DirectoryLdapConnectorRow).where(DirectoryLdapConnectorRow.tenant_id == tenant_id)
                )
            ).all()
        return [_ldap_from_row(r) for r in rows]

    async def find_by_ref(self, tenant_id: str, connector_ref: str) -> LdapConnector | None:
        async with session_scope(tenant_id=tenant_id) as session:
            row = await session.scalar(
                select(DirectoryLdapConnectorRow).where(
                    DirectoryLdapConnectorRow.tenant_id == tenant_id,
                    DirectoryLdapConnectorRow.connector_ref == connector_ref,
                )
            )
            return _ldap_from_row(row) if row else None

    def next_connector_ref(self, tenant_id: str) -> str:
        return self._local_next(tenant_id, "ldap")


class PostgresScimProviderRepository(IScimProviderRepository, _RefCounterMixin):
    async def save(self, provider: ScimProvider) -> None:
        async with session_scope(tenant_id=provider.tenant_id) as session:
            row = await session.get(DirectoryScimProviderRow, (provider.tenant_id, _uuid(provider.id)))
            if row is None:
                session.add(
                    DirectoryScimProviderRow(
                        tenant_id=provider.tenant_id,
                        id=_uuid(provider.id),
                        provider_ref=provider.provider_ref,
                        name=provider.name,
                        bearer_token=provider.bearer_token,
                        enabled=provider.enabled,
                        created_at=provider.created_at,
                    )
                )
            else:
                row.provider_ref = provider.provider_ref
                row.name = provider.name
                row.bearer_token = provider.bearer_token
                row.enabled = provider.enabled

    async def list_by_tenant(self, tenant_id: str) -> list[ScimProvider]:
        async with session_scope(tenant_id=tenant_id) as session:
            rows = (
                await session.scalars(
                    select(DirectoryScimProviderRow).where(DirectoryScimProviderRow.tenant_id == tenant_id)
                )
            ).all()
        return [_scim_from_row(r) for r in rows]

    async def find_by_ref(self, tenant_id: str, provider_ref: str) -> ScimProvider | None:
        async with session_scope(tenant_id=tenant_id) as session:
            row = await session.scalar(
                select(DirectoryScimProviderRow).where(
                    DirectoryScimProviderRow.tenant_id == tenant_id,
                    DirectoryScimProviderRow.provider_ref == provider_ref,
                )
            )
            return _scim_from_row(row) if row else None

    async def find_by_token(self, tenant_id: str, bearer_token: str) -> ScimProvider | None:
        async with session_scope(tenant_id=tenant_id) as session:
            row = await session.scalar(
                select(DirectoryScimProviderRow).where(
                    DirectoryScimProviderRow.tenant_id == tenant_id,
                    DirectoryScimProviderRow.bearer_token == bearer_token,
                    DirectoryScimProviderRow.enabled.is_(True),
                )
            )
            return _scim_from_row(row) if row else None

    def next_provider_ref(self, tenant_id: str) -> str:
        return self._local_next(tenant_id, "scim")


class PostgresDirectorySyncJobRepository(IDirectorySyncJobRepository, _RefCounterMixin):
    async def save(self, job: DirectorySyncJob) -> None:
        async with session_scope(tenant_id=job.tenant_id) as session:
            row = await session.get(DirectorySyncJobRow, (job.tenant_id, _uuid(job.id)))
            if row is None:
                session.add(
                    DirectorySyncJobRow(
                        tenant_id=job.tenant_id,
                        id=_uuid(job.id),
                        job_ref=job.job_ref,
                        source_type=job.source_type,
                        source_ref=job.source_ref,
                        status=job.status,
                        users_synced=job.users_synced,
                        users_created=job.users_created,
                        error_message=job.error_message,
                        created_at=job.created_at,
                        completed_at=job.completed_at,
                    )
                )
            else:
                row.job_ref = job.job_ref
                row.source_type = job.source_type
                row.source_ref = job.source_ref
                row.status = job.status
                row.users_synced = job.users_synced
                row.users_created = job.users_created
                row.error_message = job.error_message
                row.completed_at = job.completed_at

    async def list_by_tenant(self, tenant_id: str) -> list[DirectorySyncJob]:
        async with session_scope(tenant_id=tenant_id) as session:
            rows = (
                await session.scalars(
                    select(DirectorySyncJobRow).where(DirectorySyncJobRow.tenant_id == tenant_id)
                )
            ).all()
        return [_job_from_row(r) for r in rows]

    async def list_pending(self, tenant_id: str) -> list[DirectorySyncJob]:
        async with session_scope(tenant_id=tenant_id) as session:
            rows = (
                await session.scalars(
                    select(DirectorySyncJobRow).where(
                        DirectorySyncJobRow.tenant_id == tenant_id,
                        DirectorySyncJobRow.status == "pending",
                    )
                )
            ).all()
        return [_job_from_row(r) for r in rows]

    async def find_by_ref(self, tenant_id: str, job_ref: str) -> DirectorySyncJob | None:
        async with session_scope(tenant_id=tenant_id) as session:
            row = await session.scalar(
                select(DirectorySyncJobRow).where(
                    DirectorySyncJobRow.tenant_id == tenant_id,
                    DirectorySyncJobRow.job_ref == job_ref,
                )
            )
            return _job_from_row(row) if row else None

    def next_job_ref(self, tenant_id: str) -> str:
        return self._local_next(tenant_id, "sync")
