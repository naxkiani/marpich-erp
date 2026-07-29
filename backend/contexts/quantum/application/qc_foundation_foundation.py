"""Quantum P215-A foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/447-enterprise-quantum-foundation.md",
    "docs/architecture/ENTERPRISE_QUANTUM_FOUNDATION.md",
    "docs/architecture/quantum/QUANTUM_FOUNDATION_CAPABILITIES.v1.yaml",
    "docs/architecture/quantum/QUANTUM_FOUNDATION_DDD_CQRS.v1.yaml",
    "docs/architecture/quantum/QUANTUM_FOUNDATION_SECURITY.v1.yaml",
    "docs/architecture/quantum/QUANTUM_FOUNDATION_VALIDATION.v1.yaml",
    "docs/architecture/quantum/P215_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/quantum/domain/services/qc_platform_foundation.py",
    "backend/contexts/quantum/domain/aggregates/qc_foundation_aggregates.py",
    "backend/contexts/quantum/infrastructure/acl/qc_foundation_acl.py",
    "backend/contexts/quantum/application/qc_foundation_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/quantum_computing_platform",
    "backend/contexts/quantum_ai_platform",
    "backend/contexts/hybrid_quantum_platform",
    "backend/contexts/quantum_simulation_platform",
    "backend/contexts/quantum_algorithm_platform",
)
def validate_qc_foundation_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.quantum.domain.aggregates.qc_foundation_aggregates import QuantumPlatformRoot, QuantumAIRoot, HybridComputingRoot, AlgorithmFactoryRoot, SimulationRoot, ResearchRoot, QuantumTwinRoot
    from contexts.quantum.domain.services import qc_platform_foundation as catmod
    cat = catmod.catalog()
    catalog_ok = cat["prompt_id"] == "P215-A" and cat["adr"] == 447 and cat["sor"] == "quantum" and cat["capability"] == "CAP-PLT-QC-001" and cat["enterprise_quantum_computing_foundation_present_required"] is True and cat["quantum_ai"]["via_p214_v"] is True and cat["governed_by_p215_k"] is True and cat["microservices"]["service_count"] >= 10
    checks = [QuantumPlatformRoot.enable(tenant_id="t1", platform_ref="p1").is_missing() is False, QuantumAIRoot.enable(tenant_id="t1", qai_ref="q1").is_missing() is False, HybridComputingRoot.enable(tenant_id="t1", hybrid_ref="h1").is_missing() is False, AlgorithmFactoryRoot.enable(tenant_id="t1", algorithm_ref="a1").is_missing() is False, SimulationRoot.enable(tenant_id="t1", simulation_ref="s1").is_missing() is False, ResearchRoot.enable(tenant_id="t1", research_ref="r1").is_missing() is False, QuantumTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False]
    acl_text = (root / "backend/contexts/quantum/infrastructure/acl/qc_foundation_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in ("via_p209", "via_p212", "via_p213", "via_p214_t", "via_p214_v", "via_p214_z", "via_p215_k", "module_local_quantum_foundation_forbidden", "pqc_remains_secrets"))
    router = (root / "backend/contexts/quantum/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in ('@quantum_router.get("/foundation")', "/foundation/platform", "/foundation/qai", "/foundation/hybrid", "/foundation/algorithms", "/foundation/simulation", "/foundation/digital-twin", "/foundation/readiness"))
    law = (root / "docs/architecture/ENTERPRISE_QUANTUM_FOUNDATION.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in ("Never Enterprise Quantum Computing Foundation is missing", "Never Quantum AI Platform is missing", "Never Hybrid Computing Architecture is missing", "Never Quantum Algorithm Platform is missing", "Never Quantum Simulation Platform is missing", "Never Quantum Research Platform is missing", "Never Quantum Knowledge Graph is missing", "Never Quantum Digital Twin is missing", "Never CQRS architecture is missing", "Never Event architecture is missing", "Never Microservices architecture is missing", "Never API first architecture is missing", "Never Zero trust security is missing", "Never Cloud native deployment is missing", "Never Sibling Quantum BC", "P214-Z", "P215-K"))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {"prompt": "P215-A", "adr": 447, "passed": passed, "missing_artifacts": missing, "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks), "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "quantum", "capability": "CAP-PLT-QC-001", "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD"}
