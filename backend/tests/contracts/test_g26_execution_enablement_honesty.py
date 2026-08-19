"""P340 G26 enablement must not close G26 without evidence or invent actions/benefits."""
from __future__ import annotations

from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[3]
EXEC = REPO / "docs" / "meos" / "execution"
OVERLAY = EXEC / "MEOS_G26_EXECUTION_ENABLEMENT.v1.yaml"
P339 = EXEC / "MEOS_DECISION_EXECUTION.v1.yaml"
DECISIONS = EXEC / "MEOS_DECISION_REGISTRY.v1.yaml"
DEBT = EXEC / "MEOS_TECHNICAL_DEBT_REGISTRY.v1.yaml"
CHANGES = EXEC / "MEOS_CHANGE_REGISTRY.v1.yaml"
COMPOSE = REPO / "infrastructure" / "docker" / "compose" / "docker-compose.meos-prod.yml"
WORKFLOW = REPO / "backend" / "contexts" / "workflow"
CONTEXTS = REPO / "backend" / "contexts"

HOLD_IDS = frozenset(
    {"DEC-P314-001", "DEC-P319-001", "DEC-P324-001", "DEC-P326-001"}
)


def _overlay() -> dict:
    return yaml.safe_load(OVERLAY.read_text(encoding="utf-8"))


def test_outcome_b_g26_remains_blocked():
    data = _overlay()
    assert data["outcome"] == "OUTCOME_B"
    assert data["overall_status"] == "BLOCKED"
    assert data["g26"]["status"] == "BLOCKED"
    assert data["production_certified"] is False
    assert data["go_live"] == "NOT APPROVED"
    assert data["production_active"] is False
    assert data["closed_loop"] == "BLOCKED"
    assert data["smoke_path"] == "NOT_EXECUTED"
    g26 = data["g26"]
    assert g26["compose_profile"] == "EXISTS"
    assert COMPOSE.is_file()
    assert g26["cloud_cluster"] == "MISSING"
    assert g26["public_ca_tls"] == "MISSING"
    assert g26["secret_manager"] == "MISSING"
    assert g26["ci_immutable_sha_deploy"] == "BLOCKED"
    assert g26["meosprod_stack"] == "STOPPED"
    assert "dirty" in str(g26["git_describe"])


def test_no_invented_actions_benefits_or_second_engines():
    data = _overlay()
    p339 = yaml.safe_load(P339.read_text(encoding="utf-8"))
    assert data["authorized_action_count"] == 0
    assert data["runtime_action_count"] == 0
    assert data["benefit_count"] == 0
    assert data["realized_benefit_count"] == 0
    assert data["value_variance"] == "NOT_MEASURED"
    assert data["synthetic_tasks"] == "FORBIDDEN"
    assert data["synthetic_actions"] == "FORBIDDEN"
    assert data["new_pmo"] == "FORBIDDEN"
    assert data["new_workflow_engine"] == "FORBIDDEN"
    assert data["new_bpm"] == "FORBIDDEN"
    assert data["autonomy_level"] == "L0"
    assert data["ai_execution"] == "STUB"
    assert data["observability"]["g23"] == "FAIL"
    assert p339["authorized_action_count"] == 0
    assert p339["closed_loop"] == "BLOCKED"
    assert not (CONTEXTS / "pmo").exists()
    assert not (CONTEXTS / "decision_execution").exists()


def test_holds_preserved_and_workflow_unbound():
    data = _overlay()
    registry = yaml.safe_load(DECISIONS.read_text(encoding="utf-8"))
    assert set(data["holds_preserved"]) == HOLD_IDS
    assert data["workflow_binding"]["status"] == "NOT_AVAILABLE"
    assert data["workflow_binding"]["decision_ids_bound"] == 0
    assert data["task_binding"]["bound_task_count"] == 0
    for row in registry["decisions"]:
        assert row["id"] in HOLD_IDS
        assert row["workflow_task_id"] == "NOT_AVAILABLE"
        assert row["lifecycle"] == "DECIDE"
    sources = " ".join(
        p.read_text(encoding="utf-8")
        for p in WORKFLOW.rglob("*.py")
        if p.name != "__init__.py"
    )
    assert "decision_id" not in sources


def test_g26_debt_and_change_not_resolved():
    data = _overlay()
    debt = yaml.safe_load(DEBT.read_text(encoding="utf-8"))
    changes = yaml.safe_load(CHANGES.read_text(encoding="utf-8"))
    g26 = next(i for i in debt["items"] if i["id"] == "TD-G26-PROD-CLUSTER")
    assert g26["status"] != "RESOLVED"
    chg = next(c for c in changes["changes"] if c["id"] == "CHG-G26")
    assert chg["status"] == "ASSESSED"
    blk = next(b for b in changes["blockers"] if b["id"] == "BLK-G26")
    assert blk["status"] == "BLOCKED"
    assert data["g26"]["debt_id"] == "TD-G26-PROD-CLUSTER"
    assert data["g26"]["change_id"] == "CHG-G26"
