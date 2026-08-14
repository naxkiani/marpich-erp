"""Data Security P211-B Mission/Vision/Scope foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/377-enterprise-data-security-mission-vision-scope.md",
    "docs/architecture/ENTERPRISE_DATA_SECURITY_MISSION_VISION_SCOPE.md",
    "docs/architecture/data_security/DATA_SECURITY_MVS_CAPABILITIES.v1.yaml",
    "docs/architecture/data_security/DATA_SECURITY_MVS_DDD_CQRS.v1.yaml",
    "docs/architecture/data_security/DATA_SECURITY_MVS_SECURITY.v1.yaml",
    "docs/architecture/data_security/DATA_SECURITY_MVS_VALIDATION.v1.yaml",
    "backend/contexts/data_security/domain/services/ds_platform_mission_scope.py",
    "backend/contexts/data_security/domain/aggregates/ds_mission_aggregates.py",
    "backend/contexts/data_security/infrastructure/acl/ds_mission_acl.py",
    "backend/contexts/data_security/application/ds_mission_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/dspm",
    "backend/contexts/dspm_platform",
    "backend/contexts/privacy_intelligence",
    "backend/contexts/data_classification",
    "backend/contexts/data_protection_platform",
    "backend/contexts/data_lineage_platform",
)


def validate_ds_mission_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.data_security.domain.aggregates.ds_mission_aggregates import (
        DsGovernanceModelRoot,
        DsIntegrationBoundariesRoot,
        DsMissionCharterRoot,
        DsMissionScopeDefinedRoot,
        DsOwnershipModelRoot,
        DsPrivacyResponsibilitiesRoot,
        DsProtectionPrinciplesRoot,
        DsVisionCharterRoot,
    )
    from contexts.data_security.domain.services import (
        ds_platform_mission_scope as mscope,
    )

    cat = mscope.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P211-B"
        and cat.get("adr") == 377
        and cat.get("sor") == "data_security"
        and cat["data_security_scope_defined_required"] is True
        and cat["ownership_model_required"] is True
        and cat["privacy_responsibilities_clear_required"] is True
        and cat["data_protection_principles_present_required"] is True
        and cat["integration_boundaries_defined_required"] is True
        and cat["governance_model_complete_required"] is True
        and cat["enterprise_scope"]["not_undefined"] is True
        and cat["operating_model"]["not_missing"] is True
        and cat["governance"]["not_unclear"] is True
        and cat["principles"]["not_absent"] is True
        and cat["boundaries"]["not_undefined"] is True
        and cat["governance"]["not_incomplete"] is True
        and cat["strategic_objectives"]["count"] >= 6
        and cat["enterprise_scope"]["asset_type_count"] >= 20
        and cat["principles"]["count"] >= 7
        and cat["cursor_outputs"]["count"] >= 15
        and "data_security_scope_is_undefined" in cat["quality_gates"]["reject_if"]
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
            DsMissionScopeDefinedRoot.declare,
            tenant_id="t1",
            scope_ref="s1",
            defined=False,
        )
        and DsMissionScopeDefinedRoot.declare(
            tenant_id="t1", scope_ref="s2"
        ).is_undefined()
        is False
    )
    checks.append(
        not _bad(
            DsOwnershipModelRoot.register,
            tenant_id="t1",
            model_ref="o1",
            present=False,
        )
        and DsOwnershipModelRoot.register(
            tenant_id="t1", model_ref="o2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DsPrivacyResponsibilitiesRoot.clarify,
            tenant_id="t1",
            charter_ref="p1",
            clear=False,
        )
        and DsPrivacyResponsibilitiesRoot.clarify(
            tenant_id="t1", charter_ref="p2"
        ).is_unclear()
        is False
    )
    checks.append(
        not _bad(
            DsProtectionPrinciplesRoot.adopt,
            tenant_id="t1",
            set_ref="pr1",
            present=False,
        )
        and DsProtectionPrinciplesRoot.adopt(
            tenant_id="t1", set_ref="pr2"
        ).is_absent()
        is False
    )
    checks.append(
        not _bad(
            DsIntegrationBoundariesRoot.declare,
            tenant_id="t1",
            boundary_ref="b1",
            defined=False,
        )
        and DsIntegrationBoundariesRoot.declare(
            tenant_id="t1", boundary_ref="b2"
        ).is_undefined()
        is False
    )
    checks.append(
        not _bad(
            DsGovernanceModelRoot.complete,
            tenant_id="t1",
            model_ref="g1",
            complete=False,
        )
        and DsGovernanceModelRoot.complete(
            tenant_id="t1", model_ref="g2"
        ).is_incomplete()
        is False
    )
    mission = DsMissionCharterRoot.publish(tenant_id="t1", charter_ref="m1")
    vision = DsVisionCharterRoot.publish(tenant_id="t1", charter_ref="v1")
    checks.append("MissionPublished" in mission.pending_events)
    checks.append("VisionPublished" in vision.pending_events)
    aggregates_ok = all(checks)

    acl_path = (
        root / "backend/contexts/data_security/infrastructure/acl/ds_mission_acl.py"
    )
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "privacy_responsibilities_clear_required" in acl_text
        and "governance_model_complete_required" in acl_text
        and "via_consent" in acl_text
        and "via_p208" in acl_text
        and "via_p210" in acl_text
    )

    router = (
        root / "backend/contexts/data_security/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@data_security_router.get("/mission")' in router
        and "/mission/scope" in router
        and "/mission/principles" in router
        and "/mission/governance" in router
        and "/mission/readiness" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_DATA_SECURITY_MISSION_VISION_SCOPE.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never Data security scope is undefined" in law
        and "Never Ownership model is missing" in law
        and "Never Privacy responsibilities are unclear" in law
        and "Never Data protection principles are absent" in law
        and "Never Integration boundaries are undefined" in law
        and "Never Governance model is incomplete" in law
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
        "prompt": "P211-B",
        "adr": 377,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "catalog": catalog_ok,
        "aggregates": aggregates_ok,
        "acl": acl_ok,
        "router": router_ok,
        "documentation": doc_ok,
        "sor": "data_security",
        "capability": "CAP-PLT-DS-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
