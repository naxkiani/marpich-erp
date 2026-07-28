"""P214-A Enterprise AI / ML / Generative AI Platform Foundation — immutable catalog."""
from __future__ import annotations

from typing import Any

PROMPT_ID = "P214-A"
ADR = 421
SOR = "ai"
API_PREFIX = "/api/v1/ai"
PRODUCT = (
    "Enterprise Artificial Intelligence, Machine Learning "
    "& Generative AI Platform Foundation"
)
CAPABILITY = "CAP-PLT-AI-001"

PRINCIPLE = (
    "Enterprise AI Platform SHALL provide the intelligence foundation "
    "enabling every MEOS domain to consume, create, govern and "
    "operationalize artificial intelligence."
)

FABRIC = "meos_enterprise_ai_intelligence_fabric"

CORE_DOMAIN = "enterprise_artificial_intelligence_management"

SUPPORTING_DOMAINS: tuple[dict[str, str], ...] = (
    {"id": "ai_platform_management", "purpose": "AI-PaaS orchestration and service catalog."},
    {"id": "machine_learning_operations", "purpose": "ML lifecycle, training, and MLOps."},
    {"id": "generative_ai_management", "purpose": "LLM, multimodal, and content generation."},
    {"id": "model_lifecycle_management", "purpose": "Register, version, deploy, retire models."},
    {"id": "ai_runtime_management", "purpose": "Inference scaling and performance."},
    {"id": "ai_governance", "purpose": "Responsible AI, risk, and compliance."},
    {"id": "ai_experiment_management", "purpose": "Experiment tracking and evaluation."},
    {"id": "ai_knowledge_management", "purpose": "Embeddings, vectors, and RAG knowledge."},
)

LOGICAL_BOUNDED_CONTEXTS: tuple[dict[str, Any], ...] = (
    {
        "id": "ai_platform_core",
        "bc": "BC-01",
        "name": "AI Platform Core Context",
        "purpose": "AI service lifecycle, capability management, platform orchestration.",
    },
    {
        "id": "machine_learning",
        "bc": "BC-02",
        "name": "Machine Learning Context",
        "purpose": "ML development, training, validation, deployment.",
    },
    {
        "id": "generative_ai",
        "bc": "BC-03",
        "name": "Generative AI Context",
        "purpose": "LLM management, prompt engineering, RAG, content generation.",
    },
    {
        "id": "ai_runtime",
        "bc": "BC-04",
        "name": "AI Runtime Context",
        "purpose": "Model execution, inference services, scaling, performance.",
    },
    {
        "id": "ai_governance",
        "bc": "BC-05",
        "name": "AI Governance Context",
        "purpose": "AI compliance, responsible AI, model approval, risk management.",
    },
    {
        "id": "ai_knowledge",
        "bc": "BC-06",
        "name": "AI Knowledge Context",
        "purpose": "Knowledge sources, embeddings, vector intelligence, semantic retrieval.",
    },
)

AGGREGATE = {
    "name": "EnterpriseAIAggregate",
    "root": "EnterpriseAI",
    "entities": (
        "AIModel",
        "MLModel",
        "FoundationModel",
        "LLMModel",
        "AIExperiment",
        "AIService",
        "AIRuntime",
        "AIWorkflow",
        "AIArtifact",
        "AITrainingJob",
        "AIInferenceJob",
        "AIProvider",
    ),
    "value_objects": (
        "ModelVersion",
        "ModelCapability",
        "ModelAccuracy",
        "InferenceLatency",
        "TrainingConfiguration",
        "AIResourceProfile",
        "PromptTemplate",
        "EmbeddingVector",
        "AIConfidenceScore",
    ),
    "events": (
        "AIModelRegisteredEvent",
        "AITrainingStartedEvent",
        "AITrainingCompletedEvent",
        "AIModelDeployedEvent",
        "AIInferenceExecutedEvent",
        "AIModelUpdatedEvent",
        "AIGovernanceValidatedEvent",
    ),
}

