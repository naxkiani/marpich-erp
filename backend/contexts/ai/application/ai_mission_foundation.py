"""AI P214-B mission/vision/scope foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/422-enterprise-ai-mission-vision-scope.md",
    "docs/architecture/ENTERPRISE_AI_MISSION_VISION_SCOPE.md",
    "docs/architecture/enterprise_ai/AI_MVS_CAPABILITIES.v1.yaml",
    "docs/architecture/enterprise_ai/AI_MVS_DDD_CQRS.v1.yaml",
    "docs/architecture/enterprise_ai/AI_MVS_SECURITY.v1.yaml",
    "docs/architecture/enterprise_ai/AI_MVS_VALIDATION.v1.yaml",
    "backend/contexts/ai/domain/services/ai_platform_mission_scope.py",
    "backend/contexts/ai/domain/aggregates/ai_mission_aggregates.py",
    "backend/contexts/ai/infrastructure/acl/ai_mission_acl.py",
    "backend/contexts/ai/application/ai_mission_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/ml_platform",
    "backend/contexts/generative_ai",
    "backend/contexts/llm_platform",
    "backend/contexts/ai_core",
    "backend/contexts/vector_intelligence",
    "backend/contexts/model_lifecycle_platform",
)


def validate_ai_mission_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.ai.domain.aggregates.ai_mission_aggregates import (
        AiCapabilityMapRoot,
        AiGovernanceStrategyRoot,
        AiMaturityModelRoot,
        AiMissionDefinedRoot,
        AiRoadmapRoot,
        AiVisionDefinedRoot,
    )
    from contexts.ai.domain.services import ai_platform_mission_scope as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P214-B"
        and cat.get("adr") == 422
        and cat.get("sor") == "ai"
        and cat.get("capability") == "CAP-PLT-AI-001"
        and cat.get("fabric") == catmod.FABRIC
        and "continuously learning operating system" in cat["mission"]["statement"]
        and "intelligence layer that continuously learns" in cat["vision"]["statement"]
        and cat["mission_defined_required"] is True
        and cat["vision_defined_required"] is True
        and cat["ai_strategic_scope_defined_required"] is True
        and cat["ai_capability_map_present_required"] is True
        and cat["ai_operating_model_present_required"] is True
        and cat["ai_maturity_model_present_required"] is True
        and cat["ai_governance_strategy_defined_required"] is True
        and cat["ai_transformation_roadmap_present_required"] is True
        and cat["ai_value_framework_present_required"] is True
        and cat["responsible_ai_strategy_defined_required"] is True
        and cat["ai_security_strategy_present_required"] is True
        and cat["sibling_ai_bc_forbidden"] is True
        and cat["strategic_objectives"]["count"] >= 10
        and cat["capability_map"]["domain_count"] >= 6
        and cat["operating_model"]["layer_count"] >= 6
        and cat["maturity_model"]["level_count"] >= 6
        and cat["transformation_roadmap"]["phase_count"] >= 5
        and cat["value_framework"]["category_count"] >= 8
        and cat["use_case_framework"]["class_count"] >= 11
        and cat["knowledge_strategy"]["via_p213_l"] is True
        and cat["security_strategy"]["via_p210"] is True
        and cat["security_strategy"]["via_p211"] is True
        and cat["success_metrics"]["kpi_count"] >= 9
        and cat["cqrs"]["command_count"] >= 6
        and cat["cursor_outputs"]["count"] >= 18
        and "mission_is_undefined" in cat["quality_gates"]["reject_if"]
        and "P214-A" in cat["builds_on"]
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )

    def _bad(fn, **kwargs):
        try:
            fn(**kwargs)
            return True
        except ValueError:
            return False

    checks = [
        not _bad(
            AiMissionDefinedRoot.publish,
            tenant_id="t1",
            mission_ref="m1",
            defined=False,
        )
        and AiMissionDefinedRoot.publish(
            tenant_id="t1", mission_ref="m2"
        ).is_undefined()
        is False,
        not _bad(
            AiVisionDefinedRoot.publish,
            tenant_id="t1",
            vision_ref="v1",
            defined=False,
        )
        and AiVisionDefinedRoot.publish(
            tenant_id="t1", vision_ref="v2"
        ).is_undefined()
        is False,
        not _bad(
            AiCapabilityMapRoot.enable,
            tenant_id="t1",
            map_ref="c1",
            present=False,
        )
        and AiCapabilityMapRoot.enable(
            tenant_id="t1", map_ref="c2"
        ).is_missing()
        is False,
        not _bad(
            AiMaturityModelRoot.enable,
            tenant_id="t1",
            maturity_ref="mat1",
            present=False,
        )
        and AiMaturityModelRoot.enable(
            tenant_id="t1", maturity_ref="mat2"
        ).is_missing()
        is False,
        not _bad(
            AiGovernanceStrategyRoot.publish,
            tenant_id="t1",
            governance_ref="g1",
            defined=False,
        )
        and AiGovernanceStrategyRoot.publish(
            tenant_id="t1", governance_ref="g2"
        ).is_undefined()
        is False,
        not _bad(
            AiRoadmapRoot.enable,
            tenant_id="t1",
            roadmap_ref="r1",
            present=False,
        )
        and AiRoadmapRoot.enable(
            tenant_id="t1", roadmap_ref="r2"
        ).is_missing()
        is False,
    ]
    aggregates_ok = all(checks)

    acl_path = (
        root / "backend/contexts/ai/infrastructure/acl/ai_mission_acl.py"
    )
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_p207" in acl_text
        and "via_p208" in acl_text
        and "via_p210" in acl_text
        and "via_p211" in acl_text
        and "via_p212" in acl_text
        and "via_p212_j" in acl_text
        and "via_p213_l" in acl_text
        and "via_p213_m" in acl_text
        and "via_p214_a" in acl_text
        and "module_local_llm_sdk_forbidden" in acl_text
    )

    router = (
        root / "backend/contexts/ai/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@router.get("/mission")' in router
        and "/mission/readiness" in router
        and "/mission/statement" in router
        and "/mission/vision" in router
        and "/mission/objectives" in router
        and "/mission/capability-map" in router
        and "/mission/maturity" in router
        and "/mission/roadmap" in router
        and "/mission/security" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_AI_MISSION_VISION_SCOPE.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never Mission is undefined" in law
        and "Never Vision is undefined" in law
        and "Never AI strategic scope is undefined" in law
        and "Never AI capability map is missing" in law
        and "Never AI operating model is missing" in law
        and "Never AI maturity model is missing" in law
        and "Never AI governance strategy is undefined" in law
        and "Never AI transformation roadmap is missing" in law
        and "Never AI value framework is missing" in law
        and "Never Responsible AI strategy is undefined" in law
        and "Never AI security strategy is missing" in law
        and "Never Sibling AI BC" in law
        and "continuously learning operating system" in law
        and "MEOS Enterprise AI Strategic Intelligence Framework" in law
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
        "prompt": "P214-B",
        "adr": 422,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "catalog": catalog_ok,
        "aggregates": aggregates_ok,
        "acl": acl_ok,
        "router": router_ok,
        "documentation": doc_ok,
        "sor": "ai",
        "capability": "CAP-PLT-AI-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
