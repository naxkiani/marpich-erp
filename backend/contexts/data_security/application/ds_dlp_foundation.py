"""Data Security P211-G DLP foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/382-enterprise-data-security-dlp.md",
    "docs/architecture/ENTERPRISE_DATA_SECURITY_DLP.md",
    "docs/architecture/data_security/DATA_SECURITY_DLP_CAPABILITIES.v1.yaml",
    "docs/architecture/data_security/DATA_SECURITY_DLP_DDD_CQRS.v1.yaml",
    "docs/architecture/data_security/DATA_SECURITY_DLP_SECURITY.v1.yaml",
    "docs/architecture/data_security/DATA_SECURITY_DLP_VALIDATION.v1.yaml",
    "backend/contexts/data_security/domain/services/ds_platform_dlp.py",
    "backend/contexts/data_security/domain/aggregates/ds_dlp_aggregates.py",
    "backend/contexts/data_security/infrastructure/acl/ds_dlp_acl.py",
    "backend/contexts/data_security/application/ds_dlp_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/dlp",
    "backend/contexts/data_loss_prevention",
    "backend/contexts/exfiltration_prevention",
)


def validate_ds_dlp_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.data_security.domain.aggregates.ds_dlp_aggregates import (
        DsAutomatedResponseRoot,
        DsBlockedTransferRoot,
        DsEnforceablePolicyRoot,
        DsIdentifiableSensitiveRoot,
        DsInvestigableViolationRoot,
        DsManagedAiLeakageRoot,
        DsMonitoredMovementRoot,
        DsVisibleInsiderRiskRoot,
    )
    from contexts.data_security.domain.services import ds_platform_dlp as dlp

    cat = dlp.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P211-G"
        and cat.get("adr") == 382
        and cat.get("sor") == "data_security"
        and cat["sensitive_data_identifiable_required"] is True
        and cat["data_movement_monitored_required"] is True
        and cat["policies_enforceable_required"] is True
        and cat["ai_leakage_managed_required"] is True
        and cat["insider_risk_visible_required"] is True
        and cat["violations_investigable_required"] is True
        and cat["automated_response_available_required"] is True
        and cat["identification"]["not_unidentifiable"] is True
        and cat["monitoring"]["not_unmonitored"] is True
        and cat["policies"]["not_unenforceable"] is True
        and cat["channels"]["ai"]["not_unmanaged"] is True
        and cat["insider_risk"]["not_invisible"] is True
        and cat["incidents"]["not_uninvestigable"] is True
        and cat["automated_response"]["not_unavailable"] is True
        and cat["architecture"]["layer_count"] >= 8
        and cat["channels"]["channel_count"] >= 5
        and cat["cqrs"]["event_count"] >= 7
        and cat["cursor_outputs"]["count"] >= 18
        and "sensitive_data_cannot_be_identified"
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
            DsIdentifiableSensitiveRoot.identify,
            tenant_id="t1",
            asset_ref="a1",
            identifiable=False,
        )
        and DsIdentifiableSensitiveRoot.identify(
            tenant_id="t1", asset_ref="a2"
        ).is_unidentifiable()
        is False
    )
    checks.append(
        not _bad(
            DsMonitoredMovementRoot.monitor,
            tenant_id="t1",
            transfer_ref="tr1",
            monitored=False,
        )
        and DsMonitoredMovementRoot.monitor(
            tenant_id="t1", transfer_ref="tr2"
        ).is_unmonitored()
        is False
    )
    checks.append(
        not _bad(
            DsEnforceablePolicyRoot.create,
            tenant_id="t1",
            policy_ref="p1",
            enforceable=False,
        )
        and DsEnforceablePolicyRoot.create(
            tenant_id="t1", policy_ref="p2"
        ).is_unenforceable()
        is False
    )
    checks.append(
        not _bad(
            DsManagedAiLeakageRoot.protect,
            tenant_id="t1",
            ai_ref="ai1",
            managed=False,
        )
        and DsManagedAiLeakageRoot.protect(
            tenant_id="t1", ai_ref="ai2"
        ).is_unmanaged()
        is False
    )
    checks.append(
        not _bad(
            DsVisibleInsiderRiskRoot.detect,
            tenant_id="t1",
            risk_ref="r1",
            visible=False,
        )
        and DsVisibleInsiderRiskRoot.detect(
            tenant_id="t1", risk_ref="r2"
        ).is_invisible()
        is False
    )
    checks.append(
        not _bad(
            DsInvestigableViolationRoot.detect,
            tenant_id="t1",
            violation_ref="v1",
            investigable=False,
        )
        and DsInvestigableViolationRoot.detect(
            tenant_id="t1", violation_ref="v2"
        ).is_uninvestigable()
        is False
    )
    checks.append(
        not _bad(
            DsAutomatedResponseRoot.respond,
            tenant_id="t1",
            response_ref="resp1",
            available=False,
        )
        and DsAutomatedResponseRoot.respond(
            tenant_id="t1", response_ref="resp2"
        ).is_unavailable()
        is False
    )
    blocked = DsBlockedTransferRoot.block(tenant_id="t1", transfer_ref="b1")
    checks.append("TransferBlocked" in blocked.pending_events)
    aggregates_ok = all(checks)

    acl_path = (
        root / "backend/contexts/data_security/infrastructure/acl/ds_dlp_acl.py"
    )
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_p211_e_classification" in acl_text
        and "via_p211_f_dspm" in acl_text
        and "ai_leakage_managed_required" in acl_text
        and "policies_enforceable_required" in acl_text
        and "automated_response_available_required" in acl_text
        and "insider_risk_visible_required" in acl_text
    )

    router = (
        root / "backend/contexts/data_security/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@data_security_router.get("/dlp")' in router
        and "/dlp/policies" in router
        and "/dlp/enforcement" in router
        and "/dlp/insider-risk" in router
        and "/dlp/readiness" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_DATA_SECURITY_DLP.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never Sensitive data cannot be identified" in law
        and "Never Data movement cannot be monitored" in law
        and "Never Policies cannot be enforced" in law
        and "Never AI leakage is unmanaged" in law
        and "Never Insider risk is invisible" in law
        and "Never Violations cannot be investigated" in law
        and "Never Automated response is unavailable" in law
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
        "prompt": "P211-G",
        "adr": 382,
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
