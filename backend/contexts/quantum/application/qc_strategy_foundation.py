"""Quantum P215-R strategy / compliance / risk / executive foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/463-enterprise-quantum-strategy.md",
    "docs/architecture/ENTERPRISE_QUANTUM_STRATEGY.md",
    "docs/architecture/quantum/QUANTUM_STRATEGY_CAPABILITIES.v1.yaml",
    "docs/architecture/quantum/QUANTUM_STRATEGY_DDD_CQRS.v1.yaml",
    "docs/architecture/quantum/QUANTUM_STRATEGY_SECURITY.v1.yaml",
    "docs/architecture/quantum/QUANTUM_STRATEGY_VALIDATION.v1.yaml",
    "docs/architecture/quantum/P215_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/quantum/domain/services/qc_platform_strategy.py",
    "backend/contexts/quantum/domain/aggregates/qc_strategy_aggregates.py",
    "backend/contexts/quantum/infrastructure/acl/qc_strategy_acl.py",
    "backend/contexts/quantum/application/qc_strategy_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/quantum_strategy_platform",
    "backend/contexts/quantum_executive_platform",
    "backend/contexts/quantum_compliance_executive_platform",
    "backend/contexts/quantum_risk_executive_platform",
    "backend/contexts/quantum_governance",
)
def validate_qc_strategy_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.quantum.domain.aggregates.qc_strategy_aggregates import (
        QuantumGovernancePlatformRoot, QuantumStrategyPlatformRoot, QuantumComplianceIntelligenceRoot,
        QuantumRiskIntelligenceRoot, QuantumExecutiveIntelligenceRoot, QuantumPolicyManagementRoot,
        QuantumTrustFrameworkRoot, StrategyKnowledgeGraphRoot, StrategyDigitalTwinRoot,
    )
    from contexts.quantum.domain.services import qc_platform_strategy as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P215-R" and cat["adr"] == 463 and cat["sor"] == "quantum"
        and cat["capability"] == "CAP-PLT-QC-001"
        and cat["fabric"] == "meos_quantum_executive_intelligence_fabric"
        and cat["trust_gate"] == "P215-K"
        and cat["quantum_governance_platform_present_required"] is True
        and cat["quantum_strategy_platform_present_required"] is True
        and cat["quantum_compliance_intelligence_present_required"] is True
        and cat["quantum_risk_intelligence_present_required"] is True
        and cat["quantum_executive_intelligence_present_required"] is True
        and cat["quantum_policy_management_present_required"] is True
        and cat["quantum_trust_framework_present_required"] is True
        and cat["bounded_contexts"]["context_count"] >= 6
        and cat["aggregates"]["aggregate_count"] >= 7
        and cat["microservices"]["service_count"] >= 9
        and cat["builds_on_p215_a"] is True and cat["builds_on_p215_k"] is True
        and cat["builds_on_p215_q"] is True and cat["via_policy_engine"] is True
        and cat["via_p213"] is True and cat["never_replace_p215_k"] is True
        and cat["governance_platform"]["never_replace_p215_k"] is True
        and cat["policy_management"]["module_local_pdp_forbidden"] is True
        and cat["executive_intelligence"]["module_local_metrics_store_forbidden"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        QuantumGovernancePlatformRoot.enable(tenant_id="t1", governance_ref="g1").is_missing() is False,
        QuantumStrategyPlatformRoot.enable(tenant_id="t1", strategy_ref="s1").is_missing() is False,
        QuantumComplianceIntelligenceRoot.enable(tenant_id="t1", compliance_ref="c1").is_missing() is False,
        QuantumRiskIntelligenceRoot.enable(tenant_id="t1", risk_ref="r1").is_missing() is False,
        QuantumExecutiveIntelligenceRoot.enable(tenant_id="t1", executive_ref="e1").is_missing() is False,
        QuantumPolicyManagementRoot.enable(tenant_id="t1", policy_ref="p1").is_missing() is False,
        QuantumTrustFrameworkRoot.enable(tenant_id="t1", trust_ref="tr1").is_missing() is False,
        StrategyKnowledgeGraphRoot.enable(tenant_id="t1", graph_ref="kg1").is_missing() is False,
        StrategyDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/quantum/infrastructure/acl/qc_strategy_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p215_a", "via_p215_k", "via_p215_h", "via_p215_n", "via_p215_o", "via_p215_p",
        "via_p215_q", "via_p215_l", "via_policy_engine", "via_p213", "via_p214_z",
        "via_workflow", "via_audit",
        "never_replace_p215_k", "module_local_pdp_forbidden", "module_local_metrics_store_forbidden",
        "module_local_quantum_strategy_forbidden",
    ))
    router = (root / "backend/contexts/quantum/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@quantum_router.get("/strategy")', "/strategy/governance", "/strategy/compliance",
        "/strategy/risks", "/strategy/policies", "/strategy/regulatory",
        "/strategy/executive", "/strategy/trust",
        "/strategy/knowledge-graph", "/strategy/digital-twin", "/strategy/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_QUANTUM_STRATEGY.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Quantum Governance Platform is missing",
        "Never Quantum Strategy Platform is missing",
        "Never Quantum Compliance Intelligence is missing",
        "Never Quantum Risk Intelligence is missing",
        "Never Quantum Executive Intelligence is missing",
        "Never Quantum Policy Management is missing",
        "Never Quantum Trust Framework is missing",
        "Never Knowledge Graph Integration is missing",
        "Never Digital Twin Integration is missing",
        "Never CQRS architecture is missing",
        "Never Event Architecture is missing",
        "Never Microservices Architecture is missing",
        "Never API First Architecture is missing",
        "Never Cloud Native Deployment is missing",
        "Never Sibling Quantum BC",
        "Never Replace P215-K Trust Gate",
        "MEOS Quantum Governance Platform SHALL provide",
        "P215-A", "P215-K", "P215-Q", "P215-P", "P213", "Policy Engine",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P215-R", "adr": 463, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "quantum",
        "capability": "CAP-PLT-QC-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
