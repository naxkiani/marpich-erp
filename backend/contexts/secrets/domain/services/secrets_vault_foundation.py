"""Secrets P209-G Vault foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]

REQUIRED_ARTIFACTS = [
    "docs/adr/352-enterprise-secrets-vault.md",
    "docs/architecture/ENTERPRISE_SECRETS_VAULT.md",
    "docs/architecture/secrets/SECRETS_VAULT_CAPABILITIES.v1.yaml",
    "docs/architecture/secrets/SECRETS_VAULT_DDD_CQRS.v1.yaml",
    "docs/architecture/secrets/SECRETS_VAULT_SECURITY.v1.yaml",
    "docs/architecture/secrets/SECRETS_VAULT_VALIDATION.v1.yaml",
    "backend/contexts/secrets/domain/services/secrets_platform_vault.py",
    "backend/contexts/secrets/domain/aggregates/secrets_vault_aggregates.py",
    "backend/contexts/secrets/infrastructure/acl/secrets_vault_acl.py",
    "backend/contexts/secrets/domain/services/secrets_vault_foundation.py",
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


def validate_secrets_vault_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.secrets.domain.aggregates.secrets_vault_aggregates import (
        SecretsVaultAccessAuditRoot,
        SecretsVaultAutoRotationRoot,
        SecretsVaultDynamicCredentialsRoot,
        SecretsVaultNoHardcodingRoot,
        SecretsVaultPlaintextForbiddenRoot,
        SecretsVaultSecretLeaseRoot,
        SecretsVaultSecretLifecycleRoot,
        SecretsVaultSecretOwnershipRoot,
    )
    from contexts.secrets.domain.services import secrets_platform_vault as vault
    from contexts.secrets.infrastructure.acl import secrets_vault_acl as acls

    cat = vault.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P209-G"
        and cat.get("adr") == 352
        and cat.get("sor") == "secrets"
        and cat["plaintext_secrets_forbidden"] is True
        and cat["hardcoded_credentials_forbidden"] is True
        and cat["secret_lifecycle_complete_required"] is True
        and cat["rotation_automatic_required"] is True
        and cat["secret_ownership_known_required"] is True
        and cat["secret_access_audited_required"] is True
        and cat["dynamic_credentials_required"] is True
        and cat["vault_capabilities"]["not_plaintext"] is True
        and cat["devsecops"]["not_hardcoded"] is True
        and cat["lifecycle"]["not_incomplete"] is True
        and cat["lifecycle"]["not_manual_only"] is True
        and cat["ownership"]["not_unknown"] is True
        and cat["audit"]["not_unaudited"] is True
        and cat["dynamic_secrets"]["not_unsupported"] is True
        and cat["lifecycle"]["stage_count"] >= 11
        and cat["cqrs"]["event_count"] >= 12
        and cat["cursor_outputs"]["count"] >= 20
        and "secrets_stored_in_plaintext" in cat["quality_gates"]["reject_if"]
        and "hardcoded_credentials_exist" in cat["quality_gates"]["reject_if"]
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )

    try:
        SecretsVaultPlaintextForbiddenRoot.store(
            tenant_id="t1", secret_ref="s1", plaintext=True
        )
        plain_bad = True
    except ValueError:
        plain_bad = False

    plain = SecretsVaultPlaintextForbiddenRoot.store(
        tenant_id="t1", secret_ref="s2"
    )
    plain_ok = not plain_bad and plain.is_plaintext() is False

    try:
        SecretsVaultNoHardcodingRoot.scan(
            tenant_id="t1", scan_ref="sc1", hardcoded=True
        )
        hard_bad = True
    except ValueError:
        hard_bad = False

    hard = SecretsVaultNoHardcodingRoot.scan(tenant_id="t1", scan_ref="sc2")
    hard_ok = not hard_bad and hard.has_hardcoding() is False

    try:
        SecretsVaultSecretLifecycleRoot.manage(
            tenant_id="t1", secret_ref="s3", complete=False
        )
        life_bad = True
    except ValueError:
        life_bad = False

    life = SecretsVaultSecretLifecycleRoot.manage(
        tenant_id="t1", secret_ref="s4"
    )
    life_ok = not life_bad and life.is_incomplete() is False

    try:
        SecretsVaultAutoRotationRoot.enable(
            tenant_id="t1", secret_ref="s5", manual_only=True
        )
        rot_bad = True
    except ValueError:
        rot_bad = False

    rot = SecretsVaultAutoRotationRoot.enable(tenant_id="t1", secret_ref="s6")
    rot_ok = not rot_bad and rot.is_manual_only() is False

    try:
        SecretsVaultSecretOwnershipRoot.bind(
            tenant_id="t1",
            secret_ref="s7",
            owner_ref="",
            known=False,
        )
        own_bad = True
    except ValueError:
        own_bad = False

    ownership = SecretsVaultSecretOwnershipRoot.bind(
        tenant_id="t1", secret_ref="s8", owner_ref="owner1"
    )
    own_ok = not own_bad and ownership.is_unknown() is False

    try:
        SecretsVaultAccessAuditRoot.record(
            tenant_id="t1",
            audit_ref="a1",
            action_ref="read",
            audited=False,
        )
        audit_bad = True
    except ValueError:
        audit_bad = False

    audit = SecretsVaultAccessAuditRoot.record(
        tenant_id="t1", audit_ref="a2", action_ref="read"
    )
    audit_ok = not audit_bad and audit.is_unaudited() is False

    try:
        SecretsVaultDynamicCredentialsRoot.enable(
            tenant_id="t1", engine_ref="e1", supported=False
        )
        dyn_bad = True
    except ValueError:
        dyn_bad = False

    dyn = SecretsVaultDynamicCredentialsRoot.enable(
        tenant_id="t1", engine_ref="e2"
    )
    dyn_ok = not dyn_bad and dyn.is_unsupported() is False

    lease = SecretsVaultSecretLeaseRoot.issue(
        tenant_id="t1", lease_ref="l1", secret_ref="s9"
    )
    lease_ok = "SecretLeaseRenewed" in lease.pending_events

    aggregates_ok = (
        plain_ok
        and hard_ok
        and life_ok
        and rot_ok
        and own_ok
        and audit_ok
        and dyn_ok
        and lease_ok
    )

    acl_ok = (
        acls.to_kms_encrypt(tenant_id="t1", secret_ref="s1")[
            "plaintext_forbidden"
        ]
        is True
        and acls.to_authorization_secret_access(
            tenant_id="t1", secret_ref="s1", principal_ref="u1"
        )["zero_trust_secret_access"]
        is True
        and acls.to_workflow_approval(tenant_id="t1", request_ref="r1")[
            "secret_access_approval_required"
        ]
        is True
        and acls.to_pam_ref_only(tenant_id="t1", secret_ref="s1")[
            "pam_refs_only"
        ]
        is True
        and acls.to_audit(
            tenant_id="t1", action="secrets.vault.read", resource_ref="s1"
        )["secret_access_audited_required"]
        is True
    )

    router = (
        root / "backend/contexts/secrets/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '/vault"' in router
        and "/vault/lifecycle" in router
        and "/vault/dynamic" in router
        and "/vault/rotation" in router
        and "/vault/devsecops" in router
        and "/vault/readiness" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_SECRETS_VAULT.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never secrets are stored in plaintext" in law
        and "Never hardcoded credentials exist" in law
        and "Never secret lifecycle is incomplete" in law
        and "Never rotation is manual only" in law
        and "Never secret ownership is unknown" in law
        and "Never secret access is unaudited" in law
        and "Never dynamic credentials are unsupported" in law
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
        "prompt": "P209-G",
        "adr": 352,
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
