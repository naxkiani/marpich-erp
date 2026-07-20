"""Secrets P209-E CA / Trust Chain foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]

REQUIRED_ARTIFACTS = [
    "docs/adr/350-enterprise-secrets-ca.md",
    "docs/architecture/ENTERPRISE_SECRETS_CA.md",
    "docs/architecture/secrets/SECRETS_CA_CAPABILITIES.v1.yaml",
    "docs/architecture/secrets/SECRETS_CA_DDD_CQRS.v1.yaml",
    "docs/architecture/secrets/SECRETS_CA_SECURITY.v1.yaml",
    "docs/architecture/secrets/SECRETS_CA_VALIDATION.v1.yaml",
    "backend/contexts/secrets/domain/services/secrets_platform_ca.py",
    "backend/contexts/secrets/domain/aggregates/secrets_ca_aggregates.py",
    "backend/contexts/secrets/infrastructure/acl/secrets_ca_acl.py",
    "backend/contexts/secrets/domain/services/secrets_ca_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/vault",
    "backend/contexts/pki_platform",
    "backend/contexts/ca_platform",
    "backend/contexts/kms_platform",
    "backend/contexts/hsm_platform",
    "backend/contexts/crypto_trust_platform",
    "backend/contexts/secrets_pam",
    "backend/contexts/enterprise_pki",
)


def validate_secrets_ca_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.secrets.domain.aggregates.secrets_ca_aggregates import (
        SecretsCaAuditTrailRoot,
        SecretsCaGovernanceRoot,
        SecretsCaKeyCeremonyRoot,
        SecretsCaOwnershipRoot,
        SecretsCaPrivateKeyHsmRoot,
        SecretsCaRevocationRoot,
        SecretsCaRootProtectionRoot,
        SecretsCaTrustChainRoot,
    )
    from contexts.secrets.domain.services import secrets_platform_ca as ca
    from contexts.secrets.infrastructure.acl import secrets_ca_acl as acls

    cat = ca.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P209-E"
        and cat.get("adr") == 350
        and cat.get("sor") == "secrets"
        and cat["root_ca_online_unprotected_forbidden"] is True
        and cat["ca_private_keys_hsm_required"] is True
        and cat["trust_chain_validation_required"] is True
        and cat["revocation_available_required"] is True
        and cat["certificate_ownership_known_required"] is True
        and cat["ca_governance_defined_required"] is True
        and cat["audit_trail_complete_required"] is True
        and cat["root_ca"]["not_online_unprotected"] is True
        and cat["root_ca"]["keys_hsm_protected"] is True
        and cat["trust_chain"]["not_unvalidatable"] is True
        and cat["revocation"]["not_unavailable"] is True
        and cat["ownership"]["not_unknown"] is True
        and cat["governance"]["not_undefined"] is True
        and cat["audit"]["not_incomplete"] is True
        and cat["hierarchy"]["count"] >= 7
        and cat["cqrs"]["event_count"] >= 12
        and cat["cursor_outputs"]["count"] >= 20
        and "root_ca_online_without_protection"
        in cat["quality_gates"]["reject_if"]
        and "ca_private_keys_lack_hsm_protection"
        in cat["quality_gates"]["reject_if"]
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )

    try:
        SecretsCaRootProtectionRoot.harden(
            tenant_id="t1", ca_ref="ca1", offline=False
        )
        root_bad = True
    except ValueError:
        root_bad = False

    root_ca = SecretsCaRootProtectionRoot.harden(tenant_id="t1", ca_ref="ca2")
    root_ok = not root_bad and root_ca.is_online_unprotected() is False

    try:
        SecretsCaPrivateKeyHsmRoot.protect(
            tenant_id="t1", ca_ref="ca3", hsm_protected=False
        )
        hsm_bad = True
    except ValueError:
        hsm_bad = False

    hsm = SecretsCaPrivateKeyHsmRoot.protect(tenant_id="t1", ca_ref="ca4")
    hsm_ok = not hsm_bad and hsm.lacks_hsm() is False

    try:
        SecretsCaTrustChainRoot.validate(
            tenant_id="t1", chain_ref="ch1", validatable=False
        )
        chain_bad = True
    except ValueError:
        chain_bad = False

    chain = SecretsCaTrustChainRoot.validate(tenant_id="t1", chain_ref="ch2")
    chain_ok = not chain_bad and chain.is_unvalidatable() is False

    try:
        SecretsCaRevocationRoot.enable(
            tenant_id="t1", revocation_ref="r1", ocsp=False
        )
        rev_bad = True
    except ValueError:
        rev_bad = False

    rev = SecretsCaRevocationRoot.enable(tenant_id="t1", revocation_ref="r2")
    rev_ok = not rev_bad and rev.is_unavailable() is False

    try:
        SecretsCaOwnershipRoot.bind(
            tenant_id="t1",
            cert_ref="c1",
            owner_ref="",
            known=False,
        )
        own_bad = True
    except ValueError:
        own_bad = False

    ownership = SecretsCaOwnershipRoot.bind(
        tenant_id="t1", cert_ref="c2", owner_ref="owner1"
    )
    own_ok = not own_bad and ownership.is_unknown() is False

    try:
        SecretsCaGovernanceRoot.define(
            tenant_id="t1", governance_ref="g1", defined=False
        )
        gov_bad = True
    except ValueError:
        gov_bad = False

    gov = SecretsCaGovernanceRoot.define(tenant_id="t1", governance_ref="g2")
    gov_ok = not gov_bad and gov.is_undefined() is False

    try:
        SecretsCaAuditTrailRoot.record(
            tenant_id="t1",
            audit_ref="a1",
            action_ref="issue",
            complete=False,
        )
        audit_bad = True
    except ValueError:
        audit_bad = False

    audit = SecretsCaAuditTrailRoot.record(
        tenant_id="t1", audit_ref="a2", action_ref="issue"
    )
    audit_ok = not audit_bad and audit.is_incomplete() is False

    ceremony = SecretsCaKeyCeremonyRoot.complete(
        tenant_id="t1", ceremony_ref="cer1"
    )
    ceremony_ok = "CaKeyCeremonyCompleted" in ceremony.pending_events

    aggregates_ok = (
        root_ok
        and hsm_ok
        and chain_ok
        and rev_ok
        and own_ok
        and gov_ok
        and audit_ok
        and ceremony_ok
    )

    acl_ok = (
        acls.to_hsm_root_ca(tenant_id="t1", ca_ref="ca1")[
            "ca_private_keys_hsm_required"
        ]
        is True
        and acls.to_workflow_ceremony(tenant_id="t1", ceremony_ref="cer1")[
            "dual_control_required"
        ]
        is True
        and acls.to_trust_distribution(
            tenant_id="t1", trust_anchor_ref="ta1"
        )["trust_store_distribution"]
        is True
        and acls.to_audit(
            tenant_id="t1", action="secrets.ca.issue", resource_ref="c1"
        )["ca_audit_trail_complete_required"]
        is True
    )

    router = (
        root / "backend/contexts/secrets/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '/ca"' in router
        and "/ca/root-ca" in router
        and "/ca/trust-chain" in router
        and "/ca/revocation" in router
        and "/ca/governance" in router
        and "/ca/readiness" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_SECRETS_CA.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never Root CA is online without protection" in law
        and "Never CA private keys lack HSM protection" in law
        and "Never trust chains cannot be validated" in law
        and "Never certificate revocation is unavailable" in law
        and "Never certificate ownership is unknown" in law
        and "Never CA governance is undefined" in law
        and "Never audit trail is incomplete" in law
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
        "prompt": "P209-E",
        "adr": 350,
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
