"""Robotics P216-V science / autonomous laboratory foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/494-enterprise-robotics-science.md",
    "docs/architecture/ENTERPRISE_ROBOTICS_SCIENCE.md",
    "docs/architecture/robotics/ROBOTICS_SCIENCE_LAB.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_SCIENCE_BOUNDED_CONTEXTS.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_SCIENCE_DDD_CQRS.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_SCIENCE_SECURITY.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_SCIENCE_VALIDATION.v1.yaml",
    "docs/architecture/robotics/P216_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/robotics/domain/services/rb_platform_science.py",
    "backend/contexts/robotics/domain/aggregates/rb_science_aggregates.py",
    "backend/contexts/robotics/infrastructure/acl/rb_science_acl.py",
    "backend/contexts/robotics/application/rb_science_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/science_robotics_platform",
    "backend/contexts/autonomous_laboratory_platform",
    "backend/contexts/scientific_ai_intelligence_platform",
    "backend/contexts/ai_scientist_platform",
)
def validate_rb_science_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.robotics.domain.aggregates.rb_science_aggregates import (
        ScienceRoboticsRoot, AutonomousLaboratoryRoot, AiScientistRoot,
        DiscoveryAccelerationRoot, ResearchAutomationRoot, ScientificDigitalTwinRoot,
        ScientificKnowledgeGraphRoot, ScienceSecurityRoot, HumanScientificOversightRoot,
    )
    from contexts.robotics.domain.services import rb_platform_science as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P216-V" and cat["adr"] == 494 and cat["sor"] == "robotics"
        and cat["capability"] == "CAP-PLT-RB-001"
        and cat["fabric"] == "meos_scientific_intelligence_fabric"
        and cat["foundation_gate"] == "P216" and cat["defense_gate"] == "P216-U"
        and cat["healthcare_gate"] == "P216-I" and cat["physical_ai_gate"] == "P216-E"
        and cat["runtime_gate"] == "P216-D"
        and cat["supreme_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["science_robotics_platform_present_required"] is True
        and cat["autonomous_laboratory_platform_present_required"] is True
        and cat["ai_scientist_platform_present_required"] is True
        and cat["scientific_discovery_engine_present_required"] is True
        and cat["research_automation_platform_present_required"] is True
        and cat["scientific_digital_twin_present_required"] is True
        and cat["scientific_knowledge_graph_present_required"] is True
        and cat["security_architecture_present_required"] is True
        and cat["human_scientific_oversight_present_required"] is True
        and cat["bounded_contexts"]["context_count"] == 8
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 7
        and cat["domain_model"]["entity_count"] == 12
        and cat["never_replace_p216_foundation"] is True
        and cat["never_replace_p216_u_defense"] is True
        and cat["no_module_local_llm"] is True
        and cat["human_scientific_oversight_required"] is True
        and cat["reproducibility_by_design_required"] is True
        and cat["research_ethics_governance_required"] is True
        and cat["explainable_ai_required"] is True
        and cat["ungated_physical_autonomy_strategy_forbidden"] is True
        and cat["opaque_safety_strategy_forbidden"] is True
        and cat["foundation_for_p216_w"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        ScienceRoboticsRoot.enable(tenant_id="t1", robotics_ref="r1").is_missing() is False,
        AutonomousLaboratoryRoot.enable(tenant_id="t1", laboratory_ref="l1").is_missing() is False,
        AiScientistRoot.enable(tenant_id="t1", scientist_ref="a1").is_missing() is False,
        DiscoveryAccelerationRoot.enable(tenant_id="t1", discovery_ref="d1").is_missing() is False,
        ResearchAutomationRoot.enable(tenant_id="t1", automation_ref="ra1").is_missing() is False,
        ScientificDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        ScientificKnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="k1").is_missing() is False,
        ScienceSecurityRoot.enable(tenant_id="t1", security_ref="sec1").is_missing() is False,
        HumanScientificOversightRoot.enable(tenant_id="t1", oversight_ref="h1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/robotics/infrastructure/acl/rb_science_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p216", "via_p216_a", "via_p216_b", "via_p216_c", "via_p216_d", "via_p216_e", "via_p216_f", "via_p216_g", "via_p216_h", "via_p216_i", "via_p216_k", "via_p216_l", "via_p216_o", "via_p216_p", "via_p216_q", "via_p216_r", "via_p216_t", "via_p216_u",
        "via_p215_z", "via_p214_z", "via_p213", "via_integration_platform",
        "via_lims_api", "via_scientific_db_api",
        "via_policy_engine", "via_workflow", "via_audit", "via_identity", "via_core_platform",
        "never_replace_p216_foundation", "never_replace_p216_u_defense",
        "never_replace_p215_z", "never_replace_ai_platform", "never_replace_core_platform",
        "no_module_local_llm", "physical_ai_via_p214z_acl_only",
        "human_scientific_oversight_required", "reproducibility_by_design_required",
        "research_ethics_governance_required", "explainable_ai_required",
        "ungated_physical_autonomy_strategy_forbidden", "opaque_safety_strategy_forbidden",
        "module_local_science_platform_forbidden",
    ))
    router = (root / "backend/contexts/robotics/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@robotics_router.get("/science")', "/science/vision", "/science/domain",
        "/science/bounded-contexts", "/science/robotics", "/science/autonomous-laboratory",
        "/science/ai-scientist", "/science/discovery", "/science/research-automation",
        "/science/digital-twin", "/science/knowledge-graph", "/science/observability",
        "/science/security", "/science/cqrs", "/science/events", "/science/microservices",
        "/science/integration", "/science/deployment", "/science/testing",
        "/science/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_ROBOTICS_SCIENCE.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Science Robotics Platform is missing",
        "Never Autonomous Laboratory Platform is missing",
        "Never AI Scientist Platform is missing",
        "Never Scientific Discovery Engine is missing",
        "Never Research Automation Platform is missing",
        "Never Scientific Digital Twin is missing",
        "Never Scientific Knowledge Graph is missing",
        "Never Security Architecture is missing",
        "Never CQRS architecture is missing",
        "Never Event Architecture is missing",
        "Never Microservices Architecture is missing",
        "Never Cloud-Edge Deployment is missing",
        "Never Enterprise Science Integration is missing",
        "Never Testing Architecture is missing",
        "Never Human Scientific Oversight is missing",
        "Never Sibling Robotics BC",
        "Never Replace P216 Foundation",
        "Never Replace P216-U Defense",
        "Never Replace Core Platform",
        "Never Replace AI Platform",
        "Never Replace Quantum Supreme (P215-Z)",
        "Never Module-Local LLM",
        "Never Ungated Physical Autonomy Strategy",
        "Never Opaque Safety Strategy",
        "Never Skip Human Scientific Oversight",
        "Never Skip Reproducibility by Design",
        "Never Skip Explainable AI for Scientific Decisions",
        "Never Skip Research Ethics Governance",
        "MEOS Scientific Intelligence Platform SHALL unify",
        "P216", "P216-U", "P215-Z", "P214-Z", "P216-W",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P216-V", "adr": 494, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "robotics",
        "capability": "CAP-PLT-RB-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
