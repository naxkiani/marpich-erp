"""Identity Federation Engine facade — composes domain engines (P200-B5)."""
from __future__ import annotations

from contexts.identity_federation.domain.services import (
    broker_intelligence_engine,
    claims_transformation_engine,
    protocol_engine,
    token_federation_engine,
    trust_management_engine,
    zero_trust_federation_engine,
)


class IdentityFederationEngine:
    """Central federation capability — no vendor SDK, no Permit/Deny."""

    def negotiate_protocol(self, *, requested: str | None = None) -> dict:
        return protocol_engine.negotiate_protocol(requested=requested)

    def protocol_catalog(self) -> dict:
        return protocol_engine.build_protocol_catalog()

    def transform_claims(self, *, raw_claims: dict, mappings: list[dict]) -> dict:
        return claims_transformation_engine.transform_claims(
            raw_claims=raw_claims, mappings=mappings
        )

    def map_attributes(self, *, external_attributes: dict, attribute_mappings: list[dict]) -> dict:
        return claims_transformation_engine.map_attributes(
            external_attributes=external_attributes,
            attribute_mappings=attribute_mappings,
        )

    def exchange_token(self, **kwargs) -> dict:
        return token_federation_engine.exchange_token(**kwargs)

    def validate_token(self, **kwargs) -> dict:
        return token_federation_engine.validate_federated_token(**kwargs)

    def resolve_identity_conflict(self, **kwargs) -> dict:
        return broker_intelligence_engine.resolve_identity_conflict(**kwargs)

    def detect_duplicates(self, **kwargs) -> dict:
        return broker_intelligence_engine.detect_duplicates(**kwargs)

    def evaluate_trust_hierarchy(self, **kwargs) -> dict:
        return trust_management_engine.evaluate_trust_hierarchy(**kwargs)

    def zero_trust_decision(self, **kwargs) -> dict:
        return zero_trust_federation_engine.evaluate_federation_zero_trust(**kwargs)


_engine: IdentityFederationEngine | None = None


def get_identity_federation_engine() -> IdentityFederationEngine:
    global _engine
    if _engine is None:
        _engine = IdentityFederationEngine()
    return _engine
