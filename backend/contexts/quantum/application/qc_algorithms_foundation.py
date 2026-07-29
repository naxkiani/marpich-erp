"""Quantum P215-E algorithms foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/451-enterprise-quantum-algorithms.md",
    "docs/architecture/ENTERPRISE_QUANTUM_ALGORITHMS.md",
    "docs/architecture/quantum/QUANTUM_ALGORITHMS_CAPABILITIES.v1.yaml",
    "docs/architecture/quantum/QUANTUM_ALGORITHMS_DDD_CQRS.v1.yaml",
    "docs/architecture/quantum/QUANTUM_ALGORITHMS_SECURITY.v1.yaml",
    "docs/architecture/quantum/QUANTUM_ALGORITHMS_VALIDATION.v1.yaml",
    "docs/architecture/quantum/P215_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/quantum/domain/services/qc_platform_algorithms.py",
    "backend/contexts/quantum/domain/aggregates/qc_algorithms_aggregates.py",
    "backend/contexts/quantum/infrastructure/acl/qc_algorithms_acl.py",
    "backend/contexts/quantum/application/qc_algorithms_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/quantum_algorithm_platform",
    "backend/contexts/quantum_software_platform",
    "backend/contexts/quantum_programming_platform",
    "backend/contexts/quantum_circuit_platform",
)
def validate_qc_algorithms_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.quantum.domain.aggregates.qc_algorithms_aggregates import (
        AlgorithmPlatformRoot, SoftwarePlatformRoot, ProgrammingEnvironmentRoot,
        CircuitIntelligenceRoot, OptimizationPlatformRoot, SoftwareLifecycleRoot,
        AlgorithmRepositoryRoot, MarketplaceRoot, AlgorithmsTwinRoot, AlgorithmsKnowledgeGraphRoot,
    )
    from contexts.quantum.domain.services import qc_platform_algorithms as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P215-E" and cat["adr"] == 451 and cat["sor"] == "quantum"
        and cat["capability"] == "CAP-PLT-QC-001"
        and cat["quantum_algorithm_platform_present_required"] is True
        and cat["quantum_software_platform_present_required"] is True
        and cat["quantum_programming_environment_present_required"] is True
        and cat["circuit_intelligence_engine_present_required"] is True
        and cat["optimization_platform_present_required"] is True
        and cat["software_lifecycle_management_present_required"] is True
        and cat["algorithm_repository_present_required"] is True
        and cat["quantum_marketplace_present_required"] is True
        and cat["bounded_contexts"]["context_count"] >= 7
        and cat["aggregates"]["aggregate_count"] >= 8
        and cat["builds_on_p215_a"] is True and cat["builds_on_p215_c"] is True
        and cat["builds_on_p215_d"] is True and cat["governed_by_p215_k"] is True
    )
    checks = [
        AlgorithmPlatformRoot.enable(tenant_id="t1", algorithm_ref="a1").is_missing() is False,
        SoftwarePlatformRoot.enable(tenant_id="t1", software_ref="s1").is_missing() is False,
        ProgrammingEnvironmentRoot.enable(tenant_id="t1", programming_ref="p1").is_missing() is False,
        CircuitIntelligenceRoot.enable(tenant_id="t1", circuit_ref="c1").is_missing() is False,
        OptimizationPlatformRoot.enable(tenant_id="t1", optimization_ref="o1").is_missing() is False,
        SoftwareLifecycleRoot.enable(tenant_id="t1", lifecycle_ref="l1").is_missing() is False,
        AlgorithmRepositoryRoot.enable(tenant_id="t1", repository_ref="r1").is_missing() is False,
        MarketplaceRoot.enable(tenant_id="t1", marketplace_ref="m1").is_missing() is False,
        AlgorithmsTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        AlgorithmsKnowledgeGraphRoot.enable(tenant_id="t1", graph_ref="g1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/quantum/infrastructure/acl/qc_algorithms_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p215_a", "via_p215_c", "via_p215_d", "via_p215_k", "via_p214_z", "via_p214_f",
        "via_p214_v", "via_p213", "module_local_quantum_algorithms_forbidden",
    ))
    router = (root / "backend/contexts/quantum/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@quantum_router.get("/algorithms")',
        "/algorithms/programming", "/algorithms/circuits", "/algorithms/optimization",
        "/algorithms/lifecycle", "/algorithms/repository", "/algorithms/marketplace",
        "/algorithms/testing", "/algorithms/knowledge-graph", "/algorithms/digital-twin",
        "/algorithms/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_QUANTUM_ALGORITHMS.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Quantum Algorithm Platform is missing",
        "Never Quantum Software Platform is missing",
        "Never Quantum Programming Environment is missing",
        "Never Circuit Intelligence Engine is missing",
        "Never Optimization Platform is missing",
        "Never Software Lifecycle Management is missing",
        "Never Algorithm Repository is missing",
        "Never Quantum Marketplace is missing",
        "Never Knowledge Graph Integration is missing",
        "Never Digital Twin Integration is missing",
        "Never CQRS architecture is missing",
        "Never Event Architecture is missing",
        "Never Microservices Architecture is missing",
        "Never API First Architecture is missing",
        "Never Cloud Native Deployment is missing",
        "Never Sibling Quantum BC",
        "P215-A", "P215-C", "P215-D",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P215-E", "adr": 451, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "quantum",
        "capability": "CAP-PLT-QC-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
