"""Space P218-K Scientific Intelligence foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/537-enterprise-space-intelligence-scientific.md",
    "docs/architecture/ENTERPRISE_SPACE_INTELLIGENCE_SCIENTIFIC.md",
    "docs/architecture/space/SCIENTIFIC_ARCHITECTURE.v1.yaml",
    "docs/architecture/space/SCIENTIFIC_LIFECYCLE.v1.yaml",
    "docs/architecture/space/SCIENTIFIC_DDD_CQRS.v1.yaml",
    "docs/architecture/space/SCIENTIFIC_SECURITY.v1.yaml",
    "docs/architecture/space/SCIENTIFIC_VALIDATION.v1.yaml",
    "docs/architecture/space/P218_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/space/domain/services/sp_platform_scientific.py",
    "backend/contexts/space/domain/aggregates/sp_scientific_aggregates.py",
    "backend/contexts/space/infrastructure/acl/sp_scientific_acl.py",
    "backend/contexts/space/application/sp_scientific_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/scientific_intelligence_platform",
    "backend/contexts/space_research_bc",
    "backend/contexts/laboratory_intelligence_bc",
)


def validate_sp_scientific_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.space.domain.aggregates.sp_scientific_aggregates import (
        DiscoveryRoot, ExperimentRoot, LaboratoryRoot, ResearchPlatformRoot,
        ScientificAiRoot, ScientificDigitalTwinRoot, ScientificGovernanceRoot,
        ScientificIntelPlatformRoot, ScientificSecurityRoot,
    )
    from contexts.space.domain.services import sp_platform_scientific as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P218-K" and cat["adr"] == 537 and cat["sor"] == "space"
        and cat["capability"] == "CAP-PLT-SP-001"
        and cat["fabric"] == "meos_scientific_intelligence_fabric"
        and cat["foundation_gate"] == "P218" and cat["mission_gate"] == "P218-A"
        and cat["strategy_gate"] == "P218-B" and cat["domain_gate"] == "P218-C"
        and cat["infrastructure_gate"] == "P218-D" and cat["space_ai_gate"] == "P218-E"
        and cat["satellite_gate"] == "P218-F" and cat["orbital_gate"] == "P218-G"
        and cat["communications_gate"] == "P218-H" and cat["navigation_gate"] == "P218-I"
        and cat["mission_intel_gate"] == "P218-J"
        and cat["bio_gate"] == "P217-Z" and cat["robotics_gate"] == "P216-Z"
        and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["scientific_intelligence_platform_present_required"] is True
        and cat["space_research_platform_present_required"] is True
        and cat["autonomous_scientific_discovery_present_required"] is True
        and cat["space_laboratory_intelligence_present_required"] is True
        and cat["scientific_ai_present_required"] is True
        and cat["experiment_management_present_required"] is True
        and cat["scientific_digital_twin_present_required"] is True
        and cat["scientific_governance_present_required"] is True
        and cat["architecture"]["layer_count"] == 5
        and cat["lifecycle"]["stage_count"] == 10
        and cat["research"]["domain_count"] == 10
        and cat["research"]["service_count"] == 8
        and cat["discovery"]["workflow_step_count"] == 10
        and cat["discovery"]["ai_capability_count"] == 8
        and cat["laboratory"]["type_count"] == 8
        and cat["laboratory"]["capability_count"] == 8
        and cat["scientific_ai"]["capability_count"] == 10
        and cat["scientific_ai"]["model_count"] == 8
        and cat["experiment"]["category_count"] == 8
        and cat["experiment"]["service_count"] == 8
        and cat["governance"]["domain_count"] == 8
        and cat["governance"]["approval_gate_count"] == 7
        and cat["bounded_contexts"]["context_count"] == 8
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 10
        and cat["never_replace_p218_j_mission_intel"] is True
        and cat["never_ungated_autonomous_experiment_execution"] is True
        and cat["never_skip_scientific_ethics_review"] is True
        and cat["never_skip_peer_review_gate"] is True
        and cat["never_skip_reproducibility_validation"] is True
        and cat["never_violate_fair_data_principles"] is True
        and cat["space_ai_via_p214z_acl_only"] is True
        and cat["no_module_local_llm"] is True
        and cat["foundation_for_p218_l"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        ScientificIntelPlatformRoot.enable(tenant_id="t1", platform_ref="p1").is_missing() is False,
        ResearchPlatformRoot.enable(tenant_id="t1", research_ref="r1").is_missing() is False,
        DiscoveryRoot.enable(tenant_id="t1", discovery_ref="d1").is_missing() is False,
        LaboratoryRoot.enable(tenant_id="t1", laboratory_ref="l1").is_missing() is False,
        ScientificAiRoot.enable(tenant_id="t1", ai_ref="a1").is_missing() is False,
        ExperimentRoot.enable(tenant_id="t1", experiment_ref="e1").is_missing() is False,
        ScientificDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        ScientificGovernanceRoot.enable(tenant_id="t1", governance_ref="g1").is_missing() is False,
        ScientificSecurityRoot.enable(tenant_id="t1", security_ref="s1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/space/infrastructure/acl/sp_scientific_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "to_space_foundation", "to_space_mission", "to_space_strategy", "to_space_domain",
        "to_space_infrastructure", "to_space_ai", "to_satellite", "to_orbital",
        "to_communications", "to_navigation", "to_mission_intel", "to_biotechnology",
        "to_robotics_supreme", "to_quantum_supreme", "to_master_ai", "to_integration",
        "to_policy_engine", "to_workflow", "to_audit", "to_identity", "to_core_platform",
        "to_enterprise_space", "never_replace_p218_j_mission_intel",
        "never_ungated_autonomous_experiment_execution", "never_skip_scientific_ethics_review",
        "never_skip_peer_review_gate", "never_skip_reproducibility_validation",
        "never_violate_fair_data_principles", "module_local_scientific_forbidden",
        "space_ai_via_p214z_acl_only", "no_module_local_llm",
    ))
    router = (root / "backend/contexts/space/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@space_router.get("/scientific")', "/scientific/vision",
        "/scientific/architecture", "/scientific/lifecycle", "/scientific/research",
        "/scientific/discovery", "/scientific/laboratory", "/scientific/scientific-ai",
        "/scientific/experiment", "/scientific/digital-twin", "/scientific/observability",
        "/scientific/governance", "/scientific/security", "/scientific/integration",
        "/scientific/deployment", "/scientific/testing", "/scientific/cqrs",
        "/scientific/events", "/scientific/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_SPACE_INTELLIGENCE_SCIENTIFIC.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Scientific Intelligence Platform is missing",
        "Never Space Research Platform is missing",
        "Never Autonomous Scientific Discovery is missing",
        "Never Space Laboratory Intelligence is missing",
        "Never Scientific AI Platform is missing",
        "Never Experiment Management Platform is missing",
        "Never Scientific Digital Twin is missing", "Never DDD Model is missing",
        "Never Scientific Governance is missing", "Never Security Architecture is missing",
        "Never Observability is missing", "Never Deployment Architecture is missing",
        "Never CQRS architecture is missing", "Never Event Architecture is missing",
        "Never Microservices Architecture is missing", "Never Sibling Space BC",
        "Never Replace P218-J Mission Intel",
        "Never Module-Local LLM", "Never Skip Scientific Ethics Review",
        "Never Skip Peer Review Gate", "Never Skip Reproducibility Validation",
        "Never Ungated Autonomous Experiment Execution",
        "Never Violate FAIR Data Principles",
        "autonomously generating hypotheses",
        "P218-K", "P218-L",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P218-K", "adr": 537, "passed": passed,
        "missing_artifacts": missing, "forbidden_sibling_present": sibling,
        "catalog": catalog_ok, "aggregates": all(checks), "acl": acl_ok,
        "router": router_ok, "documentation": doc_ok, "sor": "space",
        "capability": "CAP-PLT-SP-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
