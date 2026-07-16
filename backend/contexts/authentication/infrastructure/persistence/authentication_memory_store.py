"""In-memory authentication persistence."""
from __future__ import annotations

import time
import uuid

from contexts.authentication.domain.aggregates.authentication_platform import (
    AuthenticationProfile,
    OidcProvider,
    WebAuthnCredential,
)
from contexts.authentication.domain.ports.authentication_repositories import (
    IAuthenticationProfileRepository,
    IOidcProviderRepository,
    IOidcStateStore,
    IWebAuthnChallengeStore,
    IWebAuthnCredentialRepository,
)


class _TtlStore:
    _entries: dict[str, tuple[dict, float]] = {}

    @classmethod
    def reset(cls) -> None:
        cls._entries.clear()

    @classmethod
    def put(cls, key: str, payload: dict, ttl_seconds: int) -> None:
        cls._entries[key] = (payload, time.time() + ttl_seconds)

    @classmethod
    def pop(cls, key: str) -> dict | None:
        entry = cls._entries.pop(key, None)
        if not entry:
            return None
        payload, expires_at = entry
        if time.time() > expires_at:
            return None
        return payload


class InMemoryAuthenticationStore:
    profiles: dict[str, AuthenticationProfile] = {}
    credentials: dict[str, WebAuthnCredential] = {}
    providers: dict[str, OidcProvider] = {}
    profile_counter: dict[str, int] = {}
    credential_counter: dict[str, int] = {}
    provider_counter: dict[str, int] = {}

    @classmethod
    def reset(cls) -> None:
        cls.profiles.clear()
        cls.credentials.clear()
        cls.providers.clear()
        cls.profile_counter.clear()
        cls.credential_counter.clear()
        cls.provider_counter.clear()
        _TtlStore.reset()


class InMemoryAuthenticationProfileRepository(IAuthenticationProfileRepository):
    async def find_by_tenant(self, tenant_id: str) -> AuthenticationProfile | None:
        return InMemoryAuthenticationStore.profiles.get(tenant_id)

    async def save(self, profile: AuthenticationProfile) -> None:
        InMemoryAuthenticationStore.profiles[profile.tenant_id] = profile

    def next_profile_ref(self, tenant_id: str) -> str:
        n = InMemoryAuthenticationStore.profile_counter.get(tenant_id, 0) + 1
        InMemoryAuthenticationStore.profile_counter[tenant_id] = n
        return f"auth-profile-{tenant_id}-{n:04d}"


class InMemoryWebAuthnCredentialRepository(IWebAuthnCredentialRepository):
    async def save(self, credential: WebAuthnCredential) -> None:
        InMemoryAuthenticationStore.credentials[credential.credential_ref] = credential

    async def list_by_user(self, tenant_id: str, user_id: str) -> list[WebAuthnCredential]:
        return [
            c
            for c in InMemoryAuthenticationStore.credentials.values()
            if c.tenant_id == tenant_id and c.user_id == user_id
        ]

    async def list_by_tenant(self, tenant_id: str) -> list[WebAuthnCredential]:
        return [c for c in InMemoryAuthenticationStore.credentials.values() if c.tenant_id == tenant_id]

    async def find_by_credential_id(self, tenant_id: str, credential_id: str) -> WebAuthnCredential | None:
        for cred in InMemoryAuthenticationStore.credentials.values():
            if cred.tenant_id == tenant_id and cred.credential_id == credential_id:
                return cred
        return None

    async def find_by_ref(self, tenant_id: str, credential_ref: str) -> WebAuthnCredential | None:
        cred = InMemoryAuthenticationStore.credentials.get(credential_ref)
        if cred and cred.tenant_id == tenant_id:
            return cred
        return None

    async def delete(self, tenant_id: str, credential_ref: str) -> bool:
        cred = await self.find_by_ref(tenant_id, credential_ref)
        if not cred:
            return False
        del InMemoryAuthenticationStore.credentials[credential_ref]
        return True

    def next_credential_ref(self, tenant_id: str) -> str:
        n = InMemoryAuthenticationStore.credential_counter.get(tenant_id, 0) + 1
        InMemoryAuthenticationStore.credential_counter[tenant_id] = n
        return f"passkey-{tenant_id}-{n:04d}"


class InMemoryOidcProviderRepository(IOidcProviderRepository):
    async def save(self, provider: OidcProvider) -> None:
        InMemoryAuthenticationStore.providers[provider.provider_ref] = provider

    async def list_by_tenant(self, tenant_id: str) -> list[OidcProvider]:
        return [p for p in InMemoryAuthenticationStore.providers.values() if p.tenant_id == tenant_id]

    async def find_by_ref(self, tenant_id: str, provider_ref: str) -> OidcProvider | None:
        provider = InMemoryAuthenticationStore.providers.get(provider_ref)
        if provider and provider.tenant_id == tenant_id:
            return provider
        return None

    def next_provider_ref(self, tenant_id: str) -> str:
        n = InMemoryAuthenticationStore.provider_counter.get(tenant_id, 0) + 1
        InMemoryAuthenticationStore.provider_counter[tenant_id] = n
        return f"oidc-{tenant_id}-{n:04d}"


class InMemoryWebAuthnChallengeStore(IWebAuthnChallengeStore):
    async def put_registration(self, challenge_id: str, payload: dict, ttl_seconds: int) -> None:
        _TtlStore.put(f"reg:{challenge_id}", payload, ttl_seconds)

    async def pop_registration(self, challenge_id: str) -> dict | None:
        return _TtlStore.pop(f"reg:{challenge_id}")

    async def put_authentication(self, challenge_id: str, payload: dict, ttl_seconds: int) -> None:
        _TtlStore.put(f"auth:{challenge_id}", payload, ttl_seconds)

    async def pop_authentication(self, challenge_id: str) -> dict | None:
        return _TtlStore.pop(f"auth:{challenge_id}")


class InMemoryOidcStateStore(IOidcStateStore):
    async def put(self, state: str, payload: dict, ttl_seconds: int) -> None:
        _TtlStore.put(f"oidc:{state}", payload, ttl_seconds)

    async def pop(self, state: str) -> dict | None:
        return _TtlStore.pop(f"oidc:{state}")
