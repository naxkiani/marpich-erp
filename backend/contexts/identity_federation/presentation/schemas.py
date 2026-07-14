"""Identity Federation API schemas."""
from __future__ import annotations

from pydantic import BaseModel, Field


class RegisterProviderRequest(BaseModel):
    protocol: str
    name: str
    config: dict | None = None
    plugin_id: str | None = None


class RegisterPartnerRequest(BaseModel):
    name: str
    partner_type: str = "organization"
    trust_level: str = "medium"
    metadata: dict | None = None


class CreateTrustRequest(BaseModel):
    source_entity_type: str
    source_entity_id: str
    target_entity_type: str
    target_entity_id: str


class ClaimsMappingRequest(BaseModel):
    provider_ref: str
    source_claim: str
    target_claim: str
    transform_type: str = "direct"
    transform_config: dict | None = None
    priority: int = 100


class TransformClaimsRequest(BaseModel):
    provider_ref: str
    raw_claims: dict = Field(default_factory=dict)


class DiscoverIdentityRequest(BaseModel):
    email: str | None = None


class BrokerAuthRequest(BaseModel):
    email: str | None = None
    provider_hint: str | None = None
    raw_claims: dict = Field(default_factory=dict)


class LinkIdentityRequest(BaseModel):
    user_id: str
    provider_ref: str
    external_subject: str


class JitProvisionRequest(BaseModel):
    provider_ref: str
    claims: dict = Field(default_factory=dict)


class FederatedLogoutRequest(BaseModel):
    session_ref: str
    user_id: str


class SyncJobRequest(BaseModel):
    provider_ref: str
    direction: str = "inbound"


class TenantFederationRequest(BaseModel):
    federation_mode: str
    partner_tenant_id: str | None = None
    region: str | None = None
    shared_providers: list[str] | None = None


class EvaluateTrustRequest(BaseModel):
    organization_trust: int = 50
    partner_trust: int = 50
    identity_trust: int = 50
    device_trust: int = 50
