"""P214-E Enterprise Generative AI & LLM Platform — immutable catalog."""
from __future__ import annotations

from typing import Any

PROMPT_ID = "P214-E"
ADR = 425
SOR = "ai"
API_PREFIX = "/api/v1/ai"
PRODUCT = "Enterprise Generative AI & Large Language Model (LLM) Platform"
CAPABILITY = "CAP-PLT-AI-001"

PRINCIPLE = (
    "Enterprise Generative AI SHALL provide the cognitive interface allowing "
    "humans, applications and AI agents to communicate with enterprise "
    "knowledge and intelligence."
)

FABRIC = "meos_enterprise_cognitive_intelligence_layer"

CORE_DOMAIN = "enterprise_generative_intelligence_management"

SUPPORTING_DOMAINS: tuple[dict[str, str], ...] = (
    {"id": "llm_management", "purpose": "Register and govern LLM instances."},
    {"id": "foundation_model", "purpose": "Catalog foundation models and versions."},
    {"id": "prompt_engineering", "purpose": "Prompt lifecycle and optimization."},
    {"id": "rag_intelligence", "purpose": "Knowledge grounding and retrieval."},
    {"id": "ai_assistant", "purpose": "Enterprise copilots and assistants."},
    {"id": "conversation_intelligence", "purpose": "Session and dialogue state."},
    {"id": "multimodal_ai", "purpose": "Text, image, audio, video intelligence."},
    {"id": "ai_safety", "purpose": "Content safety and guardrails."},
    {"id": "ai_governance", "purpose": "Compliance, risk, and policy controls."},
)

AGGREGATE = {
    "name": "GenerativeAIPlatformAggregate",
    "root": "GenerativeAIPlatform",
    "entities": (
        "FoundationModel",
        "LLMInstance",
        "AIApplication",
        "AIAssistant",
        "PromptTemplate",
        "PromptVersion",
        "ConversationSession",
        "KnowledgeContext",
        "EmbeddingModel",
        "RAGPipeline",
        "GenerationRequest",
        "GenerationResponse",
    ),
    "value_objects": (
        "ModelIdentifier",
        "PromptIdentifier",
        "ContextWindow",
        "TokenBudget",
        "TemperatureSetting",
        "EmbeddingVector",
        "ConfidenceScore",
        "SafetyScore",
        "ResponseQualityScore",
    ),
    "events": (
        "LLMRegisteredEvent",
        "PromptCreatedEvent",
        "PromptApprovedEvent",
        "RAGPipelineCreatedEvent",
        "GenerationRequestedEvent",
        "GenerationCompletedEvent",
        "AIGuardrailTriggeredEvent",
    ),
}

LOGICAL_BOUNDED_CONTEXTS: tuple[dict[str, Any], ...] = (
    {
        "id": "foundation_model_management",
        "bc": "BC-01",
        "name": "Foundation Model Management Context",
        "purpose": "Model catalog, lifecycle, evaluation, selection.",
    },
    {
        "id": "llm_runtime",
        "bc": "BC-02",
        "name": "LLM Runtime Context",
        "purpose": "Model execution, inference, scaling, routing.",
    },
    {
        "id": "prompt_intelligence",
        "bc": "BC-03",
        "name": "Prompt Intelligence Context",
        "purpose": "Prompt lifecycle, templates, optimization, governance.",
    },
    {
        "id": "rag_intelligence",
        "bc": "BC-04",
        "name": "RAG Intelligence Context",
        "purpose": "Knowledge retrieval, augmentation, grounded generation.",
    },
    {
        "id": "ai_assistant",
        "bc": "BC-05",
        "name": "AI Assistant Context",
        "purpose": "Enterprise copilots, conversational and task assistance.",
    },
    {
        "id": "multimodal_ai",
        "bc": "BC-06",
        "name": "Multimodal AI Context",
        "purpose": "Text, image, audio, and video intelligence.",
    },
    {
        "id": "ai_safety_governance",
        "bc": "BC-07",
        "name": "AI Safety & Governance Context",
        "purpose": "Safety policies, content controls, compliance, risk.",
    },
)

FOUNDATION_MODEL_REGISTRY = {
    "present_required": True,
    "classes": (
        "open_source_models",
        "private_models",
        "commercial_models",
        "domain_specific_models",
        "fine_tuned_models",
    ),
    "managed_attributes": (
        "model_metadata",
        "model_versions",
        "model_capabilities",
        "model_license",
        "model_performance",
        "model_cost",
        "model_security_profile",
    ),
}