FABRIC_FLOW: tuple[str, ...] = (
    "enterprise_data",
    "enterprise_knowledge_graph",
    "enterprise_digital_twins",
    "enterprise_events",
    "business_processes",
    "ai_models",
    "generative_ai_systems",
    "autonomous_ai_agents",
    "enterprise_intelligence",
    "ai_assisted_decisions",
    "autonomous_operations",
    "continuous_learning",
    "enterprise_transformation",
)

AI_PAAS: tuple[str, ...] = (
    "ai_service_catalog",
    "ai_model_registry",
    "dataset_registry",
    "feature_store",
    "prompt_registry",
    "vector_database_platform",
    "ai_pipeline_platform",
    "ai_runtime_platform",
    "ai_marketplace",
    "ai_monitoring_platform",
)

ML_LIFECYCLE: tuple[str, ...] = (
    "data_preparation",
    "feature_engineering",
    "experimentation",
    "training",
    "validation",
    "model_registration",
    "deployment",
    "inference",
    "monitoring",
    "retraining",
)

ML_PARADIGMS: tuple[str, ...] = (
    "supervised_learning",
    "unsupervised_learning",
    "reinforcement_learning",
    "deep_learning",
    "neural_networks",
    "computer_vision",
    "nlp",
    "time_series_ml",
    "graph_machine_learning",
)

GENERATIVE_AI: tuple[str, ...] = (
    "large_language_models",
    "foundation_models",
    "multimodal_ai",
    "text_generation",
    "code_generation",
    "document_intelligence",
    "image_intelligence",
    "voice_intelligence",
    "enterprise_ai_assistants",
    "ai_copilots",
)

LLM_MANAGEMENT: dict[str, Any] = {
    "capabilities": (
        "model_selection",
        "model_evaluation",
        "model_fine_tuning",
        "model_versioning",
        "model_routing",
        "model_deployment",
        "model_monitoring",
        "cost_optimization",
    ),
    "architectures": (
        "private_llm",
        "enterprise_llm",
        "open_source_models",
        "cloud_ai_models",
        "hybrid_ai_architecture",
    ),
}

AI_DATA_FOUNDATION: dict[str, Any] = {
    "via_p212": True,
    "capabilities": (
        "training_data_management",
        "dataset_versioning",
        "data_quality_validation",
        "feature_engineering",
        "data_lineage",
        "data_privacy",
        "synthetic_data_generation",
    ),
}

VECTOR_INTELLIGENCE: dict[str, Any] = {
    "capabilities": (
        "embedding_generation",
        "vector_storage",
        "similarity_search",
        "semantic_retrieval",
        "hybrid_search",
        "knowledge_retrieval",
        "rag_architecture",
    ),
    "present_required": True,
}

AI_AGENT_FOUNDATION: dict[str, Any] = {
    "via_p213_m": True,
    "capabilities": (
        "agent_identity",
        "agent_memory",
        "agent_tools",
        "agent_planning",
        "agent_reasoning",
        "agent_communication",
        "agent_governance",
    ),
    "present_required": True,
}

KNOWLEDGE_INTEGRATION: dict[str, Any] = {
    "via_p213_l": True,
    "via_p212_j": True,
    "capabilities": (
        "knowledge_augmented_ai",
        "graph_rag",
        "semantic_reasoning",
        "enterprise_memory",
        "context_intelligence",
    ),
}

DIGITAL_TWIN_INTEGRATION: dict[str, Any] = {
    "via_p212_l": True,
    "capabilities": (
        "ai_simulation",
        "predictive_intelligence",
        "autonomous_optimization",
        "future_state_modeling",
        "scenario_intelligence",
    ),
}

COMMANDS: tuple[str, ...] = (
    "RegisterAIModelCommand",
    "TrainModelCommand",
    "DeployAIModelCommand",
    "ExecuteInferenceCommand",
    "CreatePromptCommand",
    "ValidateAIModelCommand",
)

QUERIES: tuple[str, ...] = (
    "GetAIModelQuery",
    "SearchModelsQuery",
    "GetInferenceHistoryQuery",
    "GetTrainingStatusQuery",
    "GetAIGovernanceStatusQuery",
)

