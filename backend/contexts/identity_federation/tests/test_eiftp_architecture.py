"""P200-B2 EIFTP Enterprise Architecture foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from contexts.identity_federation.application.commands.evaluate_trust import (
    EvaluateTrustCommand,
    handle_evaluate_trust,
)
from contexts.identity_federation.container import get_federation_trust_facts, reset_identity_federation_service
from contexts.identity_federation.domain.services.eiftp_architecture import (
    DELIVERABLE_COUNT,
    validate_architecture_foundation,
)
from contexts.identity_federation.infrastructure.caching import cache_key

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset_federation():
    reset_identity_federation_service()
    yield
    reset_identity_federation_service()


@pytest.mark.unit
def test_eiftp_architecture_foundation_passes():
    result = validate_architecture_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["foundation_for"] == "P200-B3"
    assert result["deliverable_count"] == DELIVERABLE_COUNT
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_deliverables_index_has_fifty():
    path = REPO_ROOT / "docs/architecture/identity/eiftp/ARCH_DELIVERABLES_INDEX.v1.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert len(data["deliverables"]) == 50
    assert set(data["deliverables"].keys()) == set(range(1, 51)) or set(
        int(k) for k in data["deliverables"]
    ) == set(range(1, 51))


@pytest.mark.unit
@pytest.mark.asyncio
async def test_evaluate_trust_command_returns_facts_not_permit():
    dto = await handle_evaluate_trust(
        EvaluateTrustCommand(tenant_id="t1", subject_id="u1", identity_trust=90)
    )
    assert dto.trust_score >= 50
    assert "permit" not in dto.to_dict()
    assert "deny" not in dto.to_dict()
    assert dto.reason_codes == ["federation.trust.evaluated"]


@pytest.mark.unit
@pytest.mark.asyncio
async def test_shared_port_evaluate_trust():
    port = get_federation_trust_facts()
    facts = await port.evaluate_trust(
        "t1",
        subject_id="agent-1",
        subject_kind="ai_agent",
        context={"identity_trust": 80, "device_trust": 70},
    )
    assert facts.tenant_id == "t1"
    assert facts.subject_kind == "ai_agent"
    assert facts.trust_score > 0


@pytest.mark.unit
def test_redis_key_pattern():
    assert cache_key("tenant-a", "session", "s1") == "fed:tenant-a:session:s1"


@pytest.mark.unit
def test_no_eiftp_sibling_bc():
    assert not (REPO_ROOT / "backend/contexts/eiftp").exists()