LLMOPS_LIFECYCLE: tuple[str, ...] = (
    "model_discovery",
    "evaluation",
    "configuration",
    "fine_tuning",
    "validation",
    "deployment",
    "monitoring",
    "optimization",
    "retirement",
)

LLMOPS_CAPABILITIES: tuple[str, ...] = (
    "model_routing",
    "model_evaluation",
    "token_management",
    "cost_optimization",
    "performance_optimization",
)

PROMPT_LIFECYCLE: tuple[str, ...] = (
    "draft",
    "review",
    "test",
    "approve",
    "deploy",
    "monitor",
    "improve",
)

PROMPT_PLATFORM = {
    "present_required": True,
    "capabilities": (
        "prompt_repository",
        "prompt_templates",
        "prompt_versioning",
        "prompt_testing",
        "prompt_optimization",
        "prompt_approval",
        "prompt_analytics",
    ),
    "lifecycle": list(PROMPT_LIFECYCLE),
}

RAG_PLATFORM = {
    "present_required": True,
    "via_p212": True,
    "via_p213_l": True,
    "integrates": (
        "P213-L Knowledge Graph",
        "P212 Data Governance",
        "documents",
        "search",
    ),
    "pipeline": (
        "document_ingestion",
        "knowledge_chunking",
        "embedding_generation",
        "vector_search",
        "semantic_retrieval",
        "hybrid_search",
        "context_ranking",
        "grounded_generation",
    ),
}

VECTOR_INTELLIGENCE = {
    "present_required": True,
    "capabilities": (
        "embedding_models",
        "vector_database",
        "similarity_search",
        "semantic_indexing",
        "knowledge_retrieval",
        "context_memory",
    ),
}

ENTERPRISE_COPILOTS: dict[str, dict[str, Any]] = {
    "executive_copilot": {
        "purpose": "C-suite briefing, KPI narrative, strategy Q&A",
        "knowledge_sources": ("analytics", "decision_intelligence", "documents"),
        "ai_model": "enterprise_reasoning_llm",
        "permissions": ("ai.assist.read", "analytics.dashboard.read"),
        "business_value": "faster executive decisions",
    },
    "finance_copilot": {
        "purpose": "GL inquiry, close assist, variance explanation",
        "knowledge_sources": ("financial_kernel", "accounting", "policy"),
        "ai_model": "finance_tuned_llm",
        "permissions": ("ai.assist.read", "finance.read"),
        "business_value": "finance productivity and control",
    },
    "hr_copilot": {
        "purpose": "policy Q&A, talent insights, workforce assist",
        "knowledge_sources": ("hr", "documents", "workflow"),
        "ai_model": "enterprise_llm",
        "permissions": ("ai.assist.read", "hr.read"),
        "business_value": "HR self-service and compliance",
    },
    "erp_copilot": {
        "purpose": "cross-module ERP navigation and process assist",
        "knowledge_sources": ("module_manifests", "workflow", "search"),
        "ai_model": "enterprise_llm",
        "permissions": ("ai.assist.read", "ai.assist.infer"),
        "business_value": "ERP adoption and speed",
    },
    "security_copilot": {
        "purpose": "SOC assist, threat narrative, control guidance",
        "knowledge_sources": ("cyber_security", "audit", "threat_intel"),
        "ai_model": "security_tuned_llm",
        "permissions": ("ai.assist.read", "security.read"),
        "business_value": "faster incident response",
    },
    "developer_copilot": {
        "purpose": "code assist within platform SDK and APIs",
        "knowledge_sources": ("docs", "openapi", "plugin_sdk"),
        "ai_model": "code_llm",
        "permissions": ("ai.assist.read", "ai.assist.infer"),
        "business_value": "engineering velocity",
    },
    "data_analyst_copilot": {
        "purpose": "metric explanation, BI narrative, query assist",
        "knowledge_sources": ("analytics", "semantic_layer", "data_products"),
        "ai_model": "analytics_llm",
        "permissions": ("ai.assist.read", "analytics.dashboard.read"),
        "business_value": "self-serve analytics",
    },
    "customer_service_copilot": {
        "purpose": "case assist, knowledge grounded replies",
        "knowledge_sources": ("crm", "documents", "rag"),
        "ai_model": "enterprise_llm",
        "permissions": ("ai.assist.read", "ai.assist.infer"),
        "business_value": "CSAT and handle time",
    },
}

