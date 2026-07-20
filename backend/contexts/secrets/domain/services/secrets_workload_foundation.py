"""Secrets P209-H Workload Identity foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]

REQUIRED_ARTIFACTS = [
    "docs/adr/353-enterprise-secrets-workload.md",
    "docs/architecture/ENTERPRISE_SECRETS_WORKLOAD.md",
    "docs/architecture/secrets/SECRETS_WORKLOAD_CAPABILITIES.v1.yaml",
    "docs/architecture/secrets/SECRETS_WORKLOAD_DDD_CQRS.v1.yaml",
    "docs/architecture/secrets/SECRETS_WORKLOAD_SECURITY.v1.yaml",
    "docs/architecture/secrets/SECRETS_WORKLOAD_VALIDATION.v1.yaml",
    "backend/contexts/secrets/domain/services/secrets_platform_workload.py",
    "backend/contexts/secrets/domain/aggregates/secrets_workload_aggregates.py",
    "backend/contexts/secrets/infrastructure/acl/secrets_workload_acl.py",
    "backend/contexts/secrets/domain/services/secrets_workload_foundation.py",
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
    "backend/contexts/workload_identity_platform",
    "backend/contexts/spiffe_platform",
    "backend/contexts/spire_platform",
)


def validate_secrets_workload_foundation(
    *, repo_root: Path | None = None
) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.secrets.domain.aggregates.secrets_workload_aggregates import (
        SecretsWorkloadAttestationRoot,
        SecretsWorkloadAutoRotationRoot,
        SecretsWorkloadCommAuditRoot,
        SecretsWorkloadCryptoIdentityRoot,
        SecretsWorkloadMtlsEnforcementRoot,
        SecretsWorkloadOwnershipRoot,
        SecretsWorkloadSecretlessRoot,
        SecretsWorkloadTrustDomainRoot,
    )
    from contexts.secrets.domain.services import (
        secrets_platform_workload as wl,
    )
    from contexts.secrets.infrastructure.acl import (
        secrets_workload_acl as acls,
    )

    cat = wl.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P209-H"
        and cat.get("adr") == 353
        and cat.get("sor") == "secrets"
        and cat["cryptographic_workload_identity_required"] is True
        and cat["static_credentials_forbidden"] is True
        and cat["mtls_enforceable_required"] is True
        and cat["certificate_rotation_automatic_required"] is True
        and cat["trust_domains_defined_required"] is True
        and cat["workload_identity_ownership_known_required"] is True
        and cat["service_communication_audited_required"] is True
        and cat["architecture"]["not_lacking_crypto"] is True
        and cat["secretless"]["not_static_required"] is True
        and cat["mtls"]["not_unenforceable"] is True
        and cat["lifecycle"]["not_manual"] is True
        and cat["trust_domain"]["not_undefined"] is True
        and cat["ownership"]["not_unknown"] is True
        and cat["audit"]["not_unaudited"] is True
        and cat["lifecycle"]["stage_count"] >= 9
        and cat["cqrs"]["event_count"] >= 12
        and cat["cursor_outputs"]["count"] >= 20
        and "workloads_lack_cryptographic_identity"
        in cat["quality_gates"]["reject_if"]
        and "static_credentials_required" in cat["quality_gates"]["reject_if"]
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )

    try:
        SecretsWorkloadCryptoIdentityRoot.issue(
            tenant_id="t1",
            workload_ref="w1",
            spiffe_id="",
            cryptographic=False,
        )
        crypto_bad = True
    except ValueError:
        crypto_bad = False

    crypto = SecretsWorkloadCryptoIdentityRoot.issue(
        tenant_id="t1",
        workload_ref="w2",
        spiffe_id="spiffe://marpich/ns/default/sa/api",
    )
    crypto_ok = not crypto_bad and crypto.lacks_crypto() is False

    try:
        SecretsWorkloadSecretlessRoot.enable(
            tenant_id="t1", workload_ref="w3", static_required=True
        )
        sec_bad = True
    except ValueError:
        sec_bad = False

    secretless = SecretsWorkloadSecretlessRoot.enable(
        tenant_id="t1", workload_ref="w4"
    )
    sec_ok = not sec_bad and secretless.requires_static() is False

    try:
        SecretsWorkloadMtlsEnforcementRoot.enforce(
            tenant_id="t1", mesh_ref="m1", enforceable=False
        )
        mtls_bad = True
    except ValueError:
        mtls_bad = False

    mtls = SecretsWorkloadMtlsEnforcementRoot.enforce(
        tenant_id="t1", mesh_ref="m2"
    )
    mtls_ok = not mtls_bad and mtls.is_unenforceable() is False

    try:
        SecretsWorkloadAutoRotationRoot.enable(
            tenant_id="t1", identity_ref="i1", manual=True
        )
        rot_bad = True
    except ValueError:
        rot_bad = False

    rot = SecretsWorkloadAutoRotationRoot.enable(
        tenant_id="t1", identity_ref="i2"
    )
    rot_ok = not rot_bad and rot.is_manual() is False

    try:
        SecretsWorkloadTrustDomainRoot.define(
            tenant_id="t1", trust_domain="", defined=False
        )
        td_bad = True
    except ValueError:
        td_bad = False

    td = SecretsWorkloadTrustDomainRoot.define(
        tenant_id="t1", trust_domain="marpich.local"
    )
    td_ok = not td_bad and td.is_undefined() is False

    try:
        SecretsWorkloadOwnershipRoot.bind(
            tenant_id="t1",
            workload_ref="w5",
            owner_ref="",
            known=False,
        )
        own_bad = True
    except ValueError:
        own_bad = False

    ownership = SecretsWorkloadOwnershipRoot.bind(
        tenant_id="t1", workload_ref="w6", owner_ref="owner1"
    )
    own_ok = not own_bad and ownership.is_unknown() is False

    try:
        SecretsWorkloadCommAuditRoot.record(
            tenant_id="t1",
            audit_ref="a1",
            connection_ref="c1",
            audited=False,
        )
        audit_bad = True
    except ValueError:
        audit_bad = False

    audit = SecretsWorkloadCommAuditRoot.record(
        tenant_id="t1", audit_ref="a2", connection_ref="c2"
    )
    audit_ok = not audit_bad and audit.is_unaudited() is False

    att = SecretsWorkloadAttestationRoot.attest(
        tenant_id="t1", workload_ref="w7"
    )
    att_ok = "WorkloadAttested" in att.pending_events

    aggregates_ok = (
        crypto_ok
        and sec_ok
        and mtls_ok
        and rot_ok
        and td_ok
        and own_ok
        and audit_ok
        and att_ok
    )

    acl_ok = (
        acls.to_spiffe(
            tenant_id="t1",
            workload_ref="w1",
            spiffe_id="spiffe://marpich/ns/x/sa/y",
        )["cryptographic_workload_identity_required"]
        is True
        and acls.to_authorization_workload(
            tenant_id="t1", workload_ref="w1", principal_ref="u1"
        )["via_p208"]
        is True
        and acls.to_mesh_mtls(tenant_id="t1", mesh_ref="m1")[
            "mtls_enforceable_required"
        ]
        is True
        and acls.to_pki_svid(tenant_id="t1", identity_ref="i1")[
            "svid_issuance"
        ]
        is True
        and acls.to_audit(
            tenant_id="t1",
            action="secrets.workload.connect",
            resource_ref="c1",
        )["service_communication_audited_required"]
        is True
    )

    router = (
        root / "backend/contexts/secrets/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '/workload"' in router
        and "/workload/spiffe" in router
        and "/workload/mtls" in router
        and "/workload/trust-domain" in router
        and "/workload/secretless" in router
        and "/workload/readiness" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_SECRETS_WORKLOAD.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never workloads lack cryptographic identity" in law
        and "Never static credentials are required" in law
        and "Never mTLS cannot be enforced" in law
        and "Never certificate rotation is manual" in law
        and "Never trust domains are undefined" in law
        and "Never workload identity ownership is unknown" in law
        and "Never service communication is unaudited" in law
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
        "prompt": "P209-H",
        "adr": 353,
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
