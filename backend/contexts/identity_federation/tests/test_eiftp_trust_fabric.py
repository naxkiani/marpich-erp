"""P200-B6 Trust Fabric foundation + CQRS tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.identity_federation.application.commands.trust_fabric_commands import (
    AddTrustEvidenceCommand,
    ApproveTrustCommand,
    CreateTrustRelationshipCommand,
    EvaluateTrustContinuousCommand,
    RevokeTrustCommand,
    handle_add_trust_evidence,
    handle_approve_trust,
    handle_create_trust_relationship,
    handle_evaluate_trust_continuous,
    handle_revoke_trust,
)
from contexts.identity_federation.application.queries.trust_fabric_queries import (
    GetTrustStatusQuery,
    handle_get_trust_fabric_surface,
    handle_get_trust_status,
)
from contexts.identity_federation.container import (
    get_trust_relationship_repository,
    reset_identity_federation_service,
)
from contexts.identity_federation.domain.services.eiftp_trust_fabric import (
    validate_trust_fabric_foundation,
)
from contexts.identity_federation.domain.services.trust_fabric_engine import get_trust_fabric_engine
from contexts.identity_federation.domain.services.trust_score_engine import compute_continuous_score
from contexts.identity_federation.domain.value_objects.trust_levels import (
    can_transition,
    level_from_score,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_identity_federation_service()
    yield
    reset_identity_federation_service()


@pytest.mark.unit
def test_trust_fabric_foundation_passes():
    result = validate_trust_fabric_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["foundation_for"] == "P200-B7"
    assert result["levels_0_to_5"] is True
    assert result["explainable_scores"] is True
    assert result["no_permit_deny_in_score"] is True


@pytest.mark.unit
def test_score_engine_explainable_and_risk_invert():
    high = compute_continuous_score(
        inputs={
            "identity_assurance": 90,
            "authentication_strength": 90,
            "behavior_analysis": 80,
            "risk_signals": 10,
            "compliance_status": 85,
            "device_security": 80,
            "network_context": 70,
            "historical_trust": 80,
            "threat_intelligence": 70,
            "ai_analysis": 75,
        }
    )
    low = compute_continuous_score(inputs={"risk_signals": 95, "identity_assurance": 20})
    assert high["explainable"] is True
    assert high["permit_deny"] is None if "permit_deny" in high else True
    assert high["trust_score"] > low["trust_score"]
    assert "factors" in high and high["factors"]


@pytest.mark.unit
def test_level_bands_and_transition_gates():
    assert level_from_score(10) == 0
    assert level_from_score(50) == 2
    assert level_from_score(95) == 5
    skip = can_transition(from_level=1, to_level=4, score=95, evidence_types={"authn"})
    assert skip["allowed"] is False
    ok = can_transition(
        from_level=1,
        to_level=2,
        score=50,
        evidence_types={"authn", "assurance"},
    )
    assert ok["allowed"] is True


@pytest.mark.unit
def test_fabric_never_returns_permit_deny():
    evaluation = get_trust_fabric_engine().evaluate_continuous(
        inputs={"identity_assurance": 80, "risk_signals": 20},
        zero_trust_ctx={"risk_score": 90},
    )
    assert evaluation["permit_deny"] is None
    assert evaluation["decision_type"] == "trust_facts"
    assert "enterprise_level" in evaluation


@pytest.mark.unit
@pytest.mark.asyncio
async def test_create_approve_evaluate_revoke_lifecycle():
    trusts = get_trust_relationship_repository()
    created = await handle_create_trust_relationship(
        CreateTrustRelationshipCommand(
            tenant_id="tenant-a",
            source_entity_type="organization",
            source_entity_id="org-1",
            target_entity_type="organization",
            target_entity_id="org-2",
            trust_score=55,
        ),
        trusts=trusts,
    )
    ref = created["trust_ref"]
    approved = await handle_approve_trust(
        ApproveTrustCommand(tenant_id="tenant-a", trust_ref=ref),
        trusts=trusts,
    )
    assert approved["status"] in ("active", "granted", "established")
    await handle_add_trust_evidence(
        AddTrustEvidenceCommand(
            tenant_id="tenant-a",
            trust_ref=ref,
            evidence_type="authn",
            payload={"mfa": True},
        )
    )
    evaluated = await handle_evaluate_trust_continuous(
        EvaluateTrustContinuousCommand(
            tenant_id="tenant-a",
            trust_ref=ref,
            inputs={"identity_assurance": 85, "risk_signals": 15},
        ),
        trusts=trusts,
    )
    assert evaluated["permit_deny"] is None
    assert "evaluation" in evaluated
    status = await handle_get_trust_status(
        GetTrustStatusQuery(tenant_id="tenant-a", trust_ref=ref),
        trusts=trusts,
    )
    assert status["trust_ref"] == ref
    revoked = await handle_revoke_trust(
        RevokeTrustCommand(tenant_id="tenant-a", trust_ref=ref, reason="partner_exit"),
        trusts=trusts,
    )
    assert revoked["enterprise_level"] == 0


@pytest.mark.unit
def test_surface_and_no_sibling_bc():
    surface = handle_get_trust_fabric_surface()
    assert surface["adr"] == 220
    assert surface["validation"]["passed"] is True
    assert not (REPO_ROOT / "backend/contexts/eiftp").exists()
