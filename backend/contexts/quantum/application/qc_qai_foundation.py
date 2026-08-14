"""Quantum P215-F QAI foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/452-enterprise-quantum-qai.md",
    "docs/architecture/ENTERPRISE_QUANTUM_QAI.md",
    "docs/architecture/quantum/QUANTUM_QAI_CAPABILITIES.v1.yaml",
    "docs/architecture/quantum/QUANTUM_QAI_DDD_CQRS.v1.yaml",
    "docs/architecture/quantum/QUANTUM_QAI_SECURITY.v1.yaml",
    "docs/architecture/quantum/QUANTUM_QAI_VALIDATION.v1.yaml",
    "docs/architecture/quantum/P215_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/quantum/domain/services/qc_platform_qai.py",
    "backend/contexts/quantum/domain/aggregates/qc_qai_aggregates.py",
    "backend/contexts/quantum/infrastructure/acl/qc_qai_acl.py",
    "backend/contexts/quantum/application/qc_qai_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/quantum_ai_platform",
    "backend/contexts/quantum_ml_platform",
    "backend/contexts/quantum_neural_platform",
    "backend/contexts/qml_platform",
)
def validate_qc_qai_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.quantum.domain.aggregates.qc_qai_aggregates import (
        QuantumAIPlatformRoot, QuantumMLPlatformRoot, ModelLifecycleRoot,
        NeuralIntelligenceRoot, FeatureIntelligenceRoot, AIAgentFoundationRoot,
        QaiTwinRoot, QaiKnowledgeGraphRoot,
    )
    from contexts.quantum.domain.services import qc_platform_qai as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P215-F" and cat["adr"] == 452 and cat["sor"] == "quantum"
        and cat["capability"] == "CAP-PLT-QC-001"
        and cat["quantum_ai_platform_present_required"] is True
        and cat["quantum_machine_learning_platform_present_required"] is True
        and cat["quantum_model_lifecycle_present_required"] is True
        and cat["quantum_neural_intelligence_present_required"] is True
        and cat["quantum_feature_intelligence_present_required"] is True
        and cat["quantum_ai_agent_foundation_present_required"] is True
        and cat["bounded_contexts"]["context_count"] >= 8
        and cat["aggregates"]["aggregate_count"] >= 8
        and cat["builds_on_p215_a"] is True and cat["builds_on_p215_d"] is True
        and cat["builds_on_p215_e"] is True and cat["governed_by_p215_k"] is True
    )
    checks = [
        QuantumAIPlatformRoot.enable(tenant_id="t1", qai_ref="q1").is_missing() is False,
        QuantumMLPlatformRoot.enable(tenant_id="t1", ml_ref="m1").is_missing() is False,
        ModelLifecycleRoot.enable(tenant_id="t1", lifecycle_ref="l1").is_missing() is False,
        NeuralIntelligenceRoot.enable(tenant_id="t1", neural_ref="n1").is_missing() is False,
        FeatureIntelligenceRoot.enable(tenant_id="t1", feature_ref="f1").is_missing() is False,
        AIAgentFoundationRoot.enable(tenant_id="t1", agent_ref="a1").is_missing() is False,
        QaiTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        QaiKnowledgeGraphRoot.enable(tenant_id="t1", graph_ref="g1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/quantum/infrastructure/acl/qc_qai_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p215_a", "via_p215_d", "via_p215_e", "via_p215_k", "via_p214_z", "via_p214_f",
        "via_p214_v", "via_p214_l", "via_p213", "via_p212", "module_local_quantum_qai_forbidden",
    ))
    router = (root / "backend/contexts/quantum/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@quantum_router.get("/qai")', "/qai/ml", "/qai/models", "/qai/neural", "/qai/features",
        "/qai/training", "/qai/inference", "/qai/agents", "/qai/governance",
        "/qai/knowledge-graph", "/qai/digital-twin", "/qai/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_QUANTUM_QAI.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Quantum AI Platform is missing",
        "Never Quantum Machine Learning Platform is missing",
        "Never Quantum Model Lifecycle is missing",
        "Never Quantum Neural Intelligence is missing",
        "Never Quantum Feature Intelligence is missing",
        "Never Quantum AI Agent Foundation is missing",
        "Never Knowledge Graph Integration is missing",
        "Never Digital Twin Integration is missing",
        "Never CQRS architecture is missing",
        "Never Event Architecture is missing",
        "Never Microservices Architecture is missing",
        "Never API First Architecture is missing",
        "Never Cloud Native Deployment is missing",
        "Never Sibling Quantum BC",
        "P215-A", "P215-D", "P215-E",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P215-F", "adr": 452, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "quantum",
        "capability": "CAP-PLT-QC-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
