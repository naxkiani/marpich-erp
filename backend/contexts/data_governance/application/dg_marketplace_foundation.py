"""Data Governance P212-G Data Marketplace foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/400-enterprise-data-governance-data-marketplace.md",
    "docs/architecture/ENTERPRISE_DATA_GOVERNANCE_DATA_MARKETPLACE.md",
    "docs/architecture/data_governance/DATA_GOVERNANCE_MARKETPLACE_CAPABILITIES.v1.yaml",
    "docs/architecture/data_governance/DATA_GOVERNANCE_MARKETPLACE_DDD_CQRS.v1.yaml",
    "docs/architecture/data_governance/DATA_GOVERNANCE_MARKETPLACE_SECURITY.v1.yaml",
    "docs/architecture/data_governance/DATA_GOVERNANCE_MARKETPLACE_VALIDATION.v1.yaml",
    "backend/contexts/data_governance/domain/services/dg_platform_marketplace.py",
    "backend/contexts/data_governance/domain/aggregates/dg_marketplace_aggregates.py",
    "backend/contexts/data_governance/infrastructure/acl/dg_marketplace_acl.py",
    "backend/contexts/data_governance/application/dg_marketplace_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/data_mesh",
    "backend/contexts/data_product_platform",
    "backend/contexts/data_marketplace",
    "backend/contexts/enterprise_intelligence",
    "backend/contexts/data_quality_platform",
    "backend/contexts/metadata_governance_platform",
)


def validate_dg_marketplace_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.data_governance.domain.aggregates.dg_marketplace_aggregates import (
        DgMarketplaceArchitectureRoot,
        DgMarketplaceCatalogRoot,
        DgMarketplaceDiscoveryRoot,
        DgMarketplaceConsumptionRoot,
        DgMarketplaceAccessGovernanceRoot,
        DgMarketplaceAiRecommendationRoot,
        DgMarketplaceMeshAlignmentRoot,
        DgMarketplaceKnowledgeGraphRoot,
        DgMarketplaceDigitalTwinRoot,
        DgMarketplaceCqrsRoot,
        DgMarketplaceEventSourcingRoot,
        DgMarketplaceMicroservicesRoot,
        DgMarketplaceZeroTrustRoot,
        DgMarketplaceScalabilityRoot,
    )
    from contexts.data_governance.domain.services import (
        dg_platform_marketplace as mkt,
    )

    cat = mkt.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P212-G"
        and cat.get("adr") == 400
        and cat.get("sor") == "data_governance"
        and cat.get("capability") == "CAP-PLT-DG-001"
        and cat["marketplace_architecture_complete_required"] is True
        and cat["data_catalog_architecture_present_required"] is True
        and cat["data_discovery_architecture_present_required"] is True
        and cat["data_product_consumption_model_present_required"] is True
        and cat["data_access_governance_present_required"] is True
        and cat["ai_recommendation_intelligence_present_required"] is True
        and cat["data_mesh_alignment_present_required"] is True
        and cat["knowledge_graph_integration_present_required"] is True
        and cat["digital_twin_integration_present_required"] is True
        and cat["cqrs_architecture_present_required"] is True
        and cat["event_sourcing_architecture_present_required"] is True
        and cat["microservices_architecture_present_required"] is True
        and cat["zero_trust_alignment_present_required"] is True
        and cat["enterprise_scalability_present_required"] is True
        and cat["marketplace_architecture"]["not_incomplete"] is True
        and cat["data_catalog"]["not_missing"] is True
        and cat["discovery"]["not_missing"] is True
        and cat["consumption"]["not_missing"] is True
        and cat["access_governance"]["not_missing"] is True
        and cat["ai_recommendation"]["not_missing"] is True
        and cat["mesh_alignment"]["not_missing"] is True
        and cat["knowledge_graph"]["not_missing"] is True
        and cat["digital_twin"]["not_missing"] is True
        and cat["cqrs"]["not_missing"] is True
        and cat["event_sourcing"]["not_missing"] is True
        and cat["microservices"]["not_missing"] is True
        and cat["zero_trust"]["not_missing"] is True
        and cat["scalability"]["not_missing"] is True
        and cat["marketplace_architecture"]["bc_count"] >= 6
        and cat["data_catalog"]["capability_count"] >= 4
        and cat["discovery"]["capability_count"] >= 5
        and cat["access_governance"]["step_count"] >= 7
        and cat["microservices"]["service_count"] >= 7
        and cat["cqrs"]["event_count"] >= 7
        and cat["cursor_outputs"]["count"] >= 18
        and (
            "enterprise_data_marketplace_architecture_is_incomplete"
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
            DgMarketplaceArchitectureRoot.publish,
            tenant_id="t1",
            architecture_ref="r0",
            complete=False,
        )
        and DgMarketplaceArchitectureRoot.publish(
            tenant_id="t1", architecture_ref="ok0"
        ).is_incomplete()
        is False
    )
    checks.append(
        not _bad(
            DgMarketplaceCatalogRoot.define,
            tenant_id="t1",
            catalog_ref="r1",
            present=False,
        )
        and DgMarketplaceCatalogRoot.define(
            tenant_id="t1", catalog_ref="ok1"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgMarketplaceDiscoveryRoot.enable,
            tenant_id="t1",
            discovery_ref="r2",
            present=False,
        )
        and DgMarketplaceDiscoveryRoot.enable(
            tenant_id="t1", discovery_ref="ok2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgMarketplaceConsumptionRoot.enable,
            tenant_id="t1",
            consumption_ref="r3",
            present=False,
        )
        and DgMarketplaceConsumptionRoot.enable(
            tenant_id="t1", consumption_ref="ok3"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgMarketplaceAccessGovernanceRoot.enable,
            tenant_id="t1",
            access_ref="r4",
            present=False,
        )
        and DgMarketplaceAccessGovernanceRoot.enable(
            tenant_id="t1", access_ref="ok4"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgMarketplaceAiRecommendationRoot.enable,
            tenant_id="t1",
            ai_ref="r5",
            present=False,
        )
        and DgMarketplaceAiRecommendationRoot.enable(
            tenant_id="t1", ai_ref="ok5"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgMarketplaceMeshAlignmentRoot.align,
            tenant_id="t1",
            mesh_ref="r6",
            present=False,
        )
        and DgMarketplaceMeshAlignmentRoot.align(
            tenant_id="t1", mesh_ref="ok6"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgMarketplaceKnowledgeGraphRoot.integrate,
            tenant_id="t1",
            graph_ref="r7",
            present=False,
        )
        and DgMarketplaceKnowledgeGraphRoot.integrate(
            tenant_id="t1", graph_ref="ok7"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgMarketplaceDigitalTwinRoot.integrate,
            tenant_id="t1",
            twin_ref="r8",
            present=False,
        )
        and DgMarketplaceDigitalTwinRoot.integrate(
            tenant_id="t1", twin_ref="ok8"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgMarketplaceCqrsRoot.align,
            tenant_id="t1",
            cqrs_ref="r9",
            present=False,
        )
        and DgMarketplaceCqrsRoot.align(
            tenant_id="t1", cqrs_ref="ok9"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgMarketplaceEventSourcingRoot.enable,
            tenant_id="t1",
            es_ref="r10",
            present=False,
        )
        and DgMarketplaceEventSourcingRoot.enable(
            tenant_id="t1", es_ref="ok10"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgMarketplaceMicroservicesRoot.declare,
            tenant_id="t1",
            ms_ref="r11",
            present=False,
        )
        and DgMarketplaceMicroservicesRoot.declare(
            tenant_id="t1", ms_ref="ok11"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgMarketplaceZeroTrustRoot.confirm,
            tenant_id="t1",
            zt_ref="r12",
            present=False,
        )
        and DgMarketplaceZeroTrustRoot.confirm(
            tenant_id="t1", zt_ref="ok12"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgMarketplaceScalabilityRoot.confirm,
            tenant_id="t1",
            scale_ref="r13",
            present=False,
        )
        and DgMarketplaceScalabilityRoot.confirm(
            tenant_id="t1", scale_ref="ok13"
        ).is_missing()
        is False
    )
    aggregates_ok = all(checks)

    acl_path = (
        root
        / "backend/contexts/data_governance/infrastructure/acl/dg_marketplace_acl.py"
    )
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_p212_d" in acl_text
        and "via_p212_e" in acl_text
        and "via_p212_f" in acl_text
        and "via_p207" in acl_text
        and "via_p208" in acl_text
        and "ai_recommendation_intelligence_present_required" in acl_text
        and "via_enterprise_search" in acl_text
        and "via_workflow" in acl_text
    )

    router = (
        root / "backend/contexts/data_governance/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@data_governance_router.get("/marketplace")' in router
        and "/marketplace/catalog" in router
        and "/marketplace/discovery" in router
        and "/marketplace/access-governance" in router
        and "/marketplace/readiness" in router
    )

    law = (
        root
        / "docs/architecture/ENTERPRISE_DATA_GOVERNANCE_DATA_MARKETPLACE.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never Enterprise data marketplace architecture is incomplete" in law
        and "Never Data catalog architecture is missing" in law
        and "Never Data discovery architecture is missing" in law
        and "Never Data product consumption model is missing" in law
        and "Never Data access governance is missing" in law
        and "Never AI recommendation intelligence is missing" in law
        and "Never Data mesh alignment is missing" in law
        and "Never Knowledge graph integration is missing" in law
        and "Never Digital twin integration is missing" in law
        and "Never CQRS architecture is missing" in law
        and "Never Event sourcing architecture is missing" in law
        and "Never Microservices architecture is missing" in law
        and "Never Zero trust security alignment is missing" in law
        and "Never Enterprise scalability is missing" in law
        and "Never Sibling data marketplace BC" in law
        and (
            "Enterprise data SHALL become discoverable, understandable,"
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
        "prompt": "P212-G",
        "adr": 400,
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
