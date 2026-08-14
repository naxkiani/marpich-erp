"""Civilization P219-A mission / vision / strategy foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/554-enterprise-civilization-operating-system-mission.md",
    "docs/architecture/ENTERPRISE_CIVILIZATION_OPERATING_SYSTEM_MISSION.md",
    "docs/architecture/civilization/CIVILIZATION_MISSION_CAPABILITIES.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_MISSION_BOUNDED_CONTEXTS.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_MISSION_DDD_CQRS.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_MISSION_SECURITY.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_MISSION_VALIDATION.v1.yaml",
    "docs/architecture/civilization/P219_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/civilization/domain/services/civ_platform_mission.py",
    "backend/contexts/civilization/domain/aggregates/civ_mission_aggregates.py",
    "backend/contexts/civilization/infrastructure/acl/civ_mission_acl.py",
    "backend/contexts/civilization/application/civ_mission_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/civilization_mission_platform",
    "backend/contexts/civilization_vision_platform",
    "backend/contexts/civilization_strategy_platform",
)


def validate_civ_mission_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.civilization.domain.aggregates.civ_mission_aggregates import (
        CapabilityFrameworkRoot, CivilizationMissionRoot, CivilizationVisionRoot,
        EvolutionRoadmapRoot, GovernanceStrategyRoot, IntegrationStrategyRoot,
        MaturityModelRoot, StrategicPillarsRoot, StrategicScopeRoot,
    )
    from contexts.civilization.domain.services import civ_platform_mission as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P219-A" and cat["adr"] == 554 and cat["sor"] == "civilization"
        and cat["capability"] == "CAP-PLT-CIV-001"
        and cat["fabric"] == "meos_civilization_os_strategic_framework"
        and cat["foundation_gate"] == "P219"
        and cat["intelligence_nexus_gate"] == "P218-Z" and cat["space_gate"] == "P218"
        and cat["bio_gate"] == "P217-Z" and cat["robotics_gate"] == "P216-Z"
        and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["civilization_os_mission_framework_present_required"] is True
        and cat["civilization_os_vision_framework_present_required"] is True
        and cat["strategic_civilization_scope_present_required"] is True
        and cat["civilization_os_capability_framework_present_required"] is True
        and cat["strategic_pillars_framework_present_required"] is True
        and cat["maturity_model_present_required"] is True
        and cat["governance_framework_present_required"] is True
        and cat["meos_integration_strategy_present_required"] is True
        and cat["future_evolution_roadmap_present_required"] is True
        and cat["value_framework_present_required"] is True
        and cat["success_metrics_framework_present_required"] is True
        and cat["bounded_contexts"]["context_count"] >= 7
        and cat["microservices"]["service_count"] >= 8
        and cat["objectives"]["objective_count"] >= 7
        and cat["strategic_scope"]["domain_count"] == 7
        and cat["capability_framework"]["group_count"] == 8
        and cat["value_streams"]["stream_count"] >= 10
        and cat["value_streams"]["pillars"]["pillar_count"] == 6
        and cat["maturity_model"]["level_count"] == 5
        and cat["success_metrics"]["metric_count"] == 8
        and cat["never_replace_p219_foundation"] is True
        and cat["never_replace_space"] is True
        and cat["never_replace_p218_z_intelligence_nexus"] is True
        and cat["never_merge_p218_t_space_civilization"] is True
        and cat["never_opaque_unexplainable_civilization_strategy"] is True
        and cat["never_ungated_civilization_decision_strategy"] is True
        and cat["never_skip_human_authority_strategy"] is True
        and cat["never_skip_ethical_civilization_governance_strategy"] is True
        and cat["never_violate_human_sovereignty_strategy"] is True
        and cat["foundation_for_p219_b"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        CivilizationMissionRoot.enable(tenant_id="t1", mission_ref="m1").is_missing() is False,
        CivilizationVisionRoot.enable(tenant_id="t1", vision_ref="v1").is_missing() is False,
        StrategicScopeRoot.enable(tenant_id="t1", scope_ref="s1").is_missing() is False,
        CapabilityFrameworkRoot.enable(tenant_id="t1", capability_ref="c1").is_missing() is False,
        StrategicPillarsRoot.enable(tenant_id="t1", pillars_ref="p1").is_missing() is False,
        MaturityModelRoot.enable(tenant_id="t1", maturity_ref="mm1").is_missing() is False,
        EvolutionRoadmapRoot.enable(tenant_id="t1", roadmap_ref="r1").is_missing() is False,
        GovernanceStrategyRoot.enable(tenant_id="t1", governance_ref="g1").is_missing() is False,
        IntegrationStrategyRoot.enable(tenant_id="t1", integration_ref="i1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/civilization/infrastructure/acl/civ_mission_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p219", "via_p218_z", "via_p218", "via_p217", "via_p216_z", "via_p215_z", "via_p214_z",
        "via_policy_engine", "via_workflow", "via_audit", "via_identity", "via_core_platform",
        "never_replace_p219_foundation", "never_replace_p218_z_intelligence_nexus",
        "never_replace_space", "never_merge_p218_t_space_civilization",
        "never_replace_p215_z", "never_replace_p216_z", "never_replace_ai_platform",
        "never_replace_core_platform", "never_replace_biotechnology",
        "never_opaque_unexplainable_civilization_strategy",
        "never_ungated_civilization_decision_strategy",
        "never_skip_human_authority_strategy",
        "never_skip_ethical_civilization_governance_strategy",
        "never_violate_human_sovereignty_strategy",
        "module_local_civilization_mission_forbidden",
    ))
    router = (root / "backend/contexts/civilization/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@civilization_router.get("/mission")', "/mission/vision", "/mission/objectives",
        "/mission/scope", "/mission/capabilities", "/mission/value-streams",
        "/mission/maturity", "/mission/roadmap", "/mission/governance",
        "/mission/integration", "/mission/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_CIVILIZATION_OPERATING_SYSTEM_MISSION.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Civilization OS Mission Framework is missing",
        "Never Civilization OS Vision Framework is missing",
        "Never Strategic Civilization Scope is missing",
        "Never Civilization OS Capability Framework is missing",
        "Never Strategic Pillars Framework is missing",
        "Never Maturity Model is missing",
        "Never Governance Framework is missing",
        "Never MEOS Integration Strategy is missing",
        "Never Future Evolution Roadmap is missing",
        "Never Value Framework is missing",
        "Never Success Metrics Framework is missing",
        "Never Replace P219 Foundation",
        "Never Replace Core Platform",
        "Never Replace AI Platform",
        "Never Replace P215-Z Quantum",
        "Never Replace P216-Z Robotics",
        "Never Replace P217 Biotechnology",
        "Never Replace P218 Space",
        "Never Replace P218-Z Intelligence Nexus",
        "Never Merge P218-T Space Civilization Phase",
        "Never Skip Human Authority Strategy",
        "Never Skip Ethical Civilization Governance Strategy",
        "Never Opaque Unexplainable Civilization Strategy",
        "Never Ungated Civilization Decision Strategy",
        "Never Violate Human Sovereignty Strategy",
        "unified intelligent operating foundation",
        "P219-B",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P219-A", "adr": 554, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "civilization",
        "capability": "CAP-PLT-CIV-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
