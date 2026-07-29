"""Quantum P215-L digital twin / reality modeling foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/457-enterprise-quantum-twin.md",
    "docs/architecture/ENTERPRISE_QUANTUM_TWIN.md",
    "docs/architecture/quantum/QUANTUM_TWIN_CAPABILITIES.v1.yaml",
    "docs/architecture/quantum/QUANTUM_TWIN_DDD_CQRS.v1.yaml",
    "docs/architecture/quantum/QUANTUM_TWIN_SECURITY.v1.yaml",
    "docs/architecture/quantum/QUANTUM_TWIN_VALIDATION.v1.yaml",
    "docs/architecture/quantum/P215_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/quantum/domain/services/qc_platform_twin.py",
    "backend/contexts/quantum/domain/aggregates/qc_twin_aggregates.py",
    "backend/contexts/quantum/infrastructure/acl/qc_twin_acl.py",
    "backend/contexts/quantum/application/qc_twin_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/quantum_digital_twin_platform",
    "backend/contexts/quantum_simulation_intelligence_platform",
    "backend/contexts/quantum_reality_modeling_platform",
    "backend/contexts/quantum_scenario_platform",
)
def validate_qc_twin_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.quantum.domain.aggregates.qc_twin_aggregates import (
        QuantumDigitalTwinPlatformRoot, SimulationIntelligenceRoot, RealityModelingRoot,
        PredictiveIntelligenceRoot, ScenarioSimulationRoot, EvolutionIntelligenceRoot,
        TwinKnowledgeGraphRoot, TwinGovernanceIntegrationRoot,
    )
    from contexts.quantum.domain.services import qc_platform_twin as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P215-L" and cat["adr"] == 457 and cat["sor"] == "quantum"
        and cat["capability"] == "CAP-PLT-QC-001"
        and cat["fabric"] == "meos_quantum_reality_intelligence_fabric"
        and cat["quantum_digital_twin_platform_present_required"] is True
        and cat["quantum_simulation_intelligence_present_required"] is True
        and cat["quantum_reality_modeling_present_required"] is True
        and cat["predictive_intelligence_present_required"] is True
        and cat["scenario_simulation_present_required"] is True
        and cat["evolution_intelligence_present_required"] is True
        and cat["knowledge_graph_integration_present_required"] is True
        and cat["governance_integration_present_required"] is True
        and cat["bounded_contexts"]["context_count"] >= 6
        and cat["aggregates"]["aggregate_count"] >= 7
        and cat["microservices"]["service_count"] >= 10
        and cat["builds_on_p215_a"] is True and cat["builds_on_p215_d"] is True
        and cat["builds_on_p215_f"] is True and cat["builds_on_p215_g"] is True
        and cat["builds_on_p215_h"] is True and cat["builds_on_p215_i"] is True
        and cat["builds_on_p215_j"] is True and cat["governed_by_p215_k"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        QuantumDigitalTwinPlatformRoot.enable(tenant_id="t1", twin_platform_ref="tp1").is_missing() is False,
        SimulationIntelligenceRoot.enable(tenant_id="t1", simulation_ref="s1").is_missing() is False,
        RealityModelingRoot.enable(tenant_id="t1", reality_ref="r1").is_missing() is False,
        PredictiveIntelligenceRoot.enable(tenant_id="t1", prediction_ref="p1").is_missing() is False,
        ScenarioSimulationRoot.enable(tenant_id="t1", scenario_ref="sc1").is_missing() is False,
        EvolutionIntelligenceRoot.enable(tenant_id="t1", evolution_ref="e1").is_missing() is False,
        TwinKnowledgeGraphRoot.enable(tenant_id="t1", graph_ref="g1").is_missing() is False,
        TwinGovernanceIntegrationRoot.enable(tenant_id="t1", governance_ref="gov1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/quantum/infrastructure/acl/qc_twin_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p215_a", "via_p215_d", "via_p215_f", "via_p215_g", "via_p215_h", "via_p215_i",
        "via_p215_j", "via_p215_k", "via_p214_z", "via_p214_j",
        "module_local_quantum_twin_forbidden",
    ))
    router = (root / "backend/contexts/quantum/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@quantum_router.get("/twin")', "/twin/reality", "/twin/simulation",
        "/twin/scenarios", "/twin/predictions", "/twin/evolution",
        "/twin/sync", "/twin/knowledge-graph", "/twin/governance",
        "/twin/analytics", "/twin/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_QUANTUM_TWIN.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Quantum Digital Twin Platform is missing",
        "Never Quantum Simulation Intelligence is missing",
        "Never Quantum Reality Modeling is missing",
        "Never Predictive Intelligence is missing",
        "Never Scenario Simulation is missing",
        "Never Evolution Intelligence is missing",
        "Never Knowledge Graph Integration is missing",
        "Never Governance Integration is missing",
        "Never CQRS architecture is missing",
        "Never Event Architecture is missing",
        "Never Microservices Architecture is missing",
        "Never API First Architecture is missing",
        "Never Cloud Native Deployment is missing",
        "Never Sibling Quantum BC",
        "MEOS Quantum Digital Twin Platform SHALL create",
        "P215-A", "P215-D", "P215-F", "P215-G", "P215-H", "P215-I", "P215-J", "P215-K",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P215-L", "adr": 457, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "quantum",
        "capability": "CAP-PLT-QC-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
