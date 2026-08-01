"""Quantum P215-V QGI / cognitive enterprise foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/467-enterprise-quantum-qgi.md",
    "docs/architecture/ENTERPRISE_QUANTUM_QGI.md",
    "docs/architecture/quantum/QUANTUM_QGI_CAPABILITIES.v1.yaml",
    "docs/architecture/quantum/QUANTUM_QGI_DDD_CQRS.v1.yaml",
    "docs/architecture/quantum/QUANTUM_QGI_SECURITY.v1.yaml",
    "docs/architecture/quantum/QUANTUM_QGI_VALIDATION.v1.yaml",
    "docs/architecture/quantum/P215_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/quantum/domain/services/qc_platform_qgi.py",
    "backend/contexts/quantum/domain/aggregates/qc_qgi_aggregates.py",
    "backend/contexts/quantum/infrastructure/acl/qc_qgi_acl.py",
    "backend/contexts/quantum/application/qc_qgi_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/quantum_qgi_platform",
    "backend/contexts/quantum_cognitive_brain_platform",
    "backend/contexts/quantum_reasoning_platform",
    "backend/contexts/quantum_enterprise_memory_platform",
    "backend/contexts/quantum_general_intelligence_platform",
)
def validate_qc_qgi_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.quantum.domain.aggregates.qc_qgi_aggregates import (
        QuantumGeneralIntelligenceRoot, CognitiveEnterpriseBrainRoot, AdvancedReasoningEngineRoot,
        KnowledgeUnderstandingRoot, CognitiveAgentNetworkRoot, EnterpriseMemoryRoot,
        IntelligenceEvolutionRoot, QgiKnowledgeGraphRoot, QgiDigitalTwinRoot,
    )
    from contexts.quantum.domain.services import qc_platform_qgi as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P215-V" and cat["adr"] == 467 and cat["sor"] == "quantum"
        and cat["capability"] == "CAP-PLT-QC-001"
        and cat["fabric"] == "meos_quantum_cognitive_intelligence_fabric"
        and cat["evolution_gate"] == "P215-U" and cat["os_gate"] == "P215-T" and cat["trust_gate"] == "P215-K"
        and cat["quantum_general_intelligence_platform_present_required"] is True
        and cat["cognitive_enterprise_brain_present_required"] is True
        and cat["advanced_reasoning_engine_present_required"] is True
        and cat["knowledge_understanding_layer_present_required"] is True
        and cat["cognitive_agent_network_present_required"] is True
        and cat["enterprise_memory_platform_present_required"] is True
        and cat["intelligence_evolution_framework_present_required"] is True
        and cat["bounded_contexts"]["context_count"] >= 6
        and cat["aggregates"]["aggregate_count"] >= 7
        and cat["microservices"]["service_count"] >= 9
        and cat["builds_on_p215_a"] is True and cat["builds_on_p215_u"] is True
        and cat["builds_on_p215_t"] is True and cat["via_p214_z"] is True
        and cat["never_replace_p215_u"] is True and cat["never_replace_p215_t"] is True
        and cat["never_replace_p215_k"] is True
        and cat["ungated_agi_class_actions_forbidden"] is True
        and cat["opaque_unexplainable_decisions_forbidden"] is True
        and cat["cognitive_core"]["module_local_llm_forbidden"] is True
        and cat["reasoning_engine"]["opaque_unexplainable_decisions_forbidden"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        QuantumGeneralIntelligenceRoot.enable(tenant_id="t1", qgi_ref="q1").is_missing() is False,
        CognitiveEnterpriseBrainRoot.enable(tenant_id="t1", brain_ref="b1").is_missing() is False,
        AdvancedReasoningEngineRoot.enable(tenant_id="t1", reasoning_ref="r1").is_missing() is False,
        KnowledgeUnderstandingRoot.enable(tenant_id="t1", knowledge_ref="k1").is_missing() is False,
        CognitiveAgentNetworkRoot.enable(tenant_id="t1", agent_ref="a1").is_missing() is False,
        EnterpriseMemoryRoot.enable(tenant_id="t1", memory_ref="m1").is_missing() is False,
        IntelligenceEvolutionRoot.enable(tenant_id="t1", evolution_ref="e1").is_missing() is False,
        QgiKnowledgeGraphRoot.enable(tenant_id="t1", graph_ref="kg1").is_missing() is False,
        QgiDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/quantum/infrastructure/acl/qc_qgi_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p215_a", "via_p215_u", "via_p215_t", "via_p214_z", "via_p213", "via_p214_g",
        "via_p215_k", "via_p215_r", "via_p215_s", "via_p215_q", "via_p215_h", "via_p215_l",
        "via_policy_engine", "via_workflow", "via_audit", "via_document_exchange", "via_core_platform",
        "never_replace_p215_u", "never_replace_p215_t", "never_replace_p215_k", "never_replace_core_platform",
        "module_local_llm_forbidden", "ungated_agi_class_actions_forbidden",
        "opaque_unexplainable_decisions_forbidden", "module_local_quantum_qgi_forbidden",
    ))
    router = (root / "backend/contexts/quantum/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@quantum_router.get("/qgi")', "/qgi/reasoning", "/qgi/brain", "/qgi/agents",
        "/qgi/memory", "/qgi/knowledge", "/qgi/evolution",
        "/qgi/knowledge-graph", "/qgi/digital-twin", "/qgi/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_QUANTUM_QGI.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Quantum General Intelligence Platform is missing",
        "Never Cognitive Enterprise Brain is missing",
        "Never Advanced Reasoning Engine is missing",
        "Never Knowledge Understanding Layer is missing",
        "Never Cognitive Agent Network is missing",
        "Never Enterprise Memory Platform is missing",
        "Never Intelligence Evolution Framework is missing",
        "Never Knowledge Graph Integration is missing",
        "Never Digital Twin Integration is missing",
        "Never CQRS architecture is missing",
        "Never Event Architecture is missing",
        "Never Microservices Architecture is missing",
        "Never API First Architecture is missing",
        "Never Cloud Native Deployment is missing",
        "Never Sibling Quantum BC",
        "Never Replace P215-U Evolution Fabric",
        "Never Replace P215-T Control Plane",
        "Never Replace Core Platform",
        "Never Replace P215-K Trust Gate",
        "Never Module-Local LLM",
        "Never Ungated AGI-Class Actions",
        "Never Opaque Unexplainable Decisions",
        "MEOS Quantum General Intelligence Platform SHALL provide",
        "P215-A", "P215-U", "P215-T", "P214-Z", "P213", "P215-K",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P215-V", "adr": 467, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "quantum",
        "capability": "CAP-PLT-QC-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
