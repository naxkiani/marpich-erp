"""Enterprise Identity Federation & SSO Platform aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class FederationProtocol(StrEnum):
    OIDC = "oidc"
    SAML = "saml"
    LDAP = "ldap"
    AZURE_AD = "azure_ad"
    ENTRA_ID = "entra_id"
    AD = "ad"
    GOOGLE = "google"
    APPLE = "apple"
    GITHUB = "github"
    GITLAB = "gitlab"
    KEYCLOAK = "keycloak"
    OKTA = "okta"
    AUTH0 = "auth0"
    COGNITO = "cognito"
    GOVERNMENT_EID = "government_eid"
    UNIVERSITY = "university"
    HOSPITAL = "hospital"
    BANK = "bank"
    TAX_AUTHORITY = "tax_authority"
    NATIONAL_DIGITAL_ID = "national_digital_id"
    CUSTOM = "custom"
    LEGACY = "legacy"
    PARTNER = "partner"
    SCIM = "scim"


class TrustLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERIFIED = "verified"


class FederationMode(StrEnum):
    DEDICATED = "dedicated"
    SHARED = "shared"
    REGIONAL = "regional"
    CROSS_REGION = "cross_region"
    PARTNER = "partner"


class LifecycleState(StrEnum):
    REGISTERED = "registered"
    VERIFIED = "verified"
    ACTIVE = "active"
    FEDERATED = "federated"
    SUSPENDED = "suspended"
    RECOVERING = "recovering"
    DEPROVISIONED = "deprovisioned"
    ARCHIVED = "archived"
    DELETED = "deleted"


@dataclass(eq=False, kw_only=True)
class FederationProfile(AggregateRoot):
    tenant_id: str
    profile_ref: str
    federation_enabled: bool = True
    broker_enabled: bool = True
    jit_provisioning_enabled: bool = True
    identity_discovery_enabled: bool = True
    single_logout_enabled: bool = True
    cross_tenant_enabled: bool = False
    default_federation_mode: str = FederationMode.DEDICATED.value
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(cls, *, tenant_id: str, profile_ref: str) -> FederationProfile:
        return cls(id=UniqueId.generate(), tenant_id=tenant_id, profile_ref=profile_ref)

    def to_dict(self) -> dict:
        return {
            "profile_ref": self.profile_ref,
            "federation_enabled": self.federation_enabled,
            "broker_enabled": self.broker_enabled,
            "jit_provisioning_enabled": self.jit_provisioning_enabled,
            "identity_discovery_enabled": self.identity_discovery_enabled,
            "single_logout_enabled": self.single_logout_enabled,
            "cross_tenant_enabled": self.cross_tenant_enabled,
            "default_federation_mode": self.default_federation_mode,
        }


@dataclass(eq=False, kw_only=True)
class IdentityProvider(AggregateRoot):
    tenant_id: str
    provider_ref: str
    protocol: str
    name: str
    config: dict = field(default_factory=dict)
    enabled: bool = True
    plugin_id: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def register(
        cls,
        *,
        tenant_id: str,
        provider_ref: str,
        protocol: str,
        name: str,
        config: dict | None = None,
        plugin_id: str | None = None,
    ) -> IdentityProvider:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            provider_ref=provider_ref,
            protocol=protocol,
            name=name,
            config=config or {},
            plugin_id=plugin_id,
        )

    def to_dict(self) -> dict:
        return {
            "provider_ref": self.provider_ref,
            "protocol": self.protocol,
            "name": self.name,
            "config": {k: v for k, v in self.config.items() if not k.endswith("_secret")},
            "enabled": self.enabled,
            "plugin_id": self.plugin_id,
        }


@dataclass(eq=False, kw_only=True)
class FederationPartner(AggregateRoot):
    tenant_id: str
    partner_ref: str
    name: str
    partner_type: str = "organization"
    trust_level: str = TrustLevel.MEDIUM.value
    metadata: dict = field(default_factory=dict)
    enabled: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> dict:
        return {
            "partner_ref": self.partner_ref,
            "name": self.name,
            "partner_type": self.partner_type,
            "trust_level": self.trust_level,
            "metadata": self.metadata,
            "enabled": self.enabled,
        }


@dataclass(eq=False, kw_only=True)
class TrustRelationship(AggregateRoot):
    tenant_id: str
    trust_ref: str
    source_entity_type: str
    source_entity_id: str
    target_entity_type: str
    target_entity_id: str
    trust_score: int = 50
    trust_level: str = TrustLevel.MEDIUM.value
    status: str = "active"
    metadata: dict = field(default_factory=dict)
    valid_from: datetime = field(default_factory=lambda: datetime.now(UTC))
    valid_until: datetime | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> dict:
        return {
            "trust_ref": self.trust_ref,
            "source_entity_type": self.source_entity_type,
            "source_entity_id": self.source_entity_id,
            "target_entity_type": self.target_entity_type,
            "target_entity_id": self.target_entity_id,
            "trust_score": self.trust_score,
            "trust_level": self.trust_level,
            "status": self.status,
            "metadata": self.metadata,
        }


@dataclass(eq=False, kw_only=True)
class ClaimsMapping(AggregateRoot):
    tenant_id: str
    mapping_ref: str
    provider_id: str
    source_claim: str
    target_claim: str
    transform_type: str = "direct"
    transform_config: dict = field(default_factory=dict)
    enabled: bool = True
    priority: int = 100

    def to_dict(self) -> dict:
        return {
            "mapping_ref": self.mapping_ref,
            "provider_id": self.provider_id,
            "source_claim": self.source_claim,
            "target_claim": self.target_claim,
            "transform_type": self.transform_type,
            "transform_config": self.transform_config,
            "enabled": self.enabled,
            "priority": self.priority,
        }


@dataclass(eq=False, kw_only=True)
class IdentityLink(AggregateRoot):
    tenant_id: str
    link_ref: str
    user_id: str
    provider_id: str
    external_subject: str
    link_status: str = "active"
    linked_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "link_ref": self.link_ref,
            "user_id": self.user_id,
            "provider_id": self.provider_id,
            "external_subject": self.external_subject,
            "link_status": self.link_status,
            "linked_at": self.linked_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class ProvisioningPolicy(AggregateRoot):
    tenant_id: str
    policy_ref: str
    provider_id: str | None
    jit_enabled: bool = True
    auto_role_assignment: bool = False
    default_roles: list[str] = field(default_factory=list)
    sync_mode: str = "jit"
    rules: list[dict] = field(default_factory=list)
    enabled: bool = True

    def to_dict(self) -> dict:
        return {
            "policy_ref": self.policy_ref,
            "provider_id": self.provider_id,
            "jit_enabled": self.jit_enabled,
            "auto_role_assignment": self.auto_role_assignment,
            "default_roles": self.default_roles,
            "sync_mode": self.sync_mode,
            "rules": self.rules,
            "enabled": self.enabled,
        }


@dataclass(eq=False, kw_only=True)
class SynchronizationJob(AggregateRoot):
    tenant_id: str
    job_ref: str
    provider_id: str
    direction: str = "inbound"
    status: str = "pending"
    records_processed: int = 0
    records_failed: int = 0
    metadata: dict = field(default_factory=dict)
    started_at: datetime | None = None
    completed_at: datetime | None = None
    error_message: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> dict:
        return {
            "job_ref": self.job_ref,
            "provider_id": self.provider_id,
            "direction": self.direction,
            "status": self.status,
            "records_processed": self.records_processed,
            "records_failed": self.records_failed,
            "metadata": self.metadata,
        }


@dataclass(eq=False, kw_only=True)
class FederationSession(AggregateRoot):
    tenant_id: str
    session_ref: str
    provider_id: str
    protocol: str
    user_id: str | None = None
    idp_session_id: str | None = None
    status: str = "active"
    expires_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> dict:
        return {
            "session_ref": self.session_ref,
            "provider_id": self.provider_id,
            "protocol": self.protocol,
            "user_id": self.user_id,
            "status": self.status,
            "expires_at": self.expires_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class TenantFederation(AggregateRoot):
    tenant_id: str
    federation_ref: str
    federation_mode: str = FederationMode.DEDICATED.value
    partner_tenant_id: str | None = None
    region: str | None = None
    shared_providers: list[str] = field(default_factory=list)
    enabled: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> dict:
        return {
            "federation_ref": self.federation_ref,
            "federation_mode": self.federation_mode,
            "partner_tenant_id": self.partner_tenant_id,
            "region": self.region,
            "shared_providers": self.shared_providers,
            "enabled": self.enabled,
        }
