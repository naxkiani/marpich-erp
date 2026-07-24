"""Secrets P209-J Signing / Supply Chain foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]

REQUIRED_ARTIFACTS = [
    "docs/adr/355-enterprise-secrets-signing.md",
    "docs/architecture/ENTERPRISE_SECRETS_SIGNING.md",
    "docs/architecture/secrets/SECRETS_SIGNING_CAPABILITIES.v1.yaml",
    "docs/architecture/secrets/SECRETS_SIGNING_DDD_CQRS.v1.yaml",
    "docs/architecture/secrets/SECRETS_SIGNING_SECURITY.v1.yaml",
    "docs/architecture/secrets/SECRETS_SIGNING_VALIDATION.v1.yaml",
    "backend/contexts/secrets/domain/services/secrets_platform_signing.py",
    "backend/contexts/secrets/domain/aggregates/secrets_signing_aggregates.py",
    "backend/contexts/secrets/infrastructure/acl/secrets_signing_acl.py",
    "backend/contexts/secrets/domain/services/secrets_signing_foundation.py",
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
    "backend/contexts/code_signing_platform",
    "backend/contexts/supply_chain_trust_platform",
    "backend/contexts/digital_signature_platform",
    "backend/contexts/secrets_pam",
    "backend/contexts/enterprise_pki",
    "backend/contexts/workload_identity_platform",
    "backend/contexts/spiffe_platform",
    "backend/contexts/spire_platform",
)


def validate_secrets_signing_foundation(
    *, repo_root: Path | None = None
) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.secrets.domain.aggregates.secrets_signing_aggregates import (
        SecretsSigningArtifactSignedRoot,
        SecretsSigningDeploymentTrustRoot,
        SecretsSigningKeyManagedRoot,
        SecretsSigningOpAuditRoot,
        SecretsSigningOwnershipRoot,
        SecretsSigningProvenanceRoot,
        SecretsSigningReleaseGateRoot,
        SecretsSigningSbomVerifyRoot,
    )
    from contexts.secrets.domain.services import (
        secrets_platform_signing as signing,
    )
    from contexts.secrets.infrastructure.acl import secrets_signing_acl as acls

    cat = signing.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P209-J"
        and cat.get("adr") == 355
        and cat.get("sor") == "secrets"
        and cat["unsigned_artifacts_forbidden"] is True
        and cat["signing_keys_managed_required"] is True
        and cat["supply_chain_provenance_required"] is True
        and cat["sbom_verification_required"] is True
        and cat["deployment_trust_validatable_required"] is True
        and cat["artifact_ownership_known_required"] is True
        and cat["signature_operations_audited_required"] is True
        and cat["code_signing"]["not_unsigned"] is True
        and cat["hsm_signing"]["not_unmanaged"] is True
        and cat["supply_chain"]["not_unavailable"] is True
        and cat["sbom"]["not_absent"] is True
        and cat["deployment_trust"]["not_unvalidatable"] is True
        and cat["ownership"]["not_unknown"] is True
        and cat["audit"]["not_unaudited"] is True
        and cat["cqrs"]["event_count"] >= 12
        and cat["cursor_outputs"]["count"] >= 20
        and "software_artifacts_are_unsigned"
        in cat["quality_gates"]["reject_if"]
        and "sbom_verification_absent" in cat["quality_gates"]["reject_if"]
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )

    try:
        SecretsSigningArtifactSignedRoot.sign(
            tenant_id="t1", artifact_ref="a1", signed=False
        )
        art_bad = True
    except ValueError:
        art_bad = False

    art = SecretsSigningArtifactSignedRoot.sign(
        tenant_id="t1", artifact_ref="a2"
    )
    art_ok = not art_bad and art.is_unsigned() is False

    try:
        SecretsSigningKeyManagedRoot.manage(
            tenant_id="t1", key_ref="k1", managed=False
        )
        key_bad = True
    except ValueError:
        key_bad = False

    key = SecretsSigningKeyManagedRoot.manage(tenant_id="t1", key_ref="k2")
    key_ok = not key_bad and key.is_unmanaged() is False

    try:
        SecretsSigningProvenanceRoot.validate(
            tenant_id="t1", provenance_ref="p1", available=False
        )
        prov_bad = True
    except ValueError:
        prov_bad = False

    prov = SecretsSigningProvenanceRoot.validate(
        tenant_id="t1", provenance_ref="p2"
    )
    prov_ok = not prov_bad and prov.is_unavailable() is False

    try:
        SecretsSigningSbomVerifyRoot.verify(
            tenant_id="t1", sbom_ref="s1", verified=False
        )
        sbom_bad = True
    except ValueError:
        sbom_bad = False

    sbom = SecretsSigningSbomVerifyRoot.verify(tenant_id="t1", sbom_ref="s2")
    sbom_ok = not sbom_bad and sbom.is_absent() is False

    try:
        SecretsSigningDeploymentTrustRoot.validate(
            tenant_id="t1", deployment_ref="d1", validatable=False
        )
        dep_bad = True
    except ValueError:
        dep_bad = False

    dep = SecretsSigningDeploymentTrustRoot.validate(
        tenant_id="t1", deployment_ref="d2"
    )
    dep_ok = not dep_bad and dep.is_unvalidatable() is False

    try:
        SecretsSigningOwnershipRoot.bind(
            tenant_id="t1",
            artifact_ref="a3",
            owner_ref="",
            known=False,
        )
        own_bad = True
    except ValueError:
        own_bad = False

    ownership = SecretsSigningOwnershipRoot.bind(
        tenant_id="t1", artifact_ref="a4", owner_ref="owner1"
    )
    own_ok = not own_bad and ownership.is_unknown() is False

    try:
        SecretsSigningOpAuditRoot.record(
            tenant_id="t1",
            audit_ref="au1",
            operation_ref="op1",
            audited=False,
        )
        audit_bad = True
    except ValueError:
        audit_bad = False

    audit = SecretsSigningOpAuditRoot.record(
        tenant_id="t1", audit_ref="au2", operation_ref="op2"
    )
    audit_ok = not audit_bad and audit.is_unaudited() is False

    release = SecretsSigningReleaseGateRoot.approve(
        tenant_id="t1", release_ref="r1"
    )
    release_ok = "ReleaseApproved" in release.pending_events

    aggregates_ok = (
        art_ok
        and key_ok
        and prov_ok
        and sbom_ok
        and dep_ok
        and own_ok
        and audit_ok
        and release_ok
    )

    acl_ok = (
        acls.to_kms_signing_key(tenant_id="t1", key_ref="k1")[
            "signing_keys_managed_required"
        ]
        is True
        and acls.to_hsm_sign(tenant_id="t1", key_ref="k1")[
            "hsm_signing_required"
        ]
        is True
        and acls.to_pki_code_signing_cert(tenant_id="t1", cert_ref="c1")[
            "via_pki"
        ]
        is True
        and acls.to_workflow_release(tenant_id="t1", release_ref="r1")[
            "multi_person_approval_required"
        ]
        is True
        and acls.to_integration_cicd(tenant_id="t1", pipeline_ref="p1")[
            "no_embedded_vendor_sdk"
        ]
        is True
        and acls.to_audit(
            tenant_id="t1", action="secrets.signing.sign", resource_ref="a1"
        )["signature_operations_audited_required"]
        is True
    )

    router = (
        root / "backend/contexts/secrets/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '/signing"' in router
        and "/signing/code-signing" in router
        and "/signing/sbom" in router
        and "/signing/supply-chain" in router
        and "/signing/deployment-trust" in router
        and "/signing/readiness" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_SECRETS_SIGNING.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never software artifacts are unsigned" in law
        and "Never signing keys are unmanaged" in law
        and "Never supply chain provenance is unavailable" in law
        and "Never SBOM verification is absent" in law
        and "Never deployment trust cannot be validated" in law
        and "Never artifact ownership is unknown" in law
        and "Never signature operations are unaudited" in law
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
        "prompt": "P209-J",
        "adr": 355,
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
