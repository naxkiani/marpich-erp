"""Data Security P211-E Classification foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/380-enterprise-data-security-classification.md",
    "docs/architecture/ENTERPRISE_DATA_SECURITY_CLASSIFICATION.md",
    "docs/architecture/data_security/DATA_SECURITY_CLASSIFICATION_CAPABILITIES.v1.yaml",
    "docs/architecture/data_security/DATA_SECURITY_CLASSIFICATION_DDD_CQRS.v1.yaml",
    "docs/architecture/data_security/DATA_SECURITY_CLASSIFICATION_SECURITY.v1.yaml",
    "docs/architecture/data_security/DATA_SECURITY_CLASSIFICATION_VALIDATION.v1.yaml",
    "backend/contexts/data_security/domain/services/ds_platform_classification.py",
    "backend/contexts/data_security/domain/aggregates/ds_classification_aggregates.py",
    "backend/contexts/data_security/infrastructure/acl/ds_classification_acl.py",
    "backend/contexts/data_security/application/ds_classification_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/data_classification",
    "backend/contexts/label_management",
    "backend/contexts/sensitive_data_detection",
    "backend/contexts/dspm",
)


def validate_ds_classification_foundation(
    *, repo_root: Path | None = None
) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.data_security.domain.aggregates.ds_classification_aggregates import (
        DsClassifiableDataRoot,
        DsClassificationDecisionRoot,
        DsClassificationLifecycleRoot,
        DsClassificationPoliciesRoot,
        DsExplainableAiRoot,
        DsLabelAppliedRoot,
        DsManagedLabelsRoot,
        DsSensitiveDetectionRoot,
    )
    from contexts.data_security.domain.services import (
        ds_platform_classification as cls,
    )

    cat = cls.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P211-E"
        and cat.get("adr") == 380
        and cat.get("sor") == "data_security"
        and cat["data_classifiable_required"] is True
        and cat["sensitive_detection_available_required"] is True
        and cat["labels_managed_required"] is True
        and cat["ai_decisions_explainable_required"] is True
        and cat["classification_policies_present_required"] is True
        and cat["classification_lifecycle_defined_required"] is True
        and cat["taxonomy"]["not_unclassifiable"] is True
        and cat["sensitive_detection"]["not_unavailable"] is True
        and cat["labels"]["not_unmanaged"] is True
        and cat["ai_classification"]["not_unexplained"] is True
        and cat["policies"]["not_missing"] is True
        and cat["lifecycle"]["not_undefined"] is True
        and cat["architecture"]["layer_count"] >= 8
        and cat["taxonomy"]["level_count"] >= 5
        and cat["sensitive_detection"]["category_count"] >= 6
        and cat["cqrs"]["event_count"] >= 8
        and cat["cursor_outputs"]["count"] >= 16
        and "data_cannot_be_classified" in cat["quality_gates"]["reject_if"]
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
            DsClassifiableDataRoot.classify,
            tenant_id="t1",
            asset_ref="a1",
            classifiable=False,
        )
        and DsClassifiableDataRoot.classify(
            tenant_id="t1", asset_ref="a2"
        ).is_unclassifiable()
        is False
    )
    checks.append(
        not _bad(
            DsSensitiveDetectionRoot.detect,
            tenant_id="t1",
            detection_ref="d1",
            available=False,
        )
        and DsSensitiveDetectionRoot.detect(
            tenant_id="t1", detection_ref="d2"
        ).is_unavailable()
        is False
    )
    checks.append(
        not _bad(
            DsManagedLabelsRoot.apply,
            tenant_id="t1",
            label_ref="l1",
            managed=False,
        )
        and DsManagedLabelsRoot.apply(
            tenant_id="t1", label_ref="l2"
        ).is_unmanaged()
        is False
    )
    checks.append(
        not _bad(
            DsExplainableAiRoot.decide,
            tenant_id="t1",
            decision_ref="x1",
            explainable=False,
        )
        and DsExplainableAiRoot.decide(
            tenant_id="t1", decision_ref="x2"
        ).is_unexplained()
        is False
    )
    checks.append(
        not _bad(
            DsClassificationPoliciesRoot.update,
            tenant_id="t1",
            policy_ref="p1",
            present=False,
        )
        and DsClassificationPoliciesRoot.update(
            tenant_id="t1", policy_ref="p2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DsClassificationLifecycleRoot.define,
            tenant_id="t1",
            lifecycle_ref="lc1",
            defined=False,
        )
        and DsClassificationLifecycleRoot.define(
            tenant_id="t1", lifecycle_ref="lc2"
        ).is_undefined()
        is False
    )
    approved = DsClassificationDecisionRoot.approve(
        tenant_id="t1", decision_ref="dec1"
    )
    labeled = DsLabelAppliedRoot.apply(tenant_id="t1", label_ref="lab1")
    checks.append("ClassificationReviewed" in approved.pending_events)
    checks.append("LabelApplied" in labeled.pending_events)
    aggregates_ok = all(checks)

    acl_path = (
        root
        / "backend/contexts/data_security/infrastructure/acl/ds_classification_acl.py"
    )
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_p211_d_discovery" in acl_text
        and "ai_decisions_explainable_required" in acl_text
        and "via_policy_engine" in acl_text
        and "via_workflow" in acl_text
        and "sensitive_detection_available_required" in acl_text
    )

    router = (
        root / "backend/contexts/data_security/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@data_security_router.get("/classification")' in router
        and "/classification/taxonomy" in router
        and "/classification/labels" in router
        and "/classification/ai" in router
        and "/classification/readiness" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_DATA_SECURITY_CLASSIFICATION.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never Data cannot be classified" in law
        and "Never Sensitive data detection is unavailable" in law
        and "Never Labels are unmanaged" in law
        and "Never AI decisions are unexplained" in law
        and "Never Classification policies are missing" in law
        and "Never Classification lifecycle is undefined" in law
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
        "prompt": "P211-E",
        "adr": 380,
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
