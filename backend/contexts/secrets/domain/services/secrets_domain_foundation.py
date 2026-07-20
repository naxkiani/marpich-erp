"""Secrets P209-C Domain Architecture foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]

REQUIRED_ARTIFACTS = [
    "docs/adr/348-enterprise-secrets-domain.md",
    "docs/architecture/ENTERPRISE_SECRETS_DOMAIN.md",
    "docs/architecture/secrets/SECRETS_DOMAIN_CAPABILITIES.v1.yaml",
    "docs/architecture/secrets/SECRETS_DOMAIN_DDD_CQRS.v1.yaml",
    "docs/architecture/secrets/SECRETS_DOMAIN_SECURITY.v1.yaml",
    "docs/architecture/secrets/SECRETS_DOMAIN_VALIDATION.v1.yaml",
    "backend/contexts/secrets/domain/services/secrets_platform_domain.py",
    "backend/contexts/secrets/domain/aggregates/secrets_domain_aggregates.py",
    "backend/contexts/secrets/infrastructure/acl/secrets_domain_acl.py",
    "backend/contexts/secrets/domain/services/secrets_domain_foundation.py",
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


def validate_secrets_domain_foundation(
    *, repo_root: Path | None = None
) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.secrets.domain.aggregates.secrets_domain_aggregates import (
        SecretsAggregateOwnershipRoot,
        SecretsBoundedContextMapRoot,
        SecretsCryptoLifecycleDomainRoot,
        SecretsDomainBlueprintRoot,
        SecretsDomainEventsCatalogRoot,
        SecretsManagedSecretsRoot,
        SecretsPkiKmsSeparationRoot,
        SecretsTrustRelationshipModelRoot,
    )
    from contexts.secrets.domain.services import (
        secrets_platform_domain as pdom,
    )
    from contexts.secrets.infrastructure.acl import (
        secrets_domain_acl as acls,
    )

    cat = pdom.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P209-C"
        and cat.get("adr") == 348
        and cat.get("sor") == "secrets"
        and cat["domain_boundaries_clear_required"] is True
        and cat["pki_kms_separation_required"] is True
        and cat["secrets_managed_required"] is True
        and cat["trust_relationships_modeled_required"] is True
        and cat["domain_events_required"] is True
        and cat["aggregate_ownership_valid_required"] is True
        and cat["cryptographic_lifecycle_complete_required"] is True
        and cat["bounded_contexts"]["not_unclear"] is True
        and cat["pki_kms_separation"]["not_mixed"] is True
        and cat["secrets_management"]["not_unmanaged"] is True
        and cat["trust_model"]["not_unmodeled"] is True
        and cat["events"]["not_absent"] is True
        and cat["aggregates"]["not_violating_ownership"] is True
        and cat["lifecycle"]["not_incomplete"] is True
        and cat["bounded_contexts"]["count"] >= 7
        and cat["events"]["count"] >= 21
        and cat["ddd"]["aggregate_count"] >= 8
        and cat["cursor_outputs"]["count"] >= 15
        and "domain_boundaries_unclear" in cat["quality_gates"]["reject_if"]
        and "pki_and_kms_responsibilities_mixed"
        in cat["quality_gates"]["reject_if"]
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )

    try:
        SecretsDomainBlueprintRoot.publish(
            tenant_id="t1",
            blueprint_ref="b1",
            boundaries_clear=False,
        )
        bound_bad = True
    except ValueError:
        bound_bad = False

    blueprint = SecretsDomainBlueprintRoot.publish(
        tenant_id="t1", blueprint_ref="b2"
    )
    blueprint_ok = not bound_bad and blueprint.is_unclear() is False

    try:
        SecretsPkiKmsSeparationRoot.enforce(
            tenant_id="t1", separation_ref="s1", mixed=True
        )
        mix_bad = True
    except ValueError:
        mix_bad = False

    sep = SecretsPkiKmsSeparationRoot.enforce(
        tenant_id="t1", separation_ref="s2"
    )
    sep_ok = not mix_bad and sep.is_mixed() is False

    try:
        SecretsManagedSecretsRoot.register(
            tenant_id="t1", managed_ref="m1", managed=False
        )
        unm_bad = True
    except ValueError:
        unm_bad = False

    managed = SecretsManagedSecretsRoot.register(
        tenant_id="t1", managed_ref="m2"
    )
    managed_ok = not unm_bad and managed.is_unmanaged() is False

    try:
        SecretsTrustRelationshipModelRoot.model(
            tenant_id="t1", trust_ref="t1", modeled=False
        )
        trust_bad = True
    except ValueError:
        trust_bad = False

    trust = SecretsTrustRelationshipModelRoot.model(
        tenant_id="t1", trust_ref="t2"
    )
    trust_ok = not trust_bad and trust.is_unmodeled() is False

    try:
        SecretsDomainEventsCatalogRoot.publish(
            tenant_id="t1", catalog_ref="e1", event_count=2
        )
        ev_bad = True
    except ValueError:
        ev_bad = False

    events = SecretsDomainEventsCatalogRoot.publish(
        tenant_id="t1", catalog_ref="e2"
    )
    events_ok = not ev_bad and events.is_absent() is False

    try:
        SecretsAggregateOwnershipRoot.validate(
            tenant_id="t1", ownership_ref="o1", valid=False
        )
        own_bad = True
    except ValueError:
        own_bad = False

    ownership = SecretsAggregateOwnershipRoot.validate(
        tenant_id="t1", ownership_ref="o2"
    )
    ownership_ok = not own_bad and ownership.is_violating() is False

    try:
        SecretsCryptoLifecycleDomainRoot.complete_model(
            tenant_id="t1", lifecycle_ref="l1", complete=False
        )
        life_bad = True
    except ValueError:
        life_bad = False

    life = SecretsCryptoLifecycleDomainRoot.complete_model(
        tenant_id="t1", lifecycle_ref="l2"
    )
    life_ok = not life_bad and life.is_incomplete() is False

    bc_map = SecretsBoundedContextMapRoot.publish(
        tenant_id="t1", map_ref="map1"
    )
    map_ok = bc_map.context_count >= 7

    aggregates_ok = (
        blueprint_ok
        and sep_ok
        and managed_ok
        and trust_ok
        and events_ok
        and ownership_ok
        and life_ok
        and map_ok
    )

    acl_ok = (
        acls.to_pki_context(tenant_id="t1", certificate_ref="c1")[
            "pki_kms_separated"
        ]
        is True
        and acls.to_kms_context(tenant_id="t1", key_ref="k1")[
            "does_not_own_cas"
        ]
        is True
        and acls.to_secrets_context(tenant_id="t1", secret_ref="s1")[
            "managed_required"
        ]
        is True
        and acls.to_audit(
            tenant_id="t1", action="secrets.domain", resource_ref="d1"
        )["domain_event_trail"]
        is True
    )

    router = (
        root / "backend/contexts/secrets/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '/domain"' in router
        and "/domain/bounded-contexts" in router
        and "/domain/pki-kms-separation" in router
        and "/domain/events" in router
        and "/domain/readiness" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_SECRETS_DOMAIN.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never domain boundaries are unclear" in law
        and "Never PKI and KMS responsibilities are mixed" in law
        and "Never secrets are unmanaged" in law
        and "Never trust relationships are not modeled" in law
        and "Never domain events are absent" in law
        and "Never aggregates violate ownership rules" in law
        and "Never cryptographic lifecycle is incomplete" in law
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
        "prompt": "P209-C",
        "adr": 348,
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
