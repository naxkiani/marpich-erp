"""Data Governance P212-E Data Quality Intelligence foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/398-enterprise-data-governance-quality-intelligence.md",
    "docs/architecture/ENTERPRISE_DATA_GOVERNANCE_QUALITY_INTELLIGENCE.md",
    "docs/architecture/data_governance/DATA_GOVERNANCE_QUALITY_CAPABILITIES.v1.yaml",
    "docs/architecture/data_governance/DATA_GOVERNANCE_QUALITY_DDD_CQRS.v1.yaml",
    "docs/architecture/data_governance/DATA_GOVERNANCE_QUALITY_SECURITY.v1.yaml",
    "docs/architecture/data_governance/DATA_GOVERNANCE_QUALITY_VALIDATION.v1.yaml",
    "backend/contexts/data_governance/domain/services/dg_platform_quality.py",
    "backend/contexts/data_governance/domain/aggregates/dg_quality_aggregates.py",
    "backend/contexts/data_governance/infrastructure/acl/dg_quality_acl.py",
    "backend/contexts/data_governance/application/dg_quality_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/data_quality_platform",
    "backend/contexts/quality_rule_engine",
    "backend/contexts/quality_monitoring_platform",
    "backend/contexts/quality_remediation_platform",
    "backend/contexts/data_mesh",
    "backend/contexts/data_product_platform",
    "backend/contexts/data_marketplace",
    "backend/contexts/enterprise_intelligence",
    "backend/contexts/metadata_governance_platform",
)


def validate_dg_quality_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.data_governance.domain.aggregates.dg_quality_aggregates import (
        DgQualityAiIntelligenceRoot,
        DgQualityArchitectureRoot,
        DgQualityCqrsRoot,
        DgQualityDataMeshRoot,
        DgQualityDddModelRoot,
        DgQualityDigitalTwinRoot,
        DgQualityEventSourcingRoot,
        DgQualityKnowledgeGraphRoot,
        DgQualityMeasurementRoot,
        DgQualityMicroservicesRoot,
        DgQualityRuleArchitectureRoot,
        DgQualityScalabilityRoot,
    )
    from contexts.data_governance.domain.services import (
        dg_platform_quality as qual,
    )

    cat = qual.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P212-E"
        and cat.get("adr") == 398
        and cat.get("sor") == "data_governance"
        and cat.get("capability") == "CAP-PLT-DG-001"
        and cat["quality_intelligence_architecture_complete_required"] is True
        and cat["ddd_domain_model_present_required"] is True
        and cat["quality_rule_architecture_present_required"] is True
        and cat["quality_measurement_architecture_present_required"] is True
        and cat["ai_quality_intelligence_present_required"] is True
        and cat["data_mesh_alignment_present_required"] is True
        and cat["knowledge_graph_integration_present_required"] is True
        and cat["digital_twin_integration_present_required"] is True
        and cat["cqrs_architecture_present_required"] is True
        and cat["event_sourcing_architecture_present_required"] is True
        and cat["microservices_architecture_present_required"] is True
        and cat["enterprise_scalability_present_required"] is True
        and cat["quality_architecture"]["not_incomplete"] is True
        and cat["ddd_model"]["not_missing"] is True
        and cat["rule_architecture"]["not_missing"] is True
        and cat["measurement_architecture"]["not_missing"] is True
        and cat["ai_intelligence"]["not_missing"] is True
        and cat["data_mesh"]["not_missing"] is True
        and cat["knowledge_graph"]["not_missing"] is True
        and cat["digital_twin"]["not_missing"] is True
        and cat["cqrs"]["not_missing"] is True
        and cat["event_sourcing"]["not_missing"] is True
        and cat["microservices"]["not_missing"] is True
        and cat["scalability"]["not_missing"] is True
        and cat["quality_dimensions"]["dimension_count"] >= 8
        and cat["ddd_model"]["context_count"] >= 5
        and cat["microservices"]["service_count"] >= 6
        and cat["cqrs"]["event_count"] >= 9
        and cat["cursor_outputs"]["count"] >= 18
        and (
            "data_quality_intelligence_architecture_is_incomplete"
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
            DgQualityArchitectureRoot.publish,
            tenant_id="t1",
            architecture_ref="a1",
            complete=False,
        )
        and DgQualityArchitectureRoot.publish(
            tenant_id="t1", architecture_ref="a2"
        ).is_incomplete()
        is False
    )
    checks.append(
        not _bad(
            DgQualityDddModelRoot.define,
            tenant_id="t1",
            model_ref="d1",
            present=False,
        )
        and DgQualityDddModelRoot.define(
            tenant_id="t1", model_ref="d2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgQualityRuleArchitectureRoot.publish,
            tenant_id="t1",
            rule_ref="r1",
            present=False,
        )
        and DgQualityRuleArchitectureRoot.publish(
            tenant_id="t1", rule_ref="r2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgQualityMeasurementRoot.enable,
            tenant_id="t1",
            measure_ref="m1",
            present=False,
        )
        and DgQualityMeasurementRoot.enable(
            tenant_id="t1", measure_ref="m2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgQualityAiIntelligenceRoot.enable,
            tenant_id="t1",
            ai_ref="ai1",
            present=False,
        )
        and DgQualityAiIntelligenceRoot.enable(
            tenant_id="t1", ai_ref="ai2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgQualityDataMeshRoot.align,
            tenant_id="t1",
            mesh_ref="dm1",
            present=False,
        )
        and DgQualityDataMeshRoot.align(
            tenant_id="t1", mesh_ref="dm2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgQualityKnowledgeGraphRoot.integrate,
            tenant_id="t1",
            graph_ref="g1",
            present=False,
        )
        and DgQualityKnowledgeGraphRoot.integrate(
            tenant_id="t1", graph_ref="g2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgQualityDigitalTwinRoot.integrate,
            tenant_id="t1",
            twin_ref="tw1",
            present=False,
        )
        and DgQualityDigitalTwinRoot.integrate(
            tenant_id="t1", twin_ref="tw2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgQualityCqrsRoot.align,
            tenant_id="t1",
            cqrs_ref="c1",
            present=False,
        )
        and DgQualityCqrsRoot.align(
            tenant_id="t1", cqrs_ref="c2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgQualityEventSourcingRoot.enable,
            tenant_id="t1",
            es_ref="e1",
            present=False,
        )
        and DgQualityEventSourcingRoot.enable(
            tenant_id="t1", es_ref="e2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgQualityMicroservicesRoot.declare,
            tenant_id="t1",
            ms_ref="ms1",
            present=False,
        )
        and DgQualityMicroservicesRoot.declare(
            tenant_id="t1", ms_ref="ms2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgQualityScalabilityRoot.confirm,
            tenant_id="t1",
            scale_ref="sc1",
            present=False,
        )
        and DgQualityScalabilityRoot.confirm(
            tenant_id="t1", scale_ref="sc2"
        ).is_missing()
        is False
    )
    aggregates_ok = all(checks)

    acl_path = (
        root
        / "backend/contexts/data_governance/infrastructure/acl/dg_quality_acl.py"
    )
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_p212_d" in acl_text
        and "via_p211" in acl_text
        and "via_p207" in acl_text
        and "ai_quality_intelligence_present_required" in acl_text
    )

    router = (
        root / "backend/contexts/data_governance/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@data_governance_router.get("/quality")' in router
        and "/quality/rules" in router
        and "/quality/intelligence" in router
        and "/quality/dimensions" in router
        and "/quality/readiness" in router
    )

    law = (
        root
        / "docs/architecture/ENTERPRISE_DATA_GOVERNANCE_QUALITY_INTELLIGENCE.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never Data quality intelligence architecture is incomplete" in law
        and "Never DDD domain model is missing" in law
        and "Never Quality rule architecture is missing" in law
        and "Never Quality measurement architecture is missing" in law
        and "Never AI quality intelligence is missing" in law
        and "Never Data mesh alignment is missing" in law
        and "Never Knowledge graph integration is missing" in law
        and "Never Digital twin integration is missing" in law
        and "Never CQRS architecture is missing" in law
        and "Never Event sourcing architecture is missing" in law
        and "Never Microservices architecture is missing" in law
        and "Never Enterprise scalability is missing" in law
        and "Never Sibling data quality BC" in law
        and "Trusted intelligence requires trusted data" in law
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
        "prompt": "P212-E",
        "adr": 398,
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
