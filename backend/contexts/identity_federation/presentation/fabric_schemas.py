"""P198-C1 Fabric Security API schemas."""
from __future__ import annotations

from pydantic import BaseModel, Field


class MeshRouteRequest(BaseModel):
    email: str | None = None
    node_hint: str | None = None


class MeshSyncRequest(BaseModel):
    node_id: str
    direction: str = "inbound"


class TrustNodeRequest(BaseModel):
    node_id: str
    node_type: str
    attributes: dict = Field(default_factory=dict)


class TrustEdgeRequest(BaseModel):
    edge_id: str
    from_id: str
    to_id: str
    relation: str = "trust"
    weight: float = 1.0
    metadata: dict = Field(default_factory=dict)


class TrustNeighborsRequest(BaseModel):
    node_id: str
    relation: str | None = None
    depth: int = 1


class TrustPathRequest(BaseModel):
    source: str
    target: str


class TrustPropagateRequest(BaseModel):
    source: str
    base_score: int = 80


class EnterpriseTrustRequest(BaseModel):
    identity: int = 50
    organization: int = 50
    partner: int = 50
    device: int = 50
    session: int = 50
    behavior: int = 50
    application: int = 50
    network: int = 50
    certificate: int = 50
    token: int = 50


class RecalculateTrustRequest(BaseModel):
    prior_score: int
    delta: int
    reason: str = "manual"


class TrustContractRequest(BaseModel):
    partner_type: str
    source_org: str
    target_org: str
    legal_policy_ref: str | None = None


class ZeroTrustFederationRequest(BaseModel):
    user_id: str = "anonymous"
    identity_verified: bool = True
    device_trusted: bool = False
    application_trusted: bool = True
    location_allowed: bool = True
    behavior_anomaly: bool = False
    session_valid: bool = True
    network_trusted: bool = True
    organization_trusted: bool = True
    risk_score: int = 0
    trust_score: int = 50
    use_adaptive_pdp: bool = True


class SecurityValidateRequest(BaseModel):
    state: str | None = None
    expected_state: str | None = None
    nonce: str | None = None
    expected_nonce: str | None = None
    audience: str | None = None
    expected_audience: str | None = None
    origin: str | None = None
    allowed_origins: list[str] | None = None
    signature_valid: bool = True
    replay_key: str | None = None
    token_exp: int | None = None


class RiskFederationRequest(BaseModel):
    protocol: str = "oidc"
    device_risk: int = 0
    behavior_risk: int = 0
    network_risk: int = 0
    organization_risk: int = 0
    certificate_risk: int = 0
    country_risk: int = 0
    transaction_risk: int = 0
    trust_score: int = 50


class BrokerIntelRequest(BaseModel):
    email: str | None = None
    risk_score: int = 0
    trust_score: int = 50


class DuplicateDetectRequest(BaseModel):
    email: str | None = None
    external_subject: str | None = None
    candidates: list[dict] = Field(default_factory=list)


class TokenExchangeRequest(BaseModel):
    source_type: str
    target_type: str
    subject: str
    audience: str
    scopes: list[str] | None = None
    claims: dict | None = None


class TokenTranslateRequest(BaseModel):
    protocol: str
    claims: dict = Field(default_factory=dict)


class FederateSessionRequest(BaseModel):
    session_ref: str
    user_id: str
    provider_ref: str
    protocol: str = "oidc"
    apps: list[str] | None = None


class GlobalLogoutRequest(BaseModel):
    user_id: str
    sessions: list[dict] = Field(default_factory=list)
