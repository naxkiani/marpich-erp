"""Quantum P215-I data intelligence foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/455-enterprise-quantum-data.md",
    "docs/architecture/ENTERPRISE_QUANTUM_DATA.md",
    "docs/architecture/quantum/QUANTUM_DATA_CAPABILITIES.v1.yaml",
    "docs/architecture/quantum/QUANTUM_DATA_DDD_CQRS.v1.yaml",
    "docs/architecture/quantum/QUANTUM_DATA_SECURITY.v1.yaml",
    "docs/architecture/quantum/QUANTUM_DATA_VALIDATION.v1.yaml",
    "docs/architecture/quantum/P215_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/quantum/domain/services/qc_platform_data.py",
    "backend/contexts/quantum/domain/aggregates/qc_data_aggregates.py",
    "backend/contexts/quantum/infrastructure/acl/qc_data_acl.py",
    "backend/contexts/quantum/application/qc_data_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/quantum_data_platform",
    "backend/contexts/quantum_knowledge_graph_platform",
    "backend/contexts/quantum_data_governance_platform",
    "backend/contexts/quantum_metadata_platform",
)
def validate_qc_data_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.quantum.domain.aggregates.qc_data_aggregates import (
        DataIntelligencePlatformRoot, KnowledgeGraphPlatformRoot, DataGovernancePlatformRoot,
        DataMeshRoot, DataProductPlatformRoot, MetadataIntelligenceRoot, DataQualityRoot,
        DataLineageRoot, DataTwinRoot,
    )
    from contexts.quantum.domain.services import qc_platform_data as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P215-I" and cat["adr"] == 455 and cat["sor"] == "quantum"
        and cat["capability"] == "CAP-PLT-QC-001"
        and cat["quantum_data_intelligence_platform_present_required"] is True
        and cat["quantum_knowledge_graph_platform_present_required"] is True
        and cat["quantum_data_governance_platform_present_required"] is True
        and cat["quantum_data_mesh_architecture_present_required"] is True
        and cat["quantum_data_product_platform_present_required"] is True
        and cat["metadata_intelligence_present_required"] is True
        and cat["data_quality_intelligence_present_required"] is True
        and cat["data_lineage_intelligence_present_required"] is True
        and cat["via_p212"] is True
        and cat["bounded_contexts"]["context_count"] >= 7
        and cat["aggregates"]["aggregate_count"] >= 8
        and cat["builds_on_p215_a"] is True and cat["builds_on_p215_h"] is True
        and cat["governed_by_p215_k"] is True
    )
    checks = [
        DataIntelligencePlatformRoot.enable(tenant_id="t1", data_ref="d1").is_missing() is False,
        KnowledgeGraphPlatformRoot.enable(tenant_id="t1", graph_ref="g1").is_missing() is False,
        DataGovernancePlatformRoot.enable(tenant_id="t1", governance_ref="gov1").is_missing() is False,
        DataMeshRoot.enable(tenant_id="t1", mesh_ref="m1").is_missing() is False,
        DataProductPlatformRoot.enable(tenant_id="t1", product_ref="p1").is_missing() is False,
        MetadataIntelligenceRoot.enable(tenant_id="t1", metadata_ref="md1").is_missing() is False,
        DataQualityRoot.enable(tenant_id="t1", quality_ref="q1").is_missing() is False,
        DataLineageRoot.enable(tenant_id="t1", lineage_ref="l1").is_missing() is False,
        DataTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/quantum/infrastructure/acl/qc_data_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p215_a", "via_p215_d", "via_p215_f", "via_p215_g", "via_p215_h", "via_p215_k",
        "via_p212", "via_p214_z", "via_p214_g", "module_local_quantum_data_forbidden",
    ))
    router = (root / "backend/contexts/quantum/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@quantum_router.get("/data")', "/data/governance", "/data/metadata", "/data/knowledge-graph",
        "/data/products", "/data/quality", "/data/lineage", "/data/marketplace",
        "/data/trust", "/data/digital-twin", "/data/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_QUANTUM_DATA.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Quantum Data Intelligence Platform is missing",
        "Never Quantum Knowledge Graph Platform is missing",
        "Never Quantum Data Governance Platform is missing",
        "Never Quantum Data Mesh Architecture is missing",
        "Never Quantum Data Product Platform is missing",
        "Never Metadata Intelligence is missing",
        "Never Data Quality Intelligence is missing",
        "Never Data Lineage Intelligence is missing",
        "Never Digital Twin Integration is missing",
        "Never CQRS architecture is missing",
        "Never Event Architecture is missing",
        "Never Microservices Architecture is missing",
        "Never API First Architecture is missing",
        "Never Cloud Native Deployment is missing",
        "Never Sibling Quantum BC",
        "P212", "P215-A", "P215-H",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P215-I", "adr": 455, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "quantum",
        "capability": "CAP-PLT-QC-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
