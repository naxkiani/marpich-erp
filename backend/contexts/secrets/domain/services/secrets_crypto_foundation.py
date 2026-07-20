"""Secrets P209-I Cryptography Services foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]

REQUIRED_ARTIFACTS = [
    "docs/adr/354-enterprise-secrets-crypto.md",
    "docs/architecture/ENTERPRISE_SECRETS_CRYPTO.md",
    "docs/architecture/secrets/SECRETS_CRYPTO_CAPABILITIES.v1.yaml",
    "docs/architecture/secrets/SECRETS_CRYPTO_DDD_CQRS.v1.yaml",
    "docs/architecture/secrets/SECRETS_CRYPTO_SECURITY.v1.yaml",
    "docs/architecture/secrets/SECRETS_CRYPTO_VALIDATION.v1.yaml",
    "backend/contexts/secrets/domain/services/secrets_platform_crypto.py",
    "backend/contexts/secrets/domain/aggregates/secrets_crypto_ops_aggregates.py",
    "backend/contexts/secrets/infrastructure/acl/secrets_crypto_acl.py",
    "backend/contexts/secrets/domain/services/secrets_crypto_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/vault",
    "backend/contexts/pki_platform",
    "backend/contexts/ca_platform",
    "backend/contexts/kms_platform",
    "backend/contexts/hsm_platform",
    "backend/contexts/crypto_trust_platform",
    "backend/contexts/crypto_platform",
    "backend/contexts/encryption_platform",
    "backend/contexts/eaas_platform",
    "backend/contexts/secrets_pam",
    "backend/contexts/enterprise_pki",
    "backend/contexts/workload_identity_platform",
    "backend/contexts/spiffe_platform",
    "backend/contexts/spire_platform",
)


def validate_secrets_crypto_foundation(
    *, repo_root: Path | None = None
) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.secrets.domain.aggregates.secrets_crypto_ops_aggregates import (
        SecretsCryptoAlgorithmControlRoot,
        SecretsCryptoEaaSRoot,
        SecretsCryptoEncryptionPolicyRoot,
        SecretsCryptoGovernedOpsRoot,
        SecretsCryptoNoKeyExposureRoot,
        SecretsCryptoNoUnmanagedRoot,
        SecretsCryptoOpAuditRoot,
        SecretsCryptoSignatureVerifyRoot,
    )
    from contexts.secrets.domain.services import secrets_platform_crypto as crypto
    from contexts.secrets.infrastructure.acl import secrets_crypto_acl as acls

    cat = crypto.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P209-I"
        and cat.get("adr") == 354
        and cat.get("sor") == "secrets"
        and cat["unmanaged_cryptography_forbidden"] is True
        and cat["encryption_governance_required"] is True
        and cat["keys_exposed_forbidden"] is True
        and cat["algorithms_controlled_required"] is True
        and cat["signatures_verifiable_required"] is True
        and cat["crypto_operations_audited_required"] is True
        and cat["unmanaged"]["not_unmanaged"] is True
        and cat["encryption"]["not_bypass_governance"] is True
        and cat["key_exposure"]["not_exposed"] is True
        and cat["crypto_policy"]["not_uncontrolled"] is True
        and cat["signatures"]["not_unverifiable"] is True
        and cat["audit"]["not_unaudited"] is True
        and cat["cqrs"]["event_count"] >= 12
        and cat["cursor_outputs"]["count"] >= 20
        and "applications_implement_unmanaged_cryptography"
        in cat["quality_gates"]["reject_if"]
        and "keys_are_exposed" in cat["quality_gates"]["reject_if"]
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )

    try:
        SecretsCryptoNoUnmanagedRoot.bind(
            tenant_id="t1", app_ref="a1", unmanaged=True
        )
        unman_bad = True
    except ValueError:
        unman_bad = False

    unman = SecretsCryptoNoUnmanagedRoot.bind(tenant_id="t1", app_ref="a2")
    unman_ok = not unman_bad and unman.is_unmanaged() is False

    try:
        SecretsCryptoGovernedOpsRoot.perform(
            tenant_id="t1", operation_ref="o1", bypass=True
        )
        gov_bad = True
    except ValueError:
        gov_bad = False

    gov = SecretsCryptoGovernedOpsRoot.perform(
        tenant_id="t1", operation_ref="o2"
    )
    gov_ok = not gov_bad and gov.bypasses_governance() is False

    try:
        SecretsCryptoNoKeyExposureRoot.protect(
            tenant_id="t1", key_ref="k1", exposed=True
        )
        key_bad = True
    except ValueError:
        key_bad = False

    key = SecretsCryptoNoKeyExposureRoot.protect(tenant_id="t1", key_ref="k2")
    key_ok = not key_bad and key.is_exposed() is False

    try:
        SecretsCryptoAlgorithmControlRoot.approve(
            tenant_id="t1", algorithm_ref="aes", controlled=False
        )
        alg_bad = True
    except ValueError:
        alg_bad = False

    alg = SecretsCryptoAlgorithmControlRoot.approve(
        tenant_id="t1", algorithm_ref="aes-gcm"
    )
    alg_ok = not alg_bad and alg.is_uncontrolled() is False

    try:
        SecretsCryptoSignatureVerifyRoot.verify(
            tenant_id="t1", signature_ref="s1", verifiable=False
        )
        sig_bad = True
    except ValueError:
        sig_bad = False

    sig = SecretsCryptoSignatureVerifyRoot.verify(
        tenant_id="t1", signature_ref="s2"
    )
    sig_ok = not sig_bad and sig.is_unverifiable() is False

    try:
        SecretsCryptoOpAuditRoot.record(
            tenant_id="t1",
            audit_ref="a1",
            operation_ref="o3",
            audited=False,
        )
        audit_bad = True
    except ValueError:
        audit_bad = False

    audit = SecretsCryptoOpAuditRoot.record(
        tenant_id="t1", audit_ref="a2", operation_ref="o4"
    )
    audit_ok = not audit_bad and audit.lacks_audit() is False

    pol = SecretsCryptoEncryptionPolicyRoot.apply(
        tenant_id="t1", policy_ref="p1"
    )
    eaas = SecretsCryptoEaaSRoot.invoke(tenant_id="t1", eaas_ref="e1")
    extras_ok = (
        "CryptoPolicyChanged" in pol.pending_events
        and "EaaSInvoked" in eaas.pending_events
    )

    aggregates_ok = (
        unman_ok
        and gov_ok
        and key_ok
        and alg_ok
        and sig_ok
        and audit_ok
        and extras_ok
    )

    acl_ok = (
        acls.to_kms_key_ref(tenant_id="t1", key_ref="k1")[
            "keys_exposed_forbidden"
        ]
        is True
        and acls.to_hsm_accelerate(tenant_id="t1", operation_ref="o1")[
            "hsm_acceleration"
        ]
        is True
        and acls.to_policy_algorithm(
            tenant_id="t1", algorithm_ref="aes-gcm"
        )["algorithms_controlled_required"]
        is True
        and acls.to_authorization_crypto(
            tenant_id="t1", operation_ref="o1", principal_ref="u1"
        )["zero_trust_crypto_access"]
        is True
        and acls.to_audit(
            tenant_id="t1", action="secrets.crypto.encrypt", resource_ref="o1"
        )["crypto_operations_audited_required"]
        is True
    )

    router = (
        root / "backend/contexts/secrets/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '/crypto"' in router
        and "/crypto/encryption" in router
        and "/crypto/signatures" in router
        and "/crypto/eaas" in router
        and "/crypto/policy" in router
        and "/crypto/readiness" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_SECRETS_CRYPTO.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never applications implement unmanaged cryptography" in law
        and "Never encryption operations bypass governance" in law
        and "Never keys are exposed" in law
        and "Never algorithms are uncontrolled" in law
        and "Never signatures cannot be verified" in law
        and "Never cryptographic operations lack audit trails" in law
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
        "prompt": "P209-I",
        "adr": 354,
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
