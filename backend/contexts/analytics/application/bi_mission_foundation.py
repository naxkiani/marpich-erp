"""Analytics P213-B BI mission foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/395-enterprise-business-intelligence-mission-vision-scope.md",
    "docs/architecture/ENTERPRISE_BUSINESS_INTELLIGENCE_MISSION_VISION_SCOPE.md",
    "docs/architecture/business_intelligence/BI_MVS_CAPABILITIES.v1.yaml",
    "docs/architecture/business_intelligence/BI_MVS_DDD_CQRS.v1.yaml",
    "docs/architecture/business_intelligence/BI_MVS_SECURITY.v1.yaml",
    "docs/architecture/business_intelligence/BI_MVS_VALIDATION.v1.yaml",
    "backend/contexts/analytics/domain/services/bi_platform_mission_scope.py",
    "backend/contexts/analytics/domain/aggregates/bi_mission_aggregates.py",
    "backend/contexts/analytics/infrastructure/acl/bi_mission_acl.py",
    "backend/contexts/analytics/application/bi_mission_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/business_intelligence",
    "backend/contexts/decision_intelligence",
    "backend/contexts/reporting_platform",
    "backend/contexts/metric_governance_platform",
    "backend/contexts/visualization_platform",
    "backend/contexts/bi_core",
)


def validate_bi_mission_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.analytics.domain.aggregates.bi_mission_aggregates import (
        BiMissionDefinedRoot,
    )
    from contexts.analytics.domain.services import (
        bi_platform_mission_scope as mscope,
    )

    cat = mscope.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P213-B"
        and cat.get("adr") == 395
        and cat.get("sor") == "analytics"
        and cat.get("capability") == "CAP-PLT-BI-001"
        and cat["mission_defined_required"] is True
        and cat["vision_defined_required"] is True
        and cat["decision_intelligence_scope_defined_required"] is True
        and cat["capability_map_present_required"] is True
        and cat["operating_model_present_required"] is True
        and cat["governance_model_present_required"] is True
        and cat["ai_strategy_defined_required"] is True
        and cat["knowledge_graph_alignment_present_required"] is True
        and cat["digital_twin_alignment_present_required"] is True
        and cat["meos_integration_alignment_present_required"] is True
        and "trusted enterprise data" in cat["mission"]["statement"]
        and cat["strategic_objectives"]["count"] >= 6
        and cat["capability_map"]["capability_count"] >= 10
        and cat["enterprise_scope"]["scope_category_count"] >= 4
        and cat["operating_model"]["lifecycle_step_count"] >= 8
        and cat["maturity_model"]["level_count"] >= 6
        and cat["ai_strategy"]["level_count"] >= 5
        and cat["enterprise_roadmap"]["phase_count"] >= 5
        and cat["knowledge_graph_alignment"]["via_p212_j"] is True
        and cat["digital_twin_alignment"]["via_p212_l"] is True
        and cat["cursor_outputs"]["count"] >= 15
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
        and "mission_is_undefined" in cat["quality_gates"]["reject_if"]
    )

    try:
        BiMissionDefinedRoot.publish(
            tenant_id="t1", mission_ref="m1", defined=False
        )
        aggregates_ok = False
    except ValueError:
        aggregates_ok = not BiMissionDefinedRoot.publish(
            tenant_id="t1", mission_ref="m2"
        ).is_undefined()

    acl_path = (
        root
        / "backend/contexts/analytics/infrastructure/acl/bi_mission_acl.py"
    )
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_p212" in acl_text
        and "via_p212_j" in acl_text
        and "via_p212_l" in acl_text
        and "via_p207" in acl_text
        and "via_p208" in acl_text
        and "via_p211" in acl_text
        and "via_enterprise_ai" in acl_text
    )

    router = (
        root / "backend/contexts/analytics/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@router.get("/mission")' in router
        and "/mission/readiness" in router
    )

    law = (
        root
        / "docs/architecture/ENTERPRISE_BUSINESS_INTELLIGENCE_MISSION_VISION_SCOPE.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never Mission is undefined" in law
        and "Never Vision is undefined" in law
        and "Never Decision intelligence scope is undefined" in law
        and "Never Capability map is missing" in law
        and "Never Operating model is missing" in law
        and "Never Governance model is missing" in law
        and "Never AI strategy is undefined" in law
        and "Never Knowledge graph alignment is missing" in law
        and "Never Digital twin alignment is missing" in law
        and "Never MEOS integration alignment is missing" in law
        and "Never Sibling business intelligence BC" in law
        and (
            "MEOS Enterprise Intelligence mission is to transform"
            in law
        )
    )

    passed = (
        not missing
        and not sibling
        and catalog_ok
        and aggregates_ok
        and acl_ok
        and router_ok
        and doc_ok
    )
    return {
        "prompt": "P213-B",
        "adr": 395,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "catalog": catalog_ok,
        "aggregates": aggregates_ok,
        "acl": acl_ok,
        "router": router_ok,
        "documentation": doc_ok,
        "sor": "analytics",
        "capability": "CAP-PLT-BI-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