MULTIMODAL = {
    "present_required": True,
    "modalities": (
        "text_intelligence",
        "image_intelligence",
        "audio_intelligence",
        "speech_recognition",
        "speech_generation",
        "video_understanding",
        "document_intelligence",
    ),
    "pipeline": (
        "ingest_modality",
        "normalize",
        "encode",
        "cross_modal_fuse",
        "reason",
        "generate",
        "safety_filter",
        "audit_emit",
    ),
}

AGENT_INTEGRATION = {
    "next_prompt": "P214-F",
    "capabilities": (
        "agent_communication",
        "tool_usage",
        "knowledge_access",
        "task_execution",
        "memory_integration",
    ),
}

COMMANDS: tuple[str, ...] = (
    "RegisterLLMCommand",
    "CreatePromptCommand",
    "DeployModelCommand",
    "CreateAssistantCommand",
    "ExecuteGenerationCommand",
    "ApprovePromptCommand",
)

QUERIES: tuple[str, ...] = (
    "GetModelQuery",
    "GetPromptQuery",
    "GetAssistantQuery",
    "GetConversationQuery",
    "GetGenerationHistoryQuery",
)

CORE_EVENTS: tuple[dict[str, str], ...] = (
    {"name": "LLMRegisteredEvent", "owner": "ai", "consumers": "audit,analytics"},
    {"name": "ModelDeployedEvent", "owner": "ai", "consumers": "audit,observability"},
    {"name": "PromptCreatedEvent", "owner": "ai", "consumers": "audit"},
    {"name": "PromptApprovedEvent", "owner": "ai", "consumers": "audit,compliance"},
    {"name": "GenerationStartedEvent", "owner": "ai", "consumers": "observability"},
    {"name": "GenerationCompletedEvent", "owner": "ai", "consumers": "audit,analytics"},
    {"name": "SafetyViolationDetectedEvent", "owner": "ai", "consumers": "security,audit"},
    {"name": "ModelPerformanceChangedEvent", "owner": "ai", "consumers": "analytics"},
)

MICROSERVICES: tuple[dict[str, Any], ...] = (
    {
        "id": "llm_management_service",
        "responsibility": "foundation model catalog and lifecycle",
        "api": "/ai/genai/models",
        "db": "ai_*",
        "events": ("LLMRegisteredEvent", "ModelDeployedEvent"),
        "security": ("ai.assist.read", "ai.assist.infer"),
        "scaling": "catalog_read_replicas",
    },
    {
        "id": "model_runtime_service",
        "responsibility": "inference execution and routing",
        "api": "/ai/genai/generation",
        "db": "ai_*",
        "events": ("GenerationStartedEvent", "GenerationCompletedEvent"),
        "security": ("ai.assist.infer",),
        "scaling": "gpu_autoscaling_hpa",
    },
    {
        "id": "prompt_service",
        "responsibility": "prompt lifecycle and templates",
        "api": "/ai/genai/prompts",
        "db": "ai_*",
        "events": ("PromptCreatedEvent", "PromptApprovedEvent"),
        "security": ("ai.assist.read", "ai.assist.infer"),
        "scaling": "stateless_replicas",
    },
    {
        "id": "rag_service",
        "responsibility": "retrieval and grounded generation",
        "api": "/ai/genai/rag",
        "db": "ai_*",
        "events": ("RAGPipelineCreatedEvent",),
        "security": ("ai.assist.read", "ai.assist.infer"),
        "scaling": "async_retrieval_workers",
    },
    {
        "id": "embedding_service",
        "responsibility": "embedding generation",
        "api": "/ai/genai/embeddings",
        "db": "ai_*",
        "events": ("GenerationCompletedEvent",),
        "security": ("ai.assist.infer",),
        "scaling": "batch_and_online_pools",
    },
    {
        "id": "vector_search_service",
        "responsibility": "similarity and hybrid search",
        "api": "/ai/genai/vectors",
        "db": "ai_*",
        "events": (),
        "security": ("ai.assist.read",),
        "scaling": "vector_index_shards",
    },
    {
        "id": "assistant_service",
        "responsibility": "enterprise copilots",
        "api": "/ai/genai/assistants",
        "db": "ai_*",
        "events": (),
        "security": ("ai.assist.read", "ai.assist.infer"),
        "scaling": "stateless_replicas",
    },
    {
        "id": "conversation_service",
        "responsibility": "session and dialogue state",
        "api": "/ai/genai/conversations",
        "db": "ai_*",
        "events": (),
        "security": ("ai.assist.read",),
        "scaling": "session_affinity_optional",
    },
    {
        "id": "safety_service",
        "responsibility": "content safety and guardrails",
        "api": "/ai/genai/safety",
        "db": "ai_*",
        "events": ("SafetyViolationDetectedEvent", "AIGuardrailTriggeredEvent"),
        "security": ("ai.assist.infer",),
        "scaling": "inline_and_async",
    },
    {
        "id": "governance_service",
        "responsibility": "LLM governance and compliance",
        "api": "/ai/genai/governance",
        "db": "ai_*",
        "events": (),
        "security": ("ai.assist.read",),
        "scaling": "control_plane",
    },
    {
        "id": "analytics_service",
        "responsibility": "GenAI usage metrics via Analytics SoR",
        "api": "/analytics (delegated)",
        "db": "analytics_*",
        "events": ("GenerationCompletedEvent",),
        "security": ("analytics.dashboard.read",),
        "scaling": "analytics_platform",
    },
)

