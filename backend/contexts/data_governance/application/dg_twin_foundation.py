"""Data Governance P212-L Digital Twin foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/404-enterprise-data-governance-digital-twin.md",
    "docs/architecture/ENTERPRISE_DATA_GOVERNANCE_DIGITAL_TWIN.md",
    "docs/architecture/data_governance/DATA_GOVERNANCE_TWIN_CAPABILITIES.v1.yaml",
    "docs/architecture/data_governance/DATA_GOVERNANCE_TWIN_DDD_CQRS.v1.yaml",
    "docs/architecture/data_governance/DATA_GOVERNANCE_TWIN_SECURITY.v1.yaml",
    "docs/architecture/data_governance/DATA_GOVERNANCE_TWIN_VALIDATION.v1.yaml",
    "backend/contexts/data_governance/domain/services/dg_platform_twin.py",
    "backend/contexts/data_governance/domain/aggregates/dg_twin_aggregates.py",
    "backend/contexts/data_governance/infrastructure/acl/dg_twin_acl.py",
    "backend/contexts/data_governance/application/dg_twin_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/governance_twin",
    "backend/contexts/governance_simulation",
    "backend/contexts/twin_platform",
    "backend/contexts/data_mesh",
    "backend/contexts/data_marketplace",
    "backend/contexts/metadata_governance_platform",
)


def validate_dg_twin_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.data_governance.domain.aggregates.dg_twin_aggregates import (
        DgTwinArchitectureRoot,
        DgTwinStateModelRoot,
        DgTwinSimulationEngineRoot,
        DgTwinWhatIfRoot,
        DgTwinRiskPredictionRoot,
        DgTwinOptimizationRoot,
        DgTwinAiGovernanceRoot,
        DgTwinKnowledgeGraphRoot,
        DgTwinMeshIntegrationRoot,
        DgTwinPolicySimulationRoot,
        DgTwinCqrsRoot,
        DgTwinEventSourcingRoot,
        DgTwinMicroservicesRoot,
        DgTwinZeroTrustRoot,
        DgTwinScalabilityRoot,
    )
    from contexts.data_governance.domain.services import (
        dg_platform_twin as twin,
    )

    cat = twin.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P212-L"
        and cat.get("adr") == 404
        and cat.get("sor") == "data_governance"
        and cat.get("capability") == "CAP-PLT-DG-001"
        and cat["digital_twin_architecture_complete_required"] is True
        and cat["governance_state_model_present_required"] is True
        and cat["simulation_engine_present_required"] is True
        and cat["what_if_analysis_present_required"] is True
        and cat["risk_prediction_intelligence_present_required"] is True
        and cat["optimization_engine_present_required"] is True
        and cat["ai_governance_integration_present_required"] is True
        and cat["knowledge_graph_integration_present_required"] is True
        and cat["data_mesh_integration_present_required"] is True
        and cat["policy_simulation_present_required"] is True
        and cat["cqrs_architecture_present_required"] is True
        and cat["event_sourcing_architecture_present_required"] is True
        and cat["microservices_architecture_present_required"] is True
        and cat["zero_trust_security_present_required"] is True
        and cat["enterprise_scalability_present_required"] is True
        and cat["twin_architecture"]["not_incomplete"] is True
        and cat["governance_state_model"]["not_missing"] is True
        and cat["simulation_engine"]["not_missing"] is True
        and cat["what_if_analysis"]["not_missing"] is True
        and cat["risk_prediction"]["not_missing"] is True
        and cat["optimization_engine"]["not_missing"] is True
        and cat["ai_governance_integration"]["not_missing"] is True
        and cat["knowledge_graph_integration"]["not_missing"] is True
        and cat["data_mesh_integration"]["not_missing"] is True
        and cat["policy_simulation"]["not_missing"] is True
        and cat["cqrs"]["not_missing"] is True
        and cat["event_sourcing"]["not_missing"] is True
        and cat["microservices"]["not_missing"] is True
        and cat["zero_trust"]["not_missing"] is True
        and cat["scalability"]["not_missing"] is True
        and cat["twin_architecture"]["bc_count"] >= 5
        and cat["governance_state_model"]["layer_count"] >= 4
        and cat["simulation_engine"]["type_count"] >= 4
        and cat["what_if_analysis"]["capability_count"] >= 4
        and cat["microservices"]["service_count"] >= 6
        and cat["cqrs"]["event_count"] >= 6
        and cat["cursor_outputs"]["count"] >= 18
        and (
            "data_governance_digital_twin_architecture_is_incomplete"
            in cat["quality_gates"]["reject_if"]
        )
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
            DgTwinArchitectureRoot.publish,
            tenant_id="t1",
            architecture_ref="r0",
            complete=False,
        )
        and DgTwinArchitectureRoot.publish(
            tenant_id="t1", architecture_ref="ok0"
        ).is_incomplete()
        is False
    )
    checks.append(
        not _bad(
            DgTwinStateModelRoot.define,
            tenant_id="t1",
            state_ref="r1",
            present=False,
        )
        and DgTwinStateModelRoot.define(
            tenant_id="t1", state_ref="ok1"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgTwinSimulationEngineRoot.enable,
            tenant_id="t1",
            simulation_ref="r2",
            present=False,
        )
        and DgTwinSimulationEngineRoot.enable(
            tenant_id="t1", simulation_ref="ok2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgTwinWhatIfRoot.enable,
            tenant_id="t1",
            whatif_ref="r3",
            present=False,
        )
        and DgTwinWhatIfRoot.enable(
            tenant_id="t1", whatif_ref="ok3"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgTwinRiskPredictionRoot.enable,
            tenant_id="t1",
            risk_ref="r4",
            present=False,
        )
        and DgTwinRiskPredictionRoot.enable(
            tenant_id="t1", risk_ref="ok4"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgTwinOptimizationRoot.enable,
            tenant_id="t1",
            opt_ref="r5",
            present=False,
        )
        and DgTwinOptimizationRoot.enable(
            tenant_id="t1", opt_ref="ok5"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgTwinAiGovernanceRoot.integrate,
            tenant_id="t1",
            ai_ref="r6",
            present=False,
        )
        and DgTwinAiGovernanceRoot.integrate(
            tenant_id="t1", ai_ref="ok6"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgTwinKnowledgeGraphRoot.integrate,
            tenant_id="t1",
            graph_ref="r7",
            present=False,
        )
        and DgTwinKnowledgeGraphRoot.integrate(
            tenant_id="t1", graph_ref="ok7"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgTwinMeshIntegrationRoot.align,
            tenant_id="t1",
            mesh_ref="r8",
            present=False,
        )
        and DgTwinMeshIntegrationRoot.align(
            tenant_id="t1", mesh_ref="ok8"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgTwinPolicySimulationRoot.enable,
            tenant_id="t1",
            policy_ref="r9",
            present=False,
        )
        and DgTwinPolicySimulationRoot.enable(
            tenant_id="t1", policy_ref="ok9"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgTwinCqrsRoot.align,
            tenant_id="t1",
            cqrs_ref="r10",
            present=False,
        )
        and DgTwinCqrsRoot.align(
            tenant_id="t1", cqrs_ref="ok10"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgTwinEventSourcingRoot.enable,
            tenant_id="t1",
            es_ref="r11",
            present=False,
        )
        and DgTwinEventSourcingRoot.enable(
            tenant_id="t1", es_ref="ok11"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgTwinMicroservicesRoot.declare,
            tenant_id="t1",
            ms_ref="r12",
            present=False,
        )
        and DgTwinMicroservicesRoot.declare(
            tenant_id="t1", ms_ref="ok12"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgTwinZeroTrustRoot.confirm,
            tenant_id="t1",
            zt_ref="r13",
            present=False,
        )
        and DgTwinZeroTrustRoot.confirm(
            tenant_id="t1", zt_ref="ok13"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgTwinScalabilityRoot.confirm,
            tenant_id="t1",
            scale_ref="r14",
            present=False,
        )
        and DgTwinScalabilityRoot.confirm(
            tenant_id="t1", scale_ref="ok14"
        ).is_missing()
        is False
    )
    aggregates_ok = all(checks)

    acl_path = (
        root
        / "backend/contexts/data_governance/infrastructure/acl/dg_twin_acl.py"
    )
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_p212_e" in acl_text
        and "via_p212_f" in acl_text
        and "via_p212_h" in acl_text
        and "via_p212_j" in acl_text
        and "via_p212_k" in acl_text
        and "via_enterprise_ai" in acl_text
        and "via_p208" in acl_text
        and "knowledge_graph_integration_present_required" in acl_text
    )

    router = (
        root / "backend/contexts/data_governance/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@data_governance_router.get("/twin")' in router
        and "/twin/simulation" in router
        and "/twin/what-if" in router
        and "/twin/risk-prediction" in router
        and "/twin/readiness" in router
    )

    law = (
        root
        / "docs/architecture/ENTERPRISE_DATA_GOVERNANCE_DIGITAL_TWIN.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never Data governance digital twin architecture is incomplete" in law
        and "Never Governance state model is missing" in law
        and "Never Simulation engine is missing" in law
        and "Never What-if analysis platform is missing" in law
        and "Never Risk prediction intelligence is missing" in law
        and "Never Optimization engine is missing" in law
        and "Never AI governance integration is missing" in law
        and "Never Knowledge graph integration is missing" in law
        and "Never Data mesh integration is missing" in law
        and "Never Policy simulation is missing" in law
        and "Never CQRS architecture is missing" in law
        and "Never Event sourcing architecture is missing" in law
        and "Never Microservices architecture is missing" in law
        and "Never Zero trust security is missing" in law
        and "Never Enterprise scalability is missing" in law
        and "Never Sibling governance twin BC" in law
        and (
            "Enterprise governance SHALL not only observe reality,"
            in law
        )
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
        "prompt": "P212-L",
        "adr": 404,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "catalog": catalog_ok,
        "aggregates": aggregates_ok,
        "acl": acl_ok,
        "router": router_ok,
        "documentation": doc_ok,
        "sor": "data_governance",
        "capability": "CAP-PLT-DG-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
