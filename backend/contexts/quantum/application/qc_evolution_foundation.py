"""Quantum P215-U autonomous evolution / self-healing foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/466-enterprise-quantum-evolution.md",
    "docs/architecture/ENTERPRISE_QUANTUM_EVOLUTION.md",
    "docs/architecture/quantum/QUANTUM_EVOLUTION_CAPABILITIES.v1.yaml",
    "docs/architecture/quantum/QUANTUM_EVOLUTION_DDD_CQRS.v1.yaml",
    "docs/architecture/quantum/QUANTUM_EVOLUTION_SECURITY.v1.yaml",
    "docs/architecture/quantum/QUANTUM_EVOLUTION_VALIDATION.v1.yaml",
    "docs/architecture/quantum/P215_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/quantum/domain/services/qc_platform_evolution.py",
    "backend/contexts/quantum/domain/aggregates/qc_evolution_aggregates.py",
    "backend/contexts/quantum/infrastructure/acl/qc_evolution_acl.py",
    "backend/contexts/quantum/application/qc_evolution_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/quantum_evolution_platform",
    "backend/contexts/quantum_autonomous_intelligence_platform",
    "backend/contexts/quantum_self_healing_platform",
    "backend/contexts/quantum_singularity_platform",
    "backend/contexts/quantum_agent_evolution_platform",
)
def validate_qc_evolution_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.quantum.domain.aggregates.qc_evolution_aggregates import (
        QuantumAutonomousIntelligenceRoot, SelfHealingEcosystemRoot, AutonomousAgentsRoot,
        EvolutionIntelligenceRoot, SingularityReadinessRoot, SelfOptimizationRoot,
        EvolutionKnowledgeGraphRoot, EvolutionDigitalTwinRoot, AutonomousGovernanceEvolutionRoot,
    )
    from contexts.quantum.domain.services import qc_platform_evolution as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P215-U" and cat["adr"] == 466 and cat["sor"] == "quantum"
        and cat["capability"] == "CAP-PLT-QC-001"
        and cat["fabric"] == "meos_quantum_autonomous_evolution_fabric"
        and cat["os_gate"] == "P215-T" and cat["trust_gate"] == "P215-K"
        and cat["quantum_autonomous_intelligence_platform_present_required"] is True
        and cat["self_healing_ecosystem_present_required"] is True
        and cat["autonomous_agents_present_required"] is True
        and cat["evolution_intelligence_present_required"] is True
        and cat["singularity_readiness_framework_present_required"] is True
        and cat["self_optimization_present_required"] is True
        and cat["bounded_contexts"]["context_count"] >= 6
        and cat["aggregates"]["aggregate_count"] >= 7
        and cat["microservices"]["service_count"] >= 9
        and cat["builds_on_p215_a"] is True and cat["builds_on_p215_t"] is True
        and cat["via_p214_z"] is True and cat["via_p215_k"] is True
        and cat["never_replace_p215_t"] is True and cat["never_replace_core_platform"] is True
        and cat["never_replace_p215_k"] is True
        and cat["ungated_autonomous_actions_forbidden"] is True
        and cat["autonomous_intelligence"]["module_local_llm_forbidden"] is True
        and cat["singularity_readiness"]["ungated_autonomous_actions_forbidden"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        QuantumAutonomousIntelligenceRoot.enable(tenant_id="t1", intelligence_ref="i1").is_missing() is False,
        SelfHealingEcosystemRoot.enable(tenant_id="t1", healing_ref="h1").is_missing() is False,
        AutonomousAgentsRoot.enable(tenant_id="t1", agent_ref="a1").is_missing() is False,
        EvolutionIntelligenceRoot.enable(tenant_id="t1", evolution_ref="e1").is_missing() is False,
        SingularityReadinessRoot.enable(tenant_id="t1", singularity_ref="s1").is_missing() is False,
        SelfOptimizationRoot.enable(tenant_id="t1", optimization_ref="o1").is_missing() is False,
        EvolutionKnowledgeGraphRoot.enable(tenant_id="t1", graph_ref="kg1").is_missing() is False,
        EvolutionDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        AutonomousGovernanceEvolutionRoot.enable(tenant_id="t1", governance_ref="g1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/quantum/infrastructure/acl/qc_evolution_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p215_a", "via_p215_t", "via_p215_n", "via_p214_j", "via_p215_s", "via_p215_r",
        "via_p215_q", "via_p215_k", "via_p215_h", "via_p215_l", "via_p214_z", "via_p213",
        "via_policy_engine", "via_workflow", "via_audit", "via_core_platform",
        "never_replace_p215_t", "never_replace_p215_k", "never_replace_core_platform",
        "ungated_autonomous_actions_forbidden", "module_local_llm_forbidden",
        "module_local_quantum_evolution_forbidden",
    ))
    router = (root / "backend/contexts/quantum/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@quantum_router.get("/evolution")', "/evolution/intelligence", "/evolution/healing",
        "/evolution/agents", "/evolution/optimization", "/evolution/singularity",
        "/evolution/governance", "/evolution/knowledge-graph", "/evolution/digital-twin",
        "/evolution/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_QUANTUM_EVOLUTION.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Quantum Autonomous Intelligence Platform is missing",
        "Never Self-Healing Ecosystem is missing",
        "Never Autonomous Agents is missing",
        "Never Evolution Intelligence is missing",
        "Never Singularity Readiness Framework is missing",
        "Never Self Optimization is missing",
        "Never Knowledge Graph Integration is missing",
        "Never Digital Twin Integration is missing",
        "Never CQRS architecture is missing",
        "Never Event Architecture is missing",
        "Never Microservices Architecture is missing",
        "Never API First Architecture is missing",
        "Never Cloud Native Deployment is missing",
        "Never Sibling Quantum BC",
        "Never Replace P215-T Control Plane",
        "Never Replace Core Platform",
        "Never Replace P215-K Trust Gate",
        "Never Ungated Autonomous Actions",
        "Never Module-Local LLM",
        "MEOS Quantum Autonomous Intelligence Platform SHALL",
        "P215-A", "P215-T", "P215-N", "P215-S", "P214-Z", "P213", "P215-K",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P215-U", "adr": 466, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "quantum",
        "capability": "CAP-PLT-QC-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