API_SURFACES: tuple[str, ...] = (
    "/api/v1/ai/models",
    "/api/v1/ai/llm",
    "/api/v1/ai/prompts",
    "/api/v1/ai/rag",
    "/api/v1/ai/assistants",
    "/api/v1/ai/conversations",
    "/api/v1/ai/generation",
    "/api/v1/ai/genai",
)

API_STYLES: tuple[str, ...] = ("REST", "GraphQL", "gRPC", "Streaming", "Event")

SECURITY = {
    "present_required": True,
    "zero_trust": True,
    "integrates": ("P207", "P208", "P209", "P210", "P211"),
    "controls": (
        "prompt_security",
        "model_security",
        "data_protection",
        "ai_access_control",
        "content_safety",
        "hallucination_management",
        "explainability",
        "auditability",
    ),
}

DEPLOYMENT = {
    "present_required": True,
    "cloud_native": True,
    "via_p213_o": True,
    "components": (
        "kubernetes",
        "gpu_infrastructure",
        "model_serving",
        "vector_database",
        "ai_runtime",
        "api_gateway",
        "observability",
        "auto_scaling",
    ),
    "modes": ("cloud", "private_cloud", "on_premise", "hybrid_ai"),
}

TESTING: tuple[str, ...] = (
    "llm_evaluation_testing",
    "prompt_testing",
    "rag_accuracy_testing",
    "safety_testing",
    "performance_testing",
    "latency_testing",
    "security_testing",
    "regression_testing",
    "human_evaluation_testing",
)

CURSOR_OUTPUTS: tuple[str, ...] = (
    "enterprise_genai_vision",
    "ddd_domain_model",
    "bounded_context_map",
    "foundation_model_registry",
    "llmops_lifecycle",
    "prompt_intelligence_platform",
    "rag_platform",
    "vector_intelligence_layer",
    "ai_assistant_framework",
    "enterprise_copilot_catalog",
    "multimodal_pipeline",
    "agent_integration_hooks",
    "cqrs_commands_queries",
    "event_sourcing_schema",
    "microservice_boundaries",
    "api_first_surfaces",
    "security_responsible_ai",
    "cloud_native_deployment",
    "testing_architecture",
    "quality_gates_dod",
    "adr_425",
    "enterprise_ai_generative_llm_law",
)

QUALITY_GATES_REJECT_IF: tuple[str, ...] = (
    "enterprise_generative_ai_platform_is_missing",
    "llm_platform_is_missing",
    "foundation_model_management_is_missing",
    "prompt_intelligence_platform_is_missing",
    "rag_platform_is_missing",
    "vector_intelligence_is_missing",
    "ai_assistant_platform_is_missing",
    "multimodal_ai_foundation_is_missing",
    "llmops_architecture_is_missing",
    "ai_governance_is_missing",
    "cqrs_architecture_is_missing",
    "event_architecture_is_missing",
    "microservices_architecture_is_missing",
    "api_first_architecture_is_missing",
    "zero_trust_security_is_missing",
    "cloud_native_deployment_is_missing",
    "sibling_ai_bc",
)


