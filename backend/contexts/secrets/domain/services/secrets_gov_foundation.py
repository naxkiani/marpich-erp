"""Secrets P209-M AI Security / Governance / Compliance foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]

REQUIRED_ARTIFACTS = [
    "docs/adr/358-enterprise-secrets-governance.md",
    "docs/architecture/ENTERPRISE_SECRETS_GOVERNANCE.md",
    "docs/architecture/secrets/SECRETS_GOV_CAPABILITIES.v1.yaml",
    "docs/architecture/secrets/SECRETS_GOV_DDD_CQRS.v1.yaml",
    "docs/architecture/secrets/SECRETS_GOV_SECURITY.v1.yaml",
    "docs/architecture/secrets/SECRETS_GOV_VALIDATION.v1.yaml",
    "backend/contexts/secrets/domain/services/secrets_platform_gov.py",
    "backend/contexts/secrets/domain/aggregates/secrets_gov_aggregates.py",
    "backend/contexts/secrets/infrastructure/acl/secrets_gov_acl.py",
    "backend/contexts/secrets/domain/services/secrets_gov_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/vault",
    "backend/contexts/pki_platform",
    "backend/contexts/ca_platform",
    "backend/contexts/kms_platform",
    "backend/contexts/hsm_platform",
    "backend/contexts/crypto_trust_platform",
    "backend/contexts/governance_platform",
    "backend/contexts/crypto_compliance_platform",
    "backend/contexts/crypto_governance_platform",
    "backend/contexts/ai_security_governance_platform",
    "backend/contexts/ops_platform",
    "backend/contexts/crypto_ops_platform",
    "backend/contexts/secrets_pam",
    "backend/contexts/enterprise_pki",
)


def validate_secrets_gov_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.secrets.domain.aggregates.secrets_gov_aggregates import (
        SecretsGovAiExplainableRoot,
        SecretsGovAuditCompleteRoot,
        SecretsGovEvidenceAutomatedRoot,
        SecretsGovHumanOversightRoot,
        SecretsGovOwnershipDefinedRoot,
        SecretsGovPolicyManagedRoot,
        SecretsGovRemediationAutomatedRoot,
        SecretsGovRiskMeasurableRoot,
    )
    from contexts.secrets.domain.services import secrets_platform_gov as gov
    from contexts.secrets.infrastructure.acl import secrets_gov_acl as acls

    cat = gov.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P209-M"
        and cat.get("adr") == 358
        and cat.get("sor") == "secrets"
        and cat["ai_decisions_explainable_required"] is True
        and cat["crypto_policies_managed_required"] is True
        and cat["compliance_evidence_automated_required"] is True
        and cat["risks_measurable_required"] is True
        and cat["governance_ownership_defined_required"] is True
        and cat["audit_trails_complete_required"] is True
        and cat["remediation_automatable_required"] is True
        and cat["ai_security_governance"]["not_unexplainable"] is True
        and cat["cryptographic_governance"]["not_unmanaged"] is True
        and cat["compliance_automation"]["not_manual_only"] is True
        and cat["risk_intelligence"]["not_unmeasurable"] is True
        and cat["microservices"]["not_undefined_ownership"] is True
        and cat["security"]["not_incomplete_audit"] is True
        and cat["incident_response"]["not_cannot_automate"] is True
        and cat["cqrs"]["event_count"] >= 14
        and cat["cursor_outputs"]["count"] >= 20
        and "ai_security_decisions_not_explainable"
        in cat["quality_gates"]["reject_if"]
        and "remediation_cannot_be_automated"
        in cat["quality_gates"]["reject_if"]
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )

    try:
        SecretsGovAiExplainableRoot.record(
            tenant_id="t1", decision_ref="d1", explainable=False
        )
        ai_bad = True
    except ValueError:
        ai_bad = False

    ai = SecretsGovAiExplainableRoot.record(
        tenant_id="t1", decision_ref="d2"
    )
    ai_ok = not ai_bad and ai.is_unexplainable() is False

    try:
        SecretsGovPolicyManagedRoot.manage(
            tenant_id="t1", policy_ref="p1", managed=False
        )
        pol_bad = True
    except ValueError:
        pol_bad = False

    pol = SecretsGovPolicyManagedRoot.manage(
        tenant_id="t1", policy_ref="encryption-policy"
    )
    pol_ok = not pol_bad and pol.is_unmanaged() is False

    try:
        SecretsGovEvidenceAutomatedRoot.automate(
            tenant_id="t1", evidence_ref="e1", automated=False
        )
        ev_bad = True
    except ValueError:
        ev_bad = False

    ev = SecretsGovEvidenceAutomatedRoot.automate(
        tenant_id="t1", evidence_ref="ctrl-iso27001"
    )
    ev_ok = not ev_bad and ev.is_manual_only() is False

    try:
        SecretsGovRiskMeasurableRoot.measure(
            tenant_id="t1", risk_ref="r1", measurable=False
        )
        risk_bad = True
    except ValueError:
        risk_bad = False

    risk = SecretsGovRiskMeasurableRoot.measure(
        tenant_id="t1", risk_ref="r2", score=0.33
    )
    risk_ok = not risk_bad and risk.cannot_be_measured() is False

    try:
        SecretsGovOwnershipDefinedRoot.define(
            tenant_id="t1",
            asset_ref="a1",
            owner_ref="",
            ownership_defined=False,
        )
        own_bad = True
    except ValueError:
        own_bad = False

    own = SecretsGovOwnershipDefinedRoot.define(
        tenant_id="t1", asset_ref="key-1", owner_ref="owner-1"
    )
    own_ok = not own_bad and own.is_undefined() is False

    try:
        SecretsGovAuditCompleteRoot.complete_trail(
            tenant_id="t1", trail_ref="tr1", complete=False
        )
        audit_bad = True
    except ValueError:
        audit_bad = False

    audit = SecretsGovAuditCompleteRoot.complete_trail(
        tenant_id="t1", trail_ref="crypto-ops"
    )
    audit_ok = not audit_bad and audit.is_incomplete() is False

    try:
        SecretsGovRemediationAutomatedRoot.enable(
            tenant_id="t1", remediation_ref="rem1", automatable=False
        )
        rem_bad = True
    except ValueError:
        rem_bad = False

    rem = SecretsGovRemediationAutomatedRoot.enable(
        tenant_id="t1", remediation_ref="rotate-key"
    )
    rem_ok = not rem_bad and rem.cannot_be_automated() is False

    oversight = SecretsGovHumanOversightRoot.require(
        tenant_id="t1", decision_ref="approve-policy"
    )
    oversight_ok = "HumanOversightRequired" in oversight.pending_events

    aggregates_ok = (
        ai_ok
        and pol_ok
        and ev_ok
        and risk_ok
        and own_ok
        and audit_ok
        and rem_ok
        and oversight_ok
    )

    acl_ok = (
        acls.to_policy_evaluate(
            tenant_id="t1", policy_ref="p1", context={}
        )["crypto_policies_managed_required"]
        is True
        and acls.to_compliance_evidence(
            tenant_id="t1", control_ref="c1"
        )["compliance_evidence_automated_required"]
        is True
        and acls.to_workflow_oversight(
            tenant_id="t1", decision_ref="d1"
        )["human_oversight_required"]
        is True
        and acls.to_ai_gov_infer(
            tenant_id="t1", surface="crypto_risk", context={}
        )["ai_decisions_explainable_required"]
        is True
        and acls.to_audit(
            tenant_id="t1", action="secrets.gov.assess", resource_ref="r1"
        )["audit_trails_complete_required"]
        is True
    )

    router = (
        root / "backend/contexts/secrets/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '/gov"' in router
        and "/gov/ai-security" in router
        and "/gov/compliance" in router
        and "/gov/policy" in router
        and "/gov/responsible-ai" in router
        and "/gov/readiness" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_SECRETS_GOVERNANCE.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never AI security decisions are not explainable" in law
        and "Never cryptographic policies are unmanaged" in law
        and "Never compliance evidence is manual only" in law
        and "Never risks cannot be measured" in law
        and "Never governance ownership is undefined" in law
        and "Never audit trails are incomplete" in law
        and "Never remediation cannot be automated" in law
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
        "prompt": "P209-M",
        "adr": 358,
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
