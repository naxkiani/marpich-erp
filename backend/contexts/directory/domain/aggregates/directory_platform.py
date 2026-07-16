"""Directory platform aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class DirectoryCapability(StrEnum):
    SAML_PROVIDER_REGISTRY = "saml_provider_registry"
    SAML_AUTHORIZATION = "saml_authorization"
    SAML_ASSERTION_CONSUMER = "saml_assertion_consumer"
    LDAP_CONNECTOR_REGISTRY = "ldap_connector_registry"
    LDAP_DIRECTORY_SYNC = "ldap_directory_sync"
    SCIM_PROVIDER_REGISTRY = "scim_provider_registry"
    SCIM_USER_PROVISIONING = "scim_user_provisioning"
    DIRECTORY_SYNC_WORKER = "directory_sync_worker"
    POLICY_DRIVEN_DIRECTORY = "policy_driven_directory"
    DIRECTORY_API = "directory_api"


class SyncJobStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass(eq=False, kw_only=True)
class DirectoryProfile(AggregateRoot):
    tenant_id: str
    profile_ref: str
    saml_enabled: bool = True
    ldap_enabled: bool = True
    scim_enabled: bool = True
    auto_provision: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(cls, *, tenant_id: str, profile_ref: str) -> DirectoryProfile:
        return cls(id=UniqueId.generate(), tenant_id=tenant_id, profile_ref=profile_ref)

    def to_dict(self) -> dict:
        return {
            "profile_ref": self.profile_ref,
            "tenant_id": self.tenant_id,
            "saml_enabled": self.saml_enabled,
            "ldap_enabled": self.ldap_enabled,
            "scim_enabled": self.scim_enabled,
            "auto_provision": self.auto_provision,
        }


@dataclass(eq=False, kw_only=True)
class SamlProvider(AggregateRoot):
    tenant_id: str
    provider_ref: str
    name: str
    entity_id: str
    sso_url: str
    x509_cert: str
    enabled: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def register(
        cls,
        *,
        tenant_id: str,
        provider_ref: str,
        name: str,
        entity_id: str,
        sso_url: str,
        x509_cert: str,
    ) -> SamlProvider:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            provider_ref=provider_ref,
            name=name,
            entity_id=entity_id,
            sso_url=sso_url.rstrip("/"),
            x509_cert=x509_cert,
        )

    def to_dict(self) -> dict:
        return {
            "provider_ref": self.provider_ref,
            "tenant_id": self.tenant_id,
            "name": self.name,
            "entity_id": self.entity_id,
            "sso_url": self.sso_url,
            "enabled": self.enabled,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class LdapConnector(AggregateRoot):
    tenant_id: str
    connector_ref: str
    name: str
    host: str
    port: int
    bind_dn: str
    bind_password: str
    base_dn: str
    user_filter: str = "(objectClass=person)"
    enabled: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def register(
        cls,
        *,
        tenant_id: str,
        connector_ref: str,
        name: str,
        host: str,
        port: int,
        bind_dn: str,
        bind_password: str,
        base_dn: str,
        user_filter: str = "(objectClass=person)",
    ) -> LdapConnector:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            connector_ref=connector_ref,
            name=name,
            host=host,
            port=port,
            bind_dn=bind_dn,
            bind_password=bind_password,
            base_dn=base_dn,
            user_filter=user_filter,
        )

    def to_dict(self, *, include_secret: bool = False) -> dict:
        data = {
            "connector_ref": self.connector_ref,
            "tenant_id": self.tenant_id,
            "name": self.name,
            "host": self.host,
            "port": self.port,
            "bind_dn": self.bind_dn,
            "base_dn": self.base_dn,
            "user_filter": self.user_filter,
            "enabled": self.enabled,
            "created_at": self.created_at.isoformat(),
        }
        if include_secret:
            data["bind_password"] = self.bind_password
        return data


@dataclass(eq=False, kw_only=True)
class ScimProvider(AggregateRoot):
    tenant_id: str
    provider_ref: str
    name: str
    bearer_token: str
    enabled: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def register(
        cls,
        *,
        tenant_id: str,
        provider_ref: str,
        name: str,
        bearer_token: str,
    ) -> ScimProvider:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            provider_ref=provider_ref,
            name=name,
            bearer_token=bearer_token,
        )

    def to_dict(self, *, include_secret: bool = False) -> dict:
        data = {
            "provider_ref": self.provider_ref,
            "tenant_id": self.tenant_id,
            "name": self.name,
            "enabled": self.enabled,
            "created_at": self.created_at.isoformat(),
        }
        if include_secret:
            data["bearer_token"] = self.bearer_token
        return data


@dataclass(eq=False, kw_only=True)
class DirectorySyncJob(AggregateRoot):
    tenant_id: str
    job_ref: str
    source_type: str
    source_ref: str
    status: str = SyncJobStatus.PENDING.value
    users_synced: int = 0
    users_created: int = 0
    error_message: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    completed_at: datetime | None = None

    @classmethod
    def enqueue(
        cls,
        *,
        tenant_id: str,
        job_ref: str,
        source_type: str,
        source_ref: str,
    ) -> DirectorySyncJob:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            job_ref=job_ref,
            source_type=source_type,
            source_ref=source_ref,
        )

    def mark_running(self) -> None:
        self.status = SyncJobStatus.RUNNING.value

    def mark_completed(self, *, synced: int, created: int) -> None:
        self.status = SyncJobStatus.COMPLETED.value
        self.users_synced = synced
        self.users_created = created
        self.completed_at = datetime.now(UTC)

    def mark_failed(self, message: str) -> None:
        self.status = SyncJobStatus.FAILED.value
        self.error_message = message
        self.completed_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "job_ref": self.job_ref,
            "tenant_id": self.tenant_id,
            "source_type": self.source_type,
            "source_ref": self.source_ref,
            "status": self.status,
            "users_synced": self.users_synced,
            "users_created": self.users_created,
            "error_message": self.error_message,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }
