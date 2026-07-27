"""Data Governance P212-D Ownership/Stewardship foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/397-enterprise-data-governance-ownership-stewardship.md",
    "docs/architecture/ENTERPRISE_DATA_GOVERNANCE_OWNERSHIP_STEWARDSHIP.md",
    "docs/architecture/data_governance/DATA_GOVERNANCE_OWNERSHIP_CAPABILITIES.v1.yaml",
    "docs/architecture/data_governance/DATA_GOVERNANCE_OWNERSHIP_DDD_CQRS.v1.yaml",
    "docs/architecture/data_governance/DATA_GOVERNANCE_OWNERSHIP_SECURITY.v1.yaml",
    "docs/architecture/data_governance/DATA_GOVERNANCE_OWNERSHIP_VALIDATION.v1.yaml",
    "backend/contexts/data_governance/domain/services/dg_platform_ownership.py",
    "backend/contexts/data_governance/domain/aggregates/dg_ownership_aggregates.py",
    "backend/contexts/data_governance/infrastructure/acl/dg_ownership_acl.py",
    "backend/contexts/data_governance/application/dg_ownership_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/data_ownership",
    "backend/contexts/data_stewardship",
    "backend/contexts/accountability_platform",
    "backend/contexts/ownership_registry",
    "backend/contexts/data_mesh",
    "backend/contexts/data_product_platform",
    "backend/contexts/data_marketplace",
    "backend/contexts/enterprise_intelligence",
    "backend/contexts/data_quality_platform",
    "backend/contexts/metadata_governance_platform",
)


def validate_dg_ownership_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.data_governance.domain.aggregates.dg_ownership_aggregates import (
        DgAccountabilityFrameworkRoot,
        DgOwnershipAiIntelligenceRoot,
        DgOwnershipArchitectureRoot,
        DgOwnershipCqrsRoot,
        DgOwnershipDataMeshRoot,
        DgOwnershipDddModelRoot,
        DgOwnershipDigitalTwinRoot,
        DgOwnershipEventSourcingRoot,
        DgOwnershipKnowledgeGraphRoot,
        DgOwnershipScalabilityRoot,
        DgOwnershipZeroTrustRoot,
        DgStewardshipArchitectureRoot,
    )
    from contexts.data_governance.domain.services import (
        dg_platform_ownership as own,
    )

    cat = own.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P212-D"
        and cat.get("adr") == 397
        and cat.get("sor") == "data_governance"
        and cat.get("capability") == "CAP-PLT-DG-001"
        and cat["ownership_architecture_complete_required"] is True
        and cat["stewardship_architecture_complete_required"] is True
        and cat["accountability_framework_present_required"] is True
        and cat["ddd_domain_model_present_required"] is True
        and cat["cqrs_design_present_required"] is True
        and cat["event_sourcing_design_present_required"] is True
        and cat["data_mesh_alignment_present_required"] is True
        and cat["knowledge_graph_integration_present_required"] is True
        and cat["digital_twin_integration_present_required"] is True
        and cat["ai_ownership_intelligence_present_required"] is True
        and cat["zero_trust_alignment_present_required"] is True
        and cat["enterprise_scalability_present_required"] is True
        and cat["ownership_architecture"]["not_incomplete"] is True
        and cat["stewardship_architecture"]["not_incomplete"] is True
        and cat["accountability_framework"]["not_missing"] is True
        and cat["ddd_model"]["not_missing"] is True
        and cat["cqrs"]["not_missing"] is True
        and cat["event_sourcing"]["not_missing"] is True
        and cat["data_mesh"]["not_missing"] is True
        and cat["knowledge_graph"]["not_missing"] is True
        and cat["digital_twin"]["not_missing"] is True
        and cat["ai_intelligence"]["not_missing"] is True
        and cat["zero_trust"]["not_missing"] is True
        and cat["scalability"]["not_missing"] is True
        and cat["accountability_framework"]["dimension_count"] >= 4
        and cat["microservices"]["service_count"] >= 5
        and cat["cqrs"]["event_count"] >= 10
        and cat["cursor_outputs"]["count"] >= 18
        and (
            "data_ownership_architecture_is_incomplete"
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
            DgOwnershipArchitectureRoot.publish,
            tenant_id="t1",
            architecture_ref="a1",
            complete=False,
        )
        and DgOwnershipArchitectureRoot.publish(
            tenant_id="t1", architecture_ref="a2"
        ).is_incomplete()
        is False
    )
    checks.append(
        not _bad(
            DgStewardshipArchitectureRoot.publish,
            tenant_id="t1",
            architecture_ref="s1",
            complete=False,
        )
        and DgStewardshipArchitectureRoot.publish(
            tenant_id="t1", architecture_ref="s2"
        ).is_incomplete()
        is False
    )
    checks.append(
        not _bad(
            DgAccountabilityFrameworkRoot.establish,
            tenant_id="t1",
            framework_ref="f1",
            present=False,
        )
        and DgAccountabilityFrameworkRoot.establish(
            tenant_id="t1", framework_ref="f2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgOwnershipDddModelRoot.define,
            tenant_id="t1",
            model_ref="d1",
            present=False,
        )
        and DgOwnershipDddModelRoot.define(
            tenant_id="t1", model_ref="d2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgOwnershipCqrsRoot.align,
            tenant_id="t1",
            cqrs_ref="c1",
            present=False,
        )
        and DgOwnershipCqrsRoot.align(
            tenant_id="t1", cqrs_ref="c2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgOwnershipEventSourcingRoot.enable,
            tenant_id="t1",
            es_ref="e1",
            present=False,
        )
        and DgOwnershipEventSourcingRoot.enable(
            tenant_id="t1", es_ref="e2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgOwnershipDataMeshRoot.align,
            tenant_id="t1",
            mesh_ref="m1",
            present=False,
        )
        and DgOwnershipDataMeshRoot.align(
            tenant_id="t1", mesh_ref="m2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgOwnershipKnowledgeGraphRoot.integrate,
            tenant_id="t1",
            graph_ref="g1",
            present=False,
        )
        and DgOwnershipKnowledgeGraphRoot.integrate(
            tenant_id="t1", graph_ref="g2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgOwnershipDigitalTwinRoot.integrate,
            tenant_id="t1",
            twin_ref="tw1",
            present=False,
        )
        and DgOwnershipDigitalTwinRoot.integrate(
            tenant_id="t1", twin_ref="tw2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgOwnershipAiIntelligenceRoot.enable,
            tenant_id="t1",
            ai_ref="ai1",
            present=False,
        )
        and DgOwnershipAiIntelligenceRoot.enable(
            tenant_id="t1", ai_ref="ai2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgOwnershipZeroTrustRoot.align,
            tenant_id="t1",
            zt_ref="z1",
            present=False,
        )
        and DgOwnershipZeroTrustRoot.align(
            tenant_id="t1", zt_ref="z2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgOwnershipScalabilityRoot.confirm,
            tenant_id="t1",
            scale_ref="sc1",
            present=False,
        )
        and DgOwnershipScalabilityRoot.confirm(
            tenant_id="t1", scale_ref="sc2"
        ).is_missing()
        is False
    )
    aggregates_ok = all(checks)

    acl_path = (
        root
        / "backend/contexts/data_governance/infrastructure/acl/dg_ownership_acl.py"
    )
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_p207" in acl_text
        and "via_p208" in acl_text
        and "via_p211" in acl_text
        and "ai_ownership_intelligence_present_required" in acl_text
        and "zero_trust_alignment_present_required" in acl_text
    )

    router = (
        root / "backend/contexts/data_governance/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@data_governance_router.get("/ownership")' in router
        and "/ownership/stewards" in router
        and "/ownership/accountability" in router
        and "/ownership/intelligence" in router
        and "/ownership/readiness" in router
    )

    law = (
        root
        / "docs/architecture/ENTERPRISE_DATA_GOVERNANCE_OWNERSHIP_STEWARDSHIP.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never Data ownership architecture is incomplete" in law
        and "Never Data stewardship architecture is incomplete" in law
        and "Never Accountability framework is missing" in law
        and "Never DDD domain model is missing" in law
        and "Never CQRS design is missing" in law
        and "Never Event sourcing design is missing" in law
        and "Never Data mesh alignment is missing" in law
        and "Never Knowledge graph integration is missing" in law
        and "Never Digital twin integration is missing" in law
        and "Never AI ownership intelligence is missing" in law
        and "Never Zero trust security alignment is missing" in law
        and "Never Enterprise scalability is missing" in law
        and "Never Sibling ownership stewardship BC" in law
        and "Every enterprise data asset SHALL have a clear accountable owner"
        in law
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
        "prompt": "P212-D",
        "adr": 397,
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