def vision() -> dict[str, Any]:
    return {
        "role": "MEOS Enterprise Cognitive Intelligence Layer",
        "principle": PRINCIPLE,
        "equation": (
            "Enterprise Data + Knowledge Graph + Documents + Processes + "
            "Applications + Foundation Models + AI Agents → "
            "Natural Language Enterprise Intelligence"
        ),
        "outcomes": (
            "human_ai_collaboration",
            "knowledge_augmented_reasoning",
            "automated_enterprise_assistance",
            "autonomous_business_intelligence",
        ),
        "pillars": (
            "enterprise_knowledge_interaction",
            "natural_language_interfaces",
            "ai_powered_productivity",
            "intelligent_automation",
            "enterprise_copilots",
            "decision_augmentation",
            "autonomous_assistance",
        ),
    }


def domain_model() -> dict[str, Any]:
    return {
        "core_domain": CORE_DOMAIN,
        "supporting_domains": [dict(d) for d in SUPPORTING_DOMAINS],
        "supporting_count": len(SUPPORTING_DOMAINS),
        "aggregate": dict(AGGREGATE),
    }


def bounded_contexts() -> dict[str, Any]:
    return {
        "contexts": [dict(c) for c in LOGICAL_BOUNDED_CONTEXTS],
        "context_count": len(LOGICAL_BOUNDED_CONTEXTS),
        "logical_partitions_same_sor": True,
    }


def foundation_registry() -> dict[str, Any]:
    return dict(FOUNDATION_MODEL_REGISTRY)


def llmops() -> dict[str, Any]:
    return {
        "present_required": True,
        "lifecycle": list(LLMOPS_LIFECYCLE),
        "stage_count": len(LLMOPS_LIFECYCLE),
        "capabilities": list(LLMOPS_CAPABILITIES),
    }


def prompt_platform() -> dict[str, Any]:
    return dict(PROMPT_PLATFORM)


def rag_platform() -> dict[str, Any]:
    return {
        **dict(RAG_PLATFORM),
        "pipeline_count": len(RAG_PLATFORM["pipeline"]),
    }


def vector_intelligence() -> dict[str, Any]:
    return dict(VECTOR_INTELLIGENCE)


def assistants() -> dict[str, Any]:
    return {
        "present_required": True,
        "copilots": dict(ENTERPRISE_COPILOTS),
        "copilot_count": len(ENTERPRISE_COPILOTS),
    }


def multimodal() -> dict[str, Any]:
    return dict(MULTIMODAL)


def agent_integration() -> dict[str, Any]:
    return dict(AGENT_INTEGRATION)


def cqrs() -> dict[str, Any]:
    return {
        "commands": list(COMMANDS),
        "command_count": len(COMMANDS),
        "queries": list(QUERIES),
        "query_count": len(QUERIES),
        "alignment_present_required": True,
    }


def events() -> dict[str, Any]:
    return {
        "core_events": [dict(e) for e in CORE_EVENTS],
        "core_event_count": len(CORE_EVENTS),
        "event_driven_required": True,
        "retention_policy": "tenant_scoped_immutable_append",
        "version_strategy": "event_version_field",
        "ownership": "ai",
    }


def microservices() -> dict[str, Any]:
    return {
        "services": [dict(s) for s in MICROSERVICES],
        "service_count": len(MICROSERVICES),
        "logical_decomposition": True,
    }


def api() -> dict[str, Any]:
    return {
        "surfaces": list(API_SURFACES),
        "styles": list(API_STYLES),
        "api_first_present_required": True,
    }


def security() -> dict[str, Any]:
    return dict(SECURITY)


def deployment() -> dict[str, Any]:
    return dict(DEPLOYMENT)


def testing() -> dict[str, Any]:
    return {"suites": list(TESTING), "suite_count": len(TESTING)}


def cursor_outputs() -> dict[str, Any]:
    return {"outputs": list(CURSOR_OUTPUTS), "count": len(CURSOR_OUTPUTS)}


def quality_gates() -> dict[str, Any]:
    return {
        "reject_if": list(QUALITY_GATES_REJECT_IF),
        "count": len(QUALITY_GATES_REJECT_IF),
    }


