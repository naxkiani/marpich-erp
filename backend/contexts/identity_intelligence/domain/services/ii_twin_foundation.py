"""Identity Intelligence P207-F Digital Twin Platform foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]

REQUIRED_ARTIFACTS = [
    "docs/adr/321-enterprise-identity-intelligence-digital-twin-platform.md",
    "docs/architecture/ENTERPRISE_IDENTITY_INTELLIGENCE_DIGITAL_TWIN_PLATFORM.md",
    "docs/architecture/identity/intelligence/II_TWIN_CAPABILITIES.v1.yaml",
    "docs/architecture/identity/intelligence/II_TWIN_DDD_CQRS.v1.yaml",
    "docs/architecture/identity/intelligence/II_TWIN_SECURITY.v1.yaml",
    "docs/architecture/identity/intelligence/II_TWIN_VALIDATION.v1.yaml",
    "backend/contexts/identity_intelligence/domain/services/ii_platform_twins.py",
    "backend/contexts/identity_intelligence/domain/aggregates/ii_twin_aggregates.py",
    "backend/contexts/identity_intelligence/infrastructure/acl/ii_twin_acl.py",
    "backend/contexts/identity_intelligence/domain/services/ii_twin_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/identity_twin_platform",
    "backend/contexts/identity_simulation_platform",
    "backend/contexts/digital_twin_iam",
)


def validate_ii_twin_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.identity_intelligence.domain.aggregates.ii_twin_aggregates import (
        IdentityTwinOrchestrationContractRoot,
        TwinDecisionRecommendationRoot,
        TwinImpactAnalysisRoot,
        TwinPredictionCaseRoot,
        TwinSecurityPolicyRoot,
        TwinSimulationRunRoot,
        TwinSyncSessionRoot,
    )
    from contexts.identity_intelligence.domain.services import (
        ii_platform_twins as twins,
    )
    from contexts.identity_intelligence.infrastructure.acl import (
        ii_twin_acl as acls,
    )

    cat = twins.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P207-F"
        and cat.get("adr") == 321
        and cat.get("sor") == "identity_intelligence"
        and cat.get("twin_storage_peer") == "identity_digital_twin"
        and cat["not_data_copy_only"] is True
        and cat["realtime_sync_required"] is True
        and cat["simulation_required"] is True
        and cat["impact_analysis_required"] is True
        and cat["capabilities"]["not_data_copy"] is True
        and cat["capabilities"]["not_sync_absent"] is True
        and cat["capabilities"]["not_simulation_missing"] is True
        and cat["capabilities"]["not_impact_unavailable"] is True
        and cat["capabilities"]["not_weak_ai"] is True
        and cat["capabilities"]["not_undefined_security"] is True
        and cat["capabilities"]["not_duplicates_twin_sor"] is True
        and cat["simulation"]["not_missing"] is True
        and cat["synchronization"]["not_absent"] is True
        and cat["impact_analysis"]["not_unavailable"] is True
        and cat["predictive"]["not_weak"] is True
        and cat["security"]["not_undefined"] is True
        and cat["ddd"]["aggregate_count"] >= 7
        and cat["cqrs"]["event_count"] >= 6
        and cat["integrations"]["twin_integration_complete"] is True
        and "twin_only_data_copy" in cat["quality_gates"]["reject_if"]
        and "realtime_sync_absent" in cat["quality_gates"]["reject_if"]
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )

    try:
        IdentityTwinOrchestrationContractRoot.create(
            tenant_id="t1",
            twin_ref="tw1",
            peer_twin_ref="peer1",
            data_copy_only=True,
        )
        copy_only = True
    except ValueError:
        copy_only = False

    try:
        IdentityTwinOrchestrationContractRoot.create(
            tenant_id="t1",
            twin_ref="tw2",
            peer_twin_ref="peer1",
            owns_twin_sor=True,
        )
        dup_sor = True
    except ValueError:
        dup_sor = False

    try:
        IdentityTwinOrchestrationContractRoot.create(
            tenant_id="t1",
            twin_ref="tw3",
            peer_twin_ref="peer1",
            simulation_capable=False,
        )
        no_sim = True
    except ValueError:
        no_sim = False

    try:
        IdentityTwinOrchestrationContractRoot.create(
            tenant_id="t1",
            twin_ref="tw4",
            peer_twin_ref="peer1",
            realtime_sync=False,
        )
        no_sync = True
    except ValueError:
        no_sync = False

    contract = IdentityTwinOrchestrationContractRoot.create(
        tenant_id="t1",
        twin_ref="tw5",
        peer_twin_ref="peer-tw5",
    )
    contract_ok = (
        not copy_only
        and not dup_sor
        and not no_sim
        and not no_sync
        and contract.is_data_copy_only() is False
        and "TwinCreated" in contract.pending_events
    )

    try:
        TwinSyncSessionRoot.start(
            tenant_id="t1",
            session_ref="s1",
            twin_ref="tw5",
            realtime=False,
        )
        sync_absent = True
    except ValueError:
        sync_absent = False

    sync = TwinSyncSessionRoot.start(
        tenant_id="t1", session_ref="s2", twin_ref="tw5"
    )
    sync.complete()
    sync_ok = (
        not sync_absent
        and sync.is_sync_absent() is False
        and "TwinSynced" in sync.pending_events
    )

    try:
        TwinSimulationRunRoot.run(
            tenant_id="t1",
            run_ref="r1",
            twin_ref="tw5",
            scenario_type="invalid",
        )
        bad_sim = True
    except ValueError:
        bad_sim = False

    try:
        TwinSimulationRunRoot.run(
            tenant_id="t1",
            run_ref="r2",
            twin_ref="tw5",
            scenario_type="access_simulation",
            isolated=False,
        )
        not_iso = True
    except ValueError:
        not_iso = False

    sim = TwinSimulationRunRoot.run(
        tenant_id="t1",
        run_ref="r3",
        twin_ref="tw5",
        scenario_type="access_simulation",
    )
    sim.complete(result_summary="Would revoke 2 apps; no mutation")
    sim_ok = (
        not bad_sim
        and not not_iso
        and sim.is_simulation_missing() is False
        and "SimulationCompleted" in sim.pending_events
    )

    try:
        TwinImpactAnalysisRoot.analyze(
            tenant_id="t1",
            analysis_ref="i1",
            twin_ref="tw5",
            available=False,
        )
        no_impact = True
    except ValueError:
        no_impact = False

    impact = TwinImpactAnalysisRoot.analyze(
        tenant_id="t1", analysis_ref="i2", twin_ref="tw5"
    )
    impact_ok = (
        not no_impact
        and impact.is_unavailable() is False
        and "ImpactDetected" in impact.pending_events
    )

    try:
        TwinPredictionCaseRoot.predict(
            tenant_id="t1",
            case_ref="p1",
            twin_ref="tw5",
            prediction="risk up",
            ai_strong=False,
        )
        weak_ai = True
    except ValueError:
        weak_ai = False

    try:
        TwinPredictionCaseRoot.predict(
            tenant_id="t1",
            case_ref="p2",
            twin_ref="tw5",
            prediction="risk up",
            via_ai_platform=False,
        )
        no_ai_plat = True
    except ValueError:
        no_ai_plat = False

    pred = TwinPredictionCaseRoot.predict(
        tenant_id="t1",
        case_ref="p3",
        twin_ref="tw5",
        prediction="Access need likely increases after org change",
    )
    pred_ok = (
        not weak_ai
        and not no_ai_plat
        and pred.is_weak_ai() is False
        and "PredictionGenerated" in pred.pending_events
    )

    try:
        TwinDecisionRecommendationRoot.recommend(
            tenant_id="t1",
            decision_ref="d1",
            twin_ref="tw5",
            recommendation="revoke",
            high_impact=True,
            hitl_approved=False,
        )
        no_hitl = True
    except ValueError:
        no_hitl = False

    decision = TwinDecisionRecommendationRoot.recommend(
        tenant_id="t1",
        decision_ref="d2",
        twin_ref="tw5",
        recommendation="Simulate then stage revoke",
        high_impact=True,
        hitl_approved=True,
    )
    decision_ok = (
        not no_hitl and "OptimizationRecommended" in decision.pending_events
    )

    try:
        TwinSecurityPolicyRoot.define(
            tenant_id="t1",
            policy_ref="sec1",
            security_controls_defined=False,
        )
        undef_sec = True
    except ValueError:
        undef_sec = False

    sec = TwinSecurityPolicyRoot.define(tenant_id="t1", policy_ref="sec2")
    sec_ok = not undef_sec and sec.is_undefined_security() is False

    aggregates_ok = (
        contract_ok
        and sync_ok
        and sim_ok
        and impact_ok
        and pred_ok
        and decision_ok
        and sec_ok
    )

    acl_ok = (
        acls.to_digital_twin(tenant_id="t1", twin_ref="tw5")[
            "duplicates_twin_sor_forbidden"
        ]
        is True
        and acls.to_digital_twin(tenant_id="t1", twin_ref="tw5")[
            "not_data_copy_only"
        ]
        is True
        and acls.to_directory_graph(tenant_id="t1", projection_ref="g1")[
            "twin_relationship_reasoning"
        ]
        is True
        and acls.to_ai_infer(tenant_id="t1", surface="twin", context={})[
            "weak_ai_forbidden"
        ]
        is True
        and acls.to_authz_check(
            tenant_id="t1", subject_id="u1", action="identity_intelligence.read"
        )["twin_access_control"]
        is True
        and acls.to_workflow_approval(tenant_id="t1", decision_ref="d2")[
            "hitl_required"
        ]
        is True
        and acls.to_audit(tenant_id="t1", action="ii.twin.sim", resource_ref="r3")[
            "twin_actions_audited"
        ]
        is True
        and acls.to_agent_task(
            tenant_id="t1", agent_kind="simulation_agent", twin_ref="tw5"
        )["via_p207e"]
        is True
    )

    router = (
        root
        / "backend/contexts/identity_intelligence/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@identity_intelligence_router.get("/twins"' in router
        and "/twins/model" in router
        and "/twins/synchronization" in router
        and "/twins/simulation" in router
        and "/twins/impact" in router
        and "/twins/security" in router
        and "/twins/readiness" in router
    )

    law = (
        root
        / "docs/architecture/ENTERPRISE_IDENTITY_INTELLIGENCE_DIGITAL_TWIN_PLATFORM.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never twin as data copy only" in law
        and "Never absent real-time synchronization" in law
        and "Never missing simulation" in law
        and "Never unavailable impact analysis" in law
        and "Never weak AI integration" in law
        and "Never undefined security controls" in law
        and "HITL" in law
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
        "prompt": "P207-F",
        "adr": 321,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "catalog": catalog_ok,
        "aggregates": aggregates_ok,
        "acl": acl_ok,
        "router": router_ok,
        "documentation": doc_ok,
        "sor": "identity_intelligence",
        "twin_storage_peer": "identity_digital_twin",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
