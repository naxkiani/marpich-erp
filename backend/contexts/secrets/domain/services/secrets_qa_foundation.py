"""Secrets P209-O Testing / Governance / Security Validation / DoD foundation."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]

REQUIRED_ARTIFACTS = [
    "docs/adr/360-enterprise-secrets-qa.md",
    "docs/architecture/ENTERPRISE_SECRETS_QA.md",
    "docs/architecture/secrets/SECRETS_QA_CAPABILITIES.v1.yaml",
    "docs/architecture/secrets/SECRETS_QA_DDD_CQRS.v1.yaml",
    "docs/architecture/secrets/SECRETS_QA_SECURITY.v1.yaml",
    "docs/architecture/secrets/SECRETS_QA_VALIDATION.v1.yaml",
    "backend/contexts/secrets/domain/services/secrets_platform_qa.py",
    "backend/contexts/secrets/domain/aggregates/secrets_qa_aggregates.py",
    "backend/contexts/secrets/infrastructure/acl/secrets_qa_acl.py",
    "backend/contexts/secrets/domain/services/secrets_qa_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/qa_platform",
    "backend/contexts/crypto_assurance_platform",
    "backend/contexts/secrets_testing_platform",
    "backend/contexts/crypto_dod_platform",
    "backend/contexts/governance_platform",
    "backend/contexts/deploy_platform",
    "backend/contexts/vault",
    "backend/contexts/pki_platform",
    "backend/contexts/kms_platform",
)


def validate_secrets_qa_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.secrets.domain.aggregates.secrets_qa_aggregates import (
        SecretsQaAuditTrailsRoot,
        SecretsQaComplianceEvidenceRoot,
        SecretsQaCryptoControlsRoot,
        SecretsQaDefinitionOfDoneRoot,
        SecretsQaDeployGateRoot,
        SecretsQaGovernanceOwnershipRoot,
        SecretsQaProductionReadinessRoot,
        SecretsQaSecurityTestingRoot,
    )
    from contexts.secrets.domain.services import secrets_platform_qa as qa
    from contexts.secrets.infrastructure.acl import secrets_qa_acl as acls

    cat = qa.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P209-O"
        and cat.get("adr") == 360
        and cat.get("sor") == "secrets"
        and cat["security_testing_complete_required"] is True
        and cat["compliance_evidence_available_required"] is True
        and cat["cryptographic_controls_validated_required"] is True
        and cat["production_readiness_defined_required"] is True
        and cat["governance_ownership_present_required"] is True
        and cat["audit_trails_complete_required"] is True
        and cat["security_failures_block_deployment_required"] is True
        and cat["architecture"]["not_incomplete"] is True
        and cat["compliance"]["not_unavailable"] is True
        and cat["cryptographic_testing"]["not_unvalidated"] is True
        and cat["production_readiness"]["not_undefined"] is True
        and cat["governance"]["not_missing"] is True
        and cat["security"]["not_incomplete_audit"] is True
        and cat["devsecops_validation"]["not_cannot_block"] is True
        and cat["cqrs"]["event_count"] >= 14
        and cat["cursor_outputs"]["count"] >= 20
        and "security_testing_incomplete" in cat["quality_gates"]["reject_if"]
        and "security_failures_cannot_block_deployment"
        in cat["quality_gates"]["reject_if"]
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )

    try:
        SecretsQaSecurityTestingRoot.complete_plan(
            tenant_id="t1", plan_ref="p1", complete=False
        )
        sec_bad = True
    except ValueError:
        sec_bad = False

    sec = SecretsQaSecurityTestingRoot.complete_plan(
        tenant_id="t1", plan_ref="crypto-sec"
    )
    sec_ok = not sec_bad and sec.is_incomplete() is False

    try:
        SecretsQaComplianceEvidenceRoot.publish(
            tenant_id="t1", evidence_ref="e1", available=False
        )
        ev_bad = True
    except ValueError:
        ev_bad = False

    ev = SecretsQaComplianceEvidenceRoot.publish(
        tenant_id="t1", evidence_ref="iso27001"
    )
    ev_ok = not ev_bad and ev.is_unavailable() is False

    try:
        SecretsQaCryptoControlsRoot.validate(
            tenant_id="t1", control_ref="c1", validated=False
        )
        ctrl_bad = True
    except ValueError:
        ctrl_bad = False

    ctrl = SecretsQaCryptoControlsRoot.validate(
        tenant_id="t1", control_ref="key-rotation"
    )
    ctrl_ok = not ctrl_bad and ctrl.is_unvalidated() is False

    try:
        SecretsQaProductionReadinessRoot.define(
            tenant_id="t1", checklist_ref="cl1", defined=False
        )
        ready_bad = True
    except ValueError:
        ready_bad = False

    ready = SecretsQaProductionReadinessRoot.define(
        tenant_id="t1", checklist_ref="p209-dod"
    )
    ready_ok = not ready_bad and ready.is_undefined() is False

    try:
        SecretsQaGovernanceOwnershipRoot.assign(
            tenant_id="t1", body_ref="b1", present=False
        )
        gov_bad = True
    except ValueError:
        gov_bad = False

    gov = SecretsQaGovernanceOwnershipRoot.assign(
        tenant_id="t1", body_ref="crypto-security-council"
    )
    gov_ok = not gov_bad and gov.is_missing() is False

    try:
        SecretsQaAuditTrailsRoot.complete_trail(
            tenant_id="t1", trail_ref="tr1", complete=False
        )
        audit_bad = True
    except ValueError:
        audit_bad = False

    audit = SecretsQaAuditTrailsRoot.complete_trail(
        tenant_id="t1", trail_ref="qa-audit"
    )
    audit_ok = not audit_bad and audit.is_incomplete() is False

    try:
        SecretsQaDeployGateRoot.enforce(
            tenant_id="t1", gate_ref="g1", can_block=False
        )
        gate_bad = True
    except ValueError:
        gate_bad = False

    gate = SecretsQaDeployGateRoot.enforce(
        tenant_id="t1", gate_ref="security-pass"
    )
    gate_ok = not gate_bad and gate.cannot_block() is False

    dod = SecretsQaDefinitionOfDoneRoot.meet(tenant_id="t1")
    dod_ok = "DefinitionOfDoneMet" in dod.pending_events and dod.is_unmet() is False

    aggregates_ok = (
        sec_ok
        and ev_ok
        and ctrl_ok
        and ready_ok
        and gov_ok
        and audit_ok
        and gate_ok
        and dod_ok
    )

    acl_ok = (
        acls.to_compliance_evidence(tenant_id="t1", control_ref="c1")[
            "compliance_evidence_available_required"
        ]
        is True
        and acls.to_policy_validate(
            tenant_id="t1", policy_ref="p1", context={}
        )["cryptographic_controls_validated_required"]
        is True
        and acls.to_workflow_release(tenant_id="t1", release_ref="r1")[
            "security_failures_block_deployment_required"
        ]
        is True
        and acls.to_deploy_gate(tenant_id="t1", gate_ref="g1")[
            "can_reject_deployment"
        ]
        is True
        and acls.to_audit(
            tenant_id="t1", action="secrets.qa.test", resource_ref="t1"
        )["audit_trails_complete_required"]
        is True
    )

    router = (
        root / "backend/contexts/secrets/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '/qa"' in router
        and "/qa/cryptographic" in router
        and "/qa/compliance" in router
        and "/qa/definition-of-done" in router
        and "/qa/devsecops" in router
        and "/qa/readiness" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_SECRETS_QA.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never security testing is incomplete" in law
        and "Never compliance evidence is unavailable" in law
        and "Never cryptographic controls are not validated" in law
        and "Never production readiness is undefined" in law
        and "Never governance ownership is missing" in law
        and "Never audit trails are incomplete" in law
        and "Never security failures cannot block deployment" in law
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
        "prompt": "P209-O",
        "adr": 360,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "catalog": catalog_ok,
        "aggregates": aggregates_ok,
        "acl": acl_ok,
        "router": router_ok,
        "documentation": doc_ok,
        "sor": "secrets",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
