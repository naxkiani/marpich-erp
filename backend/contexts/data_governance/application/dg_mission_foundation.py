"""Data Governance P212-B Mission/Vision/Scope foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/393-enterprise-data-governance-mission-vision-scope.md",
    "docs/architecture/ENTERPRISE_DATA_GOVERNANCE_MISSION_VISION_SCOPE.md",
    "docs/architecture/data_governance/DATA_GOVERNANCE_MVS_CAPABILITIES.v1.yaml",
    "docs/architecture/data_governance/DATA_GOVERNANCE_MVS_DDD_CQRS.v1.yaml",
    "docs/architecture/data_governance/DATA_GOVERNANCE_MVS_SECURITY.v1.yaml",
    "docs/architecture/data_governance/DATA_GOVERNANCE_MVS_VALIDATION.v1.yaml",
    "backend/contexts/data_governance/domain/services/dg_platform_mission_scope.py",
    "backend/contexts/data_governance/domain/aggregates/dg_mission_aggregates.py",
    "backend/contexts/data_governance/infrastructure/acl/dg_mission_acl.py",
    "backend/contexts/data_governance/application/dg_mission_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/data_mesh",
    "backend/contexts/data_product_platform",
    "backend/contexts/data_marketplace",
    "backend/contexts/enterprise_intelligence",
    "backend/contexts/data_quality_platform",
    "backend/contexts/metadata_governance_platform",
)


def validate_dg_mission_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.data_governance.domain.aggregates.dg_mission_aggregates import (
        DgAiGovernanceDirectionRoot,
        DgDomainBoundariesRoot,
        DgEnterpriseGovernanceStandardRoot,
        DgEnterpriseScopeDefinedRoot,
        DgMaturityModelRoot,
        DgMeosIntegrationAlignmentRoot,
        DgMissionDefinedRoot,
        DgOperatingModelRoot,
        DgStrategicObjectivesRoot,
        DgVisionDefinedRoot,
    )
    from contexts.data_governance.domain.services import (
        dg_platform_mission_scope as mscope,
    )

    cat = mscope.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P212-B"
        and cat.get("adr") == 393
        and cat.get("sor") == "data_governance"
        and cat["mission_defined_required"] is True
        and cat["vision_defined_required"] is True
        and cat["enterprise_scope_defined_required"] is True
        and cat["strategic_objectives_present_required"] is True
        and cat["operating_model_present_required"] is True
        and cat["maturity_model_present_required"] is True
        and cat["ai_governance_direction_present_required"] is True
        and cat["meos_integration_alignment_present_required"] is True
        and cat["domain_boundaries_clear_required"] is True
        and cat["enterprise_governance_standard_compliant_required"] is True
        and cat["mission"]["not_undefined"] is True
        and cat["vision"]["not_undefined"] is True
        and cat["enterprise_scope"]["not_undefined"] is True
        and cat["strategic_objectives"]["not_missing"] is True
        and cat["operating_model"]["not_missing"] is True
        and cat["maturity_model"]["not_missing"] is True
        and cat["ai_governance_direction"]["not_missing"] is True
        and cat["meos_alignment"]["not_missing"] is True
        and cat["domain_boundaries"]["not_unclear"] is True
        and cat["governance_standard"]["not_noncompliant"] is True
        and cat["strategic_objectives"]["count"] >= 6
        and cat["maturity_model"]["level_count"] >= 5
        and cat["cursor_outputs"]["count"] >= 15
        and "mission_is_undefined" in cat["quality_gates"]["reject_if"]
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
            DgMissionDefinedRoot.publish,
            tenant_id="t1",
            mission_ref="m1",
            defined=False,
        )
        and DgMissionDefinedRoot.publish(
            tenant_id="t1", mission_ref="m2"
        ).is_undefined()
        is False
    )
    checks.append(
        not _bad(
            DgVisionDefinedRoot.publish,
            tenant_id="t1",
            vision_ref="v1",
            defined=False,
        )
        and DgVisionDefinedRoot.publish(
            tenant_id="t1", vision_ref="v2"
        ).is_undefined()
        is False
    )
    checks.append(
        not _bad(
            DgEnterpriseScopeDefinedRoot.declare,
            tenant_id="t1",
            scope_ref="s1",
            defined=False,
        )
        and DgEnterpriseScopeDefinedRoot.declare(
            tenant_id="t1", scope_ref="s2"
        ).is_undefined()
        is False
    )
    checks.append(
        not _bad(
            DgStrategicObjectivesRoot.register,
            tenant_id="t1",
            objectives_ref="o1",
            present=False,
        )
        and DgStrategicObjectivesRoot.register(
            tenant_id="t1", objectives_ref="o2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgOperatingModelRoot.establish,
            tenant_id="t1",
            model_ref="om1",
            present=False,
        )
        and DgOperatingModelRoot.establish(
            tenant_id="t1", model_ref="om2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgMaturityModelRoot.publish,
            tenant_id="t1",
            maturity_ref="mat1",
            present=False,
        )
        and DgMaturityModelRoot.publish(
            tenant_id="t1", maturity_ref="mat2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgAiGovernanceDirectionRoot.establish,
            tenant_id="t1",
            ai_ref="ai1",
            present=False,
        )
        and DgAiGovernanceDirectionRoot.establish(
            tenant_id="t1", ai_ref="ai2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgMeosIntegrationAlignmentRoot.confirm,
            tenant_id="t1",
            alignment_ref="al1",
            present=False,
        )
        and DgMeosIntegrationAlignmentRoot.confirm(
            tenant_id="t1", alignment_ref="al2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgDomainBoundariesRoot.clarify,
            tenant_id="t1",
            boundary_ref="b1",
            clear=False,
        )
        and DgDomainBoundariesRoot.clarify(
            tenant_id="t1", boundary_ref="b2"
        ).is_unclear()
        is False
    )
    checks.append(
        not _bad(
            DgEnterpriseGovernanceStandardRoot.certify,
            tenant_id="t1",
            standard_ref="eg1",
            compliant=False,
        )
        and DgEnterpriseGovernanceStandardRoot.certify(
            tenant_id="t1", standard_ref="eg2"
        ).is_noncompliant()
        is False
    )
    aggregates_ok = all(checks)

    acl_path = (
        root
        / "backend/contexts/data_governance/infrastructure/acl/dg_mission_acl.py"
    )
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_p211" in acl_text
        and "via_p207" in acl_text
        and "via_p208" in acl_text
        and "encryption_out_of_scope" in acl_text
        and "ai_governance_direction_present_required" in acl_text
    )

    router = (
        root / "backend/contexts/data_governance/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@data_governance_router.get("/mission")' in router
        and "/mission/vision" in router
        and "/mission/scope" in router
        and "/mission/maturity" in router
        and "/mission/readiness" in router
    )

    law = (
        root
        / "docs/architecture/ENTERPRISE_DATA_GOVERNANCE_MISSION_VISION_SCOPE.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never Mission is undefined" in law
        and "Never Vision is undefined" in law
        and "Never Enterprise scope is undefined" in law
        and "Never Strategic objectives are missing" in law
        and "Never Operating model is missing" in law
        and "Never Maturity model is missing" in law
        and "Never AI governance direction is missing" in law
        and "Never MEOS integration alignment is missing" in law
        and "Never Domain boundaries are unclear" in law
        and "Never Enterprise Governance Standard is noncompliant" in law
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
        "prompt": "P212-B",
        "adr": 393,
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
