"""Secrets P209-L CQRS / Events / APIs / Microservices foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]

REQUIRED_ARTIFACTS = [
    "docs/adr/357-enterprise-secrets-ops.md",
    "docs/architecture/ENTERPRISE_SECRETS_OPS.md",
    "docs/architecture/secrets/SECRETS_OPS_CAPABILITIES.v1.yaml",
    "docs/architecture/secrets/SECRETS_OPS_DDD_CQRS.v1.yaml",
    "docs/architecture/secrets/SECRETS_OPS_SECURITY.v1.yaml",
    "docs/architecture/secrets/SECRETS_OPS_VALIDATION.v1.yaml",
    "backend/contexts/secrets/domain/services/secrets_platform_ops.py",
    "backend/contexts/secrets/domain/aggregates/secrets_ops_aggregates.py",
    "backend/contexts/secrets/infrastructure/acl/secrets_ops_acl.py",
    "backend/contexts/secrets/domain/services/secrets_ops_foundation.py",
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
    "backend/contexts/ops_platform",
    "backend/contexts/crypto_ops_platform",
    "backend/contexts/secrets_microservices_platform",
    "backend/contexts/secrets_pam",
    "backend/contexts/enterprise_pki",
    "backend/contexts/workload_identity_platform",
    "backend/contexts/spiffe_platform",
    "backend/contexts/spire_platform",
)


def validate_secrets_ops_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.secrets.domain.aggregates.secrets_ops_aggregates import (
        SecretsOpsApiSecurityRoot,
        SecretsOpsCryptoAuditableRoot,
        SecretsOpsDbOwnershipRoot,
        SecretsOpsEventsPresentRoot,
        SecretsOpsObservabilityRoot,
        SecretsOpsScalableDeployRoot,
        SecretsOpsSeriesCloseoutRoot,
        SecretsOpsServiceOwnershipRoot,
    )
    from contexts.secrets.domain.services import secrets_platform_ops as ops
    from contexts.secrets.infrastructure.acl import secrets_ops_acl as acls

    cat = ops.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P209-L"
        and cat.get("adr") == 357
        and cat.get("sor") == "secrets"
        and cat["no_shared_databases_required"] is True
        and cat["events_present_required"] is True
        and cat["api_security_required"] is True
        and cat["crypto_operations_auditable_required"] is True
        and cat["microservice_ownership_clear_required"] is True
        and cat["observability_complete_required"] is True
        and cat["deployment_scalable_required"] is True
        and cat["data_architecture"]["not_shared"] is True
        and cat["event_streaming"]["not_missing"] is True
        and cat["api_security"]["not_lacking_security"] is True
        and cat["security"]["not_unauditable"] is True
        and cat["microservice_map"]["not_unclear_ownership"] is True
        and cat["observability"]["not_incomplete"] is True
        and cat["deployment"]["not_cannot_scale"] is True
        and cat["cqrs"]["event_count"] >= 26
        and cat["cqrs"]["command_count"] >= 18
        and cat["cursor_outputs"]["count"] >= 20
        and "services_share_databases" in cat["quality_gates"]["reject_if"]
        and "observability_incomplete" in cat["quality_gates"]["reject_if"]
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
        and cat["series_closeout"] is True
        and len(cat["microservice_map"]["logical_services"]) >= 12
    )

    try:
        SecretsOpsDbOwnershipRoot.verify(
            tenant_id="t1",
            service_ref="s1",
            shares_database=True,
        )
        db_bad = True
    except ValueError:
        db_bad = False

    db = SecretsOpsDbOwnershipRoot.verify(
        tenant_id="t1", service_ref="key-management-service"
    )
    db_ok = not db_bad and db.shares_databases() is False

    try:
        SecretsOpsEventsPresentRoot.verify(
            tenant_id="t1", stream_ref="st1", events_present=False
        )
        ev_bad = True
    except ValueError:
        ev_bad = False

    ev = SecretsOpsEventsPresentRoot.verify(
        tenant_id="t1", stream_ref="crypto.trust"
    )
    ev_ok = not ev_bad and ev.are_missing() is False

    try:
        SecretsOpsApiSecurityRoot.secure(
            tenant_id="t1", api_ref="a1", secured=False
        )
        api_bad = True
    except ValueError:
        api_bad = False

    api = SecretsOpsApiSecurityRoot.secure(
        tenant_id="t1", api_ref="/secrets/ops"
    )
    api_ok = not api_bad and api.lacks_security() is False

    try:
        SecretsOpsCryptoAuditableRoot.record(
            tenant_id="t1", operation_ref="o1", auditable=False
        )
        crypto_bad = True
    except ValueError:
        crypto_bad = False

    crypto = SecretsOpsCryptoAuditableRoot.record(
        tenant_id="t1", operation_ref="EncryptData"
    )
    crypto_ok = not crypto_bad and crypto.is_unauditable() is False

    try:
        SecretsOpsServiceOwnershipRoot.assign(
            tenant_id="t1", service_ref="s1", ownership_clear=False
        )
        own_bad = True
    except ValueError:
        own_bad = False

    own = SecretsOpsServiceOwnershipRoot.assign(
        tenant_id="t1", service_ref="pki-management-service"
    )
    own_ok = not own_bad and own.is_unclear() is False

    try:
        SecretsOpsObservabilityRoot.complete_surface(
            tenant_id="t1", service_ref="s1", complete=False
        )
        obs_bad = True
    except ValueError:
        obs_bad = False

    obs = SecretsOpsObservabilityRoot.complete_surface(
        tenant_id="t1", service_ref="cryptographic-trust-service"
    )
    obs_ok = not obs_bad and obs.is_incomplete() is False

    try:
        SecretsOpsScalableDeployRoot.enable(
            tenant_id="t1", deploy_ref="d1", scalable=False
        )
        scale_bad = True
    except ValueError:
        scale_bad = False

    scale = SecretsOpsScalableDeployRoot.enable(
        tenant_id="t1", deploy_ref="secrets-ha"
    )
    scale_ok = not scale_bad and scale.cannot_scale() is False

    close = SecretsOpsSeriesCloseoutRoot.close(tenant_id="t1")
    close_ok = "OpsSeriesClosed" in close.pending_events and close.is_open() is False

    aggregates_ok = (
        db_ok
        and ev_ok
        and api_ok
        and crypto_ok
        and own_ok
        and obs_ok
        and scale_ok
        and close_ok
    )

    acl_ok = (
        acls.to_event_fabric(tenant_id="t1", event_name="KeyRotated")[
            "events_present_required"
        ]
        is True
        and acls.to_api_gateway(tenant_id="t1", route="/secrets/ops")[
            "api_security_required"
        ]
        is True
        and acls.to_authorization_ops(
            tenant_id="t1", principal_ref="u1", action="secrets.ops.read"
        )["via_authorization"]
        is True
        and acls.to_observability(
            tenant_id="t1", service_ref="key-management-service"
        )["observability_complete_required"]
        is True
        and acls.to_audit(
            tenant_id="t1", action="secrets.ops.encrypt", resource_ref="k1"
        )["crypto_operations_auditable_required"]
        is True
    )

    router = (
        root / "backend/contexts/secrets/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '/ops"' in router
        and "/ops/microservices" in router
        and "/ops/cqrs" in router
        and "/ops/events" in router
        and "/ops/observability" in router
        and "/ops/readiness" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_SECRETS_OPS.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never services share databases" in law
        and "Never events are missing" in law
        and "Never APIs lack security" in law
        and "Never cryptographic operations are not auditable" in law
        and "Never microservices have unclear ownership" in law
        and "Never observability is incomplete" in law
        and "Never deployment cannot scale" in law
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
        "prompt": "P209-L",
        "adr": 357,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "catalog": catalog_ok,
        "aggregates": aggregates_ok,
        "acl": acl_ok,
        "router": router_ok,
        "documentation": doc_ok,
        "sor": "secrets",
        "series_status": "complete",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
