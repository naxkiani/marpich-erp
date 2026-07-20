"""Secrets P209-D PKI foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]

REQUIRED_ARTIFACTS = [
    "docs/adr/349-enterprise-secrets-pki.md",
    "docs/architecture/ENTERPRISE_SECRETS_PKI.md",
    "docs/architecture/secrets/SECRETS_PKI_CAPABILITIES.v1.yaml",
    "docs/architecture/secrets/SECRETS_PKI_DDD_CQRS.v1.yaml",
    "docs/architecture/secrets/SECRETS_PKI_SECURITY.v1.yaml",
    "docs/architecture/secrets/SECRETS_PKI_VALIDATION.v1.yaml",
    "backend/contexts/secrets/domain/services/secrets_platform_pki.py",
    "backend/contexts/secrets/domain/aggregates/secrets_pki_aggregates.py",
    "backend/contexts/secrets/infrastructure/acl/secrets_pki_acl.py",
    "backend/contexts/secrets/domain/services/secrets_pki_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/vault",
    "backend/contexts/pki_platform",
    "backend/contexts/kms_platform",
    "backend/contexts/hsm_platform",
    "backend/contexts/crypto_trust_platform",
    "backend/contexts/secrets_pam",
    "backend/contexts/enterprise_pki",
)


def validate_secrets_pki_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.secrets.domain.aggregates.secrets_pki_aggregates import (
        SecretsPkiAuditEvidenceRoot,
        SecretsPkiCertLifecycleRoot,
        SecretsPkiIssuingCaRoot,
        SecretsPkiOwnershipRoot,
        SecretsPkiRaWorkflowRoot,
        SecretsPkiRevocationRoot,
        SecretsPkiRootCaProtectionRoot,
        SecretsPkiTrustChainRoot,
    )
    from contexts.secrets.domain.services import secrets_platform_pki as pki
    from contexts.secrets.infrastructure.acl import secrets_pki_acl as acls

    cat = pki.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P209-D"
        and cat.get("adr") == 349
        and cat.get("sor") == "secrets"
        and cat["root_ca_keys_protected_required"] is True
        and cat["certificates_auto_managed_required"] is True
        and cat["certificate_lifecycle_complete_required"] is True
        and cat["revocation_mechanisms_required"] is True
        and cat["trust_chain_validation_required"] is True
        and cat["certificate_ownership_known_required"] is True
        and cat["audit_evidence_required"] is True
        and cat["root_ca"]["not_unprotected"] is True
        and cat["lifecycle"]["not_manual"] is True
        and cat["lifecycle"]["not_incomplete"] is True
        and cat["revocation"]["not_absent"] is True
        and cat["validation"]["not_unvalidatable"] is True
        and cat["ownership"]["not_unknown"] is True
        and cat["audit"]["not_unavailable"] is True
        and cat["lifecycle"]["stage_count"] >= 12
        and cat["cqrs"]["event_count"] >= 12
        and cat["cursor_outputs"]["count"] >= 20
        and "root_ca_keys_not_protected" in cat["quality_gates"]["reject_if"]
        and "certificates_manually_managed" in cat["quality_gates"]["reject_if"]
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )

    try:
        SecretsPkiRootCaProtectionRoot.harden(
            tenant_id="t1", ca_ref="ca1", hsm_protected=False
        )
        root_bad = True
    except ValueError:
        root_bad = False

    root_ca = SecretsPkiRootCaProtectionRoot.harden(
        tenant_id="t1", ca_ref="ca2"
    )
    root_ok = not root_bad and root_ca.is_unprotected() is False

    try:
        SecretsPkiCertLifecycleRoot.manage(
            tenant_id="t1", cert_ref="c1", manual=True
        )
        man_bad = True
    except ValueError:
        man_bad = False

    try:
        SecretsPkiCertLifecycleRoot.manage(
            tenant_id="t1", cert_ref="c2", complete=False
        )
        life_bad = True
    except ValueError:
        life_bad = False

    life = SecretsPkiCertLifecycleRoot.manage(tenant_id="t1", cert_ref="c3")
    life_ok = (
        not man_bad
        and not life_bad
        and life.is_manual_or_incomplete() is False
    )

    try:
        SecretsPkiRevocationRoot.enable(
            tenant_id="t1", revocation_ref="r1", ocsp=False
        )
        rev_bad = True
    except ValueError:
        rev_bad = False

    rev = SecretsPkiRevocationRoot.enable(
        tenant_id="t1", revocation_ref="r2"
    )
    rev_ok = not rev_bad and rev.is_absent() is False

    try:
        SecretsPkiTrustChainRoot.validate(
            tenant_id="t1", chain_ref="ch1", validatable=False
        )
        chain_bad = True
    except ValueError:
        chain_bad = False

    chain = SecretsPkiTrustChainRoot.validate(
        tenant_id="t1", chain_ref="ch2"
    )
    chain_ok = not chain_bad and chain.is_unvalidatable() is False

    try:
        SecretsPkiOwnershipRoot.bind(
            tenant_id="t1",
            cert_ref="c4",
            owner_ref="",
            known=False,
        )
        own_bad = True
    except ValueError:
        own_bad = False

    ownership = SecretsPkiOwnershipRoot.bind(
        tenant_id="t1", cert_ref="c5", owner_ref="owner1"
    )
    own_ok = not own_bad and ownership.is_unknown() is False

    try:
        SecretsPkiAuditEvidenceRoot.record(
            tenant_id="t1",
            evidence_ref="e1",
            action_ref="issue",
            available=False,
        )
        audit_bad = True
    except ValueError:
        audit_bad = False

    audit = SecretsPkiAuditEvidenceRoot.record(
        tenant_id="t1", evidence_ref="e2", action_ref="issue"
    )
    audit_ok = not audit_bad and audit.is_unavailable() is False

    issuing = SecretsPkiIssuingCaRoot.activate(
        tenant_id="t1", ca_ref="iss1"
    )
    ra = SecretsPkiRaWorkflowRoot.submit(
        tenant_id="t1", request_ref="req1"
    )
    extras_ok = (
        "CertificateIssued" in issuing.pending_events
        and "CertificateRequested" in ra.pending_events
    )

    aggregates_ok = (
        root_ok
        and life_ok
        and rev_ok
        and chain_ok
        and own_ok
        and audit_ok
        and extras_ok
    )

    acl_ok = (
        acls.to_hsm_root_ca(tenant_id="t1", ca_ref="ca1")[
            "root_ca_hsm_required"
        ]
        is True
        and acls.to_workflow_ra(tenant_id="t1", request_ref="r1")[
            "manual_cert_bypass_forbidden"
        ]
        is True
        and acls.to_kms_boundary(tenant_id="t1", key_ref="k1")[
            "pki_kms_separated"
        ]
        is True
        and acls.to_audit(
            tenant_id="t1", action="secrets.pki.issue", resource_ref="c1"
        )["pki_audit_evidence_required"]
        is True
    )

    router = (
        root / "backend/contexts/secrets/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '/pki"' in router
        and "/pki/root-ca" in router
        and "/pki/lifecycle" in router
        and "/pki/revocation" in router
        and "/pki/readiness" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_SECRETS_PKI.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never Root CA keys are not protected" in law
        and "Never certificates are manually managed" in law
        and "Never certificate lifecycle is incomplete" in law
        and "Never revocation mechanisms are absent" in law
        and "Never trust chains cannot be validated" in law
        and "Never certificate ownership is unknown" in law
        and "Never audit evidence is unavailable" in law
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
        "prompt": "P209-D",
        "adr": 349,
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