CORE_EVENTS: tuple[dict[str, Any], ...] = (
    {
        "name": "AIModelRegisteredEvent",
        "producer": "ai_platform_core",
        "consumers": ("model_lifecycle", "ai_governance", "audit"),
        "payload": ("tenant_id", "model_id", "model_version"),
        "version": "v1",
    },
    {
        "name": "AITrainingStartedEvent",
        "producer": "machine_learning",
        "consumers": ("ai_runtime", "observability"),
        "payload": ("tenant_id", "job_id", "model_id"),
        "version": "v1",
    },
    {
        "name": "AITrainingCompletedEvent",
        "producer": "machine_learning",
        "consumers": ("model_lifecycle", "ai_governance"),
        "payload": ("tenant_id", "job_id", "metrics"),
        "version": "v1",
    },
    {
        "name": "AIModelDeployedEvent",
        "producer": "ai_runtime",
        "consumers": ("ai_platform_core", "observability", "audit"),
        "payload": ("tenant_id", "model_id", "runtime_ref"),
        "version": "v1",
    },
    {
        "name": "AIInferenceExecutedEvent",
        "producer": "ai_runtime",
        "consumers": ("ai_monitoring", "audit"),
        "payload": ("tenant_id", "inference_id", "model_id", "latency_ms"),
        "version": "v1",
    },
    {
        "name": "AIModelUpdatedEvent",
        "producer": "model_lifecycle",
        "consumers": ("ai_runtime", "ai_governance"),
        "payload": ("tenant_id", "model_id", "from_version", "to_version"),
        "version": "v1",
    },
    {
        "name": "AIGovernanceValidatedEvent",
        "producer": "ai_governance",
        "consumers": ("ai_platform_core", "audit"),
        "payload": ("tenant_id", "model_id", "validation_ref"),
        "version": "v1",
    },
    {
        "name": "AIModelRetiredEvent",
        "producer": "model_lifecycle",
        "consumers": ("ai_runtime", "audit"),
        "payload": ("tenant_id", "model_id", "reason"),
        "version": "v1",
    },
)

