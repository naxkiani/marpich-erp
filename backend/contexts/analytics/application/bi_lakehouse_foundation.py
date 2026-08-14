"""Analytics P213-F BI lakehouse foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/410-enterprise-business-intelligence-lakehouse.md",
    "docs/architecture/ENTERPRISE_BUSINESS_INTELLIGENCE_LAKEHOUSE.md",
    "docs/architecture/business_intelligence/BI_LAKEHOUSE_CAPABILITIES.v1.yaml",
    "docs/architecture/business_intelligence/BI_LAKEHOUSE_DDD_CQRS.v1.yaml",
    "docs/architecture/business_intelligence/BI_LAKEHOUSE_SECURITY.v1.yaml",
    "docs/architecture/business_intelligence/BI_LAKEHOUSE_VALIDATION.v1.yaml",
    "backend/contexts/analytics/domain/services/bi_platform_lakehouse.py",
    "backend/contexts/analytics/domain/aggregates/bi_lakehouse_aggregates.py",
    "backend/contexts/analytics/infrastructure/acl/bi_lakehouse_acl.py",
    "backend/contexts/analytics/application/bi_lakehouse_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/business_intelligence",
    "backend/contexts/decision_intelligence",
    "backend/contexts/reporting_platform",
    "backend/contexts/metric_governance_platform",
    "backend/contexts/visualization_platform",
    "backend/contexts/bi_core",
)


def validate_bi_lakehouse_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.analytics.domain.aggregates.bi_lakehouse_aggregates import (
        BiAiDataFoundationRoot,
        BiDataMeshAlignedRoot,
        BiLakehouseProfileRoot,
        BiProcessingArchitectureRoot,
        BiStorageArchitectureRoot,
    )
    from contexts.analytics.domain.services import bi_platform_lakehouse as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P213-F"
        and cat.get("adr") == 410
        and cat.get("sor") == "analytics"
        and cat.get("capability") == "CAP-PLT-BI-001"
        and cat.get("principle") == catmod.PRINCIPLE
        and cat.get("fabric") == catmod.FABRIC
        and "analytics, AI, and decision intelligence" in cat["principle"]
        and cat["enterprise_lakehouse_architecture_present_required"] is True
        and cat["unified_data_platform_present_required"] is True
        and cat["data_warehouse_integration_present_required"] is True
        and cat["data_lake_capability_present_required"] is True
        and cat["ai_data_foundation_present_required"] is True
        and cat["data_mesh_alignment_present_required"] is True
        and cat["data_governance_alignment_present_required"] is True
        and cat["knowledge_graph_integration_present_required"] is True
        and cat["digital_twin_integration_present_required"] is True
        and cat["cqrs_architecture_present_required"] is True
        and cat["event_driven_architecture_present_required"] is True
        and cat["microservice_architecture_present_required"] is True
        and cat["api_first_architecture_present_required"] is True
        and cat["cloud_native_deployment_present_required"] is True
        and cat["architecture_present_required"] is True
        and cat["storage_architecture_present_required"] is True
        and cat["data_processing_architecture_present_required"] is True
        and cat["semantic_layer_present_required"] is True
        and cat["sibling_business_intelligence_bc_forbidden"] is True
        and cat["domain_model"]["supporting_count"] >= 7
        and cat["bounded_contexts"]["context_count"] >= 5
        and cat["architecture"]["layers"]["layer_count"] >= 4
        and cat["architecture"]["capability_count"] >= 5
        and cat["ai_native"]["agent_count"] >= 5
        and cat["ai_native"]["via_enterprise_ai"] is True
        and cat["data_products"]["via_p212_f"] is True
        and cat["knowledge_graph"]["via_p212_j"] is True
        and cat["digital_twin"]["via_p212_l"] is True
        and cat["semantic_layer"]["via_p213_e"] is True
        and cat["cqrs"]["command_count"] >= 5
        and cat["cqrs"]["query_count"] >= 4
        and cat["events"]["core_event_count"] >= 5
        and cat["microservices"]["service_count"] >= 7
        and cat["deployment"]["cloud_native"] is True
        and cat["cursor_outputs"]["count"] >= 19
        and "lakehouse_architecture_is_incomplete"
        in cat["quality_gates"]["reject_if"]
        and "ai_data_foundation_is_missing"
        in cat["quality_gates"]["reject_if"]
        and "P213-E" in cat["builds_on"]
        and "P212-G" in cat["builds_on"]
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
            BiLakehouseProfileRoot.publish,
            tenant_id="t1",
            profile_ref="r1",
            complete=False,
        )
        and BiLakehouseProfileRoot.publish(
            tenant_id="t1", profile_ref="r2"
        ).is_incomplete()
        is False
    )
    checks.append(
        not _bad(
            BiAiDataFoundationRoot.enable,
            tenant_id="t1",
            foundation_ref="a1",
            present=False,
        )
        and BiAiDataFoundationRoot.enable(
            tenant_id="t1", foundation_ref="a2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            BiDataMeshAlignedRoot.align,
            tenant_id="t1",
            mesh_ref="m1",
            present=False,
        )
        and BiDataMeshAlignedRoot.align(
            tenant_id="t1", mesh_ref="m2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            BiStorageArchitectureRoot.publish,
            tenant_id="t1",
            storage_ref="s1",
            present=False,
        )
        and BiStorageArchitectureRoot.publish(
            tenant_id="t1", storage_ref="s2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            BiProcessingArchitectureRoot.enable,
            tenant_id="t1",
            processing_ref="p1",
            present=False,
        )
        and BiProcessingArchitectureRoot.enable(
            tenant_id="t1", processing_ref="p2"
        ).is_missing()
        is False
    )
    aggregates_ok = all(checks)

    acl_path = (
        root
        / "backend/contexts/analytics/infrastructure/acl/bi_lakehouse_acl.py"
    )
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_p207" in acl_text
        and "via_p208" in acl_text
        and "via_p209" in acl_text
        and "via_p211" in acl_text
        and "via_p212" in acl_text
        and "via_p212_f" in acl_text
        and "via_p212_g" in acl_text
        and "via_p212_j" in acl_text
        and "via_p212_k" in acl_text
        and "via_p212_l" in acl_text
        and "via_p213_e" in acl_text
        and "via_enterprise_ai" in acl_text
        and "module_local_llm_sdk_forbidden" in acl_text
    )

    router = (
        root / "backend/contexts/analytics/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@router.get("/lakehouse")' in router
        and "/lakehouse/readiness" in router
        and "/lakehouse/vision" in router
        and "/lakehouse/layers" in router
        and "/lakehouse/ai" in router
        and "/lakehouse/data-products" in router
    )

    law = (
        root
        / "docs/architecture/ENTERPRISE_BUSINESS_INTELLIGENCE_LAKEHOUSE.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never Enterprise lakehouse architecture is missing" in law
        and "Never Unified data platform is missing" in law
        and "Never Data warehouse integration is missing" in law
        and "Never Data lake capability is missing" in law
        and "Never AI data foundation is missing" in law
        and "Never Data mesh alignment is missing" in law
        and "Never Data governance alignment is missing" in law
        and "Never Knowledge graph integration is missing" in law
        and "Never Digital twin integration is missing" in law
        and "Never CQRS architecture is missing" in law
        and "Never Event driven architecture is missing" in law
        and "Never Microservice architecture is missing" in law
        and "Never API first architecture is missing" in law
        and "Never Cloud native deployment is missing" in law
        and "Never Lakehouse architecture is incomplete" in law
        and "Never Storage architecture is missing" in law
        and "Never Data processing architecture is missing" in law
        and "Never Semantic layer is missing" in law
        and "Never Sibling business intelligence BC" in law
        and "MEOS Enterprise Lakehouse Intelligence Fabric" in law
        and "analytics, AI, and decision intelligence converge" in law
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
        "prompt": "P213-F",
        "adr": 410,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "catalog": catalog_ok,
        "aggregates": aggregates_ok,
        "acl": acl_ok,
        "router": router_ok,
        "documentation": doc_ok,
        "sor": "analytics",
        "capability": "CAP-PLT-BI-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
