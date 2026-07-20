"""Identity Intelligence P207-C Domain Architecture foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]

REQUIRED_ARTIFACTS = [
    "docs/adr/318-enterprise-identity-intelligence-domain-architecture.md",
    "docs/architecture/ENTERPRISE_IDENTITY_INTELLIGENCE_DOMAIN_ARCHITECTURE.md",
    "docs/architecture/identity/intelligence/II_DOMAIN_CAPABILITIES.v1.yaml",
    "docs/architecture/identity/intelligence/II_DOMAIN_DDD_CQRS.v1.yaml",
    "docs/architecture/identity/intelligence/II_DOMAIN_SECURITY.v1.yaml",
    "docs/architecture/identity/intelligence/II_DOMAIN_VALIDATION.v1.yaml",
    "backend/contexts/identity_intelligence/domain/services/ii_platform_domain.py",
    "backend/contexts/identity_intelligence/domain/aggregates/ii_domain_aggregates.py",
    "backend/contexts/identity_intelligence/infrastructure/acl/ii_domain_acl.py",
    "backend/contexts/identity_intelligence/domain/services/ii_domain_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/ai_identity_ops",
    "backend/contexts/autonomous_iam",
    "backend/contexts/identity_ueai",
    "backend/contexts/identity_ai_brain",
)


def validate_ii_domain_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.identity_intelligence.domain.aggregates.ii_domain_aggregates import (
        ContextMapRoot,
        DomainModelBlueprintRoot,
        IdentityInsightRoot,
        RecommendationCaseRoot,
    )
    from contexts.identity_intelligence.domain.services import (
        ii_platform_domain as pdom,
    )
    from contexts.identity_intelligence.infrastructure.acl import (
        ii_domain_acl as acls,
    )

    cat = pdom.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P207-C"
        and cat.get("adr") == 318
        and cat.get("sor") == "identity_intelligence"
        and cat["ddd_boundaries_clear"] is True
        and cat["purpose"]["not_absent"] is True
        and cat["ddd"]["not_unclear"] is True
        and cat["ddd"]["not_anemic"] is True
        and cat["ddd"]["logical_count"] >= 12
        and cat["ddd"]["aggregate_count"] >= 12
        and cat["cqrs"]["not_absent"] is True
        and cat["cqrs"]["not_missing_events"] is True
        and cat["cqrs"]["event_count"] >= 9
        and cat["context_map"]["not_undefined"] is True
        and cat["context_map"]["does_not_replace_peers"] is True
        and cat["meos_placement"]["does_not_replace_peers"] is True
        and cat["ai_governance"]["not_chatbot_only"] is True
        and cat["ai_governance"]["not_removed_human_control"] is True
        and cat["ubiquitous_language"]["count"] >= 10
        and cat["integrations"]["domain_integration_complete"] is True
        and "ddd_boundaries_unclear" in cat["quality_gates"]["reject_if"]
        and "anemic_domain_model" in cat["quality_gates"]["reject_if"]
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )

    try:
        DomainModelBlueprintRoot.define(
            tenant_id="t1",
            blueprint_ref="bp1",
            purpose=("identity_understanding",),
        )
        no_purpose = True
    except ValueError:
        no_purpose = False

    try:
        DomainModelBlueprintRoot.define(
            tenant_id="t1",
            blueprint_ref="bp2",
            boundaries_clear=False,
        )
        unclear = True
    except ValueError:
        unclear = False

    try:
        DomainModelBlueprintRoot.define(
            tenant_id="t1", blueprint_ref="bp3", anemic=True
        )
        anemic = True
    except ValueError:
        anemic = False

    try:
        DomainModelBlueprintRoot.define(
            tenant_id="t1", blueprint_ref="bp4", cqrs_ready=False
        )
        no_cqrs = True
    except ValueError:
        no_cqrs = False

    bp = DomainModelBlueprintRoot.define(tenant_id="t1", blueprint_ref="bp5")
    bp_ok = (
        not no_purpose
        and not unclear
        and not anemic
        and not no_cqrs
        and bp.is_unclear() is False
        and bp.is_anemic() is False
    )

    try:
        ContextMapRoot.publish(
            tenant_id="t1", map_ref="m1", partnership=("a",), replaces_peers=False
        )
        undef_map = True
    except ValueError:
        undef_map = False

    try:
        ContextMapRoot.publish(
            tenant_id="t1", map_ref="m2", replaces_peers=True
        )
        replaces = True
    except ValueError:
        replaces = False

    cmap = ContextMapRoot.publish(tenant_id="t1", map_ref="m3")
    map_ok = (
        not undef_map
        and not replaces
        and cmap.is_undefined() is False
        and "GraphIntegrationConnected" in cmap.pending_events
    )

    try:
        IdentityInsightRoot.generate(
            tenant_id="t1",
            insight_ref="i1",
            subject_ref="u1",
            explanation="",
        )
        no_exp = True
    except ValueError:
        no_exp = False

    insight = IdentityInsightRoot.generate(
        tenant_id="t1",
        insight_ref="i2",
        subject_ref="u1",
        explanation="Elevated privilege path via graph relationships",
    )
    insight_ok = (
        not no_exp
        and insight.is_anemic() is False
        and "InsightGenerated" in insight.pending_events
    )

    try:
        RecommendationCaseRoot.recommend(
            tenant_id="t1",
            case_ref="r1",
            subject_ref="u1",
            action="revoke_excess",
            explanation="SoD risk",
            governed=False,
        )
        ungov = True
    except ValueError:
        ungov = False

    try:
        RecommendationCaseRoot.recommend(
            tenant_id="t1",
            case_ref="r2",
            subject_ref="u1",
            action="revoke_excess",
            explanation="SoD risk",
            human_control=False,
        )
        no_human = True
    except ValueError:
        no_human = False

    rec = RecommendationCaseRoot.recommend(
        tenant_id="t1",
        case_ref="r3",
        subject_ref="u1",
        action="revoke_excess",
        explanation="SoD conflict predicted from graph",
    )
    rec_ok = (
        not ungov
        and not no_human
        and "ActionRecommended" in rec.pending_events
    )

    aggregates_ok = bp_ok and map_ok and insight_ok and rec_ok

    acl_ok = (
        acls.to_ai_infer(tenant_id="t1", surface="reasoning", context={})[
            "domain_reasoning"
        ]
        is True
        and acls.to_authz_check(
            tenant_id="t1", subject_id="u1", action="identity_intelligence.read"
        )["domain_does_not_own_pdp"]
        is True
        and acls.to_directory_graph(tenant_id="t1", projection_ref="g1")[
            "domain_graph_via_acl"
        ]
        is True
        and acls.to_digital_twin(tenant_id="t1", twin_ref="tw1")[
            "domain_twin_orchestration_only"
        ]
        is True
        and acls.to_lifecycle(tenant_id="t1", subject_ref="u1")[
            "context_map_partnership"
        ]
        is True
        and acls.to_iga(tenant_id="t1", subject_ref="u1")["context_map_partnership"]
        is True
        and acls.to_policy_evaluate(
            tenant_id="t1", policy_key="ii.domain", context={}
        )["domain_invariant_enforcement"]
        is True
        and acls.to_audit(tenant_id="t1", action="ii.domain", resource_ref="bp1")[
            "domain_event_audit"
        ]
        is True
    )

    router = (
        root
        / "backend/contexts/identity_intelligence/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@identity_intelligence_router.get("/domain"' in router
        and "/domain/purpose" in router
        and "/domain/bounded-contexts" in router
        and "/domain/aggregates" in router
        and "/domain/cqrs" in router
        and "/domain/context-map" in router
        and "/domain/readiness" in router
    )

    law = (
        root
        / "docs/architecture/ENTERPRISE_IDENTITY_INTELLIGENCE_DOMAIN_ARCHITECTURE.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never unclear DDD boundaries" in law
        and "Never anemic owned aggregates" in law
        and "Never replace peer SoRs" in law
        and "Never chatbot-only AI" in law
        and "HITL" in law
        and "Actionable Enterprise Identity Intelligence" in law
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
        "prompt": "P207-C",
        "adr": 318,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "catalog": catalog_ok,
        "aggregates": aggregates_ok,
        "acl": acl_ok,
        "router": router_ok,
        "documentation": doc_ok,
        "sor": "identity_intelligence",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