MICROSERVICES: tuple[dict[str, Any], ...] = (
    {
        "name": "ai-platform-service",
        "responsibility": "AI-PaaS orchestration and capability catalog.",
        "database_boundary": "ai_platform",
        "api_boundary": "/api/v1/ai/foundation",
        "events": ("AIModelRegisteredEvent",),
        "security_model": "ai.platform.*",
        "scaling_strategy": "horizontal_stateless",
    },
    {
        "name": "model-registry-service",
        "responsibility": "Model and artifact registry with versioning.",
        "database_boundary": "ai_registry",
        "api_boundary": "/api/v1/ai/models",
        "events": ("AIModelRegisteredEvent", "AIModelUpdatedEvent"),
        "security_model": "ai.models.*",
        "scaling_strategy": "horizontal_stateless",
    },
    {
        "name": "training-service",
        "responsibility": "Distributed training job orchestration.",
        "database_boundary": "ai_training",
        "api_boundary": "/api/v1/ai/training",
        "events": ("AITrainingStartedEvent", "AITrainingCompletedEvent"),
        "security_model": "ai.training.*",
        "scaling_strategy": "gpu_backed_workers",
    },
    {
        "name": "inference-service",
        "responsibility": "Model serving and inference execution.",
        "database_boundary": "ai_inference",
        "api_boundary": "/api/v1/ai/inference",
        "events": ("AIInferenceExecutedEvent", "AIModelDeployedEvent"),
        "security_model": "ai.inference.*",
        "scaling_strategy": "autoscaling_gpu_pools",
    },
    {
        "name": "prompt-management-service",
        "responsibility": "Prompt registry, templates, and evaluation.",
        "database_boundary": "ai_prompts",
        "api_boundary": "/api/v1/ai/prompts",
        "events": ("AIModelUpdatedEvent",),
        "security_model": "ai.prompts.*",
        "scaling_strategy": "horizontal_stateless",
    },
    {
        "name": "vector-intelligence-service",
        "responsibility": "Embeddings, vector store, RAG retrieval.",
        "database_boundary": "ai_vectors",
        "api_boundary": "/api/v1/ai/embeddings",
        "events": ("AIInferenceExecutedEvent",),
        "security_model": "ai.embeddings.*",
        "scaling_strategy": "vector_db_cluster",
    },
    {
        "name": "feature-store-service",
        "responsibility": "Online/offline feature serving for ML.",
        "database_boundary": "ai_features",
        "api_boundary": "/api/v1/ai/features",
        "events": ("AITrainingStartedEvent",),
        "security_model": "ai.features.*",
        "scaling_strategy": "horizontal_stateless",
    },
    {
        "name": "ai-governance-service",
        "responsibility": "Responsible AI controls and model approval.",
        "database_boundary": "ai_governance",
        "api_boundary": "/api/v1/ai/governance",
        "events": ("AIGovernanceValidatedEvent",),
        "security_model": "ai.governance.*",
        "scaling_strategy": "horizontal_stateless",
    },
    {
        "name": "ai-monitoring-service",
        "responsibility": "Model drift, latency, and cost telemetry.",
        "database_boundary": "ai_monitoring",
        "api_boundary": "/api/v1/ai/monitoring",
        "events": ("AIInferenceExecutedEvent",),
        "security_model": "ai.monitoring.*",
        "scaling_strategy": "horizontal_stateless",
    },
    {
        "name": "ai-marketplace-service",
        "responsibility": "Internal AI asset marketplace listings.",
        "database_boundary": "ai_marketplace",
        "api_boundary": "/api/v1/ai/marketplace",
        "events": ("AIModelRegisteredEvent",),
        "security_model": "ai.marketplace.*",
        "scaling_strategy": "horizontal_stateless",
    },
)

API_SURFACES: tuple[str, ...] = (
    "/api/v1/ai/models",
    "/api/v1/ai/training",
    "/api/v1/ai/inference",
    "/api/v1/ai/prompts",
    "/api/v1/ai/embeddings",
    "/api/v1/ai/agents",
    "/api/v1/ai/governance",
)

API_PROTOCOLS: tuple[str, ...] = (
    "rest",
    "graphql",
    "grpc",
    "streaming_apis",
    "event_apis",
)

SECURITY: dict[str, Any] = {
    "via_p207": True,
    "via_p208": True,
    "via_p209": True,
    "via_p210": True,
    "via_p211": True,
    "via_p212": True,
    "controls": (
        "ai_identity",
        "model_authorization",
        "prompt_security",
        "data_protection",
        "model_encryption",
        "ai_audit_trail",
        "responsible_ai_controls",
        "ai_risk_management",
    ),
    "zero_trust": True,
    "privacy_by_design": True,
}

DEPLOYMENT: dict[str, Any] = {
    "kubernetes": True,
    "gpu_clusters": True,
    "ai_accelerators": True,
    "model_serving_infrastructure": True,
    "vector_database_cluster": True,
    "distributed_training_platform": True,
    "mlops_pipeline": True,
    "observability": True,
    "auto_scaling": True,
    "cloud_native": True,
    "via_p213_o": True,
}

TESTING: tuple[str, ...] = (
    "ai_model_testing",
    "data_testing",
    "prompt_testing",
    "bias_testing",
    "security_testing",
    "performance_testing",
    "inference_testing",
    "regression_testing",
    "ai_safety_testing",
    "governance_testing",
)

CURSOR_OUTPUTS: tuple[str, ...] = (
    "enterprise_ai_platform_vision",
    "ddd_domain_model",
    "enterprise_ai_domain_architecture",
    "enterprise_ai_platform_foundation",
    "machine_learning_platform",
    "generative_ai_platform",
    "llm_management_platform",
    "ai_data_foundation",
    "vector_intelligence_platform",
    "ai_agent_foundation",
    "ai_knowledge_integration",
    "digital_twin_ai_integration",
    "cqrs_architecture",
    "event_sourcing_architecture",
    "microservice_architecture",
    "api_first_architecture",
    "security_ai_governance_foundation",
    "deployment_architecture",
    "testing_architecture",
    "production_readiness_checklist",
)

