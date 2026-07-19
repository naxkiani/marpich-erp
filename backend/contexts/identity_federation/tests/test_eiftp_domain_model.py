"""P200-B4 EIFTP Tactical Domain Model tests."""
from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from contexts.identity_federation.application.commands.establish_trust import (
    EstablishTrustCommand,
    handle_establish_trust,
)
from contexts.identity_federation.application.commands.register_ai_identity import (
    RegisterAIIdentityCommand,
    handle_register_ai_identity,
)
from contexts.identity_federation.domain.factories import TrustRelationshipFactory
from contexts.identity_federation.domain.services.eiftp_domain_model import (
    validate_domain_model_foundation,
)
from contexts.identity_federation.domain.specifications import ActiveTrustSpec
from contexts.identity_federation.domain.value_objects import TrustScore
from contexts.identity_federation.infrastructure.persistence.federation_memory_store import (
    InMemoryTrustRelationshipRepository,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.mark.unit
def test_domain_model_foundation_passes():
    result = validate_domain_model_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["foundation_for"] == "P200-B5"
    assert result["non_anemic_behaviors"] is True


@pytest.mark.unit
def test_trust_score_invariant():
    assert TrustScore(80).to_level() == "high"
    with pytest.raises(ValueError):
        TrustScore(101)


@pytest.mark.unit
def test_trust_grant_raises_domain_event():
    trust = TrustRelationshipFactory.create_pending(
        tenant_id="tenant-a",
        trust_ref="tr-1",
        source_entity_type="tenant",
        source_entity_id="tenant-a",
        target_entity_type="partner",
        target_entity_id="p1",
    )
    trust.grant()
    assert ActiveTrustSpec().is_satisfied_by(trust)
    names = [e.event_name for e in trust.domain_events]
    assert "federation.domain.trust.granted" in names


@pytest.mark.unit
@pytest.mark.asyncio
async def test_establish_trust_command():
    repo = InMemoryTrustRelationshipRepository()
    result = await handle_establish_trust(
        EstablishTrustCommand(
            tenant_id="tenant-a",
            trust_ref="tr-2",
            source_entity_type="org",
            source_entity_id="o1",
            target_entity_type="org",
            target_entity_id="o2",
            trust_score=90,
        ),
        trusts=repo,
    )
    assert result["status"] == "active"
    assert "federation.domain.trust.granted" in result["domain_events"]


@pytest.mark.unit
@pytest.mark.asyncio
async def test_register_ai_identity_requires_owner_and_emits():
    with pytest.raises(ValueError, match="owner"):
        await handle_register_ai_identity(
            RegisterAIIdentityCommand(
                tenant_id="tenant-a",
                agent_ref="agent-1",
                owner_principal_id="",
                display_name="Bot",
            )
        )
    result = await handle_register_ai_identity(
        RegisterAIIdentityCommand(
            tenant_id="tenant-a",
            agent_ref="agent-1",
            owner_principal_id="user-1",
            display_name="Bot",
            capabilities=["read", "summarize"],
        )
    )
    assert result["status"] == "active"
    assert "federation.domain.ai.registered" in result["domain_events"]


@pytest.mark.unit
def test_companion_identity_not_federation_sor():
    path = REPO_ROOT / "docs/architecture/identity/eiftp/MODEL_AGGREGATE_MAP.v1.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    companions = {c["name"]: c["bc"] for c in data["companion_owned_not_persisted_here"]}
    assert companions["Identity"] == "identity"
    assert companions["Credential"] == "authentication"
    fed_names = {a["name"] for a in data["federation_owned"]}
    assert "AiFederatedAgent" in fed_names
    assert "Identity" not in fed_names
