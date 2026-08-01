"""Quantum P215-P marketplace / economy / innovation foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/461-enterprise-quantum-marketplace.md",
    "docs/architecture/ENTERPRISE_QUANTUM_MARKETPLACE.md",
    "docs/architecture/quantum/QUANTUM_MARKETPLACE_CAPABILITIES.v1.yaml",
    "docs/architecture/quantum/QUANTUM_MARKETPLACE_DDD_CQRS.v1.yaml",
    "docs/architecture/quantum/QUANTUM_MARKETPLACE_SECURITY.v1.yaml",
    "docs/architecture/quantum/QUANTUM_MARKETPLACE_VALIDATION.v1.yaml",
    "docs/architecture/quantum/P215_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/quantum/domain/services/qc_platform_marketplace.py",
    "backend/contexts/quantum/domain/aggregates/qc_marketplace_aggregates.py",
    "backend/contexts/quantum/infrastructure/acl/qc_marketplace_acl.py",
    "backend/contexts/quantum/application/qc_marketplace_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/quantum_marketplace_platform",
    "backend/contexts/quantum_capability_exchange_platform",
    "backend/contexts/quantum_algorithm_marketplace_platform",
    "backend/contexts/quantum_economy_platform",
    "backend/contexts/quantum_innovation_ecosystem_platform",
)
def validate_qc_marketplace_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.quantum.domain.aggregates.qc_marketplace_aggregates import (
        QuantumMarketplacePlatformRoot, CapabilityExchangePlatformRoot, QuantumServiceEconomyRoot,
        AlgorithmMarketplaceRoot, ApplicationMarketplaceRoot, InnovationEcosystemRoot,
        EconomicIntelligenceRoot, MarketplaceKnowledgeGraphRoot, MarketplaceDigitalTwinRoot,
    )
    from contexts.quantum.domain.services import qc_platform_marketplace as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P215-P" and cat["adr"] == 461 and cat["sor"] == "quantum"
        and cat["capability"] == "CAP-PLT-QC-001"
        and cat["fabric"] == "meos_quantum_economy_intelligence_fabric"
        and cat["quantum_marketplace_platform_present_required"] is True
        and cat["capability_exchange_platform_present_required"] is True
        and cat["quantum_service_economy_present_required"] is True
        and cat["algorithm_marketplace_present_required"] is True
        and cat["application_marketplace_present_required"] is True
        and cat["innovation_ecosystem_present_required"] is True
        and cat["economic_intelligence_present_required"] is True
        and cat["bounded_contexts"]["context_count"] >= 7
        and cat["aggregates"]["aggregate_count"] >= 8
        and cat["microservices"]["service_count"] >= 10
        and cat["builds_on_p215_a"] is True and cat["builds_on_p215_e"] is True
        and cat["builds_on_p215_m"] is True and cat["builds_on_p215_o"] is True
        and cat["via_p213"] is True and cat["via_plugin_platform"] is True
        and cat["via_financial_kernel"] is True and cat["governed_by_p215_k"] is True
        and cat["application_marketplace"]["module_local_plugin_marketplace_forbidden"] is True
        and cat["security"]["module_local_payment_processor_forbidden"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        QuantumMarketplacePlatformRoot.enable(tenant_id="t1", marketplace_ref="m1").is_missing() is False,
        CapabilityExchangePlatformRoot.enable(tenant_id="t1", capability_ref="c1").is_missing() is False,
        QuantumServiceEconomyRoot.enable(tenant_id="t1", service_economy_ref="s1").is_missing() is False,
        AlgorithmMarketplaceRoot.enable(tenant_id="t1", algorithm_ref="a1").is_missing() is False,
        ApplicationMarketplaceRoot.enable(tenant_id="t1", application_ref="ap1").is_missing() is False,
        InnovationEcosystemRoot.enable(tenant_id="t1", innovation_ref="i1").is_missing() is False,
        EconomicIntelligenceRoot.enable(tenant_id="t1", economy_ref="e1").is_missing() is False,
        MarketplaceKnowledgeGraphRoot.enable(tenant_id="t1", graph_ref="g1").is_missing() is False,
        MarketplaceDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/quantum/infrastructure/acl/qc_marketplace_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p215_a", "via_p215_d", "via_p215_e", "via_p215_f", "via_p215_h", "via_p215_i",
        "via_p215_k", "via_p215_l", "via_p215_m", "via_p215_o", "via_p213",
        "via_plugin_platform", "via_financial_kernel", "via_enterprise_search",
        "module_local_quantum_marketplace_forbidden", "module_local_plugin_marketplace_forbidden",
        "module_local_payment_processor_forbidden", "ungated_capability_publish_forbidden",
    ))
    router = (root / "backend/contexts/quantum/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@quantum_router.get("/marketplace")', "/marketplace/capabilities", "/marketplace/services",
        "/marketplace/algorithms", "/marketplace/applications", "/marketplace/resources",
        "/marketplace/innovation", "/marketplace/economy", "/marketplace/knowledge-graph",
        "/marketplace/digital-twin", "/marketplace/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_QUANTUM_MARKETPLACE.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Quantum Marketplace Platform is missing",
        "Never Capability Exchange Platform is missing",
        "Never Quantum Service Economy is missing",
        "Never Algorithm Marketplace is missing",
        "Never Application Marketplace is missing",
        "Never Innovation Ecosystem is missing",
        "Never Economic Intelligence is missing",
        "Never Knowledge Graph Integration is missing",
        "Never Digital Twin Integration is missing",
        "Never CQRS architecture is missing",
        "Never Event Architecture is missing",
        "Never Microservices Architecture is missing",
        "Never API First Architecture is missing",
        "Never Cloud Native Deployment is missing",
        "Never Sibling Quantum BC",
        "MEOS Quantum Marketplace Platform SHALL provide",
        "P215-A", "P215-E", "P215-M", "P215-O", "P215-K", "P213", "Plugin Platform", "Financial Kernel",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P215-P", "adr": 461, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "quantum",
        "capability": "CAP-PLT-QC-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
