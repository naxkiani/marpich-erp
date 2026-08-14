"""Quantum P215-D infrastructure foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/450-enterprise-quantum-infrastructure.md",
    "docs/architecture/ENTERPRISE_QUANTUM_INFRASTRUCTURE.md",
    "docs/architecture/quantum/QUANTUM_INFRASTRUCTURE_CAPABILITIES.v1.yaml",
    "docs/architecture/quantum/QUANTUM_INFRASTRUCTURE_DDD_CQRS.v1.yaml",
    "docs/architecture/quantum/QUANTUM_INFRASTRUCTURE_SECURITY.v1.yaml",
    "docs/architecture/quantum/QUANTUM_INFRASTRUCTURE_VALIDATION.v1.yaml",
    "docs/architecture/quantum/P215_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/quantum/domain/services/qc_platform_infrastructure.py",
    "backend/contexts/quantum/domain/aggregates/qc_infrastructure_aggregates.py",
    "backend/contexts/quantum/infrastructure/acl/qc_infrastructure_acl.py",
    "backend/contexts/quantum/application/qc_infrastructure_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/quantum_infrastructure_platform",
    "backend/contexts/quantum_cloud_platform",
    "backend/contexts/quantum_hardware_platform",
    "backend/contexts/quantum_runtime_platform",
)
def validate_qc_infrastructure_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.quantum.domain.aggregates.qc_infrastructure_aggregates import (
        InfrastructurePlatformRoot, HardwareAbstractionRoot, QuantumCloudRoot,
        ResourceFabricRoot, WorkloadOrchestrationRoot, HybridComputeRoot,
        InfraSecurityRoot, InfraTwinRoot, InfraKnowledgeGraphRoot,
    )
    from contexts.quantum.domain.services import qc_platform_infrastructure as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P215-D" and cat["adr"] == 450 and cat["sor"] == "quantum"
        and cat["capability"] == "CAP-PLT-QC-001"
        and cat["quantum_infrastructure_platform_present_required"] is True
        and cat["quantum_cloud_architecture_present_required"] is True
        and cat["hardware_abstraction_layer_present_required"] is True
        and cat["quantum_resource_fabric_present_required"] is True
        and cat["workload_orchestration_present_required"] is True
        and cat["hybrid_computing_architecture_present_required"] is True
        and cat["bounded_contexts"]["context_count"] >= 7
        and cat["aggregates"]["aggregate_count"] >= 8
        and cat["builds_on_p215_a"] is True and cat["builds_on_p215_c"] is True
        and cat["governed_by_p215_k"] is True
    )
    checks = [
        InfrastructurePlatformRoot.enable(tenant_id="t1", infra_ref="i1").is_missing() is False,
        HardwareAbstractionRoot.enable(tenant_id="t1", hardware_ref="h1").is_missing() is False,
        QuantumCloudRoot.enable(tenant_id="t1", cloud_ref="c1").is_missing() is False,
        ResourceFabricRoot.enable(tenant_id="t1", resource_ref="r1").is_missing() is False,
        WorkloadOrchestrationRoot.enable(tenant_id="t1", workload_ref="w1").is_missing() is False,
        HybridComputeRoot.enable(tenant_id="t1", hybrid_ref="hy1").is_missing() is False,
        InfraSecurityRoot.enable(tenant_id="t1", security_ref="s1").is_missing() is False,
        InfraTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        InfraKnowledgeGraphRoot.enable(tenant_id="t1", graph_ref="g1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/quantum/infrastructure/acl/qc_infrastructure_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p215_a", "via_p215_c", "via_p215_k", "via_p214_z", "via_p214_v", "via_p214_t",
        "via_p213", "via_p209", "via_p210", "module_local_quantum_infrastructure_forbidden",
    ))
    router = (root / "backend/contexts/quantum/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@quantum_router.get("/infrastructure")',
        "/infrastructure/hardware", "/infrastructure/cloud", "/infrastructure/runtime",
        "/infrastructure/resources", "/infrastructure/workloads", "/infrastructure/hybrid",
        "/infrastructure/security", "/infrastructure/observability",
        "/infrastructure/knowledge-graph", "/infrastructure/digital-twin",
        "/infrastructure/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_QUANTUM_INFRASTRUCTURE.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Quantum Infrastructure Platform is missing",
        "Never Quantum Cloud Architecture is missing",
        "Never Hardware Abstraction Layer is missing",
        "Never Quantum Resource Fabric is missing",
        "Never Workload Orchestration is missing",
        "Never Hybrid Computing Architecture is missing",
        "Never Zero Trust Security is missing",
        "Never Digital Twin Integration is missing",
        "Never Knowledge Graph Integration is missing",
        "Never CQRS architecture is missing",
        "Never Event Architecture is missing",
        "Never Microservices Architecture is missing",
        "Never API First Architecture is missing",
        "Never Cloud Native Deployment is missing",
        "Never Sibling Quantum BC",
        "P215-A", "P215-C",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P215-D", "adr": 450, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "quantum",
        "capability": "CAP-PLT-QC-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
