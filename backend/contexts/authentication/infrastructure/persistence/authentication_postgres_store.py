"""PostgreSQL repositories — Authentication SoR (profiles, passkeys, OIDC)."""
from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import delete, select

from contexts.authentication.domain.aggregates.authentication_platform import (
    AuthenticationProfile,
    OidcProvider,
    WebAuthnCredential,
)
from contexts.authentication.domain.ports.authentication_repositories import (
    IAuthenticationProfileRepository,
    IOidcProviderRepository,
    IWebAuthnCredentialRepository,
)
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.database.engine import session_scope
from shared.infrastructure.database.orm import (
    AuthenticationOidcProviderRow,
    AuthenticationProfileRow,
    AuthenticationWebAuthnCredentialRow,
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


def _profile_from_row(row: object) -> AuthenticationProfile:
    return AuthenticationProfile(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        profile_ref=row.profile_ref,
        webauthn_enabled=bool(row.webauthn_enabled),
        passkeys_required=bool(row.passkeys_required),
        oidc_enabled=bool(row.oidc_enabled),
        password_enabled=bool(row.password_enabled),
        created_at=row.created_at or datetime.now(UTC),
    )


def _credential_from_row(row: object) -> WebAuthnCredential:
    return WebAuthnCredential(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        user_id=row.user_id,
        credential_ref=row.credential_ref,
        credential_id=row.credential_id,
        public_key=row.public_key,
        sign_count=int(row.sign_count),
        nickname=row.nickname,
        transports=list(row.transports or []),
        aaguid=row.aaguid,
        created_at=row.created_at or datetime.now(UTC),
        last_used_at=row.last_used_at,
    )


def _oidc_from_row(row: object) -> OidcProvider:
    return OidcProvider(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        provider_ref=row.provider_ref,
        name=row.name,
        issuer_url=row.issuer_url,
        client_id=row.client_id,
        client_secret=row.client_secret,
        redirect_uri=row.redirect_uri,
        scopes=row.scopes,
        enabled=bool(row.enabled),
        created_at=row.created_at or datetime.now(UTC),
    )


class PostgresAuthenticationProfileRepository(IAuthenticationProfileRepository, _RefCounterMixin):
    async def find_by_tenant(self, tenant_id: str) -> AuthenticationProfile | None:
        async with session_scope(tenant_id=tenant_id) as session:
            row = await session.scalar(
                select(AuthenticationProfileRow).where(AuthenticationProfileRow.tenant_id == tenant_id)
            )
            return _profile_from_row(row) if row else None

    async def save(self, profile: AuthenticationProfile) -> None:
        async with session_scope(tenant_id=profile.tenant_id) as session:
            row = await session.get(AuthenticationProfileRow, (profile.tenant_id, _uuid(profile.id)))
            if row is None:
                session.add(
                    AuthenticationProfileRow(
                        tenant_id=profile.tenant_id,
                        id=_uuid(profile.id),
                        profile_ref=profile.profile_ref,
                        webauthn_enabled=profile.webauthn_enabled,
                        passkeys_required=profile.passkeys_required,
                        oidc_enabled=profile.oidc_enabled,
                        password_enabled=profile.password_enabled,
                        created_at=profile.created_at,
                    )
                )
            else:
                row.profile_ref = profile.profile_ref
                row.webauthn_enabled = profile.webauthn_enabled
                row.passkeys_required = profile.passkeys_required
                row.oidc_enabled = profile.oidc_enabled
                row.password_enabled = profile.password_enabled

    def next_profile_ref(self, tenant_id: str) -> str:
        return self._local_next(tenant_id, "auth-profile")


class PostgresWebAuthnCredentialRepository(IWebAuthnCredentialRepository, _RefCounterMixin):
    async def save(self, credential: WebAuthnCredential) -> None:
        async with session_scope(tenant_id=credential.tenant_id) as session:
            row = await session.get(
                AuthenticationWebAuthnCredentialRow, (credential.tenant_id, _uuid(credential.id))
            )
            if row is None:
                session.add(
                    AuthenticationWebAuthnCredentialRow(
                        tenant_id=credential.tenant_id,
                        id=_uuid(credential.id),
                        credential_ref=credential.credential_ref,
                        user_id=credential.user_id,
                        credential_id=credential.credential_id,
                        public_key=credential.public_key,
                        sign_count=credential.sign_count,
                        nickname=credential.nickname,
                        transports=list(credential.transports or []),
                        aaguid=credential.aaguid,
                        created_at=credential.created_at,
                        last_used_at=credential.last_used_at,
                    )
                )
            else:
                row.credential_ref = credential.credential_ref
                row.user_id = credential.user_id
                row.credential_id = credential.credential_id
                row.public_key = credential.public_key
                row.sign_count = credential.sign_count
                row.nickname = credential.nickname
                row.transports = list(credential.transports or [])
                row.aaguid = credential.aaguid
                row.last_used_at = credential.last_used_at

    async def list_by_user(self, tenant_id: str, user_id: str) -> list[WebAuthnCredential]:
        async with session_scope(tenant_id=tenant_id) as session:
            rows = (
                await session.scalars(
                    select(AuthenticationWebAuthnCredentialRow).where(
                        AuthenticationWebAuthnCredentialRow.tenant_id == tenant_id,
                        AuthenticationWebAuthnCredentialRow.user_id == user_id,
                    )
                )
            ).all()
        return [_credential_from_row(r) for r in rows]

    async def list_by_tenant(self, tenant_id: str) -> list[WebAuthnCredential]:
        async with session_scope(tenant_id=tenant_id) as session:
            rows = (
                await session.scalars(
                    select(AuthenticationWebAuthnCredentialRow).where(
                        AuthenticationWebAuthnCredentialRow.tenant_id == tenant_id
                    )
                )
            ).all()
        return [_credential_from_row(r) for r in rows]

    async def find_by_credential_id(self, tenant_id: str, credential_id: str) -> WebAuthnCredential | None:
        async with session_scope(tenant_id=tenant_id) as session:
            row = await session.scalar(
                select(AuthenticationWebAuthnCredentialRow).where(
                    AuthenticationWebAuthnCredentialRow.tenant_id == tenant_id,
                    AuthenticationWebAuthnCredentialRow.credential_id == credential_id,
                )
            )
            return _credential_from_row(row) if row else None

    async def find_by_ref(self, tenant_id: str, credential_ref: str) -> WebAuthnCredential | None:
        async with session_scope(tenant_id=tenant_id) as session:
            row = await session.scalar(
                select(AuthenticationWebAuthnCredentialRow).where(
                    AuthenticationWebAuthnCredentialRow.tenant_id == tenant_id,
                    AuthenticationWebAuthnCredentialRow.credential_ref == credential_ref,
                )
            )
            return _credential_from_row(row) if row else None

    async def delete(self, tenant_id: str, credential_ref: str) -> bool:
        async with session_scope(tenant_id=tenant_id) as session:
            result = await session.execute(
                delete(AuthenticationWebAuthnCredentialRow).where(
                    AuthenticationWebAuthnCredentialRow.tenant_id == tenant_id,
                    AuthenticationWebAuthnCredentialRow.credential_ref == credential_ref,
                )
            )
            return bool(result.rowcount)

    def next_credential_ref(self, tenant_id: str) -> str:
        return self._local_next(tenant_id, "passkey")


class PostgresOidcProviderRepository(IOidcProviderRepository, _RefCounterMixin):
    async def save(self, provider: OidcProvider) -> None:
        async with session_scope(tenant_id=provider.tenant_id) as session:
            row = await session.get(AuthenticationOidcProviderRow, (provider.tenant_id, _uuid(provider.id)))
            if row is None:
                session.add(
                    AuthenticationOidcProviderRow(
                        tenant_id=provider.tenant_id,
                        id=_uuid(provider.id),
                        provider_ref=provider.provider_ref,
                        name=provider.name,
                        issuer_url=provider.issuer_url,
                        client_id=provider.client_id,
                        client_secret=provider.client_secret,
                        redirect_uri=provider.redirect_uri,
                        scopes=provider.scopes,
                        enabled=provider.enabled,
                        created_at=provider.created_at,
                    )
                )
            else:
                row.provider_ref = provider.provider_ref
                row.name = provider.name
                row.issuer_url = provider.issuer_url
                row.client_id = provider.client_id
                row.client_secret = provider.client_secret
                row.redirect_uri = provider.redirect_uri
                row.scopes = provider.scopes
                row.enabled = provider.enabled

    async def list_by_tenant(self, tenant_id: str) -> list[OidcProvider]:
        async with session_scope(tenant_id=tenant_id) as session:
            rows = (
                await session.scalars(
                    select(AuthenticationOidcProviderRow).where(
                        AuthenticationOidcProviderRow.tenant_id == tenant_id
                    )
                )
            ).all()
        return [_oidc_from_row(r) for r in rows]

    async def find_by_ref(self, tenant_id: str, provider_ref: str) -> OidcProvider | None:
        async with session_scope(tenant_id=tenant_id) as session:
            row = await session.scalar(
                select(AuthenticationOidcProviderRow).where(
                    AuthenticationOidcProviderRow.tenant_id == tenant_id,
                    AuthenticationOidcProviderRow.provider_ref == provider_ref,
                )
            )
            return _oidc_from_row(row) if row else None

    def next_provider_ref(self, tenant_id: str) -> str:
        return self._local_next(tenant_id, "oidc")
