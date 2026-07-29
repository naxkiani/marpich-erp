"""Quantum P215-N operations / AIOps / self-healing foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/459-enterprise-quantum-operations.md",
    "docs/architecture/ENTERPRISE_QUANTUM_OPERATIONS.md",
    "docs/architecture/quantum/QUANTUM_OPERATIONS_CAPABILITIES.v1.yaml",
    "docs/architecture/quantum/QUANTUM_OPERATIONS_DDD_CQRS.v1.yaml",
    "docs/architecture/quantum/QUANTUM_OPERATIONS_SECURITY.v1.yaml",
    "docs/architecture/quantum/QUANTUM_OPERATIONS_VALIDATION.v1.yaml",
    "docs/architecture/quantum/P215_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/quantum/domain/services/qc_platform_operations.py",
    "backend/contexts/quantum/domain/aggregates/qc_operations_aggregates.py",
    "backend/contexts/quantum/infrastructure/acl/qc_operations_acl.py",
    "backend/contexts/quantum/application/qc_operations_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/quantum_operations_platform",
    "backend/contexts/quantum_aiops_platform",
    "backend/contexts/quantum_self_healing_platform",
    "backend/contexts/quantum_observability_platform",
)
def validate_qc_operations_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.quantum.domain.aggregates.qc_operations_aggregates import (
        QuantumOperationsPlatformRoot, QuantumAIOpsPlatformRoot, ObservabilityIntelligenceRoot,
        IncidentAutomationRoot, SelfHealingInfrastructureRoot, AutonomousManagementRoot,
        ReliabilityEngineeringRoot, PerformanceIntelligenceRoot,
        OperationsKnowledgeGraphRoot, OperationsDigitalTwinRoot,
    )
    from contexts.quantum.domain.services import qc_platform_operations as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P215-N" and cat["adr"] == 459 and cat["sor"] == "quantum"
        and cat["capability"] == "CAP-PLT-QC-001"
        and cat["fabric"] == "meos_quantum_autonomous_operations_fabric"
        and cat["quantum_operations_platform_present_required"] is True
        and cat["quantum_aiops_platform_present_required"] is True
        and cat["autonomous_management_present_required"] is True
        and cat["self_healing_infrastructure_present_required"] is True
        and cat["observability_intelligence_present_required"] is True
        and cat["incident_automation_present_required"] is True
        and cat["reliability_engineering_present_required"] is True
        and cat["performance_intelligence_present_required"] is True
        and cat["bounded_contexts"]["context_count"] >= 7
        and cat["aggregates"]["aggregate_count"] >= 8
        and cat["microservices"]["service_count"] >= 10
        and cat["builds_on_p215_a"] is True and cat["builds_on_p215_d"] is True
        and cat["builds_on_p215_f"] is True and cat["builds_on_p215_l"] is True
        and cat["builds_on_p215_m"] is True and cat["via_p214_j"] is True
        and cat["governed_by_p215_k"] is True
        and cat["observability_platform"]["via_observability_platform"] is True
        and cat["observability_platform"]["module_local_metrics_store_forbidden"] is True
        and cat["aiops_platform"]["via_p214_j"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        QuantumOperationsPlatformRoot.enable(tenant_id="t1", operations_ref="o1").is_missing() is False,
        QuantumAIOpsPlatformRoot.enable(tenant_id="t1", aiops_ref="a1").is_missing() is False,
        ObservabilityIntelligenceRoot.enable(tenant_id="t1", observability_ref="obs1").is_missing() is False,
        IncidentAutomationRoot.enable(tenant_id="t1", incident_ref="i1").is_missing() is False,
        SelfHealingInfrastructureRoot.enable(tenant_id="t1", healing_ref="h1").is_missing() is False,
        AutonomousManagementRoot.enable(tenant_id="t1", autonomous_ref="au1").is_missing() is False,
        ReliabilityEngineeringRoot.enable(tenant_id="t1", reliability_ref="r1").is_missing() is False,
        PerformanceIntelligenceRoot.enable(tenant_id="t1", performance_ref="p1").is_missing() is False,
        OperationsKnowledgeGraphRoot.enable(tenant_id="t1", graph_ref="g1").is_missing() is False,
        OperationsDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/quantum/infrastructure/acl/qc_operations_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p215_a", "via_p215_d", "via_p215_f", "via_p215_h", "via_p215_i", "via_p215_j",
        "via_p215_k", "via_p215_l", "via_p215_m", "via_p214_j",
        "via_observability_platform", "module_local_metrics_store_forbidden",
        "via_policy_engine", "via_workflow", "module_local_quantum_operations_forbidden",
    ))
    router = (root / "backend/contexts/quantum/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@quantum_router.get("/operations")', "/operations/monitoring", "/operations/observability",
        "/operations/aiops", "/operations/incidents", "/operations/automation",
        "/operations/self-healing", "/operations/performance", "/operations/reliability",
        "/operations/knowledge-graph", "/operations/digital-twin", "/operations/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_QUANTUM_OPERATIONS.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Quantum Operations Platform is missing",
        "Never Quantum AIOps Platform is missing",
        "Never Autonomous Management is missing",
        "Never Self-Healing Infrastructure is missing",
        "Never Observability Intelligence is missing",
        "Never Incident Automation is missing",
        "Never Reliability Engineering is missing",
        "Never Performance Intelligence is missing",
        "Never Knowledge Graph Integration is missing",
        "Never Digital Twin Integration is missing",
        "Never CQRS architecture is missing",
        "Never Event Architecture is missing",
        "Never Microservices Architecture is missing",
        "Never API First Architecture is missing",
        "Never Cloud Native Deployment is missing",
        "Never Sibling Quantum BC",
        "MEOS Quantum Operations Platform SHALL provide",
        "P215-A", "P215-D", "P215-F", "P215-H", "P215-K", "P215-L", "P215-M", "P214-J",
        "Observability Platform", "module-local metrics",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P215-N", "adr": 459, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "quantum",
        "capability": "CAP-PLT-QC-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
