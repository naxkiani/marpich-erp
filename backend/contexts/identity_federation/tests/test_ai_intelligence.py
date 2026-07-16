"""P198-C2 AI identity intelligence unit tests."""
import pytest

from contexts.identity_federation.container import (
    get_fabric_intelligence_service,
    get_identity_federation_ai_service,
    get_identity_federation_service,
    reset_identity_federation_service,
)
from contexts.identity_federation.domain.services import (
    ai_identity_copilot,
    ai_identity_intelligence_engine as ai_engine,
    federation_privacy_engine,
    identity_analytics_engine,
)
from contexts.identity_federation.domain.services.ai_identity_intelligence_engine import (
    IdentityFeatureVector,
)


@pytest.fixture(autouse=True)
def _reset():
    reset_identity_federation_service()
    yield
    reset_identity_federation_service()


@pytest.mark.unit
def test_ai_predict_explainable():
    result = ai_engine.predict_identity_intelligence(
        IdentityFeatureVector(failed_logins=8, device_confidence=0.2, geo_risk=0.8),
        confidence_threshold=0.7,
    )
    assert "explanation" in result
    assert result["explanation"]["explainable"] is True
    assert result["identity_health_score"] >= 0


@pytest.mark.unit
def test_model_registry_and_pipelines():
    models = ai_engine.list_models()
    assert len(models) >= 5
    manifest = ai_engine.ml_pipeline_manifest()
    assert "feature_store" in manifest


@pytest.mark.unit
def test_analytics_and_insights():
    analytics = identity_analytics_engine.build_identity_analytics(
        providers=[{"protocol": "oidc", "enabled": True}],
        partners=[],
        trusts=[{"trust_score": 80}],
        audit_entries=[{"decision": "deny", "event_type": "login"}],
        risk_scores=[20, 75, 90],
    )
    insights = identity_analytics_engine.synthesize_ai_insights(analytics)
    assert analytics["failed_logins"] == 1
    assert len(insights) >= 1
    exec_report = identity_analytics_engine.executive_report(analytics, insights=insights)
    assert exec_report["report_type"] == "executive"


@pytest.mark.unit
def test_copilot_explains_errors():
    answer = ai_identity_copilot.explain_federation_error(
        error_code="federation.errors.no_provider_routed"
    )
    assert "explanation" in answer


@pytest.mark.unit
def test_privacy_controls_cover_frameworks():
    controls = federation_privacy_engine.privacy_controls()
    assert "GDPR" in controls["frameworks"]
    assert "HIPAA" in controls["frameworks"]
    assert len(federation_privacy_engine.retention_policies()) >= 3


@pytest.mark.unit
@pytest.mark.asyncio
async def test_intelligence_service_predict_and_dashboard():
    fed = get_identity_federation_service()
    await fed.seed("intel-t1")
    intel = get_fabric_intelligence_service()
    pred = await intel.predict(
        "intel-t1",
        features={"failed_logins": 3, "device_confidence": 0.3},
    )
    assert pred.succeeded
    assert "prediction_id" in pred.unwrap()
    dash = (await intel.intelligence_dashboard("intel-t1")).unwrap()
    assert "quality_gates" in dash
    surfaces = (await get_identity_federation_ai_service().list_surfaces()).unwrap()
    assert surfaces["surfaces"]["assistant"] is True
    copilot = await intel.copilot("intel-t1", question="What policies should I improve?")
    assert copilot.succeeded
