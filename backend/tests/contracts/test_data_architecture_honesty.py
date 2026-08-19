"""P337 data overlay must not invent published products, lineage, quality, or a new data platform."""
from __future__ import annotations

from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[3]
EXEC = REPO / "docs" / "meos" / "execution"
OVERLAY = EXEC / "MEOS_DATA_ARCHITECTURE.v1.yaml"
ARCH = EXEC / "MEOS_ARCHITECTURE_RATIONALIZATION.v1.yaml"
INITIATIVES = EXEC / "MEOS_INITIATIVE_PORTFOLIO.v1.yaml"
DEBT = EXEC / "MEOS_TECHNICAL_DEBT_REGISTRY.v1.yaml"
CONTEXTS = REPO / "backend" / "contexts"
DG_CONTEXT = CONTEXTS / "data_governance" / "context.yaml"
MIGRATIONS = REPO / "infrastructure" / "docker" / "migrations"
EVENTS = REPO / "docs" / "architecture" / "events"

FORBIDDEN_PRODUCT_STATUS = frozenset({"PUBLISHED", "ACTIVE", "HEALTHY"})
FORBIDDEN_RECOMMEND = frozenset({"RETIRE", "DELETE", "DESTROY"})


def _overlay() -> dict:
    return yaml.safe_load(OVERLAY.read_text(encoding="utf-8"))


def test_overlay_is_inventoried_not_operating():
    data = _overlay()
    assert data["overall_status"] == "INVENTORIED"
    assert data["maturity"] == "INVENTORIED"
    assert data["production_active"] is False
    assert data["published_data_product_count"] == 0
    assert data["active_data_product_count"] == 0
    assert data["lineage"] == "LINEAGE_INCOMPLETE"
    assert data["quality"] == "NOT_MEASURED"
    assert data["quality_incident_count"] == 0
    assert data["data_product_health"] == "NOT_MEASURED"
    assert data["retention_policy"] == "POLICY_GAP"
    assert data["data_value"] == "NOT_MEASURED"
    assert data["data_cost"] == "NOT_MEASURED"
    assert data["graphql_runtime"] == "NOT_AVAILABLE"
    assert data["autonomous_data"] == "BLOCKED"
    assert data["max_autonomy_level"] == "L0"
    assert data["ai_data_provenance"] == "NOT_AVAILABLE"
    assert data["dsar_runtime"] == "FAIL"
    assert data["recovery_production_rto_rpo"] == "NOT_VERIFIED"
    assert data["data_warehouse"] == "NOT_IMPLEMENTED"
    assert data["data_lake"] == "NOT_IMPLEMENTED"
    assert data["mdm_platform"] == "NOT_IMPLEMENTED"
    assert data["data_product_runtime"] == "CATALOG_ONLY"
    assert data["retirement_candidates"] == []
    assert data["new_data_platform"] == "FORBIDDEN"
    assert data["new_data_catalog"] == "FORBIDDEN"
    assert data["new_data_mesh"] == "FORBIDDEN"
    assert data["new_data_warehouse"] == "FORBIDDEN"
    assert data["new_mdm"] == "FORBIDDEN"


def test_file_inventory_matches_overlay_counts():
    data = _overlay()
    migrations = list(MIGRATIONS.glob("*.sql"))
    events = list(EVENTS.glob("*.json"))
    assert data["migration_file_count"] == len(migrations) == 55
    assert data["event_schema_file_count"] == len(events) == 47
    assert data["postgres_schema_count"] == 54
    assert data["postgres_table_count"] == 223
    assert data["rls_table_count"] == 93
    assert data["data_governance_schema_in_postgres"] == "ABSENT"


def test_does_not_create_forbidden_data_platforms():
    data = _overlay()
    ctx_yaml = yaml.safe_load(DG_CONTEXT.read_text(encoding="utf-8"))
    assert (CONTEXTS / "data_governance").is_dir()
    assert not (CONTEXTS / "data_mesh").exists()
    assert not (CONTEXTS / "data_product_platform").exists()
    assert not (CONTEXTS / "data_marketplace").exists()
    assert not (CONTEXTS / "data_quality_platform").exists()
    assert not (CONTEXTS / "metadata_governance_platform").exists()
    assert data["data_mesh_context"] == "ABSENT"
    assert data["data_product_platform_context"] == "ABSENT"
    assert ctx_yaml["schema"] == "data_governance"
    assert set(data["forbidden_sibling_contexts"]) == set(ctx_yaml["forbidden_sibling_bc"])
    for sibling in ctx_yaml["forbidden_sibling_bc"]:
        assert not (CONTEXTS / sibling).exists()


def test_no_published_products_or_retire_recommendations():
    data = _overlay()
    for product in data["products"]:
        assert product["status"] not in FORBIDDEN_PRODUCT_STATUS
        assert product["status"] == "NONE"
    for row in data["rationalization"]:
        assert row["recommendation"] not in FORBIDDEN_RECOMMEND
        assert row["recommendation"] != "RETIRE"
    for row in data["duplication"]:
        assert row["action"] in {"DO_NOT_DELETE", "DO_NOT_CONSOLIDATE", "TREAT_DOCS_AS_DESIGNED"}
        assert row["class"] in {"CONFIRMED", "LIKELY", "UNKNOWN"}
    assert all(d.get("owner") == "NOT_AVAILABLE" for d in data["domains"])


def test_p336_feed_reuses_existing_initiatives():
    overlay = _overlay()
    arch = yaml.safe_load(ARCH.read_text(encoding="utf-8"))
    initiatives = yaml.safe_load(INITIATIVES.read_text(encoding="utf-8"))
    debt = yaml.safe_load(DEBT.read_text(encoding="utf-8"))
    init_ids = {row["id"] for row in initiatives["initiatives"]}
    debt_ids = {item["id"] for item in debt["items"]}
    feed = overlay["p336_feed"]
    assert feed["new_data_platform"] == "FORBIDDEN"
    assert feed["new_initiative"] == "FORBIDDEN"
    for iid in feed["initiative_ids"]:
        assert iid in init_ids
    for did in feed["debt_ids"]:
        assert did in debt_ids
    assert arch.get("data_architecture_sor") == "docs/meos/execution/MEOS_DATA_ARCHITECTURE.v1.yaml"
    assert overlay["architecture_sor"] == "docs/meos/execution/MEOS_ARCHITECTURE_RATIONALIZATION.v1.yaml"
