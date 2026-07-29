"""AI P214-E Generative AI & LLM foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/425-enterprise-ai-generative-llm.md",
    "docs/architecture/ENTERPRISE_AI_GENERATIVE_LLM.md",
    "docs/architecture/enterprise_ai/AI_GENAI_CAPABILITIES.v1.yaml",
    "docs/architecture/enterprise_ai/AI_GENAI_DDD_CQRS.v1.yaml",
    "docs/architecture/enterprise_ai/AI_GENAI_SECURITY.v1.yaml",
    "docs/architecture/enterprise_ai/AI_GENAI_VALIDATION.v1.yaml",
    "backend/contexts/ai/domain/services/ai_platform_genai.py",
    "backend/contexts/ai/domain/aggregates/ai_genai_aggregates.py",
    "backend/contexts/ai/infrastructure/acl/ai_genai_acl.py",
    "backend/contexts/ai/application/ai_genai_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/ml_platform",
    "backend/contexts/generative_ai",
    "backend/contexts/llm_platform",
    "backend/contexts/ai_core",
    "backend/contexts/vector_intelligence",
    "backend/contexts/prompt_platform",
    "backend/contexts/rag_platform",
    "backend/contexts/foundation_model_registry",
    "backend/contexts/ai_assistant_platform",
    "backend/contexts/multimodal_ai",
    "backend/contexts/model_lifecycle_platform",
)


def validate_ai_genai_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.ai.domain.aggregates.ai_genai_aggregates import (
        AssistantPlatformRoot,
        FoundationModelRoot,
        GenaiPlatformRoot,
        PromptPlatformRoot,
        RagPlatformRoot,
        VectorIntelligenceRoot,
    )
    from contexts.ai.domain.services import ai_platform_genai as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P214-E"
        and cat.get("adr") == 425
        and cat.get("sor") == "ai"
        and cat.get("capability") == "CAP-PLT-AI-001"
        and cat.get("principle") == catmod.PRINCIPLE
        and cat.get("fabric") == catmod.FABRIC
        and "cognitive interface" in cat["principle"]
        and cat["domain_model"]["core_domain"] == catmod.CORE_DOMAIN
        and cat["domain_model"]["supporting_count"] >= 9
        and cat["bounded_contexts"]["context_count"] >= 7
        and cat["llmops"]["stage_count"] >= 9
        and cat["assistants"]["copilot_count"] >= 8
        and cat["rag_platform"]["pipeline_count"] >= 8
        and cat["enterprise_generative_ai_platform_present_required"] is True
        and cat["llm_platform_present_required"] is True
        and cat["foundation_model_management_present_required"] is True
        and cat["prompt_intelligence_platform_present_required"] is True
        and cat["rag_platform_present_required"] is True
        and cat["vector_intelligence_present_required"] is True
        and cat["ai_assistant_platform_present_required"] is True
        and cat["multimodal_ai_foundation_present_required"] is True
        and cat["llmops_architecture_present_required"] is True
        and cat["ai_governance_present_required"] is True
        and cat["cqrs_architecture_present_required"] is True
        and cat["event_architecture_present_required"] is True
        and cat["microservices_architecture_present_required"] is True
        and cat["api_first_architecture_present_required"] is True
        and cat["zero_trust_security_present_required"] is True
        and cat["cloud_native_deployment_present_required"] is True
        and cat["sibling_ai_bc_forbidden"] is True
        and cat["rag_platform"]["via_p212"] is True
        and cat["rag_platform"]["via_p213_l"] is True
        and cat["deployment"]["via_p213_o"] is True
        and cat["cqrs"]["command_count"] >= 6
        and cat["events"]["core_event_count"] >= 8
        and cat["microservices"]["service_count"] >= 10
        and cat["cursor_outputs"]["count"] >= 20
        and "enterprise_generative_ai_platform_is_missing"
        in cat["quality_gates"]["reject_if"]
        and "P214-D" in cat["builds_on"]
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
            GenaiPlatformRoot.enable,
            tenant_id="t1",
            platform_ref="p1",
            present=False,
        )
        and GenaiPlatformRoot.enable(
            tenant_id="t1", platform_ref="p2"
        ).is_missing()
        is False,
        not _bad(
            FoundationModelRoot.enable,
            tenant_id="t1",
            model_ref="m1",
            present=False,
        )
        and FoundationModelRoot.enable(
            tenant_id="t1", model_ref="m2"
        ).is_missing()
        is False,
        not _bad(
            PromptPlatformRoot.enable,
            tenant_id="t1",
            prompt_ref="pr1",
            present=False,
        )
        and PromptPlatformRoot.enable(
            tenant_id="t1", prompt_ref="pr2"
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
            AssistantPlatformRoot.enable,
            tenant_id="t1",
            assistant_ref="a1",
            present=False,
        )
        and AssistantPlatformRoot.enable(
            tenant_id="t1", assistant_ref="a2"
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
    ]
    aggregates_ok = all(checks)

    acl_path = root / "backend/contexts/ai/infrastructure/acl/ai_genai_acl.py"
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
        and "via_p214_d" in acl_text
        and "model_signing" in acl_text
        and "module_local_llm_sdk_forbidden" in acl_text
    )

    router = (
        root / "backend/contexts/ai/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@router.get("/genai")' in router
        and "/genai/readiness" in router
        and "/genai/rag" in router
        and "/genai/prompts" in router
        and "/genai/assistants" in router
        and "/genai/vectors" in router
        and "/genai/foundation-registry" in router
    )

    law = (root / "docs/architecture/ENTERPRISE_AI_GENERATIVE_LLM.md").read_text(
        encoding="utf-8"
    )
    doc_ok = (
        "Never Enterprise Generative AI platform is missing" in law
        and "Never LLM platform is missing" in law
        and "Never Foundation model management is missing" in law
        and "Never Prompt intelligence platform is missing" in law
        and "Never RAG platform is missing" in law
        and "Never Vector intelligence is missing" in law
        and "Never AI assistant platform is missing" in law
        and "Never Multimodal AI foundation is missing" in law
        and "Never LLMOps architecture is missing" in law
        and "Never AI governance is missing" in law
        and "Never CQRS architecture is missing" in law
        and "Never Event architecture is missing" in law
        and "Never Microservices architecture is missing" in law
        and "Never API first architecture is missing" in law
        and "Never Zero trust security is missing" in law
        and "Never Cloud native deployment is missing" in law
        and "Never Sibling AI BC" in law
        and "MEOS Enterprise Cognitive Intelligence Layer" in law
        and "cognitive interface" in law
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
        "prompt": "P214-E",
        "adr": 425,
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
