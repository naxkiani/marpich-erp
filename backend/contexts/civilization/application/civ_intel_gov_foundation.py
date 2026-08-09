"""Civilization P219-T intelligence governance foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/573-enterprise-civilization-operating-system-intelligence-governance.md",
    "docs/architecture/ENTERPRISE_CIVILIZATION_OPERATING_SYSTEM_INTELLIGENCE_GOVERNANCE.md",
    "docs/architecture/civilization/CIVILIZATION_INTEL_GOV_CAPABILITIES.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_INTEL_GOV_ARCHITECTURE.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_INTEL_GOV_DDD_CQRS.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_INTEL_GOV_SECURITY.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_INTEL_GOV_VALIDATION.v1.yaml",
    "docs/architecture/civilization/P219_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/civilization/domain/services/civ_platform_intel_gov.py",
    "backend/contexts/civilization/domain/aggregates/civ_intel_gov_aggregates.py",
    "backend/contexts/civilization/infrastructure/acl/civ_intel_gov_acl.py",
    "backend/contexts/civilization/application/civ_intel_gov_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/civilization_intelligence_governance_platform",
    "backend/contexts/strategic_alignment_platform_bc",
    "backend/contexts/global_decision_assurance_bc",
)


def validate_civ_intel_gov_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.civilization.domain.aggregates.civ_intel_gov_aggregates import (
        CivilizationIntelligenceGovernancePlatformRoot,
        DecisionAssurancePlatformRoot,
        EnterprisePolicyIntelligenceRoot,
        GovernanceDigitalTwinRoot,
        GovernanceKnowledgeGraphRoot,
        IntelligenceGovernanceEventArchitectureRoot,
        MeosCivilizationGovernanceAlignmentIntelligenceCoreRoot,
        StrategicAlignmentPlatformRoot,
        TrustAndComplianceFrameworkRoot,
    )
    from contexts.civilization.domain.services import civ_platform_intel_gov as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P219-T" and cat["adr"] == 573 and cat["sor"] == "civilization"
        and cat["capability"] == "CAP-PLT-CIV-001"
        and cat["fabric"] == "meos_civilization_os_civilization_governance_alignment_intelligence_framework"
        and cat["foundation_gate"] == "P219" and cat["mission_gate"] == "P219-A"
        and cat["strategy_gate"] == "P219-B" and cat["domain_gate"] == "P219-C"
        and cat["planetary_gate"] == "P219-D" and cat["ai_os_gate"] == "P219-E"
        and cat["simulation_gate"] == "P219-F" and cat["resources_gate"] == "P219-G"
        and cat["economy_gate"] == "P219-H" and cat["knowledge_gate"] == "P219-I"
        and cat["human_gate"] == "P219-J" and cat["governance_gate"] == "P219-K"
        and cat["innovation_gate"] == "P219-L" and cat["security_gate"] == "P219-M"
        and cat["sustainability_gate"] == "P219-N" and cat["prosperity_gate"] == "P219-O"
        and cat["collaboration_gate"] == "P219-P" and cat["consciousness_gate"] == "P219-Q"
        and cat["evolution_gate"] == "P219-R" and cat["futures_gate"] == "P219-S"
        and cat["intelligence_nexus_gate"] == "P218-Z" and cat["space_gate"] == "P218"
        and cat["bio_gate"] == "P217-Z" and cat["robotics_gate"] == "P216-Z"
        and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["civilization_intelligence_governance_platform_present_required"] is True
        and cat["strategic_alignment_platform_present_required"] is True
        and cat["enterprise_policy_intelligence_present_required"] is True
        and cat["trust_and_compliance_framework_present_required"] is True
        and cat["decision_assurance_platform_present_required"] is True
        and cat["governance_knowledge_graph_present_required"] is True
        and cat["governance_digital_twin_present_required"] is True
        and cat["meos_civilization_governance_alignment_intelligence_core_present_required"] is True
        and cat["intelligence_governance_event_architecture_present_required"] is True
        and cat["intelligence_governance_cqrs_model_present_required"] is True
        and cat["meos_intelligence_governance_integration_map_present_required"] is True
        and cat["architecture"]["maturity_stage_count"] == 6
        and cat["architecture"]["layer_count"] == 6
        and cat["architecture"]["governance_domain_count"] == 10
        and cat["architecture"]["intelligence_governance_domain_count"] == 10
        and cat["architecture"]["alignment_dimension_count"] == 9
        and cat["architecture"]["policy_lifecycle_step_count"] == 7
        and cat["architecture"]["policy_domain_count"] == 9
        and cat["architecture"]["trust_domain_count"] == 6
        and cat["architecture"]["compliance_domain_count"] == 5
        and cat["architecture"]["decision_lifecycle_step_count"] == 8
        and cat["agents"]["agent_count"] == 5
        and cat["knowledge_graph"]["entity_count"] == 11
        and cat["knowledge_graph"]["relationship_count"] == 8
        and cat["digital_twin"]["twin_count"] == 5
        and cat["bounded_contexts"]["context_count"] == 4
        and cat["aggregates"]["aggregate_count"] == 5
        and cat["events"]["core_event_count"] == 12
        and cat["cqrs"]["command_count"] == 6 and cat["cqrs"]["query_count"] == 6
        and cat["microservices"]["service_count"] == 10
        and cat["never_replace_p219_foundation"] is True
        and cat["never_replace_p219_k_governance"] is True
        and cat["never_replace_p219_s_futures"] is True
        and cat["never_replace_policy_engine"] is True
        and cat["never_ungated_governance_decision_execution"] is True
        and cat["never_opaque_unexplainable_governance_decisions"] is True
        and cat["never_bypass_human_supervision_governance"] is True
        and cat["never_bypass_human_accountability"] is True
        and cat["no_module_local_llm"] is True
        and cat["foundation_for_p219_u"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        CivilizationIntelligenceGovernancePlatformRoot.enable(
            tenant_id="t1", igov_ref="g1"
        ).is_missing() is False,
        StrategicAlignmentPlatformRoot.enable(
            tenant_id="t1", alignment_ref="a1"
        ).is_missing() is False,
        EnterprisePolicyIntelligenceRoot.enable(
            tenant_id="t1", policy_ref="p1"
        ).is_missing() is False,
        TrustAndComplianceFrameworkRoot.enable(
            tenant_id="t1", trust_ref="tr1"
        ).is_missing() is False,
        DecisionAssurancePlatformRoot.enable(
            tenant_id="t1", assurance_ref="d1"
        ).is_missing() is False,
        GovernanceDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        MeosCivilizationGovernanceAlignmentIntelligenceCoreRoot.enable(
            tenant_id="t1", core_ref="core1"
        ).is_missing() is False,
        GovernanceKnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="k1").is_missing() is False,
        IntelligenceGovernanceEventArchitectureRoot.enable(
            tenant_id="t1", events_ref="ev1"
        ).is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/civilization/infrastructure/acl/civ_intel_gov_acl.py").read_text(
        encoding="utf-8"
    )
    acl_ok = all(x in acl_text for x in (
        "via_p219", "via_p219_e", "via_p219_f", "via_p219_k", "via_p219_s",
        "via_policy_engine", "via_workflow", "via_audit",
        "via_p218_z", "via_p214_z", "via_core_platform", "via_identity",
        "never_replace_p219_foundation", "never_replace_p219_e_ai_os",
        "never_replace_p219_f_simulation", "never_replace_p219_k_governance",
        "never_replace_p219_s_futures", "never_replace_policy_engine",
        "never_opaque_unexplainable_governance_decisions",
        "never_ungated_governance_decision_execution",
        "never_skip_ethical_governance_assurance",
        "never_skip_human_authority_governance",
        "never_violate_human_sovereignty_governance",
        "never_bypass_trusted_governance_validation",
        "never_bypass_human_supervision_governance",
        "never_bypass_human_accountability",
        "module_local_llm_forbidden",
        "module_local_civilization_intelligence_governance_forbidden",
    ))
    router = (root / "backend/contexts/civilization/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@civilization_router.get("/intelligence-governance")',
        "/intelligence-governance/architecture", "/intelligence-governance/platform",
        "/intelligence-governance/alignment", "/intelligence-governance/policy",
        "/intelligence-governance/trust", "/intelligence-governance/decision-assurance",
        "/intelligence-governance/digital-twin", "/intelligence-governance/knowledge-graph",
        "/intelligence-governance/agents", "/intelligence-governance/bounded-contexts",
        "/intelligence-governance/aggregates", "/intelligence-governance/events",
        "/intelligence-governance/cqrs", "/intelligence-governance/integration",
        "/intelligence-governance/readiness",
    ))
    law = (
        root / "docs/architecture/ENTERPRISE_CIVILIZATION_OPERATING_SYSTEM_INTELLIGENCE_GOVERNANCE.md"
    ).read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Civilization Intelligence Governance Platform is missing",
        "Never Strategic Alignment Platform is missing",
        "Never Enterprise Policy Intelligence is missing",
        "Never Trust & Compliance Framework is missing",
        "Never Decision Assurance Platform is missing",
        "Never Governance Knowledge Graph is missing",
        "Never Governance Digital Twin is missing",
        "Never MEOS Civilization Governance & Alignment Intelligence Core is missing",
        "Never Intelligence Governance Event Architecture is missing",
        "Never Intelligence Governance CQRS Model is missing",
        "Never MEOS Intelligence Governance Integration Map is missing",
        "Never Replace P219 Foundation",
        "Never Replace P219-E AI OS",
        "Never Replace P219-K Governance",
        "Never Replace P219-S Futures",
        "Never Replace Policy Engine",
        "Never Opaque Unexplainable Governance Decisions",
        "Never Ungated Governance Decision Execution",
        "Never Bypass Human Accountability",
        "aligning strategy, policy, execution and decision-making",
        "P219-U",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P219-T", "adr": 573, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "civilization",
        "capability": "CAP-PLT-CIV-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
