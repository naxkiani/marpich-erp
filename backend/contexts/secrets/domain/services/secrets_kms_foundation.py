"""Secrets P209-F KMS foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]

REQUIRED_ARTIFACTS = [
    "docs/adr/351-enterprise-secrets-kms.md",
    "docs/architecture/ENTERPRISE_SECRETS_KMS.md",
    "docs/architecture/secrets/SECRETS_KMS_CAPABILITIES.v1.yaml",
    "docs/architecture/secrets/SECRETS_KMS_DDD_CQRS.v1.yaml",
    "docs/architecture/secrets/SECRETS_KMS_SECURITY.v1.yaml",
    "docs/architecture/secrets/SECRETS_KMS_VALIDATION.v1.yaml",
    "backend/contexts/secrets/domain/services/secrets_platform_kms.py",
    "backend/contexts/secrets/domain/aggregates/secrets_kms_aggregates.py",
    "backend/contexts/secrets/infrastructure/acl/secrets_kms_acl.py",
    "backend/contexts/secrets/domain/services/secrets_kms_foundation.py",
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


def validate_secrets_kms_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.secrets.domain.aggregates.secrets_kms_aggregates import (
        SecretsKmsAutoRotationRoot,
        SecretsKmsCryptoPolicyRoot,
        SecretsKmsEnvelopeEncryptionRoot,
        SecretsKmsHsmCapabilityRoot,
        SecretsKmsKeyAuditRoot,
        SecretsKmsKeyLifecycleRoot,
        SecretsKmsKeyOwnershipRoot,
        SecretsKmsKeyProtectionRoot,
    )
    from contexts.secrets.domain.services import secrets_platform_kms as kms
    from contexts.secrets.infrastructure.acl import secrets_kms_acl as acls

    cat = kms.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P209-F"
        and cat.get("adr") == 351
        and cat.get("sor") == "secrets"
        and cat["keys_stored_without_protection_forbidden"] is True
        and cat["hsm_capability_required"] is True
        and cat["key_lifecycle_complete_required"] is True
        and cat["key_ownership_known_required"] is True
        and cat["rotation_automatic_required"] is True
        and cat["key_operations_audited_required"] is True
        and cat["cryptographic_policies_required"] is True
        and cat["protection"]["not_unprotected"] is True
        and cat["hsm"]["not_unavailable"] is True
        and cat["lifecycle"]["not_incomplete"] is True
        and cat["lifecycle"]["not_manual_only"] is True
        and cat["ownership"]["not_unknown"] is True
        and cat["audit"]["not_unaudited"] is True
        and cat["crypto_policy"]["not_absent"] is True
        and cat["lifecycle"]["stage_count"] >= 11
        and cat["cqrs"]["event_count"] >= 12
        and cat["cursor_outputs"]["count"] >= 20
        and "keys_stored_without_protection"
        in cat["quality_gates"]["reject_if"]
        and "hsm_capability_unavailable" in cat["quality_gates"]["reject_if"]
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )

    try:
        SecretsKmsKeyProtectionRoot.protect(
            tenant_id="t1", key_ref="k1", protected=False
        )
        prot_bad = True
    except ValueError:
        prot_bad = False

    prot = SecretsKmsKeyProtectionRoot.protect(tenant_id="t1", key_ref="k2")
    prot_ok = not prot_bad and prot.is_unprotected() is False

    try:
        SecretsKmsHsmCapabilityRoot.verify(
            tenant_id="t1", hsm_ref="h1", available=False
        )
        hsm_bad = True
    except ValueError:
        hsm_bad = False

    hsm = SecretsKmsHsmCapabilityRoot.verify(tenant_id="t1", hsm_ref="h2")
    hsm_ok = not hsm_bad and hsm.is_unavailable() is False

    try:
        SecretsKmsKeyLifecycleRoot.manage(
            tenant_id="t1", key_ref="k3", complete=False
        )
        life_bad = True
    except ValueError:
        life_bad = False

    life = SecretsKmsKeyLifecycleRoot.manage(tenant_id="t1", key_ref="k4")
    life_ok = not life_bad and life.is_incomplete() is False

    try:
        SecretsKmsKeyOwnershipRoot.bind(
            tenant_id="t1",
            key_ref="k5",
            owner_ref="",
            known=False,
        )
        own_bad = True
    except ValueError:
        own_bad = False

    ownership = SecretsKmsKeyOwnershipRoot.bind(
        tenant_id="t1", key_ref="k6", owner_ref="owner1"
    )
    own_ok = not own_bad and ownership.is_unknown() is False

    try:
        SecretsKmsAutoRotationRoot.enable(
            tenant_id="t1", key_ref="k7", manual_only=True
        )
        rot_bad = True
    except ValueError:
        rot_bad = False

    rot = SecretsKmsAutoRotationRoot.enable(tenant_id="t1", key_ref="k8")
    rot_ok = not rot_bad and rot.is_manual_only() is False

    try:
        SecretsKmsKeyAuditRoot.record(
            tenant_id="t1",
            audit_ref="a1",
            action_ref="rotate",
            audited=False,
        )
        audit_bad = True
    except ValueError:
        audit_bad = False

    audit = SecretsKmsKeyAuditRoot.record(
        tenant_id="t1", audit_ref="a2", action_ref="rotate"
    )
    audit_ok = not audit_bad and audit.is_unaudited() is False

    try:
        SecretsKmsCryptoPolicyRoot.apply(
            tenant_id="t1", policy_ref="p1", present=False
        )
        pol_bad = True
    except ValueError:
        pol_bad = False

    pol = SecretsKmsCryptoPolicyRoot.apply(tenant_id="t1", policy_ref="p2")
    pol_ok = not pol_bad and pol.is_absent() is False

    envelope = SecretsKmsEnvelopeEncryptionRoot.enable(
        tenant_id="t1", envelope_ref="e1"
    )
    env_ok = "EnvelopeEncryptionEnabled" in envelope.pending_events

    aggregates_ok = (
        prot_ok
        and hsm_ok
        and life_ok
        and own_ok
        and rot_ok
        and audit_ok
        and pol_ok
        and env_ok
    )

    acl_ok = (
        acls.to_hsm_key(tenant_id="t1", key_ref="k1")[
            "hsm_capability_required"
        ]
        is True
        and acls.to_integration_cloud_kms(
            tenant_id="t1", provider_ref="aws"
        )["no_embedded_vendor_sdk"]
        is True
        and acls.to_authorization_key_access(
            tenant_id="t1", key_ref="k1", principal_ref="u1"
        )["zero_trust_key_access"]
        is True
        and acls.to_policy_crypto(tenant_id="t1", policy_ref="p1")[
            "cryptographic_policies_required"
        ]
        is True
        and acls.to_audit(
            tenant_id="t1", action="secrets.kms.rotate", resource_ref="k1"
        )["key_operations_audited_required"]
        is True
    )

    router = (
        root / "backend/contexts/secrets/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '/kms"' in router
        and "/kms/lifecycle" in router
        and "/kms/hsm" in router
        and "/kms/protection" in router
        and "/kms/policy" in router
        and "/kms/readiness" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_SECRETS_KMS.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never keys are stored without protection" in law
        and "Never HSM capability is unavailable" in law
        and "Never key lifecycle is incomplete" in law
        and "Never key ownership is unknown" in law
        and "Never rotation is manual only" in law
        and "Never key operations are unaudited" in law
        and "Never cryptographic policies are absent" in law
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
        "prompt": "P209-F",
        "adr": 351,
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
