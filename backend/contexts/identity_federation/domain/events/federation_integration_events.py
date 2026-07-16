"""Identity federation integration events."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent


@dataclass(frozen=True, kw_only=True)
class IdentityProviderRegisteredIntegration(IntegrationEvent):
    provider_ref: str
    protocol: str
    name: str

    @property
    def event_name(self) -> str:
        return "federation.provider.registered"

    @property
    def source_context(self) -> str:
        return "identity_federation"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"provider_ref": self.provider_ref, "protocol": self.protocol, "name": self.name}


@dataclass(frozen=True, kw_only=True)
class IdentityFederatedIntegration(IntegrationEvent):
    user_id: str
    provider_ref: str
    session_ref: str
    protocol: str

    @property
    def event_name(self) -> str:
        return "federation.identity.federated"

    @property
    def source_context(self) -> str:
        return "identity_federation"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "user_id": self.user_id,
            "provider_ref": self.provider_ref,
            "session_ref": self.session_ref,
            "protocol": self.protocol,
        }


@dataclass(frozen=True, kw_only=True)
class IdentityLinkedIntegration(IntegrationEvent):
    user_id: str
    provider_ref: str
    external_subject: str

    @property
    def event_name(self) -> str:
        return "federation.identity.linked"

    @property
    def source_context(self) -> str:
        return "identity_federation"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "user_id": self.user_id,
            "provider_ref": self.provider_ref,
            "external_subject": self.external_subject,
        }


@dataclass(frozen=True, kw_only=True)
class IdentityProvisionedIntegration(IntegrationEvent):
    user_id: str
    provider_ref: str
    provisioning_mode: str

    @property
    def event_name(self) -> str:
        return "federation.identity.provisioned"

    @property
    def source_context(self) -> str:
        return "identity_federation"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "user_id": self.user_id,
            "provider_ref": self.provider_ref,
            "provisioning_mode": self.provisioning_mode,
        }


@dataclass(frozen=True, kw_only=True)
class FederatedLogoutIntegration(IntegrationEvent):
    session_ref: str
    user_id: str
    provider_ref: str

    @property
    def event_name(self) -> str:
        return "federation.logout.completed"

    @property
    def source_context(self) -> str:
        return "identity_federation"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"session_ref": self.session_ref, "user_id": self.user_id, "provider_ref": self.provider_ref}


@dataclass(frozen=True, kw_only=True)
class TrustRelationshipEstablishedIntegration(IntegrationEvent):
    trust_ref: str
    source_entity_id: str
    target_entity_id: str
    trust_score: int

    @property
    def event_name(self) -> str:
        return "federation.trust.established"

    @property
    def source_context(self) -> str:
        return "identity_federation"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "trust_ref": self.trust_ref,
            "source_entity_id": self.source_entity_id,
            "target_entity_id": self.target_entity_id,
            "trust_score": self.trust_score,
        }


@dataclass(frozen=True, kw_only=True)
class ExternalAuthenticationSucceededIntegration(IntegrationEvent):
    user_id: str
    protocol: str
    provider_ref: str

    @property
    def event_name(self) -> str:
        return "federation.external_auth.succeeded"

    @property
    def source_context(self) -> str:
        return "identity_federation"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"user_id": self.user_id, "protocol": self.protocol, "provider_ref": self.provider_ref}


@dataclass(frozen=True, kw_only=True)
class ExternalAuthenticationFailedIntegration(IntegrationEvent):
    protocol: str
    reason: str

    @property
    def event_name(self) -> str:
        return "federation.external_auth.failed"

    @property
    def source_context(self) -> str:
        return "identity_federation"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"protocol": self.protocol, "reason": self.reason}


@dataclass(frozen=True, kw_only=True)
class ClaimsMappedIntegration(IntegrationEvent):
    provider_ref: str
    claims_count: int

    @property
    def event_name(self) -> str:
        return "federation.claims.mapped"

    @property
    def source_context(self) -> str:
        return "identity_federation"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"provider_ref": self.provider_ref, "claims_count": self.claims_count}


@dataclass(frozen=True, kw_only=True)
class TokenExchangedIntegration(IntegrationEvent):
    client_id: str
    grant_type: str

    @property
    def event_name(self) -> str:
        return "federation.token.exchanged"

    @property
    def source_context(self) -> str:
        return "identity_federation"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"client_id": self.client_id, "grant_type": self.grant_type}


@dataclass(frozen=True, kw_only=True)
class CertificateRotatedIntegration(IntegrationEvent):
    cert_ref: str
    kid: str

    @property
    def event_name(self) -> str:
        return "federation.certificate.rotated"

    @property
    def source_context(self) -> str:
        return "identity_federation"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"cert_ref": self.cert_ref, "kid": self.kid}


@dataclass(frozen=True, kw_only=True)
class TrustDecisionIntegration(IntegrationEvent):
    decision: str
    trust_score: int
    risk_score: int

    @property
    def event_name(self) -> str:
        return "federation.trust.decision"

    @property
    def source_context(self) -> str:
        return "identity_federation"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "decision": self.decision,
            "trust_score": self.trust_score,
            "risk_score": self.risk_score,
        }


@dataclass(frozen=True, kw_only=True)
class MeshRouteResolvedIntegration(IntegrationEvent):
    node_id: str
    method: str

    @property
    def event_name(self) -> str:
        return "federation.mesh.route_resolved"

    @property
    def source_context(self) -> str:
        return "identity_federation"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"node_id": self.node_id, "method": self.method}


@dataclass(frozen=True, kw_only=True)
class ZeroTrustFederationDecisionIntegration(IntegrationEvent):
    action: str
    risk_score: int
    failed_dimensions: tuple[str, ...]

    @property
    def event_name(self) -> str:
        return "federation.zero_trust.decision"

    @property
    def source_context(self) -> str:
        return "identity_federation"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "action": self.action,
            "risk_score": self.risk_score,
            "failed_dimensions": list(self.failed_dimensions),
        }


@dataclass(frozen=True, kw_only=True)
class IdentityAiPredictionCompletedIntegration(IntegrationEvent):
    prediction_id: str
    model_id: str
    risk_score: int
    classification: str

    @property
    def event_name(self) -> str:
        return "federation.ai.prediction.completed"

    @property
    def source_context(self) -> str:
        return "identity_federation"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "prediction_id": self.prediction_id,
            "model_id": self.model_id,
            "risk_score": self.risk_score,
            "classification": self.classification,
        }


@dataclass(frozen=True, kw_only=True)
class IdentityAiInsightGeneratedIntegration(IntegrationEvent):
    insight_count: int
    insight_types: tuple[str, ...]

    @property
    def event_name(self) -> str:
        return "federation.ai.insight.generated"

    @property
    def source_context(self) -> str:
        return "identity_federation"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "insight_count": self.insight_count,
            "insight_types": list(self.insight_types),
        }