QUALITY_GATES_REJECT_IF: tuple[str, ...] = (
    "enterprise_ai_platform_foundation_is_missing",
    "machine_learning_platform_is_missing",
    "generative_ai_platform_is_missing",
    "llm_platform_is_missing",
    "ai_model_lifecycle_is_missing",
    "mlops_foundation_is_missing",
    "vector_intelligence_is_missing",
    "ai_governance_foundation_is_missing",
    "ai_agent_foundation_is_missing",
    "knowledge_graph_integration_is_missing",
    "digital_twin_integration_is_missing",
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
        "prompt_id": PROMPT_ID,
        "fabric": FABRIC,
        "principle": PRINCIPLE,
        "strategic_role": (
            "AI as enterprise operating capability enabling "
            "AI-driven business transformation, human-AI collaboration, "
            "autonomous enterprise operations, and AI-powered innovation."
        ),
        "fabric_flow": list(FABRIC_FLOW),
        "machine_intelligence_layer": True,
        "human_ai_collaboration": True,
        "autonomous_enterprise_operations": True,
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
        "contexts": list(LOGICAL_BOUNDED_CONTEXTS),
        "context_count": len(LOGICAL_BOUNDED_CONTEXTS),
        "logical_only": True,
        "sibling_bc_forbidden": True,
    }


def ai_paas() -> dict[str, Any]:
    return {
        "capabilities": list(AI_PAAS),
        "capability_count": len(AI_PAAS),
        "present_required": True,
    }


def ml_platform() -> dict[str, Any]:
    return {
        "lifecycle": list(ML_LIFECYCLE),
        "lifecycle_step_count": len(ML_LIFECYCLE),
        "paradigms": list(ML_PARADIGMS),
        "paradigm_count": len(ML_PARADIGMS),
        "present_required": True,
    }


def generative_ai() -> dict[str, Any]:
    return {
        "capabilities": list(GENERATIVE_AI),
        "capability_count": len(GENERATIVE_AI),
        "present_required": True,
    }


def llm_management() -> dict[str, Any]:
    return dict(LLM_MANAGEMENT) | {"present_required": True}


def ai_data() -> dict[str, Any]:
    return dict(AI_DATA_FOUNDATION)


def vector_intelligence() -> dict[str, Any]:
    return dict(VECTOR_INTELLIGENCE)


def agent_foundation() -> dict[str, Any]:
    return dict(AI_AGENT_FOUNDATION)


def knowledge_integration() -> dict[str, Any]:
    return dict(KNOWLEDGE_INTEGRATION)


def digital_twin_integration() -> dict[str, Any]:
    return dict(DIGITAL_TWIN_INTEGRATION)


def cqrs() -> dict[str, Any]:
    return {
        "commands": list(COMMANDS),
        "command_count": len(COMMANDS),
        "queries": list(QUERIES),
        "query_count": len(QUERIES),
        "events": [e["name"] for e in CORE_EVENTS],
        "event_count": len(CORE_EVENTS),
        "alignment_present_required": True,
    }


def events() -> dict[str, Any]:
    return {
        "core_events": [dict(e) for e in CORE_EVENTS],
        "core_event_count": len(CORE_EVENTS),
        "event_driven_required": True,
        "replay_strategy": "outbox_replay_by_event_id",
        "retention_policy": "tenant_scoped_immutable_append",
        "version_strategy": "event_version_field",
    }


def microservices() -> dict[str, Any]:
    return {
        "services": [dict(s) for s in MICROSERVICES],
        "service_count": len(MICROSERVICES),
        "logical_decomposition": True,
    }


