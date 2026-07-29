"""Data Security P211-H Access governance foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/383-enterprise-data-security-access-governance.md",
    "docs/architecture/ENTERPRISE_DATA_SECURITY_ACCESS_GOVERNANCE.md",
    "docs/architecture/data_security/DATA_SECURITY_ACCESS_CAPABILITIES.v1.yaml",
    "docs/architecture/data_security/DATA_SECURITY_ACCESS_DDD_CQRS.v1.yaml",
    "docs/architecture/data_security/DATA_SECURITY_ACCESS_SECURITY.v1.yaml",
    "docs/architecture/data_security/DATA_SECURITY_ACCESS_VALIDATION.v1.yaml",
    "backend/contexts/data_security/domain/services/ds_platform_access.py",
    "backend/contexts/data_security/domain/aggregates/ds_access_aggregates.py",
    "backend/contexts/data_security/infrastructure/acl/ds_access_acl.py",
    "backend/contexts/data_security/application/ds_access_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/data_access_governance",
    "backend/contexts/entitlement_management",
    "backend/contexts/access_certification",
)


def validate_ds_access_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.data_security.domain.aggregates.ds_access_aggregates import (
        DsAccessRequestRoot,
        DsAuditableDecisionRoot,
        DsAutomatedReviewRoot,
        DsDefinedOwnershipRoot,
        DsLeastPrivilegeRoot,
        DsManagedAiAccessRoot,
        DsRiskEvaluationRoot,
        DsVisiblePermissionsRoot,
    )
    from contexts.data_security.domain.services import (
        ds_platform_access as access,
    )

    cat = access.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P211-H"
        and cat.get("adr") == 383
        and cat.get("sor") == "data_security"
        and cat["permissions_visible_required"] is True
        and cat["ownership_defined_required"] is True
        and cat["access_reviews_not_manual_only_required"] is True
        and cat["risk_evaluation_present_required"] is True
        and cat["ai_access_managed_required"] is True
        and cat["least_privilege_enforceable_required"] is True
        and cat["authorization_decisions_auditable_required"] is True
        and cat["entitlements"]["not_invisible"] is True
        and cat["ownership"]["not_undefined"] is True
        and cat["certification"]["not_manual_only"] is True
        and cat["risk_intelligence"]["not_missing"] is True
        and cat["ai_access"]["not_unmanaged"] is True
        and cat["least_privilege"]["not_unenforceable"] is True
        and cat["auditability"]["not_unauditable"] is True
        and cat["architecture"]["layer_count"] >= 7
        and cat["entitlements"]["scope_count"] >= 8
        and cat["cqrs"]["event_count"] >= 7
        and cat["cursor_outputs"]["count"] >= 17
        and "data_permissions_are_invisible"
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
            DsVisiblePermissionsRoot.discover,
            tenant_id="t1",
            permission_ref="p1",
            visible=False,
        )
        and DsVisiblePermissionsRoot.discover(
            tenant_id="t1", permission_ref="p2"
        ).is_invisible()
        is False
    )
    checks.append(
        not _bad(
            DsDefinedOwnershipRoot.assign,
            tenant_id="t1",
            owner_ref="",
            defined=False,
        )
        and DsDefinedOwnershipRoot.assign(
            tenant_id="t1", owner_ref="o1"
        ).is_undefined()
        is False
    )
    checks.append(
        not _bad(
            DsAutomatedReviewRoot.review,
            tenant_id="t1",
            review_ref="r1",
            automated_path=False,
        )
        and DsAutomatedReviewRoot.review(
            tenant_id="t1", review_ref="r2"
        ).is_manual_only()
        is False
    )
    checks.append(
        not _bad(
            DsRiskEvaluationRoot.evaluate,
            tenant_id="t1",
            risk_ref="risk1",
            present=False,
        )
        and DsRiskEvaluationRoot.evaluate(
            tenant_id="t1", risk_ref="risk2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DsManagedAiAccessRoot.govern,
            tenant_id="t1",
            agent_ref="a1",
            managed=False,
        )
        and DsManagedAiAccessRoot.govern(
            tenant_id="t1", agent_ref="a2"
        ).is_unmanaged()
        is False
    )
    checks.append(
        not _bad(
            DsLeastPrivilegeRoot.enforce,
            tenant_id="t1",
            entitlement_ref="e1",
            enforceable=False,
        )
        and DsLeastPrivilegeRoot.enforce(
            tenant_id="t1", entitlement_ref="e2"
        ).is_unenforceable()
        is False
    )
    checks.append(
        not _bad(
            DsAuditableDecisionRoot.decide,
            tenant_id="t1",
            decision_ref="d1",
            auditable=False,
        )
        and DsAuditableDecisionRoot.decide(
            tenant_id="t1", decision_ref="d2"
        ).is_unauditable()
        is False
    )
    req = DsAccessRequestRoot.request(tenant_id="t1", request_ref="req1")
    checks.append("AccessRequested" in req.pending_events)
    aggregates_ok = all(checks)

    acl_path = (
        root
        / "backend/contexts/data_security/infrastructure/acl/ds_access_acl.py"
    )
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_p208" in acl_text
        and "module_local_pdp_forbidden" in acl_text
        and "ai_access_managed_required" in acl_text
        and "access_reviews_not_manual_only_required" in acl_text
        and "least_privilege_enforceable_required" in acl_text
        and "via_p211_g_dlp" in acl_text
    )

    router = (
        root / "backend/contexts/data_security/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@data_security_router.get("/access")' in router
        and "/access/entitlements" in router
        and "/access/zero-trust" in router
        and "/access/certification" in router
        and "/access/readiness" in router
    )

    law = (
        root
        / "docs/architecture/ENTERPRISE_DATA_SECURITY_ACCESS_GOVERNANCE.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never Data permissions are invisible" in law
        and "Never Ownership is undefined" in law
        and "Never Access reviews are manual only" in law
        and "Never Risk evaluation is missing" in law
        and "Never AI access is unmanaged" in law
        and "Never Least privilege cannot be enforced" in law
        and "Never Authorization decisions are not auditable" in law
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
        "prompt": "P211-H",
        "adr": 383,
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
