"""Quantum P215-Q research / innovation lab / discovery foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/462-enterprise-quantum-research.md",
    "docs/architecture/ENTERPRISE_QUANTUM_RESEARCH.md",
    "docs/architecture/quantum/QUANTUM_RESEARCH_CAPABILITIES.v1.yaml",
    "docs/architecture/quantum/QUANTUM_RESEARCH_DDD_CQRS.v1.yaml",
    "docs/architecture/quantum/QUANTUM_RESEARCH_SECURITY.v1.yaml",
    "docs/architecture/quantum/QUANTUM_RESEARCH_VALIDATION.v1.yaml",
    "docs/architecture/quantum/P215_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/quantum/domain/services/qc_platform_research.py",
    "backend/contexts/quantum/domain/aggregates/qc_research_aggregates.py",
    "backend/contexts/quantum/infrastructure/acl/qc_research_acl.py",
    "backend/contexts/quantum/application/qc_research_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/quantum_research_platform",
    "backend/contexts/quantum_innovation_lab_platform",
    "backend/contexts/quantum_discovery_platform",
    "backend/contexts/quantum_experiment_platform",
    "backend/contexts/quantum_future_radar_platform",
)
def validate_qc_research_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.quantum.domain.aggregates.qc_research_aggregates import (
        QuantumResearchPlatformRoot, QuantumInnovationLabRoot, ScientificCollaborationPlatformRoot,
        DiscoveryIntelligenceRoot, AiAssistedResearchRoot, ExperimentManagementRoot,
        FutureTechnologyRadarRoot, ResearchKnowledgeGraphRoot, ResearchDigitalTwinRoot,
    )
    from contexts.quantum.domain.services import qc_platform_research as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P215-Q" and cat["adr"] == 462 and cat["sor"] == "quantum"
        and cat["capability"] == "CAP-PLT-QC-001"
        and cat["fabric"] == "meos_quantum_discovery_intelligence_fabric"
        and cat["quantum_research_platform_present_required"] is True
        and cat["quantum_innovation_lab_present_required"] is True
        and cat["scientific_collaboration_platform_present_required"] is True
        and cat["discovery_intelligence_present_required"] is True
        and cat["ai_assisted_research_present_required"] is True
        and cat["experiment_management_present_required"] is True
        and cat["future_technology_radar_present_required"] is True
        and cat["bounded_contexts"]["context_count"] >= 6
        and cat["aggregates"]["aggregate_count"] >= 7
        and cat["microservices"]["service_count"] >= 9
        and cat["builds_on_p215_a"] is True and cat["builds_on_p215_g"] is True
        and cat["builds_on_p215_p"] is True and cat["via_p214_g"] is True
        and cat["via_document_exchange"] is True and cat["governed_by_p215_k"] is True
        and cat["ai_assisted_research"]["module_local_llm_forbidden"] is True
        and cat["scientific_collaboration"]["module_local_publication_blob_forbidden"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        QuantumResearchPlatformRoot.enable(tenant_id="t1", research_ref="r1").is_missing() is False,
        QuantumInnovationLabRoot.enable(tenant_id="t1", lab_ref="l1").is_missing() is False,
        ScientificCollaborationPlatformRoot.enable(tenant_id="t1", collaboration_ref="c1").is_missing() is False,
        DiscoveryIntelligenceRoot.enable(tenant_id="t1", discovery_ref="d1").is_missing() is False,
        AiAssistedResearchRoot.enable(tenant_id="t1", copilot_ref="a1").is_missing() is False,
        ExperimentManagementRoot.enable(tenant_id="t1", experiment_ref="e1").is_missing() is False,
        FutureTechnologyRadarRoot.enable(tenant_id="t1", radar_ref="f1").is_missing() is False,
        ResearchKnowledgeGraphRoot.enable(tenant_id="t1", graph_ref="g1").is_missing() is False,
        ResearchDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/quantum/infrastructure/acl/qc_research_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p215_a", "via_p215_d", "via_p215_e", "via_p215_f", "via_p215_g", "via_p215_i",
        "via_p215_k", "via_p215_l", "via_p215_o", "via_p215_p", "via_p214_g", "via_p214_z",
        "via_document_exchange", "via_workflow", "via_p213",
        "module_local_llm_forbidden", "module_local_publication_blob_forbidden",
        "ungated_dual_use_research_forbidden", "module_local_quantum_research_forbidden",
    ))
    router = (root / "backend/contexts/quantum/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@quantum_router.get("/research")', "/research/lab", "/research/experiments",
        "/research/collaboration", "/research/discovery", "/research/radar",
        "/research/knowledge-graph", "/research/digital-twin", "/research/analytics",
        "/research/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_QUANTUM_RESEARCH.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Quantum Research Platform is missing",
        "Never Quantum Innovation Lab is missing",
        "Never Scientific Collaboration Platform is missing",
        "Never Discovery Intelligence is missing",
        "Never AI Assisted Research is missing",
        "Never Experiment Management is missing",
        "Never Future Technology Radar is missing",
        "Never Knowledge Graph Integration is missing",
        "Never Digital Twin Integration is missing",
        "Never CQRS architecture is missing",
        "Never Event Architecture is missing",
        "Never Microservices Architecture is missing",
        "Never API First Architecture is missing",
        "Never Cloud Native Deployment is missing",
        "Never Sibling Quantum BC",
        "MEOS Quantum Research Platform SHALL provide",
        "P215-A", "P215-G", "P215-K", "P215-P", "P214-G", "Document Exchange",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P215-Q", "adr": 462, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "quantum",
        "capability": "CAP-PLT-QC-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
