"""Secrets P209 Cryptographic Trust foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]

REQUIRED_ARTIFACTS = [
    "docs/adr/345-enterprise-cryptographic-trust.md",
    "docs/architecture/ENTERPRISE_CRYPTOGRAPHIC_TRUST.md",
    "docs/architecture/secrets/SECRETS_CAPABILITIES.v1.yaml",
    "docs/architecture/secrets/SECRETS_DDD_CQRS.v1.yaml",
    "docs/architecture/secrets/SECRETS_SECURITY.v1.yaml",
    "docs/architecture/secrets/SECRETS_VALIDATION.v1.yaml",
    "backend/contexts/secrets/domain/services/secrets_platform.py",
    "backend/contexts/secrets/domain/aggregates/secrets_crypto_aggregates.py",
    "backend/contexts/secrets/infrastructure/acl/secrets_acl.py",
    "backend/contexts/secrets/domain/services/secrets_foundation.py",
    "backend/contexts/secrets/presentation/router.py",
    "backend/contexts/secrets/context.yaml",
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


def validate_secrets_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.secrets.domain.aggregates.secrets_crypto_aggregates import (
        SecretsCertificateRoot,
        SecretsCryptoAgilityRoot,
        SecretsEnvelopeRoot,
        SecretsHsmBindingRoot,
        SecretsKeyLifecycleRoot,
        SecretsMaterialRoot,
        SecretsTrustAuditRoot,
        SecretsWorkloadIdentityRoot,
    )
    from contexts.secrets.domain.services import secrets_platform as plat
    from contexts.secrets.infrastructure.acl import secrets_acl as acls

    cat = plat.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P209"
        and cat.get("adr") == 345
        and cat.get("sor") == "secrets"
        and cat["plaintext_secrets_forbidden"] is True
        and cat["ungoverned_keys_forbidden"] is True
        and cat["manual_certificate_management_forbidden"] is True
        and cat["hsm_integration_required"] is True
        and cat["cryptographic_agility_required"] is True
        and cat["verifiable_workload_identity_required"] is True
        and cat["auditable_trust_required"] is True
        and cat["domains"]["not_plaintext"] is True
        and cat["pki"]["not_manual"] is True
        and cat["kms"]["not_ungoverned"] is True
        and cat["hsm"]["not_absent"] is True
        and cat["pqc"]["not_unsupported"] is True
        and cat["workload_identity"]["not_unverifiable"] is True
        and cat["security"]["not_unauditable"] is True
        and cat["domains"]["count"] >= 12
        and cat["ddd"]["aggregate_count"] >= 8
        and cat["cqrs"]["event_count"] >= 12
        and cat["cursor_outputs"]["count"] >= 20
        and cat["integrations"]["crypto_integration_complete"] is True
        and "secrets_stored_in_plaintext" in cat["quality_gates"]["reject_if"]
        and "hsm_integration_absent" in cat["quality_gates"]["reject_if"]
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )

    try:
        SecretsMaterialRoot.create(
            tenant_id="t1", secret_ref="s1", plaintext=True
        )
        plain = True
    except ValueError:
        plain = False

    material = SecretsMaterialRoot.create(tenant_id="t1", secret_ref="s2")
    material_ok = not plain and material.is_plaintext() is False

    try:
        SecretsKeyLifecycleRoot.create(
            tenant_id="t1", key_ref="k1", governed=False
        )
        key_bad = True
    except ValueError:
        key_bad = False

    key = SecretsKeyLifecycleRoot.create(tenant_id="t1", key_ref="k2")
    key.rotate()
    key_ok = not key_bad and key.is_ungoverned() is False

    try:
        SecretsCertificateRoot.issue(
            tenant_id="t1", certificate_ref="c1", manual=True
        )
        cert_bad = True
    except ValueError:
        cert_bad = False

    cert = SecretsCertificateRoot.issue(tenant_id="t1", certificate_ref="c2")
    cert_ok = not cert_bad and cert.is_manual() is False

    try:
        SecretsHsmBindingRoot.bind(
            tenant_id="t1", binding_ref="h1", hsm_bound=False
        )
        hsm_bad = True
    except ValueError:
        hsm_bad = False

    hsm = SecretsHsmBindingRoot.bind(tenant_id="t1", binding_ref="h2")
    hsm_ok = not hsm_bad and hsm.is_absent() is False

    try:
        SecretsCryptoAgilityRoot.enable(
            tenant_id="t1", agility_ref="a1", supported=False
        )
        agility_bad = True
    except ValueError:
        agility_bad = False

    agility = SecretsCryptoAgilityRoot.enable(
        tenant_id="t1", agility_ref="a2"
    )
    agility_ok = not agility_bad and agility.is_unsupported() is False

    try:
        SecretsWorkloadIdentityRoot.issue(
            tenant_id="t1",
            workload_ref="w1",
            spiffe_id="",
            verifiable=False,
        )
        wl_bad = True
    except ValueError:
        wl_bad = False

    wl = SecretsWorkloadIdentityRoot.issue(
        tenant_id="t1",
        workload_ref="w2",
        spiffe_id="spiffe://marpich/ns/default/sa/api",
    )
    wl_ok = not wl_bad and wl.is_unverifiable() is False

    try:
        SecretsTrustAuditRoot.record(
            tenant_id="t1", trust_ref="tr1", audited=False
        )
        audit_bad = True
    except ValueError:
        audit_bad = False

    audit = SecretsTrustAuditRoot.record(tenant_id="t1", trust_ref="tr2")
    audit_ok = not audit_bad and audit.is_unauditable() is False

    envelope = SecretsEnvelopeRoot.wrap(
        tenant_id="t1",
        envelope_ref="e1",
        dek_ref="dek1",
        kek_ref="kek1",
    )
    envelope_ok = envelope.dek_ref == "dek1"

    aggregates_ok = (
        material_ok
        and key_ok
        and cert_ok
        and hsm_ok
        and agility_ok
        and wl_ok
        and audit_ok
        and envelope_ok
    )

    acl_ok = (
        acls.to_pam_ref(tenant_id="t1", secret_ref="s1")[
            "material_stays_in_secrets"
        ]
        is True
        and acls.to_hsm(tenant_id="t1", operation="sign", key_ref="k1")[
            "hsm_required"
        ]
        is True
        and acls.to_spiffe(
            tenant_id="t1",
            workload_ref="w1",
            spiffe_id="spiffe://x",
        )["verifiable_workload_identity"]
        is True
        and acls.to_audit(
            tenant_id="t1", action="secrets.rotate", resource_ref="s1"
        )["trust_relationships_audited"]
        is True
        and acls.to_ai_infer(tenant_id="t1", surface="crypto", context={})[
            "via_ai_platform"
        ]
        is True
    )

    router = (
        root / "backend/contexts/secrets/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        'prefix="/secrets"' in router
        and "/pki" in router
        and "/kms" in router
        and "/hsm" in router
        and "/readiness" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_CRYPTOGRAPHIC_TRUST.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never secrets are stored in plaintext" in law
        and "Never keys exist outside governed lifecycle" in law
        and "Never certificates are manually managed" in law
        and "Never HSM integration is absent" in law
        and "Never cryptographic agility is unsupported" in law
        and "Never workload identities are unverifiable" in law
        and "Never trust relationships cannot be audited" in law
    )

    registry = (root / "backend/contexts/registry.py").read_text(
        encoding="utf-8"
    )
    registry_ok = 'id="secrets"' in registry or "SECRETS =" in registry

    startup = (
        root / "backend/core/presentation/api/startup_registry.py"
    ).read_text(encoding="utf-8")
    startup_ok = "contexts.secrets" in startup

    passed = (
        not missing
        and not sibling
        and catalog_ok
        and aggregates_ok
        and acl_ok
        and router_ok
        and doc_ok
        and registry_ok
        and startup_ok
    )
    return {
        "prompt": "P209",
        "adr": 345,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "catalog": catalog_ok,
        "aggregates": aggregates_ok,
        "acl": acl_ok,
        "router": router_ok,
        "documentation": doc_ok,
        "registry": registry_ok,
        "startup": startup_ok,
        "sor": "secrets",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
