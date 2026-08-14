"""Space P218-R Commerce Intelligence foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/544-enterprise-space-intelligence-commerce.md",
    "docs/architecture/ENTERPRISE_SPACE_INTELLIGENCE_COMMERCE.md",
    "docs/architecture/space/COMMERCE_ARCHITECTURE.v1.yaml",
    "docs/architecture/space/COMMERCE_LIFECYCLE.v1.yaml",
    "docs/architecture/space/COMMERCE_DDD_CQRS.v1.yaml",
    "docs/architecture/space/COMMERCE_CONTROLS.v1.yaml",
    "docs/architecture/space/COMMERCE_VALIDATION.v1.yaml",
    "docs/architecture/space/P218_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/space/domain/services/sp_platform_commerce.py",
    "backend/contexts/space/domain/aggregates/sp_commerce_aggregates.py",
    "backend/contexts/space/infrastructure/acl/sp_commerce_acl.py",
    "backend/contexts/space/application/sp_commerce_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/space_commerce_platform",
    "backend/contexts/space_marketplace_bc",
    "backend/contexts/space_economy_bc",
)


def validate_sp_commerce_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.space.domain.aggregates.sp_commerce_aggregates import (
        CommerceAiRoot, CommerceGovernanceRoot, CommercePlatformRoot,
        CommercialOperationsRoot, ContractIntelligenceRoot, EconomicDigitalTwinRoot,
        InvestmentIntelligenceRoot, MarketplaceRoot, SpaceEconomyRoot,
    )
    from contexts.space.domain.services import sp_platform_commerce as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P218-R" and cat["adr"] == 544 and cat["sor"] == "space"
        and cat["capability"] == "CAP-PLT-SP-001"
        and cat["fabric"] == "meos_space_commerce_intelligence_fabric"
        and cat["foundation_gate"] == "P218" and cat["mission_gate"] == "P218-A"
        and cat["strategy_gate"] == "P218-B" and cat["domain_gate"] == "P218-C"
        and cat["infrastructure_gate"] == "P218-D" and cat["space_ai_gate"] == "P218-E"
        and cat["satellite_gate"] == "P218-F" and cat["orbital_gate"] == "P218-G"
        and cat["communications_gate"] == "P218-H" and cat["navigation_gate"] == "P218-I"
        and cat["mission_intel_gate"] == "P218-J" and cat["scientific_gate"] == "P218-K"
        and cat["exploration_gate"] == "P218-L" and cat["manufacturing_gate"] == "P218-M"
        and cat["resources_gate"] == "P218-N" and cat["logistics_gate"] == "P218-O"
        and cat["security_gate"] == "P218-P" and cat["sustainability_gate"] == "P218-Q"
        and cat["bio_gate"] == "P217-Z" and cat["robotics_gate"] == "P216-Z"
        and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["space_commerce_platform_present_required"] is True
        and cat["space_economy_intelligence_present_required"] is True
        and cat["commercial_operations_present_required"] is True
        and cat["space_marketplace_present_required"] is True
        and cat["investment_intelligence_present_required"] is True
        and cat["contract_intelligence_present_required"] is True
        and cat["commerce_ai_present_required"] is True
        and cat["economic_digital_twin_present_required"] is True
        and cat["governance_present_required"] is True
        and cat["architecture"]["layer_count"] == 5
        and cat["lifecycle"]["stage_count"] == 10
        and cat["marketplace"]["domain_count"] == 7
        and cat["marketplace"]["capability_count"] == 7
        and cat["marketplace"]["participant_count"] == 7
        and cat["operations"]["domain_count"] == 7
        and cat["operations"]["capability_count"] == 6
        and cat["economy"]["ai_capability_count"] == 7
        and cat["economy"]["model_count"] == 5
        and cat["investment"]["domain_count"] == 6
        and cat["investment"]["agent_count"] == 4
        and cat["contracts"]["capability_count"] == 6
        and cat["commerce_ai"]["model_count"] == 5
        and cat["knowledge_graph"]["entity_count"] == 10
        and cat["knowledge_graph"]["relationship_count"] == 6
        and cat["governance"]["domain_count"] == 8
        and cat["governance"]["approval_gate_count"] == 7
        and cat["bounded_contexts"]["context_count"] == 7
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 10
        and cat["never_replace_p218_q_sustainability"] is True
        and cat["never_ungated_commercial_transaction"] is True
        and cat["never_skip_marketplace_identity_verification"] is True
        and cat["never_skip_contract_compliance_validation"] is True
        and cat["never_opaque_unexplainable_commerce_decisions"] is True
        and cat["never_duplicate_financial_kernel"] is True
        and cat["space_ai_via_p214z_acl_only"] is True
        and cat["no_module_local_llm"] is True
        and cat["foundation_for_p218_s"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        CommercePlatformRoot.enable(tenant_id="t1", platform_ref="p1").is_missing() is False,
        MarketplaceRoot.enable(tenant_id="t1", marketplace_ref="m1").is_missing() is False,
        CommercialOperationsRoot.enable(tenant_id="t1", operations_ref="o1").is_missing() is False,
        SpaceEconomyRoot.enable(tenant_id="t1", economy_ref="e1").is_missing() is False,
        InvestmentIntelligenceRoot.enable(tenant_id="t1", investment_ref="i1").is_missing() is False,
        ContractIntelligenceRoot.enable(tenant_id="t1", contract_ref="c1").is_missing() is False,
        CommerceAiRoot.enable(tenant_id="t1", commerce_ai_ref="a1").is_missing() is False,
        EconomicDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        CommerceGovernanceRoot.enable(tenant_id="t1", governance_ref="g1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/space/infrastructure/acl/sp_commerce_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "to_space_foundation", "to_space_mission", "to_space_strategy", "to_space_domain",
        "to_space_infrastructure", "to_space_ai", "to_satellite", "to_orbital",
        "to_communications", "to_navigation", "to_mission_intel", "to_scientific",
        "to_exploration", "to_manufacturing", "to_resources", "to_logistics",
        "to_security", "to_sustainability",
        "to_biotechnology", "to_robotics_supreme", "to_quantum_supreme", "to_master_ai",
        "to_integration", "to_financial_kernel", "to_policy_engine", "to_workflow",
        "to_audit", "to_identity", "to_core_platform", "to_enterprise_space",
        "never_replace_p218_q_sustainability", "never_ungated_commercial_transaction",
        "never_skip_marketplace_identity_verification", "never_skip_contract_compliance_validation",
        "never_opaque_unexplainable_commerce_decisions", "never_duplicate_financial_kernel",
        "module_local_commerce_forbidden", "space_ai_via_p214z_acl_only", "no_module_local_llm",
    ))
    router = (root / "backend/contexts/space/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@space_router.get("/commerce")', "/commerce/vision",
        "/commerce/architecture", "/commerce/lifecycle", "/commerce/marketplace",
        "/commerce/operations", "/commerce/economy", "/commerce/investment",
        "/commerce/contracts", "/commerce/commerce-ai", "/commerce/digital-twin",
        "/commerce/knowledge-graph", "/commerce/observability", "/commerce/governance",
        "/commerce/security", "/commerce/integration", "/commerce/deployment",
        "/commerce/testing", "/commerce/cqrs", "/commerce/events",
        "/commerce/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_SPACE_INTELLIGENCE_COMMERCE.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Space Commerce Platform is missing",
        "Never Space Economy Intelligence is missing",
        "Never Commercial Operations is missing",
        "Never Space Marketplace is missing",
        "Never Investment Intelligence is missing",
        "Never Contract Intelligence is missing",
        "Never Commerce AI is missing",
        "Never Economic Digital Twin is missing",
        "Never Governance is missing", "Never Commerce Architecture is missing",
        "Never Observability is missing", "Never Deployment Architecture is missing",
        "Never CQRS architecture is missing", "Never Event Architecture is missing",
        "Never Microservices Architecture is missing", "Never Sibling Space BC",
        "Never Replace P218-Q Sustainability",
        "Never Module-Local LLM", "Never Duplicate Financial Kernel",
        "Never Ungated Commercial Transaction",
        "Never Skip Marketplace Identity Verification",
        "Never Skip Contract Compliance Validation",
        "Never Opaque Unexplainable Commerce Decisions",
        "intelligent commercial ecosystem enabling companies",
        "P218-R", "P218-S",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P218-R", "adr": 544, "passed": passed,
        "missing_artifacts": missing, "forbidden_sibling_present": sibling,
        "catalog": catalog_ok, "aggregates": all(checks), "acl": acl_ok,
        "router": router_ok, "documentation": doc_ok, "sor": "space",
        "capability": "CAP-PLT-SP-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
