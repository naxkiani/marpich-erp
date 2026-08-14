"""Quantum P215-W civilization / collective intelligence foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/468-enterprise-quantum-civilization.md",
    "docs/architecture/ENTERPRISE_QUANTUM_CIVILIZATION.md",
    "docs/architecture/quantum/QUANTUM_CIVILIZATION_CAPABILITIES.v1.yaml",
    "docs/architecture/quantum/QUANTUM_CIVILIZATION_DDD_CQRS.v1.yaml",
    "docs/architecture/quantum/QUANTUM_CIVILIZATION_SECURITY.v1.yaml",
    "docs/architecture/quantum/QUANTUM_CIVILIZATION_VALIDATION.v1.yaml",
    "docs/architecture/quantum/P215_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/quantum/domain/services/qc_platform_civilization.py",
    "backend/contexts/quantum/domain/aggregates/qc_civilization_aggregates.py",
    "backend/contexts/quantum/infrastructure/acl/qc_civilization_acl.py",
    "backend/contexts/quantum/application/qc_civilization_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/quantum_civilization_platform",
    "backend/contexts/quantum_collective_intelligence_platform",
    "backend/contexts/quantum_cognitive_ecosystem_platform",
    "backend/contexts/quantum_knowledge_civilization_platform",
    "backend/contexts/quantum_agent_society_platform",
)
def validate_qc_civilization_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.quantum.domain.aggregates.qc_civilization_aggregates import (
        QuantumCivilizationIntelligenceRoot, CollectiveIntelligenceNetworkRoot, GlobalCognitiveEcosystemRoot,
        KnowledgeCivilizationRoot, MultiAgentIntelligenceSocietyRoot, CollectiveDecisionIntelligenceRoot,
        FutureIntelligenceEvolutionRoot, CivilizationKnowledgeGraphRoot, CivilizationDigitalTwinRoot,
    )
    from contexts.quantum.domain.services import qc_platform_civilization as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P215-W" and cat["adr"] == 468 and cat["sor"] == "quantum"
        and cat["capability"] == "CAP-PLT-QC-001"
        and cat["fabric"] == "meos_quantum_civilization_intelligence_fabric"
        and cat["qgi_gate"] == "P215-V" and cat["evolution_gate"] == "P215-U"
        and cat["os_gate"] == "P215-T" and cat["trust_gate"] == "P215-K"
        and cat["quantum_civilization_intelligence_layer_present_required"] is True
        and cat["collective_intelligence_network_present_required"] is True
        and cat["global_cognitive_ecosystem_present_required"] is True
        and cat["knowledge_civilization_platform_present_required"] is True
        and cat["multi_agent_intelligence_society_present_required"] is True
        and cat["collective_decision_intelligence_present_required"] is True
        and cat["future_intelligence_evolution_present_required"] is True
        and cat["bounded_contexts"]["context_count"] >= 6
        and cat["aggregates"]["aggregate_count"] >= 7
        and cat["microservices"]["service_count"] >= 9
        and cat["builds_on_p215_a"] is True and cat["builds_on_p215_v"] is True
        and cat["builds_on_p215_u"] is True and cat["via_p213"] is True
        and cat["never_replace_p215_v"] is True and cat["never_replace_p215_u"] is True
        and cat["never_replace_p215_t"] is True and cat["never_replace_p215_k"] is True
        and cat["ungoverned_cross_tenant_intelligence_federation_forbidden"] is True
        and cat["opaque_collective_decisions_forbidden"] is True
        and cat["civilization_core"]["module_local_llm_forbidden"] is True
        and cat["collective_decision"]["opaque_collective_decisions_forbidden"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        QuantumCivilizationIntelligenceRoot.enable(tenant_id="t1", civilization_ref="c1").is_missing() is False,
        CollectiveIntelligenceNetworkRoot.enable(tenant_id="t1", network_ref="n1").is_missing() is False,
        GlobalCognitiveEcosystemRoot.enable(tenant_id="t1", ecosystem_ref="e1").is_missing() is False,
        KnowledgeCivilizationRoot.enable(tenant_id="t1", knowledge_ref="k1").is_missing() is False,
        MultiAgentIntelligenceSocietyRoot.enable(tenant_id="t1", society_ref="s1").is_missing() is False,
        CollectiveDecisionIntelligenceRoot.enable(tenant_id="t1", decision_ref="d1").is_missing() is False,
        FutureIntelligenceEvolutionRoot.enable(tenant_id="t1", evolution_ref="f1").is_missing() is False,
        CivilizationKnowledgeGraphRoot.enable(tenant_id="t1", graph_ref="kg1").is_missing() is False,
        CivilizationDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/quantum/infrastructure/acl/qc_civilization_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p215_a", "via_p215_v", "via_p215_u", "via_p215_t", "via_p213", "via_p214_g",
        "via_p215_k", "via_p215_r", "via_p215_s", "via_p215_q", "via_p215_h", "via_p215_l",
        "via_p214_z", "via_policy_engine", "via_workflow", "via_audit", "via_federation_contract",
        "via_core_platform", "never_replace_p215_v", "never_replace_p215_u", "never_replace_p215_t",
        "never_replace_p215_k", "never_replace_core_platform", "module_local_llm_forbidden",
        "ungoverned_cross_tenant_intelligence_federation_forbidden",
        "opaque_collective_decisions_forbidden", "module_local_quantum_civilization_forbidden",
    ))
    router = (root / "backend/contexts/quantum/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@quantum_router.get("/civilization")', "/civilization/network", "/civilization/ecosystem",
        "/civilization/knowledge", "/civilization/agents", "/civilization/decisions",
        "/civilization/evolution", "/civilization/knowledge-graph", "/civilization/digital-twin",
        "/civilization/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_QUANTUM_CIVILIZATION.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Quantum Civilization Intelligence Layer is missing",
        "Never Collective Intelligence Network is missing",
        "Never Global Cognitive Ecosystem is missing",
        "Never Knowledge Civilization Platform is missing",
        "Never Multi-Agent Intelligence Society is missing",
        "Never Collective Decision Intelligence is missing",
        "Never Future Intelligence Evolution is missing",
        "Never Knowledge Graph Integration is missing",
        "Never Digital Twin Integration is missing",
        "Never CQRS architecture is missing",
        "Never Event Architecture is missing",
        "Never Microservices Architecture is missing",
        "Never API First Architecture is missing",
        "Never Cloud Native Deployment is missing",
        "Never Sibling Quantum BC",
        "Never Replace P215-V QGI Fabric",
        "Never Replace P215-U Evolution Fabric",
        "Never Replace P215-T Control Plane",
        "Never Replace Core Platform",
        "Never Replace P215-K Trust Gate",
        "Never Module-Local LLM",
        "Never Ungoverned Cross-Tenant Intelligence Federation",
        "Never Opaque Collective Decisions",
        "MEOS Quantum Civilization Intelligence Platform SHALL",
        "P215-A", "P215-V", "P215-U", "P215-T", "P213", "P215-K",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P215-W", "adr": 468, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "quantum",
        "capability": "CAP-PLT-QC-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
