"""Civilization P219 foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/553-enterprise-civilization-operating-system-foundation.md",
    "docs/architecture/ENTERPRISE_CIVILIZATION_OPERATING_SYSTEM_FOUNDATION.md",
    "docs/architecture/civilization/CIVILIZATION_FOUNDATION_CAPABILITIES.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_FOUNDATION_BOUNDED_CONTEXTS.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_FOUNDATION_DDD_CQRS.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_FOUNDATION_SECURITY.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_FOUNDATION_VALIDATION.v1.yaml",
    "docs/architecture/civilization/P219_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/civilization/domain/services/civ_platform_foundation.py",
    "backend/contexts/civilization/domain/aggregates/civ_foundation_aggregates.py",
    "backend/contexts/civilization/infrastructure/acl/civ_foundation_acl.py",
    "backend/contexts/civilization/application/civ_foundation_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/civilization_os_platform",
    "backend/contexts/planetary_governance_bc",
    "backend/contexts/human_civilization_bc",
)


def validate_civ_foundation_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.civilization.domain.aggregates.civ_foundation_aggregates import (
        CivilizationDigitalTwinRoot, CivilizationGovernanceRoot, CivilizationKnowledgeGraphRoot,
        CivilizationOperatingSystemRoot, CivilizationOsKernelRoot, HumanCivilizationRoot,
        InfrastructureIntelligenceRoot, MeosCivilizationOsCoreRoot, PlanetaryIntelligenceRoot,
    )
    from contexts.civilization.domain.services import civ_platform_foundation as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P219" and cat["adr"] == 553 and cat["sor"] == "civilization"
        and cat["capability"] == "CAP-PLT-CIV-001"
        and cat["fabric"] == "meos_civilization_operating_system_fabric"
        and cat["intelligence_nexus_gate"] == "P218-Z" and cat["space_gate"] == "P218"
        and cat["bio_gate"] == "P217-Z" and cat["robotics_gate"] == "P216-Z"
        and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["civilization_operating_system_present_required"] is True
        and cat["civilization_os_kernel_present_required"] is True
        and cat["planetary_intelligence_governance_present_required"] is True
        and cat["global_infrastructure_intelligence_present_required"] is True
        and cat["human_civilization_management_present_required"] is True
        and cat["civilization_digital_twin_present_required"] is True
        and cat["civilization_knowledge_graph_present_required"] is True
        and cat["civilization_governance_present_required"] is True
        and cat["meos_civilization_os_core_present_required"] is True
        and cat["architecture"]["layer_count"] == 5
        and cat["kernel"]["component_count"] == 6
        and cat["planetary_intelligence"]["domain_count"] == 8
        and cat["infrastructure"]["system_count"] == 7
        and cat["human_civilization"]["domain_count"] == 6
        and cat["digital_twin"]["representation_count"] == 7
        and cat["knowledge_graph"]["entity_count"] == 10
        and cat["agents"]["agent_count"] == 7
        and cat["bounded_contexts"]["context_count"] == 7
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 8
        and cat["domain_model"]["entity_count"] == 7
        and cat["never_replace_core_platform"] is True
        and cat["never_replace_ai_platform"] is True
        and cat["never_replace_p215_z"] is True
        and cat["never_replace_robotics_supreme"] is True
        and cat["never_replace_biotechnology"] is True
        and cat["never_replace_space"] is True
        and cat["never_replace_p218_z_intelligence_nexus"] is True
        and cat["never_merge_p218_t_space_civilization"] is True
        and cat["no_module_local_llm"] is True
        and cat["never_opaque_unexplainable_civilization_decisions"] is True
        and cat["never_ungated_civilization_decision"] is True
        and cat["never_skip_human_authority"] is True
        and cat["never_skip_ethical_civilization_governance"] is True
        and cat["never_violate_human_sovereignty"] is True
        and cat["foundation_for_p219_a"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        CivilizationOperatingSystemRoot.enable(tenant_id="t1", cos_ref="c1").is_missing() is False,
        CivilizationOsKernelRoot.enable(tenant_id="t1", kernel_ref="k1").is_missing() is False,
        PlanetaryIntelligenceRoot.enable(tenant_id="t1", planetary_ref="p1").is_missing() is False,
        HumanCivilizationRoot.enable(tenant_id="t1", human_ref="h1").is_missing() is False,
        InfrastructureIntelligenceRoot.enable(tenant_id="t1", infra_ref="i1").is_missing() is False,
        CivilizationDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        CivilizationKnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="kg1").is_missing() is False,
        CivilizationGovernanceRoot.enable(tenant_id="t1", governance_ref="g1").is_missing() is False,
        MeosCivilizationOsCoreRoot.enable(tenant_id="t1", core_ref="core1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/civilization/infrastructure/acl/civ_foundation_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p214_z", "via_p215_z", "via_p216_z", "via_p217", "via_p218", "via_p218_z",
        "via_identity", "via_policy_engine", "via_workflow", "via_audit",
        "via_integration_platform", "via_search", "via_core_platform",
        "never_replace_p215_z", "never_replace_ai_platform", "never_replace_core_platform",
        "never_replace_robotics_supreme", "never_replace_biotechnology",
        "never_replace_space", "never_replace_p218_z_intelligence_nexus",
        "never_merge_p218_t_space_civilization", "never_replace_identity_platform",
        "module_local_llm_forbidden", "civilization_ai_via_p214z_acl_only",
        "quantum_simulation_via_p215z_acl_only", "robotics_via_p216z_acl_only",
        "bio_health_via_p217_acl_only", "space_connectivity_via_p218_acl_only",
        "supreme_coordination_via_p218z_acl_only",
        "external_systems_via_integration_platform_only",
        "never_ungated_civilization_decision", "never_skip_human_authority",
        "never_opaque_unexplainable_civilization_decisions",
        "never_skip_ethical_civilization_governance", "never_violate_human_sovereignty",
        "module_local_civilization_foundation_forbidden",
    ))
    router = (root / "backend/contexts/civilization/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@civilization_router.get("/foundation")', "/foundation/vision",
        "/foundation/architecture", "/foundation/kernel",
        "/foundation/planetary-intelligence", "/foundation/human-civilization",
        "/foundation/infrastructure", "/foundation/governance",
        "/foundation/digital-twin", "/foundation/knowledge-graph",
        "/foundation/operating-model", "/foundation/domain",
        "/foundation/bounded-contexts", "/foundation/agents",
        "/foundation/observability", "/foundation/security",
        "/foundation/cqrs", "/foundation/events", "/foundation/microservices",
        "/foundation/integration", "/foundation/deployment",
        "/foundation/roadmap", "/foundation/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_CIVILIZATION_OPERATING_SYSTEM_FOUNDATION.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Civilization Operating System is missing",
        "Never Civilization OS Kernel is missing",
        "Never Planetary Intelligence Governance is missing",
        "Never Global Infrastructure Intelligence is missing",
        "Never Human Civilization Management Platform is missing",
        "Never Civilization Digital Twin is missing",
        "Never Civilization Knowledge Graph is missing",
        "Never Civilization Governance Architecture is missing",
        "Never MEOS Civilization OS Core is missing",
        "Never CQRS architecture is missing", "Never Event Architecture is missing",
        "Never Microservices Architecture is missing", "Never Sibling Civilization BC",
        "Never Replace Core Platform", "Never Replace AI Platform",
        "Never Replace P215-Z Quantum", "Never Replace P216-Z Robotics",
        "Never Replace P217 Biotechnology", "Never Replace P218 Space",
        "Never Replace P218-Z Intelligence Nexus",
        "Never Merge P218-T Space Civilization Phase",
        "Never Module-Local LLM",
        "Never Opaque Unexplainable Civilization Decisions",
        "Never Ungated Civilization Decision",
        "Never Skip Human Authority",
        "Never Skip Ethical Civilization Governance",
        "Never Violate Human Sovereignty",
        "civilization-scale operating system that integrates intelligence",
        "P219",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P219", "adr": 553, "passed": passed,
        "missing_artifacts": missing, "forbidden_sibling_present": sibling,
        "catalog": catalog_ok, "aggregates": all(checks), "acl": acl_ok,
        "router": router_ok, "documentation": doc_ok, "sor": "civilization",
        "capability": "CAP-PLT-CIV-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
