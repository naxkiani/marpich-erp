"""Space P218-A mission / vision / strategy foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/527-enterprise-space-intelligence-mission.md",
    "docs/architecture/ENTERPRISE_SPACE_INTELLIGENCE_MISSION.md",
    "docs/architecture/space/SPACE_MISSION_CAPABILITIES.v1.yaml",
    "docs/architecture/space/SPACE_MISSION_BOUNDED_CONTEXTS.v1.yaml",
    "docs/architecture/space/SPACE_MISSION_DDD_CQRS.v1.yaml",
    "docs/architecture/space/SPACE_MISSION_SECURITY.v1.yaml",
    "docs/architecture/space/SPACE_MISSION_VALIDATION.v1.yaml",
    "docs/architecture/space/P218_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/space/domain/services/sp_platform_mission.py",
    "backend/contexts/space/domain/aggregates/sp_mission_aggregates.py",
    "backend/contexts/space/infrastructure/acl/sp_mission_acl.py",
    "backend/contexts/space/application/sp_mission_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/space_mission_platform",
    "backend/contexts/space_vision_platform",
    "backend/contexts/space_strategy_platform",
)
def validate_sp_mission_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.space.domain.aggregates.sp_mission_aggregates import (
        SpaceMissionRoot, SpaceVisionRoot, StrategicScopeRoot,
        CapabilityFrameworkRoot, ValueStreamsRoot, MaturityModelRoot,
        EvolutionRoadmapRoot, GovernanceStrategyRoot, IntegrationStrategyRoot,
    )
    from contexts.space.domain.services import sp_platform_mission as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P218-A" and cat["adr"] == 527 and cat["sor"] == "space"
        and cat["capability"] == "CAP-PLT-SP-001"
        and cat["fabric"] == "meos_space_intelligence_strategic_framework"
        and cat["foundation_gate"] == "P218" and cat["bio_gate"] == "P217-Z"
        and cat["robotics_gate"] == "P216-Z" and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["space_mission_framework_present_required"] is True
        and cat["space_vision_framework_present_required"] is True
        and cat["strategic_space_scope_present_required"] is True
        and cat["space_capability_framework_present_required"] is True
        and cat["value_streams_framework_present_required"] is True
        and cat["maturity_model_present_required"] is True
        and cat["governance_framework_present_required"] is True
        and cat["meos_integration_strategy_present_required"] is True
        and cat["future_evolution_roadmap_present_required"] is True
        and cat["bounded_contexts"]["context_count"] >= 7
        and cat["microservices"]["service_count"] >= 8
        and cat["objectives"]["objective_count"] >= 7
        and cat["drivers"]["driver_count"] >= 10
        and cat["capability_framework"]["l1_count"] >= 20
        and cat["value_streams"]["stream_count"] >= 10
        and cat["never_replace_p218_foundation"] is True
        and cat["never_replace_biotechnology"] is True
        and cat["never_replace_p216_z"] is True
        and cat["never_opaque_mission_critical_strategy"] is True
        and cat["never_ungated_autonomous_mission_strategy"] is True
        and cat["never_skip_human_mission_oversight_strategy"] is True
        and cat["never_skip_space_cybersecurity_strategy"] is True
        and cat["never_skip_space_sustainability_strategy"] is True
        and cat["foundation_for_p218_b"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        SpaceMissionRoot.enable(tenant_id="t1", mission_ref="m1").is_missing() is False,
        SpaceVisionRoot.enable(tenant_id="t1", vision_ref="v1").is_missing() is False,
        StrategicScopeRoot.enable(tenant_id="t1", scope_ref="s1").is_missing() is False,
        CapabilityFrameworkRoot.enable(tenant_id="t1", capability_ref="c1").is_missing() is False,
        ValueStreamsRoot.enable(tenant_id="t1", value_ref="vs1").is_missing() is False,
        MaturityModelRoot.enable(tenant_id="t1", maturity_ref="mm1").is_missing() is False,
        EvolutionRoadmapRoot.enable(tenant_id="t1", roadmap_ref="r1").is_missing() is False,
        GovernanceStrategyRoot.enable(tenant_id="t1", governance_ref="g1").is_missing() is False,
        IntegrationStrategyRoot.enable(tenant_id="t1", integration_ref="i1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/space/infrastructure/acl/sp_mission_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p218", "via_p217", "via_p216_z", "via_p215_z", "via_p214_z", "via_policy_engine", "via_workflow",
        "via_audit", "via_identity", "via_core_platform", "never_replace_p218_foundation",
        "never_replace_p215_z", "never_replace_p216_z", "never_replace_ai_platform",
        "never_replace_core_platform", "never_replace_biotechnology",
        "never_opaque_mission_critical_strategy", "never_ungated_autonomous_mission_strategy",
        "never_skip_human_mission_oversight_strategy", "never_skip_space_cybersecurity_strategy",
        "never_skip_space_sustainability_strategy", "module_local_space_mission_forbidden",
    ))
    router = (root / "backend/contexts/space/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@space_router.get("/mission")', "/mission/vision", "/mission/objectives",
        "/mission/scope", "/mission/capabilities", "/mission/value-streams",
        "/mission/maturity", "/mission/roadmap", "/mission/governance",
        "/mission/integration", "/mission/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_SPACE_INTELLIGENCE_MISSION.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Space Mission Framework is missing",
        "Never Space Vision Framework is missing",
        "Never Strategic Space Scope is missing",
        "Never Space Capability Framework is missing",
        "Never Value Streams Framework is missing",
        "Never Maturity Model is missing",
        "Never Governance Framework is missing",
        "Never MEOS Integration Strategy is missing",
        "Never Future Evolution Roadmap is missing",
        "Never Replace P218 Foundation",
        "Never Replace Core Platform",
        "Never Replace AI Platform",
        "Never Replace Quantum Supreme (P215-Z)",
        "Never Replace Robotics Supreme (P216-Z)",
        "Never Replace Biotechnology (P217)",
        "Never Skip Human Mission Oversight Strategy",
        "Never Skip Space Cybersecurity Strategy",
        "Never Skip Space Sustainability Strategy",
        "Never Opaque Mission-Critical Strategy",
        "Never Ungated Autonomous Mission Strategy",
        "Build a unified enterprise platform",
        "P218-B",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P218-A", "adr": 527, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "space",
        "capability": "CAP-PLT-SP-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
