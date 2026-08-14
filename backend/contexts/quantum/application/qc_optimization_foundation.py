"""Quantum P215-G optimization/scientific intelligence foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/453-enterprise-quantum-optimization.md",
    "docs/architecture/ENTERPRISE_QUANTUM_OPTIMIZATION.md",
    "docs/architecture/quantum/QUANTUM_OPTIMIZATION_CAPABILITIES.v1.yaml",
    "docs/architecture/quantum/QUANTUM_OPTIMIZATION_DDD_CQRS.v1.yaml",
    "docs/architecture/quantum/QUANTUM_OPTIMIZATION_SECURITY.v1.yaml",
    "docs/architecture/quantum/QUANTUM_OPTIMIZATION_VALIDATION.v1.yaml",
    "docs/architecture/quantum/P215_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/quantum/domain/services/qc_platform_optimization.py",
    "backend/contexts/quantum/domain/aggregates/qc_optimization_aggregates.py",
    "backend/contexts/quantum/infrastructure/acl/qc_optimization_acl.py",
    "backend/contexts/quantum/application/qc_optimization_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/quantum_optimization_platform",
    "backend/contexts/quantum_simulation_platform",
    "backend/contexts/scientific_intelligence_platform",
    "backend/contexts/quantum_discovery_platform",
)
def validate_qc_optimization_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.quantum.domain.aggregates.qc_optimization_aggregates import (
        OptimizationPlatformRoot, SimulationPlatformRoot, ScientificComputingRoot,
        DiscoveryIntelligenceRoot, DecisionOptimizationRoot, OptTwinRoot, OptKnowledgeGraphRoot,
    )
    from contexts.quantum.domain.services import qc_platform_optimization as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P215-G" and cat["adr"] == 453 and cat["sor"] == "quantum"
        and cat["capability"] == "CAP-PLT-QC-001"
        and cat["quantum_optimization_platform_present_required"] is True
        and cat["simulation_intelligence_platform_present_required"] is True
        and cat["scientific_computing_platform_present_required"] is True
        and cat["discovery_intelligence_platform_present_required"] is True
        and cat["decision_optimization_engine_present_required"] is True
        and cat["bounded_contexts"]["context_count"] >= 5
        and cat["aggregates"]["aggregate_count"] >= 6
        and cat["builds_on_p215_a"] is True and cat["builds_on_p215_d"] is True
        and cat["builds_on_p215_e"] is True and cat["builds_on_p215_f"] is True
        and cat["governed_by_p215_k"] is True
    )
    checks = [
        OptimizationPlatformRoot.enable(tenant_id="t1", optimization_ref="o1").is_missing() is False,
        SimulationPlatformRoot.enable(tenant_id="t1", simulation_ref="s1").is_missing() is False,
        ScientificComputingRoot.enable(tenant_id="t1", scientific_ref="sc1").is_missing() is False,
        DiscoveryIntelligenceRoot.enable(tenant_id="t1", discovery_ref="d1").is_missing() is False,
        DecisionOptimizationRoot.enable(tenant_id="t1", decision_ref="dec1").is_missing() is False,
        OptTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        OptKnowledgeGraphRoot.enable(tenant_id="t1", graph_ref="g1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/quantum/infrastructure/acl/qc_optimization_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p215_a", "via_p215_d", "via_p215_e", "via_p215_f", "via_p215_k", "via_p214_z",
        "via_p214_v", "via_p214_g", "via_p213", "via_p212", "module_local_quantum_optimization_forbidden",
    ))
    router = (root / "backend/contexts/quantum/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@quantum_router.get("/optimization")', "/optimization/algorithms", "/optimization/simulation",
        "/optimization/discovery", "/optimization/decision", "/optimization/models",
        "/optimization/validation", "/optimization/knowledge-graph", "/optimization/digital-twin",
        "/optimization/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_QUANTUM_OPTIMIZATION.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Quantum Optimization Platform is missing",
        "Never Simulation Intelligence Platform is missing",
        "Never Scientific Computing Platform is missing",
        "Never Discovery Intelligence Platform is missing",
        "Never Decision Optimization Engine is missing",
        "Never Knowledge Graph Integration is missing",
        "Never Digital Twin Integration is missing",
        "Never CQRS architecture is missing",
        "Never Event Architecture is missing",
        "Never Microservices Architecture is missing",
        "Never API First Architecture is missing",
        "Never Cloud Native Deployment is missing",
        "Never Sibling Quantum BC",
        "P215-A", "P215-D", "P215-E", "P215-F",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P215-G", "adr": 453, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "quantum",
        "capability": "CAP-PLT-QC-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
