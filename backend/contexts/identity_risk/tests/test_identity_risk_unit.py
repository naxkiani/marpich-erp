"""Identity risk — unit tests."""
import pytest

from contexts.identity_risk.domain.aggregates.identity_risk_platform import IdentityRiskCapability
from contexts.identity_risk.domain.services import identity_risk_engine as engine


@pytest.mark.unit
def test_capability_catalog_has_ten_capabilities():
    caps = {c["capability"] for c in engine.list_capability_catalog()}
    assert IdentityRiskCapability.AUTHENTICATION_RISK_SCORING.value in caps
    assert IdentityRiskCapability.DIRECTORY_SYNC_RISK_SCORING.value in caps
    assert len(caps) == 10


@pytest.mark.unit
def test_score_authentication_saml_higher_than_webauthn():
    saml_score, _, _ = engine.score_authentication_event(auth_method="saml")
    webauthn_score, _, _ = engine.score_authentication_event(auth_method="webauthn")
    assert saml_score > webauthn_score


@pytest.mark.unit
def test_directory_bulk_create_triggers_anomaly_factor():
    score, factors, _ = engine.score_directory_sync_event(
        users_synced=50,
        users_created=15,
        bulk_create_threshold=10,
    )
    factor_names = {f["factor"] for f in factors}
    assert "bulk_create_anomaly" in factor_names
    assert score >= 25


@pytest.mark.unit
def test_classify_risk_level():
    assert engine.classify_risk_level(30, threshold=50) == "low"
    assert engine.classify_risk_level(55, threshold=50) == "medium"
    assert engine.classify_risk_level(75, threshold=50) == "high"
