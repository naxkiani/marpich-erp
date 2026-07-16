"""Authentication platform aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class AuthenticationCapability(StrEnum):
    WEBAUTHN_REGISTRATION = "webauthn_registration"
    WEBAUTHN_AUTHENTICATION = "webauthn_authentication"
    PASSKEY_MANAGEMENT = "passkey_management"
    OIDC_PROVIDER_REGISTRY = "oidc_provider_registry"
    OIDC_AUTHORIZATION = "oidc_authorization"
    OIDC_CALLBACK = "oidc_callback"
    AUTH_METHOD_CATALOG = "auth_method_catalog"
    POLICY_DRIVEN_AUTHENTICATION = "policy_driven_authentication"
    AUTHENTICATION_DASHBOARD = "authentication_dashboard"
    AUTHENTICATION_API = "authentication_api"


@dataclass(eq=False, kw_only=True)
class AuthenticationProfile(AggregateRoot):
    tenant_id: str
    profile_ref: str
    webauthn_enabled: bool = True
    passkeys_required: bool = False
    oidc_enabled: bool = True
    password_enabled: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(cls, *, tenant_id: str, profile_ref: str) -> AuthenticationProfile:
        return cls(id=UniqueId.generate(), tenant_id=tenant_id, profile_ref=profile_ref)

    def to_dict(self) -> dict:
        return {
            "profile_ref": self.profile_ref,
            "tenant_id": self.tenant_id,
            "webauthn_enabled": self.webauthn_enabled,
            "passkeys_required": self.passkeys_required,
            "oidc_enabled": self.oidc_enabled,
            "password_enabled": self.password_enabled,
        }


@dataclass(eq=False, kw_only=True)
class WebAuthnCredential(AggregateRoot):
    tenant_id: str
    user_id: str
    credential_ref: str
    credential_id: str
    public_key: str
    sign_count: int
    nickname: str
    transports: list[str] = field(default_factory=list)
    aaguid: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    last_used_at: datetime | None = None

    @classmethod
    def register(
        cls,
        *,
        tenant_id: str,
        user_id: str,
        credential_ref: str,
        credential_id: str,
        public_key: str,
        sign_count: int,
        nickname: str,
        transports: list[str] | None = None,
        aaguid: str | None = None,
    ) -> WebAuthnCredential:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            user_id=user_id,
            credential_ref=credential_ref,
            credential_id=credential_id,
            public_key=public_key,
            sign_count=sign_count,
            nickname=nickname,
            transports=transports or [],
            aaguid=aaguid,
        )

    def mark_used(self, sign_count: int) -> None:
        self.sign_count = sign_count
        self.last_used_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "credential_ref": self.credential_ref,
            "tenant_id": self.tenant_id,
            "user_id": self.user_id,
            "credential_id": self.credential_id,
            "nickname": self.nickname,
            "transports": self.transports,
            "sign_count": self.sign_count,
            "aaguid": self.aaguid,
            "created_at": self.created_at.isoformat(),
            "last_used_at": self.last_used_at.isoformat() if self.last_used_at else None,
        }


@dataclass(eq=False, kw_only=True)
class OidcProvider(AggregateRoot):
    tenant_id: str
    provider_ref: str
    name: str
    issuer_url: str
    client_id: str
    client_secret: str
    redirect_uri: str
    scopes: str
    enabled: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def register(
        cls,
        *,
        tenant_id: str,
        provider_ref: str,
        name: str,
        issuer_url: str,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        scopes: str,
    ) -> OidcProvider:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            provider_ref=provider_ref,
            name=name,
            issuer_url=issuer_url.rstrip("/"),
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scopes=scopes,
        )

    def to_dict(self, *, include_secret: bool = False) -> dict:
        data = {
            "provider_ref": self.provider_ref,
            "tenant_id": self.tenant_id,
            "name": self.name,
            "issuer_url": self.issuer_url,
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scopes": self.scopes,
            "enabled": self.enabled,
            "created_at": self.created_at.isoformat(),
        }
        if include_secret:
            data["client_secret"] = self.client_secret
        return data
