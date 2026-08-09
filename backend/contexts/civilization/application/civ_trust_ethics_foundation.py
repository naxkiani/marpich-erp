"""Civilization P219-Y trust, ethics & alignment foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/578-enterprise-civilization-operating-system-trust-ethics-alignment.md",
    "docs/architecture/ENTERPRISE_CIVILIZATION_OPERATING_SYSTEM_TRUST_ETHICS_ALIGNMENT.md",
    "docs/architecture/civilization/CIVILIZATION_TRUST_ETHICS_CAPABILITIES.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_TRUST_ETHICS_ARCHITECTURE.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_TRUST_ETHICS_DDD_CQRS.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_TRUST_ETHICS_SECURITY.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_TRUST_ETHICS_VALIDATION.v1.yaml",
    "docs/architecture/civilization/P219_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/civilization/domain/services/civ_platform_trust_ethics.py",
    "backend/contexts/civilization/domain/aggregates/civ_trust_ethics_aggregates.py",
    "backend/contexts/civilization/infrastructure/acl/civ_trust_ethics_acl.py",
    "backend/contexts/civilization/application/civ_trust_ethics_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/enterprise_trust_platform",
    "backend/contexts/enterprise_ethics_framework_bc",
    "backend/contexts/decision_assurance_platform_bc",
)


def validate_civ_trust_ethics_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.civilization.domain.aggregates.civ_trust_ethics_aggregates import (
        ContinuousCompliancePlatformRoot,
        DecisionAssurancePlatformRoot,
        EnterpriseAlignmentPlatformRoot,
        EnterpriseEthicsFrameworkRoot,
        EnterpriseTrustPlatformRoot,
        MeosTrustEthicsAlignmentCoreRoot,
        TrustEthicsDigitalTwinRoot,
        TrustEthicsEventArchitectureRoot,
        TrustEthicsKnowledgeGraphRoot,
    )
    from contexts.civilization.domain.services import civ_platform_trust_ethics as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P219-Y" and cat["adr"] == 578 and cat["sor"] == "civilization"
        and cat["capability"] == "CAP-PLT-CIV-001"
        and cat["fabric"] == "meos_civilization_os_trust_ethics_alignment_framework"
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
        and cat["intel_gov_gate"] == "P219-T" and cat["auto_ops_gate"] == "P219-U"
        and cat["gen_intel_gate"] == "P219-V" and cat["collective_gate"] == "P219-W"
        and cat["strategic_evolution_gate"] == "P219-X"
        and cat["intelligence_nexus_gate"] == "P218-Z" and cat["space_gate"] == "P218"
        and cat["bio_gate"] == "P217-Z" and cat["robotics_gate"] == "P216-Z"
        and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["enterprise_trust_platform_present_required"] is True
        and cat["enterprise_ethics_framework_present_required"] is True
        and cat["enterprise_alignment_platform_present_required"] is True
        and cat["continuous_compliance_platform_present_required"] is True
        and cat["decision_assurance_platform_present_required"] is True
        and cat["meos_trust_ethics_alignment_core_present_required"] is True
        and cat["trust_ethics_knowledge_graph_present_required"] is True
        and cat["trust_ethics_event_architecture_present_required"] is True
        and cat["trust_ethics_cqrs_model_present_required"] is True
        and cat["meos_trust_ethics_integration_map_present_required"] is True
        and cat["architecture"]["maturity_stage_count"] == 6
        and cat["architecture"]["layer_count"] == 6
        and cat["architecture"]["core_capability_count"] == 5
        and cat["architecture"]["assurance_lifecycle_step_count"] == 8
        and cat["agents"]["agent_count"] == 5
        and cat["knowledge_graph"]["entity_count"] == 10
        and cat["knowledge_graph"]["relationship_count"] == 8
        and cat["digital_twin"]["twin_count"] == 5
        and cat["bounded_contexts"]["context_count"] == 5
        and cat["aggregates"]["aggregate_count"] == 5
        and cat["events"]["core_event_count"] == 12
        and cat["cqrs"]["command_count"] == 5 and cat["cqrs"]["query_count"] == 5
        and cat["microservices"]["service_count"] == 10
        and cat["never_replace_p219_foundation"] is True
        and cat["never_replace_p219_k_governance"] is True
        and cat["never_replace_p219_t_intelligence_governance"] is True
        and cat["never_replace_p219_x_strategic_evolution"] is True
        and cat["never_replace_compliance_platform"] is True
        and cat["never_opaque_unexplainable_trust_recommendations"] is True
        and cat["never_ungated_ethical_exception_execution"] is True
        and cat["never_bypass_human_accountability_trust_ethics"] is True
        and cat["never_autonomous_policy_override"] is True
        and cat["no_module_local_llm"] is True
        and cat["foundation_for_p219_z"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        EnterpriseTrustPlatformRoot.enable(tenant_id="t1", trust_ref="tr1").is_missing() is False,
        EnterpriseEthicsFrameworkRoot.enable(tenant_id="t1", ethics_ref="e1").is_missing() is False,
        EnterpriseAlignmentPlatformRoot.enable(
            tenant_id="t1", alignment_ref="a1"
        ).is_missing() is False,
        ContinuousCompliancePlatformRoot.enable(
            tenant_id="t1", compliance_ref="c1"
        ).is_missing() is False,
        DecisionAssurancePlatformRoot.enable(
            tenant_id="t1", assurance_ref="as1"
        ).is_missing() is False,
        MeosTrustEthicsAlignmentCoreRoot.enable(
            tenant_id="t1", core_ref="core1"
        ).is_missing() is False,
        TrustEthicsKnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="kg1").is_missing() is False,
        TrustEthicsEventArchitectureRoot.enable(
            tenant_id="t1", events_ref="ev1"
        ).is_missing() is False,
        TrustEthicsDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
    ]
    acl_text = (
        root / "backend/contexts/civilization/infrastructure/acl/civ_trust_ethics_acl.py"
    ).read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p219", "via_p219_k", "via_p219_t", "via_p219_x", "via_compliance",
        "via_policy_engine", "via_workflow", "via_audit",
        "via_p218_z", "via_p214_z", "via_core_platform", "via_identity",
        "never_replace_p219_foundation", "never_replace_p219_k_governance",
        "never_replace_p219_t_intelligence_governance",
        "never_replace_p219_x_strategic_evolution",
        "never_replace_compliance_platform",
        "never_opaque_unexplainable_trust_recommendations",
        "never_ungated_ethical_exception_execution",
        "never_bypass_human_oversight_trust_ethics",
        "never_bypass_human_accountability_trust_ethics",
        "never_skip_ethical_review_gates",
        "never_violate_institutional_governance_ownership",
        "never_bypass_trusted_assurance_validation",
        "never_bypass_continuous_assurance_monitoring",
        "never_autonomous_policy_override",
        "module_local_llm_forbidden",
        "module_local_trust_ethics_forbidden",
    ))
    router = (root / "backend/contexts/civilization/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@civilization_router.get("/trust-ethics")',
        "/trust-ethics/architecture", "/trust-ethics/ethics",
        "/trust-ethics/alignment", "/trust-ethics/compliance",
        "/trust-ethics/assurance", "/trust-ethics/digital-twin",
        "/trust-ethics/knowledge-graph", "/trust-ethics/agents",
        "/trust-ethics/bounded-contexts", "/trust-ethics/aggregates",
        "/trust-ethics/events", "/trust-ethics/cqrs",
        "/trust-ethics/integration", "/trust-ethics/readiness",
    ))
    law = (
        root / "docs/architecture/ENTERPRISE_CIVILIZATION_OPERATING_SYSTEM_TRUST_ETHICS_ALIGNMENT.md"
    ).read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Enterprise Trust Platform is missing",
        "Never Enterprise Ethics Framework is missing",
        "Never Enterprise Alignment Platform is missing",
        "Never Continuous Compliance Platform is missing",
        "Never Decision Assurance Platform is missing",
        "Never MEOS Trust, Ethics & Alignment Core is missing",
        "Never Trust Ethics Knowledge Graph is missing",
        "Never Trust Ethics Event Architecture is missing",
        "Never Trust Ethics CQRS Model is missing",
        "Never MEOS Trust Ethics Integration Map is missing",
        "Never Replace P219 Foundation",
        "Never Replace P219-K Governance",
        "Never Replace P219-T Intelligence Governance",
        "Never Replace P219-X Strategic Evolution",
        "Never Replace Compliance Platform",
        "Never Opaque Unexplainable Trust Recommendations",
        "Never Ungated Ethical Exception Execution",
        "Never Bypass Human Accountability Trust Ethics",
        "Never Autonomous Policy Override",
        "trustworthy, transparent, explainable and policy-aligned",
        "P219-Z",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P219-Y", "adr": 578, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "civilization",
        "capability": "CAP-PLT-CIV-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
