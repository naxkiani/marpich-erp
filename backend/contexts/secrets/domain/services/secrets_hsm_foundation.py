"""Secrets P209-K HSM / AI Crypto / PQC foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]

REQUIRED_ARTIFACTS = [
    "docs/adr/356-enterprise-secrets-hsm.md",
    "docs/architecture/ENTERPRISE_SECRETS_HSM.md",
    "docs/architecture/secrets/SECRETS_HSM_CAPABILITIES.v1.yaml",
    "docs/architecture/secrets/SECRETS_HSM_DDD_CQRS.v1.yaml",
    "docs/architecture/secrets/SECRETS_HSM_SECURITY.v1.yaml",
    "docs/architecture/secrets/SECRETS_HSM_VALIDATION.v1.yaml",
    "backend/contexts/secrets/domain/services/secrets_platform_hsm.py",
    "backend/contexts/secrets/domain/aggregates/secrets_hsm_aggregates.py",
    "backend/contexts/secrets/infrastructure/acl/secrets_hsm_acl.py",
    "backend/contexts/secrets/domain/services/secrets_hsm_foundation.py",
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
    "backend/contexts/confidential_computing_platform",
    "backend/contexts/pqc_platform",
    "backend/contexts/crypto_ai_platform",
    "backend/contexts/secrets_pam",
    "backend/contexts/enterprise_pki",
    "backend/contexts/workload_identity_platform",
    "backend/contexts/spiffe_platform",
    "backend/contexts/spire_platform",
)


def validate_secrets_hsm_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.secrets.domain.aggregates.secrets_hsm_aggregates import (
        SecretsHsmAiDecisionAuditRoot,
        SecretsHsmConfidentialAttestRoot,
        SecretsHsmCryptoAgilityRoot,
        SecretsHsmDualControlRoot,
        SecretsHsmHardwareTrustRoot,
        SecretsHsmPqcMigrationRoot,
        SecretsHsmProtectionRoot,
        SecretsHsmRiskMeasurableRoot,
    )
    from contexts.secrets.domain.services import secrets_platform_hsm as hsm
    from contexts.secrets.infrastructure.acl import secrets_hsm_acl as acls

    cat = hsm.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P209-K"
        and cat.get("adr") == 356
        and cat.get("sor") == "secrets"
        and cat["cryptographic_agility_required"] is True
        and cat["hsm_protection_required"] is True
        and cat["ai_crypto_decisions_auditable_required"] is True
        and cat["confidential_attestation_required"] is True
        and cat["pqc_migration_strategy_required"] is True
        and cat["hardware_trust_validated_required"] is True
        and cat["cryptographic_risks_measurable_required"] is True
        and cat["crypto_agility"]["not_cannot_evolve"] is True
        and cat["hsm"]["not_absent"] is True
        and cat["ai_crypto"]["not_unauditable"] is True
        and cat["confidential_computing"]["not_lacking_attestation"] is True
        and cat["pqc"]["not_undefined"] is True
        and cat["hardware_trust"]["not_unvalidated"] is True
        and cat["risk"]["not_unmeasurable"] is True
        and cat["cqrs"]["event_count"] >= 12
        and cat["cursor_outputs"]["count"] >= 20
        and "hsm_protection_is_absent" in cat["quality_gates"]["reject_if"]
        and "pqc_migration_strategy_undefined"
        in cat["quality_gates"]["reject_if"]
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )

    try:
        SecretsHsmCryptoAgilityRoot.enable(
            tenant_id="t1", algorithm_ref="aes", can_evolve=False
        )
        ag_bad = True
    except ValueError:
        ag_bad = False

    ag = SecretsHsmCryptoAgilityRoot.enable(
        tenant_id="t1", algorithm_ref="aes-gcm"
    )
    ag_ok = not ag_bad and ag.cannot_evolve() is False

    try:
        SecretsHsmProtectionRoot.verify(
            tenant_id="t1", hsm_ref="h1", protected=False
        )
        prot_bad = True
    except ValueError:
        prot_bad = False

    prot = SecretsHsmProtectionRoot.verify(tenant_id="t1", hsm_ref="h2")
    prot_ok = not prot_bad and prot.is_absent() is False

    try:
        SecretsHsmAiDecisionAuditRoot.record(
            tenant_id="t1", decision_ref="d1", auditable=False
        )
        ai_bad = True
    except ValueError:
        ai_bad = False

    ai = SecretsHsmAiDecisionAuditRoot.record(
        tenant_id="t1", decision_ref="d2"
    )
    ai_ok = not ai_bad and ai.is_unauditable() is False

    try:
        SecretsHsmConfidentialAttestRoot.attest(
            tenant_id="t1", workload_ref="w1", attested=False
        )
        cc_bad = True
    except ValueError:
        cc_bad = False

    cc = SecretsHsmConfidentialAttestRoot.attest(
        tenant_id="t1", workload_ref="w2"
    )
    cc_ok = not cc_bad and cc.lacks_attestation() is False

    try:
        SecretsHsmPqcMigrationRoot.define(
            tenant_id="t1", strategy_ref="s1", defined=False
        )
        pqc_bad = True
    except ValueError:
        pqc_bad = False

    pqc = SecretsHsmPqcMigrationRoot.define(
        tenant_id="t1", strategy_ref="s2"
    )
    pqc_ok = not pqc_bad and pqc.is_undefined() is False

    try:
        SecretsHsmHardwareTrustRoot.validate(
            tenant_id="t1", hardware_ref="hw1", validated=False
        )
        hw_bad = True
    except ValueError:
        hw_bad = False

    hw = SecretsHsmHardwareTrustRoot.validate(
        tenant_id="t1", hardware_ref="hw2"
    )
    hw_ok = not hw_bad and hw.is_unvalidated() is False

    try:
        SecretsHsmRiskMeasurableRoot.measure(
            tenant_id="t1", risk_ref="r1", measurable=False
        )
        risk_bad = True
    except ValueError:
        risk_bad = False

    risk = SecretsHsmRiskMeasurableRoot.measure(
        tenant_id="t1", risk_ref="r2", score=0.42
    )
    risk_ok = not risk_bad and risk.is_unmeasurable() is False

    dual = SecretsHsmDualControlRoot.enforce(
        tenant_id="t1", ceremony_ref="cer1"
    )
    dual_ok = "DualControlEnforced" in dual.pending_events

    aggregates_ok = (
        ag_ok
        and prot_ok
        and ai_ok
        and cc_ok
        and pqc_ok
        and hw_ok
        and risk_ok
        and dual_ok
    )

    acl_ok = (
        acls.to_integration_hsm(tenant_id="t1", hsm_ref="h1")[
            "hsm_protection_required"
        ]
        is True
        and acls.to_ai_crypto_infer(
            tenant_id="t1", surface="crypto_risk", context={}
        )["ai_crypto_decisions_auditable_required"]
        is True
        and acls.to_workflow_dual_control(
            tenant_id="t1", ceremony_ref="cer1"
        )["dual_control_required"]
        is True
        and acls.to_authorization_hsm(
            tenant_id="t1", hsm_ref="h1", principal_ref="u1"
        )["zero_trust_hsm_access"]
        is True
        and acls.to_audit(
            tenant_id="t1", action="secrets.hsm.attest", resource_ref="w1"
        )["hardware_trust_validated_required"]
        is True
    )

    router = (
        root / "backend/contexts/secrets/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '/hsm"' in router
        and "/hsm/ai-crypto" in router
        and "/hsm/pqc" in router
        and "/hsm/confidential" in router
        and "/hsm/agility" in router
        and "/hsm/readiness" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_SECRETS_HSM.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never cryptographic algorithms cannot evolve" in law
        and "Never HSM protection is absent" in law
        and "Never AI cryptographic decisions are unauditable" in law
        and "Never confidential workloads lack attestation" in law
        and "Never PQC migration strategy is undefined" in law
        and "Never hardware trust is not validated" in law
        and "Never cryptographic risks are not measurable" in law
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
        "prompt": "P209-K",
        "adr": 356,
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
