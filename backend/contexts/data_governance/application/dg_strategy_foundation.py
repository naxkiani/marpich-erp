"""Data Governance P212-A Strategy foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/392-enterprise-data-governance-strategy.md",
    "docs/architecture/ENTERPRISE_DATA_GOVERNANCE_STRATEGY.md",
    "docs/architecture/data_governance/DATA_GOVERNANCE_STRATEGY_CAPABILITIES.v1.yaml",
    "docs/architecture/data_governance/DATA_GOVERNANCE_STRATEGY_DDD_CQRS.v1.yaml",
    "docs/architecture/data_governance/DATA_GOVERNANCE_STRATEGY_SECURITY.v1.yaml",
    "docs/architecture/data_governance/DATA_GOVERNANCE_STRATEGY_VALIDATION.v1.yaml",
    "docs/architecture/data_governance/P212_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/data_governance/domain/services/dg_platform_strategy.py",
    "backend/contexts/data_governance/domain/aggregates/dg_strategy_aggregates.py",
    "backend/contexts/data_governance/infrastructure/acl/dg_strategy_acl.py",
    "backend/contexts/data_governance/application/dg_strategy_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/data_mesh",
    "backend/contexts/data_product_platform",
    "backend/contexts/data_marketplace",
    "backend/contexts/enterprise_intelligence",
    "backend/contexts/data_quality_platform",
    "backend/contexts/metadata_governance_platform",
)


def validate_dg_strategy_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.data_governance.domain.aggregates.dg_strategy_aggregates import (
        DgAiNativeGovernanceRoot,
        DgCloudNativeDeploymentRoot,
        DgCompleteGovernanceArchitectureRoot,
        DgCqrsArchitectureRoot,
        DgDataMeshNativeRoot,
        DgDddDomainModelRoot,
        DgDigitalTwinIntegrationRoot,
        DgEnterpriseScalabilityRoot,
        DgEventDrivenArchitectureRoot,
        DgKnowledgeGraphIntegrationRoot,
        DgMicroservicesArchitectureRoot,
        DgPrivacyByDesignRoot,
        DgStrategyProfileRoot,
        DgZeroTrustAlignmentRoot,
    )
    from contexts.data_governance.domain.services import (
        dg_platform_strategy as strat,
    )

    cat = strat.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P212-A"
        and cat.get("adr") == 392
        and cat.get("sor") == "data_governance"
        and cat.get("capability") == "CAP-PLT-DG-001"
        and cat["governance_architecture_complete_required"] is True
        and cat["ddd_domain_model_present_required"] is True
        and cat["cqrs_architecture_present_required"] is True
        and cat["event_driven_architecture_present_required"] is True
        and cat["microservices_architecture_present_required"] is True
        and cat["data_mesh_native_required"] is True
        and cat["knowledge_graph_integration_present_required"] is True
        and cat["digital_twin_integration_present_required"] is True
        and cat["ai_native_governance_present_required"] is True
        and cat["zero_trust_alignment_present_required"] is True
        and cat["privacy_by_design_present_required"] is True
        and cat["cloud_native_deployment_present_required"] is True
        and cat["enterprise_scalability_present_required"] is True
        and cat["architecture"]["layer_count"] >= 6
        and cat["domains"]["supporting_count"] >= 8
        and cat["microservices"]["service_count"] >= 11
        and cat["cqrs"]["event_count"] >= 8
        and cat["cursor_outputs"]["count"] >= 16
        and "enterprise_data_governance_architecture_is_incomplete"
        in cat["quality_gates"]["reject_if"]
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
            DgCompleteGovernanceArchitectureRoot.establish,
            tenant_id="t1",
            architecture_ref="a1",
            complete=False,
        )
        and DgCompleteGovernanceArchitectureRoot.establish(
            tenant_id="t1", architecture_ref="a2"
        ).is_incomplete()
        is False
    )
    checks.append(
        not _bad(
            DgDddDomainModelRoot.define,
            tenant_id="t1",
            model_ref="m1",
            present=False,
        )
        and DgDddDomainModelRoot.define(
            tenant_id="t1", model_ref="m2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgCqrsArchitectureRoot.define,
            tenant_id="t1",
            cqrs_ref="c1",
            present=False,
        )
        and DgCqrsArchitectureRoot.define(
            tenant_id="t1", cqrs_ref="c2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgEventDrivenArchitectureRoot.define,
            tenant_id="t1",
            events_ref="e1",
            present=False,
        )
        and DgEventDrivenArchitectureRoot.define(
            tenant_id="t1", events_ref="e2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgMicroservicesArchitectureRoot.define,
            tenant_id="t1",
            services_ref="s1",
            present=False,
        )
        and DgMicroservicesArchitectureRoot.define(
            tenant_id="t1", services_ref="s2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgDataMeshNativeRoot.enable,
            tenant_id="t1",
            mesh_ref="mesh1",
            native=False,
        )
        and DgDataMeshNativeRoot.enable(
            tenant_id="t1", mesh_ref="mesh2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgKnowledgeGraphIntegrationRoot.integrate,
            tenant_id="t1",
            graph_ref="g1",
            present=False,
        )
        and DgKnowledgeGraphIntegrationRoot.integrate(
            tenant_id="t1", graph_ref="g2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgDigitalTwinIntegrationRoot.integrate,
            tenant_id="t1",
            twin_ref="tw1",
            present=False,
        )
        and DgDigitalTwinIntegrationRoot.integrate(
            tenant_id="t1", twin_ref="tw2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgAiNativeGovernanceRoot.establish,
            tenant_id="t1",
            ai_ref="ai1",
            present=False,
        )
        and DgAiNativeGovernanceRoot.establish(
            tenant_id="t1", ai_ref="ai2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgZeroTrustAlignmentRoot.align,
            tenant_id="t1",
            zt_ref="zt1",
            present=False,
        )
        and DgZeroTrustAlignmentRoot.align(
            tenant_id="t1", zt_ref="zt2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgPrivacyByDesignRoot.apply,
            tenant_id="t1",
            privacy_ref="p1",
            present=False,
        )
        and DgPrivacyByDesignRoot.apply(
            tenant_id="t1", privacy_ref="p2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgCloudNativeDeploymentRoot.enable,
            tenant_id="t1",
            deploy_ref="d1",
            present=False,
        )
        and DgCloudNativeDeploymentRoot.enable(
            tenant_id="t1", deploy_ref="d2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgEnterpriseScalabilityRoot.enable,
            tenant_id="t1",
            scale_ref="sc1",
            present=False,
        )
        and DgEnterpriseScalabilityRoot.enable(
            tenant_id="t1", scale_ref="sc2"
        ).is_missing()
        is False
    )
    published = DgStrategyProfileRoot.publish(
        tenant_id="t1", strategy_ref="st1"
    )
    checks.append(
        "DataGovernanceStrategyPublished" in published.pending_events
    )
    aggregates_ok = all(checks)

    acl_path = (
        root
        / "backend/contexts/data_governance/infrastructure/acl/dg_strategy_acl.py"
    )
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_data_security_p211" in acl_text
        and "via_p208" in acl_text
        and "via_p209" in acl_text
        and "via_p210" in acl_text
        and "via_enterprise_ai" in acl_text
        and "module_local_llm_sdk_forbidden" in acl_text
    )

    router = (
        root / "backend/contexts/data_governance/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@data_governance_router.get("/strategy")' in router
        and "/strategy/data-mesh" in router
        and "/strategy/knowledge-graph" in router
        and "/strategy/ai-governance" in router
        and "/strategy/readiness" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_DATA_GOVERNANCE_STRATEGY.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never Enterprise Data Governance architecture is incomplete" in law
        and "Never DDD domain model is missing" in law
        and "Never CQRS architecture is missing" in law
        and "Never Event-driven architecture is missing" in law
        and "Never Microservices architecture is missing" in law
        and "Never Data Mesh native architecture is missing" in law
        and "Never Knowledge Graph integration is missing" in law
        and "Never Digital Twin integration is missing" in law
        and "Never AI native governance is missing" in law
        and "Never Zero Trust alignment is missing" in law
        and "Never Privacy by Design is missing" in law
        and "Never Cloud native deployment is missing" in law
        and "Never Enterprise scalability is missing" in law
    )

    registry = (root / "backend/contexts/registry.py").read_text(encoding="utf-8")
    registry_ok = (
        'id="data_governance"' in registry and "DATA_GOVERNANCE" in registry
    )

    startup = (
        root / "backend/core/presentation/api/startup_registry.py"
    ).read_text(encoding="utf-8")
    startup_ok = "contexts.data_governance.presentation.router" in startup

    passed = (
        not missing
        and not sibling
        and catalog_ok
        and aggregates_ok
        and acl_ok
        and router_ok
        and doc_ok
        and registry_ok
        and startup_ok
    )
    return {
        "prompt": "P212-A",
        "adr": 392,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "catalog": catalog_ok,
        "aggregates": aggregates_ok,
        "acl": acl_ok,
        "router": router_ok,
        "documentation": doc_ok,
        "registry": registry_ok,
        "startup": startup_ok,
        "sor": "data_governance",
        "capability": "CAP-PLT-DG-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
