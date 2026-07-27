"""Data Governance P212-F Data Mesh foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/399-enterprise-data-governance-data-mesh.md",
    "docs/architecture/ENTERPRISE_DATA_GOVERNANCE_DATA_MESH.md",
    "docs/architecture/data_governance/DATA_GOVERNANCE_MESH_CAPABILITIES.v1.yaml",
    "docs/architecture/data_governance/DATA_GOVERNANCE_MESH_DDD_CQRS.v1.yaml",
    "docs/architecture/data_governance/DATA_GOVERNANCE_MESH_SECURITY.v1.yaml",
    "docs/architecture/data_governance/DATA_GOVERNANCE_MESH_VALIDATION.v1.yaml",
    "backend/contexts/data_governance/domain/services/dg_platform_mesh.py",
    "backend/contexts/data_governance/domain/aggregates/dg_mesh_aggregates.py",
    "backend/contexts/data_governance/infrastructure/acl/dg_mesh_acl.py",
    "backend/contexts/data_governance/application/dg_mesh_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/data_mesh",
    "backend/contexts/data_product_platform",
    "backend/contexts/data_marketplace",
    "backend/contexts/enterprise_intelligence",
    "backend/contexts/data_quality_platform",
    "backend/contexts/metadata_governance_platform",
)


def validate_dg_mesh_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.data_governance.domain.aggregates.dg_mesh_aggregates import (
        DgMeshAiIntelligenceRoot,
        DgMeshArchitectureRoot,
        DgMeshContractRoot,
        DgMeshCqrsRoot,
        DgMeshDddModelRoot,
        DgMeshDigitalTwinRoot,
        DgMeshDomainModelRoot,
        DgMeshEventSourcingRoot,
        DgMeshKnowledgeGraphRoot,
        DgMeshLifecycleRoot,
        DgMeshMicroservicesRoot,
        DgMeshQualityIntegrationRoot,
        DgMeshScalabilityRoot,
        DgProductPlatformRoot,
    )
    from contexts.data_governance.domain.services import dg_platform_mesh as mesh

    cat = mesh.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P212-F"
        and cat.get("adr") == 399
        and cat.get("sor") == "data_governance"
        and cat.get("capability") == "CAP-PLT-DG-001"
        and cat["data_mesh_architecture_complete_required"] is True
        and cat["data_product_platform_complete_required"] is True
        and cat["ddd_domain_model_present_required"] is True
        and cat["data_domain_model_present_required"] is True
        and cat["data_product_lifecycle_present_required"] is True
        and cat["data_contract_architecture_present_required"] is True
        and cat["data_quality_integration_present_required"] is True
        and cat["knowledge_graph_integration_present_required"] is True
        and cat["digital_twin_integration_present_required"] is True
        and cat["ai_native_intelligence_present_required"] is True
        and cat["cqrs_architecture_present_required"] is True
        and cat["event_sourcing_architecture_present_required"] is True
        and cat["microservices_architecture_present_required"] is True
        and cat["enterprise_scalability_present_required"] is True
        and cat["mesh_architecture"]["not_incomplete"] is True
        and cat["product_platform"]["not_incomplete"] is True
        and cat["ddd_model"]["not_missing"] is True
        and cat["domain_model"]["not_missing"] is True
        and cat["product_lifecycle"]["not_missing"] is True
        and cat["contract_architecture"]["not_missing"] is True
        and cat["quality_integration"]["not_missing"] is True
        and cat["knowledge_graph"]["not_missing"] is True
        and cat["digital_twin"]["not_missing"] is True
        and cat["ai_intelligence"]["not_missing"] is True
        and cat["cqrs"]["not_missing"] is True
        and cat["event_sourcing"]["not_missing"] is True
        and cat["microservices"]["not_missing"] is True
        and cat["scalability"]["not_missing"] is True
        and cat["mesh_architecture"]["principle_count"] >= 4
        and cat["domain_model"]["domain_count"] >= 10
        and cat["product_lifecycle"]["stage_count"] >= 9
        and cat["microservices"]["service_count"] >= 6
        and cat["cqrs"]["event_count"] >= 10
        and cat["cursor_outputs"]["count"] >= 18
        and (
            "data_mesh_architecture_is_incomplete"
            in cat["quality_gates"]["reject_if"]
        )
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )

    def _bad(fn, **kwargs):
        try:
            fn(**kwargs)
            return True
        except ValueError:
            return False

    checks = []
    checks.append(
        not _bad(
            DgMeshArchitectureRoot.publish,
            tenant_id="t1",
            architecture_ref="a1",
            complete=False,
        )
        and DgMeshArchitectureRoot.publish(
            tenant_id="t1", architecture_ref="a2"
        ).is_incomplete()
        is False
    )
    checks.append(
        not _bad(
            DgProductPlatformRoot.publish,
            tenant_id="t1",
            platform_ref="p1",
            complete=False,
        )
        and DgProductPlatformRoot.publish(
            tenant_id="t1", platform_ref="p2"
        ).is_incomplete()
        is False
    )
    checks.append(
        not _bad(
            DgMeshDddModelRoot.define,
            tenant_id="t1",
            model_ref="d1",
            present=False,
        )
        and DgMeshDddModelRoot.define(
            tenant_id="t1", model_ref="d2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgMeshDomainModelRoot.define,
            tenant_id="t1",
            domain_ref="dm1",
            present=False,
        )
        and DgMeshDomainModelRoot.define(
            tenant_id="t1", domain_ref="dm2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgMeshLifecycleRoot.enable,
            tenant_id="t1",
            lifecycle_ref="l1",
            present=False,
        )
        and DgMeshLifecycleRoot.enable(
            tenant_id="t1", lifecycle_ref="l2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgMeshContractRoot.publish,
            tenant_id="t1",
            contract_ref="c1",
            present=False,
        )
        and DgMeshContractRoot.publish(
            tenant_id="t1", contract_ref="c2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgMeshQualityIntegrationRoot.integrate,
            tenant_id="t1",
            quality_ref="q1",
            present=False,
        )
        and DgMeshQualityIntegrationRoot.integrate(
            tenant_id="t1", quality_ref="q2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgMeshKnowledgeGraphRoot.integrate,
            tenant_id="t1",
            graph_ref="g1",
            present=False,
        )
        and DgMeshKnowledgeGraphRoot.integrate(
            tenant_id="t1", graph_ref="g2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgMeshDigitalTwinRoot.integrate,
            tenant_id="t1",
            twin_ref="tw1",
            present=False,
        )
        and DgMeshDigitalTwinRoot.integrate(
            tenant_id="t1", twin_ref="tw2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgMeshAiIntelligenceRoot.enable,
            tenant_id="t1",
            ai_ref="ai1",
            present=False,
        )
        and DgMeshAiIntelligenceRoot.enable(
            tenant_id="t1", ai_ref="ai2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgMeshCqrsRoot.align,
            tenant_id="t1",
            cqrs_ref="cq1",
            present=False,
        )
        and DgMeshCqrsRoot.align(
            tenant_id="t1", cqrs_ref="cq2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgMeshEventSourcingRoot.enable,
            tenant_id="t1",
            es_ref="e1",
            present=False,
        )
        and DgMeshEventSourcingRoot.enable(
            tenant_id="t1", es_ref="e2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgMeshMicroservicesRoot.declare,
            tenant_id="t1",
            ms_ref="ms1",
            present=False,
        )
        and DgMeshMicroservicesRoot.declare(
            tenant_id="t1", ms_ref="ms2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgMeshScalabilityRoot.confirm,
            tenant_id="t1",
            scale_ref="sc1",
            present=False,
        )
        and DgMeshScalabilityRoot.confirm(
            tenant_id="t1", scale_ref="sc2"
        ).is_missing()
        is False
    )
    aggregates_ok = all(checks)

    acl_path = (
        root
        / "backend/contexts/data_governance/infrastructure/acl/dg_mesh_acl.py"
    )
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_p212_d" in acl_text
        and "via_p212_e" in acl_text
        and "via_p207" in acl_text
        and "ai_native_intelligence_present_required" in acl_text
        and "data_quality_integration_present_required" in acl_text
    )

    router = (
        root / "backend/contexts/data_governance/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@data_governance_router.get("/mesh")' in router
        and "/mesh/products" in router
        and "/mesh/domains" in router
        and "/mesh/contracts" in router
        and "/mesh/readiness" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_DATA_GOVERNANCE_DATA_MESH.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never Data mesh architecture is incomplete" in law
        and "Never Data product platform is incomplete" in law
        and "Never DDD domain model is missing" in law
        and "Never Data domain model is missing" in law
        and "Never Data product lifecycle is missing" in law
        and "Never Data contract architecture is missing" in law
        and "Never Data quality integration is missing" in law
        and "Never Knowledge graph integration is missing" in law
        and "Never Digital twin integration is missing" in law
        and "Never AI native intelligence is missing" in law
        and "Never CQRS architecture is missing" in law
        and "Never Event sourcing architecture is missing" in law
        and "Never Microservices architecture is missing" in law
        and "Never Enterprise scalability is missing" in law
        and "Never Sibling data mesh BC" in law
        and (
            "Data SHALL be managed as a strategic product owned by business domains."
            in law
        )
    )

    passed = (
        not missing
        and not sibling
        and catalog_ok
        and aggregates_ok
        and acl_ok
        and router_ok
        and doc_ok
    )
    return {
        "prompt": "P212-F",
        "adr": 399,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "catalog": catalog_ok,
        "aggregates": aggregates_ok,
        "acl": acl_ok,
        "router": router_ok,
        "documentation": doc_ok,
        "sor": "data_governance",
        "capability": "CAP-PLT-DG-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
