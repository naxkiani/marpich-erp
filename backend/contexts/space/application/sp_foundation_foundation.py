"""Space P218 foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/526-enterprise-space-intelligence-foundation.md",
    "docs/architecture/ENTERPRISE_SPACE_INTELLIGENCE_FOUNDATION.md",
    "docs/architecture/space/SPACE_FOUNDATION_CAPABILITIES.v1.yaml",
    "docs/architecture/space/SPACE_FOUNDATION_BOUNDED_CONTEXTS.v1.yaml",
    "docs/architecture/space/SPACE_FOUNDATION_DDD_CQRS.v1.yaml",
    "docs/architecture/space/SPACE_FOUNDATION_SECURITY.v1.yaml",
    "docs/architecture/space/SPACE_FOUNDATION_VALIDATION.v1.yaml",
    "docs/architecture/space/P218_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/space/domain/services/sp_platform_foundation.py",
    "backend/contexts/space/domain/aggregates/sp_foundation_aggregates.py",
    "backend/contexts/space/infrastructure/acl/sp_foundation_acl.py",
    "backend/contexts/space/application/sp_foundation_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/space_intelligence_platform",
    "backend/contexts/orbital_civilization_platform",
    "backend/contexts/autonomous_space_operations_platform",
)
def validate_sp_foundation_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.space.domain.aggregates.sp_foundation_aggregates import (
        SpaceIntelligencePlatformRoot, SpaceAiOperatingSystemRoot, OrbitalCivilizationRoot,
        AutonomousSpaceOperationsRoot, SpaceDigitalTwinRoot, SpaceKnowledgeGraphRoot,
        SpaceIntelligenceAgentsRoot, MeosSpaceIntelligenceCoreRoot, SpaceTrustRoot, SpaceSecurityRoot,
    )
    from contexts.space.domain.services import sp_platform_foundation as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P218" and cat["adr"] == 526 and cat["sor"] == "space"
        and cat["capability"] == "CAP-PLT-SP-001"
        and cat["fabric"] == "meos_space_intelligence_fabric"
        and cat["bio_gate"] == "P217-Z" and cat["robotics_gate"] == "P216-Z"
        and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["space_intelligence_platform_present_required"] is True
        and cat["space_ai_operating_system_present_required"] is True
        and cat["orbital_civilization_architecture_present_required"] is True
        and cat["autonomous_space_operations_platform_present_required"] is True
        and cat["space_digital_twin_present_required"] is True
        and cat["space_knowledge_graph_present_required"] is True
        and cat["space_intelligence_agents_present_required"] is True
        and cat["meos_space_intelligence_core_present_required"] is True
        and cat["security_architecture_present_required"] is True
        and cat["architecture"]["layer_count"] == 5
        and cat["space_ai"]["capability_count"] == 4
        and cat["orbital_civilization"]["domain_count"] == 4
        and cat["autonomous_operations"]["capability_count"] == 4
        and cat["agents"]["agent_count"] == 6
        and cat["bounded_contexts"]["context_count"] == 8
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 7
        and cat["domain_model"]["entity_count"] == 10
        and cat["never_replace_core_platform"] is True
        and cat["never_replace_ai_platform"] is True
        and cat["never_replace_p215_z"] is True
        and cat["never_replace_robotics_supreme"] is True
        and cat["never_replace_biotechnology"] is True
        and cat["no_module_local_llm"] is True
        and cat["never_opaque_mission_critical_decisions"] is True
        and cat["never_ungated_autonomous_mission_release"] is True
        and cat["never_skip_human_mission_oversight"] is True
        and cat["never_skip_space_cybersecurity_controls"] is True
        and cat["never_skip_space_sustainability_requirements"] is True
        and cat["space_ai"]["module_local_llm_forbidden"] is True
        and cat["foundation_for_p218_a"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        SpaceIntelligencePlatformRoot.enable(tenant_id="t1", space_ref="s1").is_missing() is False,
        SpaceAiOperatingSystemRoot.enable(tenant_id="t1", saios_ref="a1").is_missing() is False,
        OrbitalCivilizationRoot.enable(tenant_id="t1", civilization_ref="c1").is_missing() is False,
        AutonomousSpaceOperationsRoot.enable(tenant_id="t1", operations_ref="o1").is_missing() is False,
        SpaceDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        SpaceKnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="k1").is_missing() is False,
        SpaceIntelligenceAgentsRoot.enable(tenant_id="t1", agents_ref="ag1").is_missing() is False,
        MeosSpaceIntelligenceCoreRoot.enable(tenant_id="t1", core_ref="core1").is_missing() is False,
        SpaceTrustRoot.enable(tenant_id="t1", trust_ref="t1").is_missing() is False,
        SpaceSecurityRoot.enable(tenant_id="t1", security_ref="sec1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/space/infrastructure/acl/sp_foundation_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p214_z", "via_p215_z", "via_p216_z", "via_p217", "via_identity", "via_policy_engine", "via_workflow",
        "via_audit", "via_integration_platform", "via_search", "via_core_platform",
        "never_replace_p215_z", "never_replace_ai_platform", "never_replace_core_platform",
        "never_replace_robotics_supreme", "never_replace_biotechnology", "never_replace_identity_platform",
        "module_local_llm_forbidden", "space_ai_via_p214z_acl_only", "robotics_via_p216z_acl_only",
        "quantum_optimization_via_p215z_acl_only", "bio_life_support_via_p217_acl_only",
        "telemetry_via_integration_platform_only", "never_ungated_autonomous_mission_release",
        "never_skip_human_mission_oversight", "never_opaque_mission_critical_decisions",
        "never_skip_space_cybersecurity_controls", "never_skip_space_sustainability_requirements",
        "module_local_space_foundation_forbidden",
    ))
    router = (root / "backend/contexts/space/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@space_router.get("/foundation")', "/foundation/vision", "/foundation/domain",
        "/foundation/bounded-contexts", "/foundation/architecture", "/foundation/space-ai",
        "/foundation/orbital-civilization", "/foundation/autonomous-operations",
        "/foundation/digital-twin", "/foundation/knowledge-graph", "/foundation/agents",
        "/foundation/governance", "/foundation/observability", "/foundation/security",
        "/foundation/cqrs", "/foundation/events", "/foundation/microservices",
        "/foundation/integration", "/foundation/deployment", "/foundation/roadmap",
        "/foundation/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_SPACE_INTELLIGENCE_FOUNDATION.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Space Intelligence Platform is missing",
        "Never Space AI Operating System is missing",
        "Never Orbital Civilization Architecture is missing",
        "Never Autonomous Space Operations Platform is missing",
        "Never Space Digital Twin is missing",
        "Never Space Knowledge Graph is missing",
        "Never Space Intelligence Agents are missing",
        "Never MEOS Space Intelligence Core is missing",
        "Never Replace Core Platform",
        "Never Replace AI Platform",
        "Never Replace P215-Z Quantum",
        "Never Replace P216-Z Robotics",
        "Never Replace P217 Biotechnology",
        "Never Module-Local LLM",
        "Never Opaque Mission-Critical Decisions",
        "Never Ungated Autonomous Mission Release",
        "Never Skip Human Mission Oversight",
        "Never Skip Space Cybersecurity Controls",
        "Never Skip Space Sustainability Requirements",
        "Create a next-generation intelligence ecosystem",
        "P214-Z", "P216-Z", "P217", "P218-A",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P218", "adr": 526, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "space",
        "capability": "CAP-PLT-SP-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
