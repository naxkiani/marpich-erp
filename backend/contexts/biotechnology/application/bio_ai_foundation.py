"""Biotechnology P217-E Bio-AI foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/504-enterprise-biotechnology-bio-ai.md",
    "docs/architecture/ENTERPRISE_BIOTECHNOLOGY_BIO_AI.md",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_BIO_AI_ARCHITECTURE.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_BIO_AI_MODELS.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_BIO_AI_DDD_CQRS.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_BIO_AI_SECURITY.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_BIO_AI_VALIDATION.v1.yaml",
    "docs/architecture/biotechnology/P217_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/biotechnology/domain/services/bio_platform_bio_ai.py",
    "backend/contexts/biotechnology/domain/aggregates/bio_ai_aggregates.py",
    "backend/contexts/biotechnology/infrastructure/acl/bio_ai_acl.py",
    "backend/contexts/biotechnology/application/bio_ai_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/biotechnology_bio_ai_platform",
    "backend/contexts/bio_foundation_model_platform",
    "backend/contexts/computational_life_intelligence_platform",
)
def validate_bio_ai_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.biotechnology.domain.aggregates.bio_ai_aggregates import (
        BioAiPlatformRoot, FoundationModelsRoot, AiBiologyEngineRoot, LifeIntelligenceCoreRoot,
        ScientificAgentsRoot, KnowledgeGraphRoot, ModelLifecycleRoot, ResponsibleBioAiRoot, BioAiSecurityRoot,
    )
    from contexts.biotechnology.domain.services import bio_platform_bio_ai as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P217-E" and cat["adr"] == 504 and cat["sor"] == "biotechnology"
        and cat["capability"] == "CAP-PLT-BIO-001"
        and cat["fabric"] == "meos_bio_ai_intelligence_fabric"
        and cat["foundation_gate"] == "P217" and cat["mission_gate"] == "P217-A"
        and cat["strategy_gate"] == "P217-B" and cat["domain_gate"] == "P217-C"
        and cat["infrastructure_gate"] == "P217-D"
        and cat["robotics_gate"] == "P216-Z" and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["bio_ai_platform_present_required"] is True
        and cat["foundation_models_present_required"] is True
        and cat["ai_biology_engine_present_required"] is True
        and cat["computational_life_intelligence_core_present_required"] is True
        and cat["scientific_ai_agents_present_required"] is True
        and cat["knowledge_graph_integration_present_required"] is True
        and cat["ai_governance_present_required"] is True
        and cat["security_architecture_present_required"] is True
        and cat["deployment_architecture_present_required"] is True
        and cat["architecture"]["layer_count"] == 5
        and cat["foundation_models"]["model_count"] == 5
        and cat["ai_biology_engine"]["component_count"] == 4
        and cat["life_intelligence_core"]["component_count"] == 4
        and cat["scientific_agents"]["agent_count"] == 5
        and cat["bounded_contexts"]["context_count"] == 7
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 8
        and cat["never_replace_p217_foundation"] is True
        and cat["never_replace_p217_d_infrastructure"] is True
        and cat["bio_ai_via_p214z_acl_only"] is True
        and cat["no_module_local_llm"] is True
        and cat["never_opaque_unexplainable_decisions"] is True
        and cat["opaque_bio_safety_strategy_forbidden"] is True
        and cat["foundation_for_p217_f"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        BioAiPlatformRoot.enable(tenant_id="t1", platform_ref="p1").is_missing() is False,
        FoundationModelsRoot.enable(tenant_id="t1", models_ref="m1").is_missing() is False,
        AiBiologyEngineRoot.enable(tenant_id="t1", engine_ref="e1").is_missing() is False,
        LifeIntelligenceCoreRoot.enable(tenant_id="t1", clic_ref="c1").is_missing() is False,
        ScientificAgentsRoot.enable(tenant_id="t1", agents_ref="a1").is_missing() is False,
        KnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="k1").is_missing() is False,
        ModelLifecycleRoot.enable(tenant_id="t1", lifecycle_ref="l1").is_missing() is False,
        ResponsibleBioAiRoot.enable(tenant_id="t1", governance_ref="g1").is_missing() is False,
        BioAiSecurityRoot.enable(tenant_id="t1", security_ref="s1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/biotechnology/infrastructure/acl/bio_ai_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p217", "via_p217_a", "via_p217_b", "via_p217_c", "via_p217_d", "via_p216_z", "via_p215_z", "via_p214_z",
        "via_policy_engine", "via_workflow", "via_audit", "via_identity", "via_core_platform",
        "never_replace_p217_foundation", "never_replace_p217_a_mission", "never_replace_p217_b_strategy",
        "never_replace_p217_c_domain", "never_replace_p217_d_infrastructure",
        "never_replace_p215_z", "never_replace_p216_z", "never_replace_ai_platform",
        "never_replace_core_platform", "bio_ai_via_p214z_acl_only", "no_module_local_llm",
        "never_opaque_unexplainable_decisions", "opaque_bio_safety_strategy_forbidden",
        "module_local_biotechnology_bio_ai_forbidden",
    ))
    router = (root / "backend/contexts/biotechnology/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@biotechnology_router.get("/bio-ai")', "/bio-ai/vision", "/bio-ai/architecture",
        "/bio-ai/foundation-models", "/bio-ai/engine", "/bio-ai/life-intelligence",
        "/bio-ai/agents", "/bio-ai/knowledge-graph", "/bio-ai/lifecycle",
        "/bio-ai/governance", "/bio-ai/security", "/bio-ai/integration",
        "/bio-ai/deployment", "/bio-ai/testing", "/bio-ai/cqrs", "/bio-ai/events",
        "/bio-ai/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_BIOTECHNOLOGY_BIO_AI.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Bio-AI Platform is missing",
        "Never Foundation Models are missing",
        "Never AI Biology Engine is missing",
        "Never Computational Life Intelligence Core is missing",
        "Never Scientific AI Agents are missing",
        "Never Knowledge Graph Integration is missing",
        "Never AI Governance is missing",
        "Never Security Architecture is missing",
        "Never Deployment Architecture is missing",
        "Never CQRS architecture is missing",
        "Never Event Architecture is missing",
        "Never Microservices Architecture is missing",
        "Never Sibling Biotechnology BC",
        "Never Replace P217 Foundation",
        "Never Replace P217-A Mission",
        "Never Replace P217-B Strategy",
        "Never Replace P217-C Domain",
        "Never Replace P217-D Infrastructure",
        "Never Replace Core Platform",
        "Never Replace AI Platform",
        "Never Replace Quantum Supreme (P215-Z)",
        "Never Replace Robotics Supreme (P216-Z)",
        "Never Replace Hospital EMR SoR",
        "Never Replace Laboratory LIMS SoR",
        "Never Replace Pharmacy SoR",
        "Never Module-Local LLM",
        "Never Opaque Unexplainable Decisions",
        "Never Skip Genomic Privacy Strategy",
        "Never Skip Ethical Bioengineering Strategy",
        "Never Skip Scientific Integrity Strategy",
        "Never Opaque Bio Safety Strategy",
        "Create an enterprise biological intelligence system",
        "P217", "P217-D", "P216-Z", "P215-Z", "P214-Z", "P217-F",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P217-E", "adr": 504, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "biotechnology",
        "capability": "CAP-PLT-BIO-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