def api_first() -> dict[str, Any]:
    return {
        "present_required": True,
        "surfaces": list(API_SURFACES),
        "surface_count": len(API_SURFACES),
        "protocols": list(API_PROTOCOLS),
        "rest": True,
        "graphql": True,
        "grpc": True,
        "streaming_apis": True,
        "event_apis": True,
        "via_api_gateway": True,
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
            "enterprise_ai_platform": True,
            "machine_learning_platform": True,
            "generative_ai_platform": True,
            "llm_management": True,
            "model_registry": True,
            "feature_store": True,
            "vector_intelligence": True,
            "ai_runtime": True,
            "ai_governance_foundation": True,
            "ai_agent_foundation": True,
            "knowledge_integration": True,
            "cqrs_architecture": True,
            "event_architecture": True,
            "microservice_architecture": True,
            "api_platform": True,
            "security_architecture": True,
            "deployment_architecture": True,
            "testing_architecture": True,
            "foundation_tests": True,
            "foundation_api_live": True,
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
        "core_domain": CORE_DOMAIN,
        "aggregate": AGGREGATE["name"],
        "builds_on": [
            "P212",
            "P212-J",
            "P212-L",
            "P213",
            "P213-L",
            "P213-M",
            "P213-N",
            "P213-O",
            "ADR-394",
            "ADR-416",
            "ADR-417",
            "ADR-418",
            "ADR-419",
            "P207",
            "P208",
            "P209",
            "P210",
            "P211",
            "AI_PLATFORM_STANDARD",
        ],
        "domain_model": domain_model(),
        "bounded_contexts": bounded_contexts(),
        "ai_paas": ai_paas(),
        "ml_platform": ml_platform(),
        "generative_ai": generative_ai(),
        "llm_management": llm_management(),
        "ai_data_foundation": ai_data(),
        "vector_intelligence": vector_intelligence(),
        "ai_agent_foundation": agent_foundation(),
        "knowledge_integration": knowledge_integration(),
        "digital_twin_integration": digital_twin_integration(),
        "cqrs": cqrs(),
        "events": events(),
        "microservices": microservices(),
        "api_first": api_first(),
        "security": security(),
        "deployment": deployment(),
        "testing": testing(),
        "cursor_outputs": cursor_outputs(),
        "quality_gates": quality_gates(),
        "production_readiness": production_readiness(),
        "enterprise_ai_platform_foundation_present_required": True,
        "machine_learning_platform_present_required": True,
        "generative_ai_platform_present_required": True,
        "llm_platform_present_required": True,
        "ai_model_lifecycle_present_required": True,
        "mlops_foundation_present_required": True,
        "vector_intelligence_present_required": True,
        "ai_governance_foundation_present_required": True,
        "ai_agent_foundation_present_required": True,
        "knowledge_graph_integration_present_required": True,
        "digital_twin_integration_present_required": True,
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
        "api_prefix": f"{API_PREFIX}/foundation",
        "forbidden_sibling_bc": [
            "ml_platform",
            "generative_ai",
            "llm_platform",
            "ai_core",
            "vector_intelligence",
            "model_lifecycle_platform",
        ],
    }


def foundation_surface() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "routes": [
            "GET /ai/foundation",
            "GET /ai/foundation/vision",
            "GET /ai/foundation/domain",
            "GET /ai/foundation/bounded-contexts",
            "GET /ai/foundation/ai-paas",
            "GET /ai/foundation/ml",
            "GET /ai/foundation/generative",
            "GET /ai/foundation/llm",
            "GET /ai/foundation/data",
            "GET /ai/foundation/vectors",
            "GET /ai/foundation/agents",
            "GET /ai/foundation/knowledge",
            "GET /ai/foundation/digital-twin",
            "GET /ai/foundation/cqrs",
            "GET /ai/foundation/events",
            "GET /ai/foundation/microservices",
            "GET /ai/foundation/api",
            "GET /ai/foundation/security",
            "GET /ai/foundation/deployment",
            "GET /ai/foundation/testing",
            "GET /ai/foundation/outputs",
            "GET /ai/foundation/production-readiness",
            "GET /ai/foundation/readiness",
        ],
    }
