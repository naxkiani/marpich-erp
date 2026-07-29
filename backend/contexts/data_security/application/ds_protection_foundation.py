"""Data Security P211-J Protection foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/385-enterprise-data-security-protection.md",
    "docs/architecture/ENTERPRISE_DATA_SECURITY_PROTECTION.md",
    "docs/architecture/data_security/DATA_SECURITY_PROTECTION_CAPABILITIES.v1.yaml",
    "docs/architecture/data_security/DATA_SECURITY_PROTECTION_DDD_CQRS.v1.yaml",
    "docs/architecture/data_security/DATA_SECURITY_PROTECTION_SECURITY.v1.yaml",
    "docs/architecture/data_security/DATA_SECURITY_PROTECTION_VALIDATION.v1.yaml",
    "backend/contexts/data_security/domain/services/ds_platform_protection.py",
    "backend/contexts/data_security/domain/aggregates/ds_protection_aggregates.py",
    "backend/contexts/data_security/infrastructure/acl/ds_protection_acl.py",
    "backend/contexts/data_security/application/ds_protection_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/data_protection_platform",
    "backend/contexts/tokenization_platform",
    "backend/contexts/encryption_platform",
)


def validate_ds_protection_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.data_security.domain.aggregates.ds_protection_aggregates import (
        DsAuditableProtectionDecisionRoot,
        DsCompletePrivacyControlsRoot,
        DsDefinedEncryptionPolicyRoot,
        DsEncryptionCompletedRoot,
        DsKeyIntegrationRoot,
        DsProtectedSensitiveRoot,
        DsProtectionViolationRoot,
        DsTokenLifecycleRoot,
    )
    from contexts.data_security.domain.services import (
        ds_platform_protection as prot,
    )

    cat = prot.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P211-J"
        and cat.get("adr") == 385
        and cat.get("sor") == "data_security"
        and cat["sensitive_data_protected_required"] is True
        and cat["encryption_policies_defined_required"] is True
        and cat["token_lifecycle_present_required"] is True
        and cat["key_integration_available_required"] is True
        and cat["protection_decisions_auditable_required"] is True
        and cat["privacy_controls_complete_required"] is True
        and cat["keys_remain_p209_secrets"] is True
        and cat["sensitive_protection"]["not_unprotected"] is True
        and cat["encryption"]["not_undefined"] is True
        and cat["tokenization"]["not_missing"] is True
        and cat["key_integration"]["not_unavailable"] is True
        and cat["decision_engine"]["not_unauditable"] is True
        and cat["anonymization"]["not_incomplete"] is True
        and cat["key_integration"]["kms_owner"] == "secrets"
        and cat["architecture"]["layer_count"] >= 7
        and cat["domain"]["context_count"] >= 7
        and cat["cqrs"]["event_count"] >= 6
        and cat["cursor_outputs"]["count"] >= 16
        and "sensitive_data_can_exist_unprotected"
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
            DsProtectedSensitiveRoot.protect,
            tenant_id="t1",
            asset_ref="a1",
            protected=False,
        )
        and DsProtectedSensitiveRoot.protect(
            tenant_id="t1", asset_ref="a2"
        ).is_unprotected()
        is False
    )
    checks.append(
        not _bad(
            DsDefinedEncryptionPolicyRoot.define,
            tenant_id="t1",
            policy_ref="p1",
            defined=False,
        )
        and DsDefinedEncryptionPolicyRoot.define(
            tenant_id="t1", policy_ref="p2"
        ).is_undefined()
        is False
    )
    checks.append(
        not _bad(
            DsTokenLifecycleRoot.manage,
            tenant_id="t1",
            token_ref="tok1",
            present=False,
        )
        and DsTokenLifecycleRoot.manage(
            tenant_id="t1", token_ref="tok2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DsKeyIntegrationRoot.bind,
            tenant_id="t1",
            key_ref="",
            available=False,
        )
        and DsKeyIntegrationRoot.bind(
            tenant_id="t1", key_ref="key1"
        ).is_unavailable()
        is False
    )
    checks.append(
        not _bad(
            DsAuditableProtectionDecisionRoot.decide,
            tenant_id="t1",
            decision_ref="d1",
            auditable=False,
        )
        and DsAuditableProtectionDecisionRoot.decide(
            tenant_id="t1", decision_ref="d2"
        ).is_unauditable()
        is False
    )
    checks.append(
        not _bad(
            DsCompletePrivacyControlsRoot.ensure,
            tenant_id="t1",
            control_ref="c1",
            complete=False,
        )
        and DsCompletePrivacyControlsRoot.ensure(
            tenant_id="t1", control_ref="c2"
        ).is_incomplete()
        is False
    )
    enc = DsEncryptionCompletedRoot.encrypt(tenant_id="t1", asset_ref="e1")
    vio = DsProtectionViolationRoot.detect(tenant_id="t1", violation_ref="v1")
    checks.append("EncryptionCompleted" in enc.pending_events)
    checks.append("ProtectionViolationDetected" in vio.pending_events)
    aggregates_ok = all(checks)

    acl_path = (
        root
        / "backend/contexts/data_security/infrastructure/acl/ds_protection_acl.py"
    )
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_p209" in acl_text
        and "module_local_kms_forbidden" in acl_text
        and "key_integration_available_required" in acl_text
        and "privacy_controls_complete_required" in acl_text
        and "via_p211_i_privacy" in acl_text
        and "protection_decisions_auditable_required" in acl_text
    )

    router = (
        root / "backend/contexts/data_security/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@data_security_router.get("/protection")' in router
        and "/protection/encryption" in router
        and "/protection/tokenization" in router
        and "/protection/keys" in router
        and "/protection/readiness" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_DATA_SECURITY_PROTECTION.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never Sensitive data can exist unprotected" in law
        and "Never Encryption policies are undefined" in law
        and "Never Token lifecycle is missing" in law
        and "Never Key integration is unavailable" in law
        and "Never Protection decisions are not auditable" in law
        and "Never Privacy controls are incomplete" in law
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
        "prompt": "P211-J",
        "adr": 385,
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
