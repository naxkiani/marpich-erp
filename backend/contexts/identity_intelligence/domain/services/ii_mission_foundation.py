"""Identity Intelligence P207-B Mission / Vision / Scope foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]

REQUIRED_ARTIFACTS = [
    "docs/adr/317-enterprise-identity-intelligence-mission-vision-scope.md",
    "docs/architecture/ENTERPRISE_IDENTITY_INTELLIGENCE_MISSION_VISION_SCOPE.md",
    "docs/architecture/identity/intelligence/II_MVS_CAPABILITIES.v1.yaml",
    "docs/architecture/identity/intelligence/II_MVS_DDD_CQRS.v1.yaml",
    "docs/architecture/identity/intelligence/II_MVS_SECURITY.v1.yaml",
    "docs/architecture/identity/intelligence/II_MVS_VALIDATION.v1.yaml",
    "backend/contexts/identity_intelligence/domain/services/ii_platform_mission_scope.py",
    "backend/contexts/identity_intelligence/domain/aggregates/ii_mission_aggregates.py",
    "backend/contexts/identity_intelligence/infrastructure/acl/ii_mission_acl.py",
    "backend/contexts/identity_intelligence/domain/services/ii_mission_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/ai_identity_ops",
    "backend/contexts/autonomous_iam",
    "backend/contexts/identity_ueai",
    "backend/contexts/identity_ai_brain",
)


def validate_ii_mission_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.identity_intelligence.domain.aggregates.ii_mission_aggregates import (
        EnterpriseScopeBoundaryRoot,
        MeosArchitecturePlacementRoot,
        MissionCharterRoot,
        StrategicObjectiveSetRoot,
    )
    from contexts.identity_intelligence.domain.services import (
        ii_platform_mission_scope as mscope,
    )
    from contexts.identity_intelligence.infrastructure.acl import (
        ii_mission_acl as acls,
    )

    cat = mscope.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P207-B"
        and cat.get("adr") == 317
        and cat.get("sor") == "identity_intelligence"
        and cat["mission_vision_required"] is True
        and cat["does_not_replace_peers"] is True
        and cat["mission"]["not_absent"] is True
        and cat["vision"]["not_absent"] is True
        and cat["purpose"]["not_absent"] is True
        and cat["strategic_objectives"]["not_undefined"] is True
        and cat["enterprise_scope"]["not_undefined"] is True
        and cat["enterprise_scope"]["out_of_scope_clear"] is True
        and cat["enterprise_scope"]["not_replacing_peers"] is True
        and cat["meos_placement"]["intelligence_layer"] is True
        and cat["ai_governance"]["not_chatbot_only"] is True
        and cat["ai_governance"]["not_removed_human_control"] is True
        and cat["mission"]["dimension_count"] >= 10
        and cat["vision"]["pillar_count"] >= 10
        and cat["strategic_objectives"]["category_count"] == 4
        and cat["enterprise_scope"]["out_of_scope_count"] >= 8
        and cat["ddd"]["aggregate_count"] >= 6
        and cat["cqrs"]["event_count"] >= 6
        and cat["integrations"]["mission_integration_complete"] is True
        and "mission_vision_absent" in cat["quality_gates"]["reject_if"]
        and "replaces_peer_sors" in cat["quality_gates"]["reject_if"]
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )

    try:
        MissionCharterRoot.publish(
            tenant_id="t1",
            charter_ref="c1",
            mission_text="",
            vision_text="v",
        )
        no_mission = True
    except ValueError:
        no_mission = False

    charter = MissionCharterRoot.publish(
        tenant_id="t1",
        charter_ref="c1",
        mission_text=mscope.MISSION_STATEMENT,
        vision_text=mscope.VISION_STATEMENT,
    )
    charter_ok = (
        not no_mission
        and charter.is_absent() is False
        and "MissionCharterPublished" in charter.pending_events
    )

    try:
        EnterpriseScopeBoundaryRoot.define(
            tenant_id="t1", boundary_ref="b1", in_scope_defined=False
        )
        no_scope = True
    except ValueError:
        no_scope = False

    try:
        EnterpriseScopeBoundaryRoot.define(
            tenant_id="t1", boundary_ref="b2", out_of_scope_defined=False
        )
        unclear = True
    except ValueError:
        unclear = False

    try:
        EnterpriseScopeBoundaryRoot.define(
            tenant_id="t1", boundary_ref="b3", replaces_peers=True
        )
        replaces = True
    except ValueError:
        replaces = False

    scope = EnterpriseScopeBoundaryRoot.define(tenant_id="t1", boundary_ref="b4")
    scope.reject_peer_replacement()
    scope_ok = (
        not no_scope
        and not unclear
        and not replaces
        and scope.is_undefined() is False
        and "PeerSorReplacementRejected" in scope.pending_events
    )

    try:
        StrategicObjectiveSetRoot.register(
            tenant_id="t1",
            set_ref="s1",
            categories=("identity_intelligence",),
        )
        incomplete_obj = True
    except ValueError:
        incomplete_obj = False

    objs = StrategicObjectiveSetRoot.register(tenant_id="t1", set_ref="s2")
    objs_ok = (
        not incomplete_obj
        and objs.is_undefined() is False
        and "StrategicObjectiveRegistered" in objs.pending_events
    )

    try:
        MeosArchitecturePlacementRoot.map(
            tenant_id="t1",
            placement_ref="p1",
            intelligence_layer=False,
        )
        no_layer = True
    except ValueError:
        no_layer = False

    try:
        MeosArchitecturePlacementRoot.map(
            tenant_id="t1", placement_ref="p2", human_control=False
        )
        no_human = True
    except ValueError:
        no_human = False

    try:
        MeosArchitecturePlacementRoot.map(
            tenant_id="t1", placement_ref="p3", chatbot_only=True
        )
        chatbot = True
    except ValueError:
        chatbot = False

    place = MeosArchitecturePlacementRoot.map(tenant_id="t1", placement_ref="p4")
    place_ok = (
        not no_layer
        and not no_human
        and not chatbot
        and place.is_absent_intelligence_layer() is False
        and "MeosPlacementMapped" in place.pending_events
    )

    aggregates_ok = charter_ok and scope_ok and objs_ok and place_ok

    acl_ok = (
        acls.to_ai_infer(tenant_id="t1", surface="mission", context={})[
            "chatbot_only_forbidden"
        ]
        is True
        and acls.to_directory(tenant_id="t1")["does_not_replace_p205"] is True
        and acls.to_iga(tenant_id="t1", subject_ref="u1")["does_not_replace_p202"]
        is True
        and acls.to_am(tenant_id="t1", subject_ref="u1")["does_not_replace_p204"]
        is True
        and acls.to_pam(tenant_id="t1", subject_ref="u1")["does_not_replace_p203"]
        is True
        and acls.to_digital_twin(tenant_id="t1", twin_ref="tw1")[
            "does_not_replace_twin_sor"
        ]
        is True
        and acls.to_policy_evaluate(
            tenant_id="t1", policy_key="ii.scope", context={}
        )["scope_boundary_enforcement"]
        is True
        and acls.to_audit(tenant_id="t1", action="ii.mission", resource_ref="c1")[
            "mission_charter_audit"
        ]
        is True
    )

    router = (
        root
        / "backend/contexts/identity_intelligence/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@identity_intelligence_router.get("/mission"' in router
        and "/mission/statement" in router
        and "/mission/vision" in router
        and "/mission/scope" in router
        and "/mission/out-of-scope" in router
        and "/mission/placement" in router
        and "/mission/objectives" in router
        and "/mission/readiness" in router
    )

    law = (
        root
        / "docs/architecture/ENTERPRISE_IDENTITY_INTELLIGENCE_MISSION_VISION_SCOPE.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never AI only a chatbot" in law
        and "Never replace peer SoRs" in law
        and "Never undefined scope" in law
        and "Never remove human control" in law
        and "HITL" in law
        and "Out of scope" in law
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
        "prompt": "P207-B",
        "adr": 317,
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
