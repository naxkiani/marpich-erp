"""Quantum P215-O testing / validation / certification foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/460-enterprise-quantum-quality.md",
    "docs/architecture/ENTERPRISE_QUANTUM_QUALITY.md",
    "docs/architecture/quantum/QUANTUM_QUALITY_CAPABILITIES.v1.yaml",
    "docs/architecture/quantum/QUANTUM_QUALITY_DDD_CQRS.v1.yaml",
    "docs/architecture/quantum/QUANTUM_QUALITY_SECURITY.v1.yaml",
    "docs/architecture/quantum/QUANTUM_QUALITY_VALIDATION.v1.yaml",
    "docs/architecture/quantum/P215_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/quantum/domain/services/qc_platform_quality.py",
    "backend/contexts/quantum/domain/aggregates/qc_quality_aggregates.py",
    "backend/contexts/quantum/infrastructure/acl/qc_quality_acl.py",
    "backend/contexts/quantum/application/qc_quality_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/quantum_testing_platform",
    "backend/contexts/quantum_validation_platform",
    "backend/contexts/quantum_benchmarking_platform",
    "backend/contexts/quantum_certification_platform",
    "backend/contexts/quantum_qa_platform",
)
def validate_qc_quality_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.quantum.domain.aggregates.qc_quality_aggregates import (
        QuantumTestingPlatformRoot, QuantumValidationPlatformRoot, QuantumBenchmarkingPlatformRoot,
        QuantumQaPlatformRoot, QuantumCertificationPlatformRoot, QualityIntelligencePlatformRoot,
        QualityKnowledgeGraphRoot, QualityDigitalTwinRoot,
    )
    from contexts.quantum.domain.services import qc_platform_quality as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P215-O" and cat["adr"] == 460 and cat["sor"] == "quantum"
        and cat["capability"] == "CAP-PLT-QC-001"
        and cat["fabric"] == "meos_quantum_quality_intelligence_fabric"
        and cat["quantum_testing_platform_present_required"] is True
        and cat["quantum_validation_platform_present_required"] is True
        and cat["quantum_benchmarking_platform_present_required"] is True
        and cat["quantum_qa_platform_present_required"] is True
        and cat["quantum_certification_platform_present_required"] is True
        and cat["quality_intelligence_platform_present_required"] is True
        and cat["knowledge_graph_integration_present_required"] is True
        and cat["digital_twin_integration_present_required"] is True
        and cat["bounded_contexts"]["context_count"] >= 6
        and cat["aggregates"]["aggregate_count"] >= 7
        and cat["microservices"]["service_count"] >= 9
        and cat["builds_on_p215_a"] is True and cat["builds_on_p215_d"] is True
        and cat["builds_on_p215_e"] is True and cat["builds_on_p215_f"] is True
        and cat["builds_on_p215_g"] is True and cat["builds_on_p215_n"] is True
        and cat["via_p214_o"] is True and cat["governed_by_p215_k"] is True
        and cat["certification_platform"]["via_workflow"] is True
        and cat["certification_platform"]["module_local_certification_authority_forbidden"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        QuantumTestingPlatformRoot.enable(tenant_id="t1", testing_ref="t1").is_missing() is False,
        QuantumValidationPlatformRoot.enable(tenant_id="t1", validation_ref="v1").is_missing() is False,
        QuantumBenchmarkingPlatformRoot.enable(tenant_id="t1", benchmark_ref="b1").is_missing() is False,
        QuantumQaPlatformRoot.enable(tenant_id="t1", qa_ref="q1").is_missing() is False,
        QuantumCertificationPlatformRoot.enable(tenant_id="t1", certification_ref="c1").is_missing() is False,
        QualityIntelligencePlatformRoot.enable(tenant_id="t1", intelligence_ref="i1").is_missing() is False,
        QualityKnowledgeGraphRoot.enable(tenant_id="t1", graph_ref="g1").is_missing() is False,
        QualityDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/quantum/infrastructure/acl/qc_quality_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p215_a", "via_p215_d", "via_p215_e", "via_p215_f", "via_p215_g", "via_p215_h",
        "via_p215_k", "via_p215_l", "via_p215_n", "via_p214_o",
        "via_workflow", "via_audit", "via_policy_engine",
        "module_local_quantum_quality_forbidden", "module_local_certification_authority_forbidden",
    ))
    router = (root / "backend/contexts/quantum/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@quantum_router.get("/testing")', "/testing/validation", "/testing/benchmarks",
        "/testing/qa", "/testing/certification", "/testing/reliability",
        "/testing/analytics", "/testing/knowledge-graph", "/testing/digital-twin",
        "/testing/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_QUANTUM_QUALITY.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Quantum Testing Platform is missing",
        "Never Quantum Validation Platform is missing",
        "Never Quantum Benchmarking Platform is missing",
        "Never Quantum QA Platform is missing",
        "Never Quantum Certification Platform is missing",
        "Never Quality Intelligence Platform is missing",
        "Never Knowledge Graph Integration is missing",
        "Never Digital Twin Integration is missing",
        "Never CQRS architecture is missing",
        "Never Event Architecture is missing",
        "Never Microservices Architecture is missing",
        "Never API First Architecture is missing",
        "Never Cloud Native Deployment is missing",
        "Never Sibling Quantum BC",
        "MEOS Quantum Quality Platform SHALL provide",
        "P215-A", "P215-D", "P215-E", "P215-F", "P215-G", "P215-H", "P215-K", "P215-N", "P214-O",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P215-O", "adr": 460, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "quantum",
        "capability": "CAP-PLT-QC-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