def production_readiness() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "checklist": {
            "enterprise_genai_platform": True,
            "llm_platform": True,
            "foundation_model_registry": True,
            "prompt_platform": True,
            "rag_platform": True,
            "vector_intelligence": True,
            "ai_assistant_platform": True,
            "multimodal_ai": True,
            "llmops": True,
            "governance_architecture": True,
            "cqrs_architecture": True,
            "event_architecture": True,
            "microservice_architecture": True,
            "api_platform": True,
            "security_architecture": True,
            "deployment_architecture": True,
            "testing_architecture": True,
            "foundation_tests": True,
            "genai_api_live": True,
        },
        "verdict": "ENTERPRISE_GRADE",
    }


def catalog() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "adr": ADR,
        "sor": SOR,
        "product": PRODUCT,
        "capability": CAPABILITY,
        "principle": PRINCIPLE,
        "fabric": FABRIC,
        "builds_on": [
            "P214-A",
            "P214-B",
            "P214-C",
            "P214-D",
            "ADR-421",
            "ADR-422",
            "ADR-423",
            "ADR-424",
            "P212",
            "P213",
            "P213-L",
            "P213-O",
            "P207",
            "P208",
            "P209",
            "P210",
            "P211",
            "AI_PLATFORM_STANDARD",
        ],
        "vision": vision(),
        "domain_model": domain_model(),
        "bounded_contexts": bounded_contexts(),
        "foundation_registry": foundation_registry(),
        "llmops": llmops(),
        "prompt_platform": prompt_platform(),
        "rag_platform": rag_platform(),
        "vector_intelligence": vector_intelligence(),
        "assistants": assistants(),
        "multimodal": multimodal(),
        "agent_integration": agent_integration(),
        "cqrs": cqrs(),
        "events": events(),
        "microservices": microservices(),
        "api": api(),
        "security": security(),
        "deployment": deployment(),
        "testing": testing(),
        "cursor_outputs": cursor_outputs(),
        "quality_gates": quality_gates(),
        "production_readiness": production_readiness(),
        "enterprise_generative_ai_platform_present_required": True,
        "llm_platform_present_required": True,
        "foundation_model_management_present_required": True,
        "prompt_intelligence_platform_present_required": True,
        "rag_platform_present_required": True,
        "vector_intelligence_present_required": True,
        "ai_assistant_platform_present_required": True,
        "multimodal_ai_foundation_present_required": True,
        "llmops_architecture_present_required": True,
        "ai_governance_present_required": True,
        "cqrs_architecture_present_required": True,
        "event_architecture_present_required": True,
        "microservices_architecture_present_required": True,
        "api_first_architecture_present_required": True,
        "zero_trust_security_present_required": True,
        "cloud_native_deployment_present_required": True,
        "sibling_ai_bc_forbidden": True,
        "module_local_llm_sdk_forbidden": True,
        "via_enterprise_ai": True,
        "via_api_gateway": True,
        "api_prefix": f"{API_PREFIX}/genai",
        "forbidden_sibling_bc": [
            "generative_ai",
            "llm_platform",
            "vector_intelligence",
            "prompt_platform",
            "rag_platform",
            "foundation_model_registry",
            "ai_assistant_platform",
            "multimodal_ai",
            "ml_platform",
            "ai_core",
        ],
    }


def genai_surface() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "routes": [
            "GET /ai/genai",
            "GET /ai/genai/vision",
            "GET /ai/genai/domain",
            "GET /ai/genai/bounded-contexts",
            "GET /ai/genai/foundation-registry",
            "GET /ai/genai/llmops",
            "GET /ai/genai/prompts",
            "GET /ai/genai/rag",
            "GET /ai/genai/vectors",
            "GET /ai/genai/assistants",
            "GET /ai/genai/multimodal",
            "GET /ai/genai/agents",
            "GET /ai/genai/cqrs",
            "GET /ai/genai/events",
            "GET /ai/genai/microservices",
            "GET /ai/genai/api",
            "GET /ai/genai/security",
            "GET /ai/genai/deployment",
            "GET /ai/genai/testing",
            "GET /ai/genai/outputs",
            "GET /ai/genai/production-readiness",
            "GET /ai/genai/readiness",
        ],
    }
