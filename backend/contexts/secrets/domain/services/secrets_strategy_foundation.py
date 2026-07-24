"""Secrets P209-A Strategy foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]

REQUIRED_ARTIFACTS = [
    "docs/adr/346-enterprise-secrets-strategy.md",
    "docs/architecture/ENTERPRISE_SECRETS_STRATEGY.md",
    "docs/architecture/secrets/SECRETS_STRATEGY_CAPABILITIES.v1.yaml",
    "docs/architecture/secrets/SECRETS_STRATEGY_DDD_CQRS.v1.yaml",
    "docs/architecture/secrets/SECRETS_STRATEGY_SECURITY.v1.yaml",
    "docs/architecture/secrets/SECRETS_STRATEGY_VALIDATION.v1.yaml",
    "backend/contexts/secrets/domain/services/secrets_platform_strategy.py",
    "backend/contexts/secrets/domain/aggregates/secrets_strategy_aggregates.py",
    "backend/contexts/secrets/infrastructure/acl/secrets_strategy_acl.py",
    "backend/contexts/secrets/domain/services/secrets_strategy_foundation.py",
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


def validate_secrets_strategy_foundation(
    *, repo_root: Path | None = None
) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.secrets.domain.aggregates.secrets_strategy_aggregates import (
        SecretsCertLifecycleStrategyRoot,
        SecretsCryptoAuditStrategyRoot,
        SecretsCryptoLifecycleRoot,
        SecretsGovernedStoreRoot,
        SecretsHsmStrategyRoot,
        SecretsKeyExportPolicyRoot,
        SecretsRootCaSecurityRoot,
        SecretsStrategyProfileRoot,
    )
    from contexts.secrets.domain.services import (
        secrets_platform_strategy as strat,
    )
    from contexts.secrets.infrastructure.acl import (
        secrets_strategy_acl as acls,
    )

    cat = strat.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P209-A"
        and cat.get("adr") == 346
        and cat.get("sor") == "secrets"
        and cat["secrets_outside_governed_stores_forbidden"] is True
        and cat["keys_exportable_without_policy_forbidden"] is True
        and cat["manual_certificate_management_forbidden"] is True
        and cat["root_ca_security_inadequate_forbidden"] is True
        and cat["hsm_integration_required"] is True
        and cat["cryptographic_lifecycle_complete_required"] is True
        and cat["cryptographic_operations_audit_required"] is True
        and cat["secrets_management"]["not_outside_governed"] is True
        and cat["kms"]["not_exportable_without_policy"] is True
        and cat["pki"]["not_manual"] is True
        and cat["root_of_trust"]["not_inadequate"] is True
        and cat["hsm"]["not_absent"] is True
        and cat["lifecycle"]["not_incomplete"] is True
        and cat["security"]["not_unaudited"] is True
        and cat["primary_domains"]["count"] >= 12
        and cat["ddd"]["aggregate_count"] >= 8
        and cat["cqrs"]["event_count"] >= 12
        and cat["cursor_outputs"]["count"] >= 20
        and "secrets_stored_outside_governed_stores"
        in cat["quality_gates"]["reject_if"]
        and "keys_exportable_without_policy"
        in cat["quality_gates"]["reject_if"]
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )

    try:
        SecretsGovernedStoreRoot.register(
            tenant_id="t1", store_ref="s1", outside=True
        )
        outside = True
    except ValueError:
        outside = False

    store = SecretsGovernedStoreRoot.register(tenant_id="t1", store_ref="s2")
    store_ok = not outside and store.is_outside() is False

    try:
        SecretsKeyExportPolicyRoot.define(
            tenant_id="t1",
            policy_ref="p1",
            key_ref="k1",
            export_allowed=True,
            policy_present=False,
        )
        export_bad = True
    except ValueError:
        export_bad = False

    export = SecretsKeyExportPolicyRoot.define(
        tenant_id="t1", policy_ref="p2", key_ref="k2"
    )
    export_ok = (
        not export_bad and export.is_exportable_without_policy() is False
    )

    try:
        SecretsCertLifecycleStrategyRoot.set(
            tenant_id="t1", strategy_ref="c1", manual=True
        )
        cert_bad = True
    except ValueError:
        cert_bad = False

    cert = SecretsCertLifecycleStrategyRoot.set(
        tenant_id="t1", strategy_ref="c2"
    )
    cert_ok = not cert_bad and cert.is_manual() is False

    try:
        SecretsRootCaSecurityRoot.harden(
            tenant_id="t1", ca_ref="ca1", offline=False
        )
        ca_bad = True
    except ValueError:
        ca_bad = False

    ca = SecretsRootCaSecurityRoot.harden(tenant_id="t1", ca_ref="ca2")
    ca_ok = not ca_bad and ca.is_inadequate() is False

    try:
        SecretsHsmStrategyRoot.bind(
            tenant_id="t1", binding_ref="h1", present=False
        )
        hsm_bad = True
    except ValueError:
        hsm_bad = False

    hsm = SecretsHsmStrategyRoot.bind(tenant_id="t1", binding_ref="h2")
    hsm_ok = not hsm_bad and hsm.is_absent() is False

    try:
        SecretsCryptoLifecycleRoot.complete_review(
            tenant_id="t1", lifecycle_ref="l1", complete=False
        )
        life_bad = True
    except ValueError:
        life_bad = False

    life = SecretsCryptoLifecycleRoot.complete_review(
        tenant_id="t1", lifecycle_ref="l2"
    )
    life_ok = not life_bad and life.is_incomplete() is False

    try:
        SecretsCryptoAuditStrategyRoot.record(
            tenant_id="t1",
            audit_ref="a1",
            operation_ref="sign",
            audited=False,
        )
        audit_bad = True
    except ValueError:
        audit_bad = False

    audit = SecretsCryptoAuditStrategyRoot.record(
        tenant_id="t1", audit_ref="a2", operation_ref="sign"
    )
    audit_ok = not audit_bad and audit.is_unaudited() is False

    profile = SecretsStrategyProfileRoot.publish(
        tenant_id="t1", profile_ref="strat1"
    )
    profile_ok = "StrategyPublished" in profile.pending_events

    aggregates_ok = (
        store_ok
        and export_ok
        and cert_ok
        and ca_ok
        and hsm_ok
        and life_ok
        and audit_ok
        and profile_ok
    )

    acl_ok = (
        acls.to_governed_store(tenant_id="t1", store_ref="s1")[
            "outside_governed_forbidden"
        ]
        is True
        and acls.to_key_export_policy(tenant_id="t1", key_ref="k1")[
            "export_without_policy_forbidden"
        ]
        is True
        and acls.to_hsm(tenant_id="t1", operation="sign", key_ref="k1")[
            "hsm_strategy_required"
        ]
        is True
        and acls.to_audit(
            tenant_id="t1", action="secrets.strategy", resource_ref="r1"
        )["crypto_ops_must_be_audited"]
        is True
    )

    router = (
        root / "backend/contexts/secrets/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '/strategy"' in router
        and "/strategy/root-of-trust" in router
        and "/strategy/kms" in router
        and "/strategy/hsm" in router
        and "/strategy/readiness" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_SECRETS_STRATEGY.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never secrets are stored outside governed secret stores" in law
        and "Never keys are exportable without policy" in law
        and "Never certificates are manually managed" in law
        and "Never Root CA security is inadequate" in law
        and "Never HSM integration is absent" in law
        and "Never cryptographic lifecycle is incomplete" in law
        and "Never cryptographic operations are unaudited" in law
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
        "prompt": "P209-A",
        "adr": 346,
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
