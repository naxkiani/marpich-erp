"""Secrets P209-B Mission / Vision / Scope foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]

REQUIRED_ARTIFACTS = [
    "docs/adr/347-enterprise-secrets-mission-vision-scope.md",
    "docs/architecture/ENTERPRISE_SECRETS_MISSION_VISION_SCOPE.md",
    "docs/architecture/secrets/SECRETS_MVS_CAPABILITIES.v1.yaml",
    "docs/architecture/secrets/SECRETS_MVS_DDD_CQRS.v1.yaml",
    "docs/architecture/secrets/SECRETS_MVS_SECURITY.v1.yaml",
    "docs/architecture/secrets/SECRETS_MVS_VALIDATION.v1.yaml",
    "backend/contexts/secrets/domain/services/secrets_platform_mission_scope.py",
    "backend/contexts/secrets/domain/aggregates/secrets_mission_aggregates.py",
    "backend/contexts/secrets/infrastructure/acl/secrets_mission_acl.py",
    "backend/contexts/secrets/domain/services/secrets_mission_foundation.py",
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


def validate_secrets_mission_foundation(
    *, repo_root: Path | None = None
) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.secrets.domain.aggregates.secrets_mission_aggregates import (
        SecretsBoundaryRoot,
        SecretsCapabilityOwnershipRoot,
        SecretsEnterpriseScopeRoot,
        SecretsEvolutionRoadmapRoot,
        SecretsGovernancePrinciplesRoot,
        SecretsIntegrationCharterRoot,
        SecretsMissionCharterRoot,
        SecretsStrategicObjectivesRoot,
    )
    from contexts.secrets.domain.services import (
        secrets_platform_mission_scope as mscope,
    )
    from contexts.secrets.infrastructure.acl import (
        secrets_mission_acl as acls,
    )

    cat = mscope.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P209-B"
        and cat.get("adr") == 347
        and cat.get("sor") == "secrets"
        and cat["mission_vision_required"] is True
        and cat["enterprise_scope_required"] is True
        and cat["boundaries_clear_required"] is True
        and cat["capability_ownership_required"] is True
        and cat["integration_responsibilities_required"] is True
        and cat["governance_principles_required"] is True
        and cat["evolution_roadmap_required"] is True
        and cat["does_not_own_business_authorization"] is True
        and cat["does_not_replace_peer_sors"] is True
        and cat["mission"]["not_absent"] is True
        and cat["vision"]["not_absent"] is True
        and cat["enterprise_scope"]["not_undefined"] is True
        and cat["boundaries"]["not_unclear"] is True
        and cat["boundaries"]["not_owning_business_authorization"] is True
        and cat["boundaries"]["not_replacing_peers"] is True
        and cat["business_capabilities"]["not_absent"] is True
        and cat["meos_integrations"]["not_absent"] is True
        and cat["principles"]["not_absent"] is True
        and cat["evolution_roadmap"]["not_absent"] is True
        and cat["strategic_objectives"]["count"] == 5
        and cat["evolution_roadmap"]["count"] == 7
        and cat["cursor_outputs"]["count"] >= 15
        and cat["ddd"]["aggregate_count"] >= 8
        and cat["cqrs"]["event_count"] >= 12
        and "mission_vision_absent" in cat["quality_gates"]["reject_if"]
        and "owns_business_authorization" in cat["quality_gates"]["reject_if"]
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )

    try:
        SecretsMissionCharterRoot.publish(
            tenant_id="t1",
            charter_ref="c1",
            mission_text="",
            vision_text="v",
        )
        mv_bad = True
    except ValueError:
        mv_bad = False

    charter = SecretsMissionCharterRoot.publish(
        tenant_id="t1",
        charter_ref="c2",
        mission_text="mission",
        vision_text="vision",
    )
    charter_ok = not mv_bad and charter.is_absent() is False

    try:
        SecretsEnterpriseScopeRoot.define(
            tenant_id="t1", scope_ref="s1", defined=False
        )
        scope_bad = True
    except ValueError:
        scope_bad = False

    scope = SecretsEnterpriseScopeRoot.define(tenant_id="t1", scope_ref="s2")
    scope_ok = not scope_bad and scope.is_undefined() is False

    try:
        SecretsBoundaryRoot.clarify(
            tenant_id="t1",
            boundary_ref="b1",
            owns_business_authorization=True,
        )
        bound_bad = True
    except ValueError:
        bound_bad = False

    try:
        SecretsBoundaryRoot.clarify(
            tenant_id="t1", boundary_ref="b2", replaces_peers=True
        )
        peer_bad = True
    except ValueError:
        peer_bad = False

    boundary = SecretsBoundaryRoot.clarify(tenant_id="t1", boundary_ref="b3")
    boundary_ok = (
        not bound_bad and not peer_bad and boundary.is_unclear() is False
    )

    try:
        SecretsCapabilityOwnershipRoot.register(
            tenant_id="t1", ownership_ref="o1", present=False
        )
        cap_bad = True
    except ValueError:
        cap_bad = False

    cap = SecretsCapabilityOwnershipRoot.register(
        tenant_id="t1", ownership_ref="o2"
    )
    cap_ok = not cap_bad and cap.is_absent() is False

    try:
        SecretsIntegrationCharterRoot.bind(
            tenant_id="t1", charter_ref="i1", present=False
        )
        integ_bad = True
    except ValueError:
        integ_bad = False

    integ = SecretsIntegrationCharterRoot.bind(
        tenant_id="t1", charter_ref="i2"
    )
    integ_ok = not integ_bad and integ.is_absent() is False

    try:
        SecretsGovernancePrinciplesRoot.publish(
            tenant_id="t1", principles_ref="g1", present=False
        )
        gov_bad = True
    except ValueError:
        gov_bad = False

    gov = SecretsGovernancePrinciplesRoot.publish(
        tenant_id="t1", principles_ref="g2"
    )
    gov_ok = not gov_bad and gov.is_absent() is False

    try:
        SecretsEvolutionRoadmapRoot.publish(
            tenant_id="t1", roadmap_ref="r1", present=False
        )
        road_bad = True
    except ValueError:
        road_bad = False

    road = SecretsEvolutionRoadmapRoot.publish(
        tenant_id="t1", roadmap_ref="r2"
    )
    road_ok = not road_bad and road.is_absent() is False

    objs = SecretsStrategicObjectivesRoot.register(
        tenant_id="t1", objectives_ref="obj1"
    )
    objs_ok = objs.objective_count >= 5

    aggregates_ok = (
        charter_ok
        and scope_ok
        and boundary_ok
        and cap_ok
        and integ_ok
        and gov_ok
        and road_ok
        and objs_ok
    )

    acl_ok = (
        acls.to_authorization_boundary(tenant_id="t1")[
            "does_not_own_business_authorization"
        ]
        is True
        and acls.to_identity_boundary(tenant_id="t1")[
            "does_not_replace_identity_sor"
        ]
        is True
        and acls.to_pam_ref(tenant_id="t1", secret_ref="s1")[
            "does_not_replace_pam_sor"
        ]
        is True
        and acls.to_audit(
            tenant_id="t1", action="secrets.mission", resource_ref="c1"
        )["mission_charter_audit"]
        is True
    )

    router = (
        root / "backend/contexts/secrets/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '/mission"' in router
        and "/mission/vision" in router
        and "/mission/boundaries" in router
        and "/mission/roadmap" in router
        and "/mission/readiness" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_SECRETS_MISSION_VISION_SCOPE.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never mission/vision absent" in law
        and "Never enterprise scope undefined" in law
        and "Never unclear boundaries" in law
        and "Never capability ownership absent" in law
        and "Never integration responsibilities absent" in law
        and "Never governance principles absent" in law
        and "Never evolution roadmap absent" in law
        and "Never replace peer SoRs" in law
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
        "prompt": "P209-B",
        "adr": 347,
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
