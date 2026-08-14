"""Data Security P211-M digital twin & privacy simulation foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/388-enterprise-data-security-twin.md",
    "docs/architecture/ENTERPRISE_DATA_SECURITY_TWIN.md",
    "docs/architecture/data_security/DATA_SECURITY_TWIN_CAPABILITIES.v1.yaml",
    "docs/architecture/data_security/DATA_SECURITY_TWIN_DDD_CQRS.v1.yaml",
    "docs/architecture/data_security/DATA_SECURITY_TWIN_SECURITY.v1.yaml",
    "docs/architecture/data_security/DATA_SECURITY_TWIN_VALIDATION.v1.yaml",
    "backend/contexts/data_security/domain/services/ds_platform_twin.py",
    "backend/contexts/data_security/domain/aggregates/ds_twin_aggregates.py",
    "backend/contexts/data_security/infrastructure/acl/ds_twin_acl.py",
    "backend/contexts/data_security/application/ds_twin_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/data_digital_twin",
    "backend/contexts/privacy_simulation",
    "backend/contexts/data_twin_platform",
)


def validate_ds_twin_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.data_security.domain.aggregates.ds_twin_aggregates import (
        DsAvailableRiskPredictionRoot,
        DsCompleteDigitalRepresentationRoot,
        DsControlOptimizedRoot,
        DsExplainableSimulationResultRoot,
        DsMeasurableComplianceImpactRoot,
        DsSimulatablePrivacyScenarioRoot,
        DsSimulationCompletedRoot,
        DsVisibleAiPrivacyRiskRoot,
    )
    from contexts.data_security.domain.services import ds_platform_twin as twin

    cat = twin.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P211-M"
        and cat.get("adr") == 388
        and cat.get("sor") == "data_security"
        and cat["digital_representation_complete_required"] is True
        and cat["privacy_scenarios_simulatable_required"] is True
        and cat["risk_prediction_available_required"] is True
        and cat["compliance_impact_measurable_required"] is True
        and cat["ai_privacy_risks_visible_required"] is True
        and cat["simulation_results_explainable_required"] is True
        and cat["digital_representation"]["not_incomplete"] is True
        and cat["privacy_simulation"]["not_unsimulatable"] is True
        and cat["risk_prediction"]["not_unavailable"] is True
        and cat["compliance_impact"]["not_unmeasurable"] is True
        and cat["ai_privacy_risks"]["not_invisible"] is True
        and cat["simulation_explainability"]["not_unexplainable"] is True
        and cat["architecture"]["layer_count"] >= 7
        and cat["domain"]["context_count"] >= 7
        and cat["cqrs"]["event_count"] >= 6
        and cat["cursor_outputs"]["count"] >= 15
        and "digital_representation_is_incomplete"
        in cat["quality_gates"]["reject_if"]
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )

    def _bad(fn, **kwargs):
        try:
            fn(**kwargs)
            return True
        except ValueError:
            return False

    checks = []
    checks.append(
        not _bad(
            DsCompleteDigitalRepresentationRoot.synchronize,
            tenant_id="t1",
            twin_ref="tw1",
            complete=False,
        )
        and DsCompleteDigitalRepresentationRoot.synchronize(
            tenant_id="t1", twin_ref="tw2"
        ).is_incomplete()
        is False
    )
    checks.append(
        not _bad(
            DsSimulatablePrivacyScenarioRoot.create,
            tenant_id="t1",
            scenario_ref="s1",
            simulatable=False,
        )
        and DsSimulatablePrivacyScenarioRoot.create(
            tenant_id="t1", scenario_ref="s2"
        ).is_unsimulatable()
        is False
    )
    checks.append(
        not _bad(
            DsAvailableRiskPredictionRoot.predict,
            tenant_id="t1",
            prediction_ref="p1",
            available=False,
        )
        and DsAvailableRiskPredictionRoot.predict(
            tenant_id="t1", prediction_ref="p2"
        ).is_unavailable()
        is False
    )
    checks.append(
        not _bad(
            DsMeasurableComplianceImpactRoot.measure,
            tenant_id="t1",
            impact_ref="i1",
            measurable=False,
        )
        and DsMeasurableComplianceImpactRoot.measure(
            tenant_id="t1", impact_ref="i2"
        ).is_unmeasurable()
        is False
    )
    checks.append(
        not _bad(
            DsVisibleAiPrivacyRiskRoot.reveal,
            tenant_id="t1",
            risk_ref="r1",
            visible=False,
        )
        and DsVisibleAiPrivacyRiskRoot.reveal(
            tenant_id="t1", risk_ref="r2"
        ).is_invisible()
        is False
    )
    checks.append(
        not _bad(
            DsExplainableSimulationResultRoot.complete,
            tenant_id="t1",
            result_ref="res1",
            explainable=False,
        )
        and DsExplainableSimulationResultRoot.complete(
            tenant_id="t1", result_ref="res2"
        ).is_unexplainable()
        is False
    )
    sim = DsSimulationCompletedRoot.run(
        tenant_id="t1", simulation_ref="sim1"
    )
    ctrl = DsControlOptimizedRoot.optimize(
        tenant_id="t1", control_ref="c1"
    )
    checks.append("SimulationCompleted" in sim.pending_events)
    checks.append("ControlOptimized" in ctrl.pending_events)
    aggregates_ok = all(checks)

    acl_path = (
        root / "backend/contexts/data_security/infrastructure/acl/ds_twin_acl.py"
    )
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_enterprise_ai" in acl_text
        and "digital_representation_complete_required" in acl_text
        and "privacy_scenarios_simulatable_required" in acl_text
        and "ai_privacy_risks_visible_required" in acl_text
        and "via_consent_acl_only" in acl_text
        and "via_p211_l_ai" in acl_text
        and "module_local_llm_sdk_forbidden" in acl_text
    )

    router = (
        root / "backend/contexts/data_security/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@data_security_router.get("/twin")' in router
        and "/twin/representation" in router
        and "/twin/simulation" in router
        and "/twin/ai-privacy" in router
        and "/twin/readiness" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_DATA_SECURITY_TWIN.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never Digital representation is incomplete" in law
        and "Never Privacy scenarios cannot be simulated" in law
        and "Never Risk prediction is unavailable" in law
        and "Never Compliance impact cannot be measured" in law
        and "Never AI privacy risks are invisible" in law
        and "Never Simulation results are not explainable" in law
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
        "prompt": "P211-M",
        "adr": 388,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "catalog": catalog_ok,
        "aggregates": aggregates_ok,
        "acl": acl_ok,
        "router": router_ok,
        "documentation": doc_ok,
        "sor": "data_security",
        "capability": "CAP-PLT-DS-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
