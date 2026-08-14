"""Civilization P219-E AI operating system foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/558-enterprise-civilization-operating-system-ai.md",
    "docs/architecture/ENTERPRISE_CIVILIZATION_OPERATING_SYSTEM_AI.md",
    "docs/architecture/civilization/CIVILIZATION_AI_OS_CAPABILITIES.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_AI_OS_ARCHITECTURE.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_AI_OS_DDD_CQRS.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_AI_OS_SECURITY.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_AI_OS_VALIDATION.v1.yaml",
    "docs/architecture/civilization/P219_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/civilization/domain/services/civ_platform_ai_os.py",
    "backend/contexts/civilization/domain/aggregates/civ_ai_os_aggregates.py",
    "backend/contexts/civilization/infrastructure/acl/civ_ai_os_acl.py",
    "backend/contexts/civilization/application/civ_ai_os_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/civilization_ai_os_platform",
    "backend/contexts/civilization_ai_kernel_bc",
    "backend/contexts/autonomous_civilization_agents_bc",
)


def validate_civ_ai_os_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.civilization.domain.aggregates.civ_ai_os_aggregates import (
        AiDigitalTwinIntelligenceRoot,
        AiGovernanceKernelRoot,
        AutonomousCivilizationAgentsRoot,
        CivilizationAiEventArchitectureRoot,
        CivilizationAiFoundationModelsRoot,
        CivilizationAiKnowledgeRoot,
        CivilizationAiOperatingSystemRoot,
        CivilizationReasoningEngineRoot,
        MeosCivilizationAiCoreRoot,
    )
    from contexts.civilization.domain.services import civ_platform_ai_os as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P219-E" and cat["adr"] == 558 and cat["sor"] == "civilization"
        and cat["capability"] == "CAP-PLT-CIV-001"
        and cat["fabric"] == "meos_civilization_os_ai_operating_system_framework"
        and cat["foundation_gate"] == "P219" and cat["mission_gate"] == "P219-A"
        and cat["strategy_gate"] == "P219-B" and cat["domain_gate"] == "P219-C"
        and cat["planetary_gate"] == "P219-D"
        and cat["intelligence_nexus_gate"] == "P218-Z" and cat["space_gate"] == "P218"
        and cat["bio_gate"] == "P217-Z" and cat["robotics_gate"] == "P216-Z"
        and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["civilization_ai_operating_system_present_required"] is True
        and cat["ai_governance_kernel_present_required"] is True
        and cat["autonomous_civilization_agents_present_required"] is True
        and cat["civilization_reasoning_engine_present_required"] is True
        and cat["civilization_ai_foundation_models_present_required"] is True
        and cat["meos_civilization_ai_core_present_required"] is True
        and cat["civilization_ai_knowledge_architecture_present_required"] is True
        and cat["ai_digital_twin_intelligence_present_required"] is True
        and cat["civilization_ai_event_architecture_present_required"] is True
        and cat["civilization_ai_cqrs_model_present_required"] is True
        and cat["meos_civilization_ai_integration_map_present_required"] is True
        and cat["architecture"]["pipeline_stage_count"] == 8
        and cat["architecture"]["kernel_component_count"] == 6
        and cat["architecture"]["governance_component_count"] == 5
        and cat["agents"]["agent_type_count"] == 7
        and cat["reasoning"]["domain_count"] == 7
        and cat["foundation_models"]["model_count"] == 7
        and cat["bounded_contexts"]["context_count"] == 3
        and cat["aggregates"]["aggregate_count"] == 4
        and cat["events"]["core_event_count"] == 8
        and cat["cqrs"]["command_count"] == 6 and cat["cqrs"]["query_count"] == 5
        and cat["microservices"]["service_count"] == 10
        and cat["never_replace_p219_foundation"] is True
        and cat["never_replace_p219_a_mission"] is True
        and cat["never_replace_p219_b_strategy"] is True
        and cat["never_replace_p219_c_domain"] is True
        and cat["never_replace_p219_d_planetary"] is True
        and cat["never_cross_context_aggregate_imports"] is True
        and cat["never_opaque_unexplainable_civilization_ai_decisions"] is True
        and cat["never_ungated_civilization_ai_autonomy"] is True
        and cat["never_bypass_ai_governance_kernel"] is True
        and cat["never_skip_human_oversight_ai"] is True
        and cat["no_module_local_llm"] is True
        and cat["foundation_for_p219_f"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        CivilizationAiOperatingSystemRoot.enable(tenant_id="t1", aios_ref="a1").is_missing() is False,
        AiGovernanceKernelRoot.enable(tenant_id="t1", gov_ref="g1").is_missing() is False,
        AutonomousCivilizationAgentsRoot.enable(tenant_id="t1", agents_ref="ag1").is_missing() is False,
        CivilizationReasoningEngineRoot.enable(tenant_id="t1", reasoning_ref="r1").is_missing() is False,
        CivilizationAiFoundationModelsRoot.enable(tenant_id="t1", models_ref="m1").is_missing() is False,
        MeosCivilizationAiCoreRoot.enable(tenant_id="t1", core_ref="c1").is_missing() is False,
        AiDigitalTwinIntelligenceRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        CivilizationAiKnowledgeRoot.enable(tenant_id="t1", knowledge_ref="k1").is_missing() is False,
        CivilizationAiEventArchitectureRoot.enable(tenant_id="t1", events_ref="e1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/civilization/infrastructure/acl/civ_ai_os_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p219", "via_p219_a", "via_p219_b", "via_p219_c", "via_p219_d",
        "via_p218_z", "via_p218", "via_p217", "via_p216_z", "via_p215_z", "via_p214_z",
        "via_policy_engine", "via_workflow", "via_audit", "via_identity", "via_core_platform",
        "never_replace_p219_foundation", "never_replace_p219_a_mission", "never_replace_p219_b_strategy",
        "never_replace_p219_c_domain", "never_replace_p219_d_planetary",
        "never_replace_p218_z_intelligence_nexus", "never_replace_space",
        "never_merge_p218_t_space_civilization", "never_cross_context_aggregate_imports",
        "never_opaque_unexplainable_civilization_ai_decisions",
        "never_ungated_civilization_ai_autonomy",
        "never_skip_human_oversight_ai",
        "never_skip_ethical_ai_validation",
        "never_skip_ai_alignment_validation",
        "never_bypass_ai_governance_kernel",
        "never_violate_human_sovereignty_ai",
        "module_local_llm_forbidden",
        "module_local_civilization_ai_os_forbidden",
    ))
    router = (root / "backend/contexts/civilization/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@civilization_router.get("/ai-os")',
        "/ai-os/architecture", "/ai-os/governance", "/ai-os/agents",
        "/ai-os/reasoning", "/ai-os/models", "/ai-os/knowledge",
        "/ai-os/digital-twin", "/ai-os/bounded-contexts", "/ai-os/aggregates",
        "/ai-os/events", "/ai-os/cqrs", "/ai-os/microservices",
        "/ai-os/integration", "/ai-os/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_CIVILIZATION_OPERATING_SYSTEM_AI.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Civilization AI Operating System is missing",
        "Never AI Governance Kernel is missing",
        "Never Autonomous Civilization Agents is missing",
        "Never Civilization Reasoning Engine is missing",
        "Never Civilization AI Foundation Models is missing",
        "Never MEOS Civilization AI Core is missing",
        "Never Civilization AI Knowledge Architecture is missing",
        "Never AI Digital Twin Intelligence is missing",
        "Never Civilization AI Event Architecture is missing",
        "Never Civilization AI CQRS Model is missing",
        "Never MEOS Civilization AI Integration Map is missing",
        "Never Replace P219 Foundation",
        "Never Replace P219-A Mission",
        "Never Replace P219-B Strategy",
        "Never Replace P219-C Domain",
        "Never Replace P219-D Planetary",
        "Never Replace Core Platform",
        "Never Replace AI Platform",
        "Never Replace P215-Z Quantum",
        "Never Replace P216-Z Robotics",
        "Never Replace P217 Biotechnology",
        "Never Replace P218 Space",
        "Never Replace P218-Z Intelligence Nexus",
        "Never Merge P218-T Space Civilization Phase",
        "Never Module-Local LLM",
        "Never Cross-Context Aggregate Imports",
        "Never Opaque Unexplainable Civilization AI Decisions",
        "Never Ungated Civilization AI Autonomy",
        "Never Skip Human Oversight AI",
        "Never Skip Ethical AI Validation",
        "Never Violate Human Sovereignty AI",
        "Never Skip AI Alignment Validation",
        "Never Bypass AI Governance Kernel",
        "explainability and controlled autonomy",
        "P219-F",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P219-E", "adr": 558, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "civilization",
        "capability": "CAP-PLT-CIV-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
