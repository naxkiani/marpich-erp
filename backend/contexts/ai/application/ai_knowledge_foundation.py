"""AI P214-G Knowledge / RAG / Cognitive foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/427-enterprise-ai-knowledge.md",
    "docs/architecture/ENTERPRISE_AI_KNOWLEDGE.md",
    "docs/architecture/enterprise_ai/AI_KNOWLEDGE_CAPABILITIES.v1.yaml",
    "docs/architecture/enterprise_ai/AI_KNOWLEDGE_DDD_CQRS.v1.yaml",
    "docs/architecture/enterprise_ai/AI_KNOWLEDGE_SECURITY.v1.yaml",
    "docs/architecture/enterprise_ai/AI_KNOWLEDGE_VALIDATION.v1.yaml",
    "backend/contexts/ai/domain/services/ai_platform_knowledge.py",
    "backend/contexts/ai/domain/aggregates/ai_knowledge_aggregates.py",
    "backend/contexts/ai/infrastructure/acl/ai_knowledge_acl.py",
    "backend/contexts/ai/application/ai_knowledge_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/ml_platform",
    "backend/contexts/generative_ai",
    "backend/contexts/llm_platform",
    "backend/contexts/ai_core",
    "backend/contexts/vector_intelligence",
    "backend/contexts/ai_knowledge",
    "backend/contexts/rag_platform",
    "backend/contexts/cognitive_intelligence",
    "backend/contexts/knowledge_graph_platform",
    "backend/contexts/semantic_intelligence",
    "backend/contexts/ai_memory_platform",
)


def validate_ai_knowledge_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.ai.domain.aggregates.ai_knowledge_aggregates import (
        AiMemoryRoot,
        ContextEngineRoot,
        KnowledgeGraphRoot,
        KnowledgePlatformRoot,
        RagPlatformRoot,
        VectorIntelligenceRoot,
    )
    from contexts.ai.domain.services import ai_platform_knowledge as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P214-G"
        and cat.get("adr") == 427
        and cat.get("sor") == "ai"
        and cat.get("capability") == "CAP-PLT-AI-001"
        and cat.get("principle") == catmod.PRINCIPLE
        and cat.get("fabric") == catmod.FABRIC
        and "trusted cognitive foundation" in cat["principle"]
        and cat["domain_model"]["core_domain"] == catmod.CORE_DOMAIN
        and cat["domain_model"]["supporting_count"] >= 9
        and cat["bounded_contexts"]["context_count"] >= 7
        and cat["rag_platform"]["pipeline_count"] >= 11
        and cat["knowledge_fabric"]["lifecycle_stage_count"] >= 8
        and cat["enterprise_ai_knowledge_platform_present_required"] is True
        and cat["rag_platform_present_required"] is True
        and cat["vector_intelligence_platform_present_required"] is True
        and cat["knowledge_graph_integration_present_required"] is True
        and cat["semantic_intelligence_present_required"] is True
        and cat["ai_memory_platform_present_required"] is True
        and cat["context_intelligence_present_required"] is True
        and cat["cognitive_reasoning_present_required"] is True
        and cat["knowledge_governance_present_required"] is True
        and cat["cqrs_architecture_present_required"] is True
        and cat["event_architecture_present_required"] is True
        and cat["microservices_architecture_present_required"] is True
        and cat["api_first_architecture_present_required"] is True
        and cat["zero_trust_security_present_required"] is True
        and cat["cloud_native_deployment_present_required"] is True
        and cat["sibling_ai_bc_forbidden"] is True
        and cat["governance"]["via_p212"] is True
        and cat["semantic"]["via_p213_l"] is True
        and cat["graph_rag"]["via_p213_l"] is True
        and cat["rag_platform"]["via_p214_e"] is True
        and cat["memory"]["via_p214_f"] is True
        and cat["deployment"]["via_p213_o"] is True
        and cat["cqrs"]["command_count"] >= 6
        and cat["events"]["core_event_count"] >= 8
        and cat["microservices"]["service_count"] >= 10
        and cat["cursor_outputs"]["count"] >= 20
        and "enterprise_ai_knowledge_platform_is_missing"
        in cat["quality_gates"]["reject_if"]
        and "P214-F" in cat["builds_on"]
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )

    def _bad(fn, **kwargs):
        try:
            fn(**kwargs)
            return True
        except ValueError:
            return False

    checks = [
        not _bad(
            KnowledgePlatformRoot.enable,
            tenant_id="t1",
            platform_ref="p1",
            present=False,
        )
        and KnowledgePlatformRoot.enable(
            tenant_id="t1", platform_ref="p2"
        ).is_missing()
        is False,
        not _bad(
            RagPlatformRoot.enable,
            tenant_id="t1",
            pipeline_ref="r1",
            present=False,
        )
        and RagPlatformRoot.enable(
            tenant_id="t1", pipeline_ref="r2"
        ).is_missing()
        is False,
        not _bad(
            VectorIntelligenceRoot.enable,
            tenant_id="t1",
            vector_ref="v1",
            present=False,
        )
        and VectorIntelligenceRoot.enable(
            tenant_id="t1", vector_ref="v2"
        ).is_missing()
        is False,
        not _bad(
            KnowledgeGraphRoot.enable,
            tenant_id="t1",
            graph_ref="g1",
            present=False,
        )
        and KnowledgeGraphRoot.enable(
            tenant_id="t1", graph_ref="g2"
        ).is_missing()
        is False,
        not _bad(
            AiMemoryRoot.enable,
            tenant_id="t1",
            memory_ref="m1",
            present=False,
        )
        and AiMemoryRoot.enable(
            tenant_id="t1", memory_ref="m2"
        ).is_missing()
        is False,
        not _bad(
            ContextEngineRoot.enable,
            tenant_id="t1",
            context_ref="c1",
            present=False,
        )
        and ContextEngineRoot.enable(
            tenant_id="t1", context_ref="c2"
        ).is_missing()
        is False,
    ]
    aggregates_ok = all(checks)

    acl_path = (
        root / "backend/contexts/ai/infrastructure/acl/ai_knowledge_acl.py"
    )
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_p207" in acl_text
        and "via_p208" in acl_text
        and "via_p209" in acl_text
        and "via_p210" in acl_text
        and "via_p211" in acl_text
        and "via_p212" in acl_text
        and "via_p213_l" in acl_text
        and "via_p213_o" in acl_text
        and "via_p214_a" in acl_text
        and "via_p214_c" in acl_text
        and "via_p214_e" in acl_text
        and "via_p214_f" in acl_text
        and "module_local_vector_sdk_forbidden" in acl_text
    )

    router = (
        root / "backend/contexts/ai/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@router.get("/knowledge")' in router
        and "/knowledge/readiness" in router
        and "/knowledge/rag" in router
        and "/knowledge/vectors" in router
        and "/knowledge/memory" in router
        and "/knowledge/graph-rag" in router
        and "/knowledge/fabric" in router
    )

    law = (root / "docs/architecture/ENTERPRISE_AI_KNOWLEDGE.md").read_text(
        encoding="utf-8"
    )
    doc_ok = (
        "Never Enterprise AI Knowledge platform is missing" in law
        and "Never RAG platform is missing" in law
        and "Never Vector intelligence platform is missing" in law
        and "Never Knowledge graph integration is missing" in law
        and "Never Semantic intelligence is missing" in law
        and "Never AI memory platform is missing" in law
        and "Never Context intelligence is missing" in law
        and "Never Cognitive reasoning is missing" in law
        and "Never Knowledge governance is missing" in law
        and "Never CQRS architecture is missing" in law
        and "Never Event architecture is missing" in law
        and "Never Microservices architecture is missing" in law
        and "Never API first architecture is missing" in law
        and "Never Zero trust security is missing" in law
        and "Never Cloud native deployment is missing" in law
        and "Never Sibling AI BC" in law
        and "MEOS Enterprise Cognitive Knowledge Fabric" in law
        and "trusted cognitive foundation" in law
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
        "prompt": "P214-G",
        "adr": 427,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "catalog": catalog_ok,
        "aggregates": aggregates_ok,
        "acl": acl_ok,
        "router": router_ok,
        "documentation": doc_ok,
        "sor": "ai",
        "capability": "CAP-PLT-AI-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
