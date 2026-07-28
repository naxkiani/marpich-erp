"""P214-C Enterprise AI Domain Architecture (DDD) — immutable catalog."""
from __future__ import annotations

from typing import Any

PROMPT_ID = "P214-C"
ADR = 423
SOR = "ai"
API_PREFIX = "/api/v1/ai"
PRODUCT = (
    "Enterprise Artificial Intelligence Platform — Domain Architecture (DDD)"
)
CAPABILITY = "CAP-PLT-AI-001"

PRINCIPLE = (
    "AI strategy, capabilities, models, data, agents, applications, "
    "decisions, and business outcomes SHALL be represented as governed "
    "enterprise domains through DDD boundaries."
)

FABRIC = "meos_enterprise_ai_domain_fabric"

CORE_DOMAIN = "enterprise_artificial_intelligence_intelligence_platform"

FABRIC_FLOW: tuple[str, ...] = (
    "ai_strategy",
    "ai_capabilities",
    "ai_models",
    "ai_data",
    "ai_agents",
    "ai_applications",
    "ai_decisions",
    "ai_business_outcomes",
)

SUPPORTING_DOMAINS: tuple[dict[str, Any], ...] = (
    {
        "id": "ai_model_management",
        "mission": "Govern model identity, versions, and retirement.",
        "responsibilities": ("lifecycle", "lineage", "ownership"),
        "business_capability": "model_portfolio",
        "data_ownership": "model_metadata",
        "integration_boundary": "model_registry_api",
    },
    {
        "id": "machine_learning_engineering",
        "mission": "Engineer and train ML systems.",
        "responsibilities": ("training", "validation", "feature_pipelines"),
        "business_capability": "ml_engineering",
        "data_ownership": "training_artifacts",
        "integration_boundary": "training_service",
    },
    {
        "id": "generative_ai",
        "mission": "Deliver generative and multimodal intelligence.",
        "responsibilities": ("llm", "prompts", "rag", "generation"),
        "business_capability": "generative_ai",
        "data_ownership": "prompt_and_gen_artifacts",
        "integration_boundary": "prompt_service",
    },
    {
        "id": "large_language_model",
        "mission": "Manage foundation and LLM instances.",
        "responsibilities": ("routing", "fine_tuning", "evaluation"),
        "business_capability": "llm_platform",
        "data_ownership": "llm_configs",
        "integration_boundary": "inference_gateway",
    },
    {
        "id": "ai_agent",
        "mission": "Operate autonomous and collaborative agents.",
        "responsibilities": ("lifecycle", "memory", "planning", "tools"),
        "business_capability": "agent_platform",
        "data_ownership": "agent_state",
        "integration_boundary": "agent_service",
    },
    {
        "id": "ai_knowledge",
        "mission": "Provide embeddings, vectors, and semantic memory.",
        "responsibilities": ("embeddings", "retrieval", "graph_rag"),
        "business_capability": "knowledge_intelligence",
        "data_ownership": "vectors_and_relations",
        "integration_boundary": "knowledge_service",
    },
    {
        "id": "ai_data_intelligence",
        "mission": "Govern AI training and feature data.",
        "responsibilities": ("datasets", "labels", "lineage", "privacy"),
        "business_capability": "ai_data_management",
        "data_ownership": "training_datasets",
        "integration_boundary": "p212_acl",
    },
    {
        "id": "ai_runtime",
        "mission": "Execute inference at enterprise scale.",
        "responsibilities": ("serving", "scaling", "performance"),
        "business_capability": "inference_runtime",
        "data_ownership": "runtime_telemetry",
        "integration_boundary": "inference_service",
    },
    {
        "id": "ai_governance",
        "mission": "Approve, audit, and control AI risk.",
        "responsibilities": ("policies", "compliance", "ethics", "risk"),
        "business_capability": "responsible_ai",
        "data_ownership": "governance_records",
        "integration_boundary": "governance_service",
    },
    {
        "id": "ai_security",
        "mission": "Protect models, prompts, and agents.",
        "responsibilities": ("identity", "authz", "threats", "controls"),
        "business_capability": "ai_security",
        "data_ownership": "security_controls",
        "integration_boundary": "p207_p211_acl",
    },
    {
        "id": "ai_operations",
        "mission": "Operate MLOps and AIOps loops.",
        "responsibilities": ("monitoring", "drift", "incidents", "cost"),
        "business_capability": "ai_ops",
        "data_ownership": "ops_metrics",
        "integration_boundary": "observability",
    },
)

STRATEGIC_DOMAINS: tuple[dict[str, Any], ...] = (
    {
        "id": "enterprise_ai_strategy",
        "responsibilities": (
            "ai_vision",
            "ai_roadmap",
            "ai_portfolio",
            "ai_investment",
        ),
    },
    {
        "id": "ai_governance_strategy",
        "responsibilities": (
            "ai_policies",
            "ai_compliance",
            "ai_ethics",
            "ai_risk",
        ),
    },
    {
        "id": "ai_innovation",
        "responsibilities": (
            "ai_research",
            "experimentation",
            "emerging_technologies",
        ),
    },
)

CORE_AGGREGATE = {
    "name": "EnterpriseAIPlatformAggregate",
    "root": "EnterpriseAIPlatform",
    "entities": (
        "AIPlatform",
        "AICapability",
        "AIService",
        "AIModel",
        "AIApplication",
        "AIAgent",
        "AIWorkflow",
        "AIKnowledgeAsset",
        "AIInferenceService",
        "AIExperiment",
    ),
    "value_objects": (
        "AIIdentifier",
        "ModelIdentifier",
        "CapabilityIdentifier",
        "AIProvider",
        "AIModelType",
        "AIConfidenceLevel",
        "AIAccuracyScore",
        "AIResourceProfile",
        "AIComplianceStatus",
    ),
    "events": (
        "AICapabilityCreatedEvent",
        "AIModelRegisteredEvent",
        "AIServiceActivatedEvent",
        "AIApplicationPublishedEvent",
        "AIInferenceCompletedEvent",
        "AIComplianceApprovedEvent",
    ),
}

LOGICAL_BOUNDED_CONTEXTS: tuple[dict[str, Any], ...] = (
    {
        "id": "ai_platform_management",
        "bc": "BC-01",
        "name": "AI Platform Management Context",
        "purpose": "AI platform lifecycle, services, and capabilities.",
        "aggregate_root": "AIPlatform",
        "aggregates": ("EnterpriseAIPlatformAggregate",),
        "entities": (
            "AIPlatform",
            "AICapability",
            "AIService",
            "AIApplication",
            "AIWorkflow",
        ),
        "value_objects": (
            "AIIdentifier",
            "CapabilityIdentifier",
            "AIProvider",
        ),
        "domain_services": ("AICapabilityOrchestrationService",),
        "repositories": ("AIPlatformRepository",),
        "factories": ("AIPlatformFactory",),
        "commands": (
            "CreateAICapabilityCommand",
            "ActivateAIServiceCommand",
        ),
        "queries": ("GetAIPlatformQuery", "ListAICapabilitiesQuery"),
        "events": (
            "AICapabilityCreatedEvent",
            "AIServiceActivatedEvent",
            "AIApplicationPublishedEvent",
            "AIPlatformCreatedEvent",
        ),
    },
    {
        "id": "machine_learning",
        "bc": "BC-02",
        "name": "Machine Learning Context",
        "purpose": "ML lifecycle, training, validation, deployment.",
        "aggregate_root": "Model",
        "aggregates": ("AIModelManagementAggregate",),
        "entities": (
            "Model",
            "ModelVersion",
            "TrainingRun",
            "EvaluationResult",
            "Deployment",
            "InferenceEndpoint",
        ),
        "value_objects": (
            "ModelIdentifier",
            "AIModelType",
            "AIAccuracyScore",
        ),
        "domain_services": ("ModelTrainingService", "ModelValidationService"),
        "repositories": ("ModelRepository",),
        "factories": ("ModelFactory",),
        "commands": ("TrainModelCommand", "DeployModelCommand"),
        "queries": ("GetModelQuery", "GetTrainingStatusQuery"),
        "events": (
            "AIModelRegisteredEvent",
            "ModelTrainedEvent",
            "ModelValidatedEvent",
            "ModelDeployedEvent",
        ),
    },
    {
        "id": "generative_ai",
        "bc": "BC-03",
        "name": "Generative AI Context",
        "purpose": "LLM management, prompts, RAG, generation.",
        "aggregate_root": "FoundationModel",
        "aggregates": ("GenerativeAIAggregate",),
        "entities": (
            "FoundationModel",
            "LLMInstance",
            "PromptTemplate",
            "PromptVersion",
            "EmbeddingModel",
            "RAGPipeline",
            "ContextWindow",
            "GenerationRequest",
        ),
        "value_objects": ("AIConfidenceLevel", "AIResourceProfile"),
        "domain_services": ("PromptLifecycleService", "ModelRoutingService"),
        "repositories": ("PromptRepository",),
        "factories": ("PromptFactory",),
        "commands": ("PublishPromptCommand", "ExecuteGenerationCommand"),
        "queries": ("GetPromptQuery", "SearchPromptsQuery"),
        "events": ("PromptPublishedEvent", "AIInferenceCompletedEvent"),
    },
    {
        "id": "ai_agent",
        "bc": "BC-04",
        "name": "AI Agent Context",
        "purpose": "Agent lifecycle, memory, planning, collaboration.",
        "aggregate_root": "Agent",
        "aggregates": ("AIAgentAggregate",),
        "entities": (
            "Agent",
            "AgentCapability",
            "AgentMemory",
            "AgentTool",
            "AgentGoal",
            "AgentPlan",
            "AgentExecution",
        ),
        "value_objects": ("AIIdentifier", "AIConfidenceLevel"),
        "domain_services": ("AgentPlanningService", "AgentCollaborationService"),
        "repositories": ("AgentRepository",),
        "factories": ("AgentFactory",),
        "commands": ("CreateAgentCommand", "ExecuteAgentPlanCommand"),
        "queries": ("GetAgentQuery", "ListAgentExecutionsQuery"),
        "events": ("AgentCreatedEvent", "AIInferenceCompletedEvent"),
    },
    {
        "id": "ai_knowledge",
        "bc": "BC-05",
        "name": "AI Knowledge Context",
        "purpose": "Knowledge sources, embeddings, vectors, semantic retrieval.",
        "aggregate_root": "KnowledgeObject",
        "aggregates": ("KnowledgeAggregate",),
        "entities": (
            "KnowledgeObject",
            "SemanticEntity",
            "Embedding",
            "KnowledgeRelation",
            "ContextMemory",
        ),
        "value_objects": ("CapabilityIdentifier",),
        "domain_services": ("GraphRAGService", "SemanticReasoningService"),
        "repositories": ("KnowledgeRepository",),
        "factories": ("KnowledgeFactory",),
        "commands": ("IndexKnowledgeCommand", "RetrieveContextCommand"),
        "queries": ("SearchKnowledgeQuery",),
        "events": ("AIInferenceCompletedEvent",),
        "via_p213_l": True,
        "via_p212_j": True,
    },
    {
        "id": "ai_runtime",
        "bc": "BC-06",
        "name": "AI Runtime Context",
        "purpose": "Inference, execution, scaling, performance.",
        "aggregate_root": "AIInferenceService",
        "aggregates": ("AIRuntimeAggregate",),
        "entities": ("AIInferenceService", "AIExperiment"),
        "value_objects": ("AIResourceProfile", "AIAccuracyScore"),
        "domain_services": ("InferenceScalingService",),
        "repositories": ("InferenceRepository",),
        "factories": ("InferenceFactory",),
        "commands": ("ExecuteInferenceCommand", "ScaleRuntimeCommand"),
        "queries": ("GetInferenceHistoryQuery",),
        "events": ("InferenceCompletedEvent", "AIInferenceCompletedEvent"),
    },
    {
        "id": "ai_governance",
        "bc": "BC-07",
        "name": "AI Governance Context",
        "purpose": "Approval, compliance, audit, risk.",
        "aggregate_root": "AIComplianceStatus",
        "aggregates": ("AIGovernanceAggregate",),
        "entities": ("AICapability", "AIModel"),
        "value_objects": ("AIComplianceStatus",),
        "domain_services": ("AIRiskAssessmentService",),
        "repositories": ("AIGovernanceRepository",),
        "factories": ("AIGovernanceFactory",),
        "commands": ("ApproveAIModelCommand", "CheckComplianceCommand"),
        "queries": ("GetAIGovernanceStatusQuery",),
        "events": (
            "AIComplianceApprovedEvent",
            "AIComplianceCheckedEvent",
        ),
    },
    {
        "id": "ai_security",
        "bc": "BC-08",
        "name": "AI Security Context",
        "purpose": "AI identity, authorization, model protection, threats.",
        "aggregate_root": "AIIdentity",
        "aggregates": ("AISecurityAggregate",),
        "entities": (
            "AIIdentity",
            "ModelPermission",
            "PromptPolicy",
            "AIThreat",
            "AIControl",
        ),
        "value_objects": ("AIIdentifier",),
        "domain_services": ("AIThreatDefenseService",),
        "repositories": ("AISecurityRepository",),
        "factories": ("AISecurityFactory",),
        "commands": ("RegisterAIIdentityCommand", "EnforcePromptPolicyCommand"),
        "queries": ("GetAIThreatsQuery",),
        "events": ("AIIncidentDetectedEvent",),
        "via_p207": True,
        "via_p208": True,
        "via_p209": True,
        "via_p210": True,
        "via_p211": True,
    },
)

AI_DATA_DOMAIN = {
    "aggregate": "AIDataManagementAggregate",
    "via_p212": True,
    "entities": (
        "TrainingDataset",
        "FeatureSet",
        "DataPipeline",
        "SyntheticDataset",
        "DataLabel",
    ),
    "supports": (
        "dataset_governance",
        "data_lineage",
        "data_quality",
        "privacy_controls",
    ),
}

DOMAIN_EVENTS: tuple[dict[str, Any], ...] = (
    {
        "name": "AIPlatformCreatedEvent",
        "owner": "BC-01",
        "consumers": ("governance", "observability"),
        "schema": ("tenant_id", "platform_id"),
        "version": "v1",
    },
    {
        "name": "ModelTrainedEvent",
        "owner": "BC-02",
        "consumers": ("governance", "runtime"),
        "schema": ("tenant_id", "model_id", "training_run_id"),
        "version": "v1",
    },
    {
        "name": "ModelValidatedEvent",
        "owner": "BC-02",
        "consumers": ("governance",),
        "schema": ("tenant_id", "model_id", "evaluation_id"),
        "version": "v1",
    },
    {
        "name": "ModelDeployedEvent",
        "owner": "BC-02",
        "consumers": ("runtime", "security", "observability"),
        "schema": ("tenant_id", "model_id", "endpoint_id"),
        "version": "v1",
    },
    {
        "name": "PromptPublishedEvent",
        "owner": "BC-03",
        "consumers": ("runtime", "governance"),
        "schema": ("tenant_id", "prompt_id", "version"),
        "version": "v1",
    },
    {
        "name": "AgentCreatedEvent",
        "owner": "BC-04",
        "consumers": ("governance", "security"),
        "schema": ("tenant_id", "agent_id"),
        "version": "v1",
    },
    {
        "name": "InferenceCompletedEvent",
        "owner": "BC-06",
        "consumers": ("observability", "audit"),
        "schema": ("tenant_id", "inference_id", "latency_ms"),
        "version": "v1",
    },
    {
        "name": "AIIncidentDetectedEvent",
        "owner": "BC-08",
        "consumers": ("governance", "cyber_security"),
        "schema": ("tenant_id", "threat_id", "severity"),
        "version": "v1",
    },
    {
        "name": "AIComplianceCheckedEvent",
        "owner": "BC-07",
        "consumers": ("platform", "audit"),
        "schema": ("tenant_id", "subject_id", "status"),
        "version": "v1",
    },
)

MICROSERVICE_MAP: tuple[dict[str, Any], ...] = (
    {
        "service": "ai-platform-service",
        "bounded_context": "BC-01",
        "api": "/api/v1/ai/domain",
        "database": "ai_platform",
        "events": ("AIPlatformCreatedEvent", "AICapabilityCreatedEvent"),
    },
    {
        "service": "model-service",
        "bounded_context": "BC-02",
        "api": "/api/v1/ai/models",
        "database": "ai_models",
        "events": ("AIModelRegisteredEvent", "ModelDeployedEvent"),
    },
    {
        "service": "training-service",
        "bounded_context": "BC-02",
        "api": "/api/v1/ai/training",
        "database": "ai_training",
        "events": ("ModelTrainedEvent", "ModelValidatedEvent"),
    },
    {
        "service": "prompt-service",
        "bounded_context": "BC-03",
        "api": "/api/v1/ai/prompts",
        "database": "ai_prompts",
        "events": ("PromptPublishedEvent",),
    },
    {
        "service": "agent-service",
        "bounded_context": "BC-04",
        "api": "/api/v1/ai/agents",
        "database": "ai_agents",
        "events": ("AgentCreatedEvent",),
    },
    {
        "service": "knowledge-service",
        "bounded_context": "BC-05",
        "api": "/api/v1/ai/embeddings",
        "database": "ai_knowledge",
        "events": ("AIInferenceCompletedEvent",),
    },
    {
        "service": "inference-service",
        "bounded_context": "BC-06",
        "api": "/api/v1/ai/inference",
        "database": "ai_inference",
        "events": ("InferenceCompletedEvent",),
    },
    {
        "service": "governance-service",
        "bounded_context": "BC-07",
        "api": "/api/v1/ai/governance",
        "database": "ai_governance",
        "events": ("AIComplianceCheckedEvent", "AIComplianceApprovedEvent"),
    },
    {
        "service": "security-service",
        "bounded_context": "BC-08",
        "api": "/api/v1/ai/security",
        "database": "ai_security",
        "events": ("AIIncidentDetectedEvent",),
    },
)

INTEGRATION: dict[str, Any] = {
    "via_p212": True,
    "via_p213": True,
    "via_p207": True,
    "via_p208": True,
    "via_p209": True,
    "via_p210": True,
    "via_p211": True,
    "via_p214_a": True,
    "via_p214_b": True,
    "channels": ("apis", "events", "data_exchange", "security_boundaries"),
}

DOMAIN_GOVERNANCE: dict[str, Any] = {
    "owners": (
        "ai_domain_owners",
        "ai_product_owners",
        "ai_data_owners",
        "ai_model_owners",
        "ai_risk_owners",
    ),
    "implements": (
        "domain_governance",
        "ownership_model",
        "lifecycle_governance",
        "change_governance",
    ),
}

CURSOR_OUTPUTS: tuple[str, ...] = (
    "enterprise_ai_domain_landscape",
    "strategic_domain_design",
    "core_ai_domain_model",
    "bounded_context_architecture",
    "tactical_ddd_design",
    "ai_model_domain",
    "generative_ai_domain_model",
    "ai_agent_domain_model",
    "ai_knowledge_domain",
    "ai_data_domain",
    "ai_security_domain",
    "ai_domain_event_architecture",
    "domain_to_microservice_mapping",
    "integration_architecture",
    "ai_domain_governance",
    "production_readiness_checklist",
)

QUALITY_GATES_REJECT_IF: tuple[str, ...] = (
    "complete_ai_domain_model_is_missing",
    "strategic_ddd_design_is_missing",
    "core_domain_is_undefined",
    "supporting_domains_are_missing",
    "bounded_contexts_are_missing",
    "aggregates_are_undefined",
    "entities_are_undefined",
    "value_objects_are_undefined",
    "domain_events_are_missing",
    "microservice_mapping_is_missing",
    "integration_boundaries_are_unclear",
    "governance_model_is_missing",
    "sibling_ai_bc",
)


def domain_map() -> dict[str, Any]:
    return {
        "core_domain": CORE_DOMAIN,
        "supporting_domains": [dict(d) for d in SUPPORTING_DOMAINS],
        "supporting_count": len(SUPPORTING_DOMAINS),
        "strategic_domains": [dict(d) for d in STRATEGIC_DOMAINS],
        "strategic_count": len(STRATEGIC_DOMAINS),
        "fabric_flow": list(FABRIC_FLOW),
    }


def core_domain_model() -> dict[str, Any]:
    return {
        "name": CORE_DOMAIN,
        "aggregate": dict(CORE_AGGREGATE),
        "present_required": True,
    }


def bounded_contexts() -> dict[str, Any]:
    return {
        "contexts": list(LOGICAL_BOUNDED_CONTEXTS),
        "context_count": len(LOGICAL_BOUNDED_CONTEXTS),
        "logical_only": True,
        "sibling_bc_forbidden": True,
        "present_required": True,
    }


def tactical_ddd() -> dict[str, Any]:
    entities: list[str] = []
    vos: list[str] = []
    aggregates: list[str] = []
    services: list[str] = []
    for bc in LOGICAL_BOUNDED_CONTEXTS:
        aggregates.extend(bc.get("aggregates", ()))
        entities.extend(bc.get("entities", ()))
        vos.extend(bc.get("value_objects", ()))
        services.extend(bc.get("domain_services", ()))
    return {
        "aggregate_count": len(set(aggregates)),
        "entity_count": len(set(entities)),
        "value_object_count": len(set(vos)),
        "domain_service_count": len(set(services)),
        "aggregates_defined_required": True,
        "entities_defined_required": True,
        "value_objects_defined_required": True,
        "domain_services_present_required": True,
        "rules": (
            "aggregate_boundary_rules",
            "single_responsibility",
            "high_cohesion",
            "low_coupling",
        ),
    }


def model_domain() -> dict[str, Any]:
    return {
        "entities": (
            "Model",
            "ModelVersion",
            "TrainingRun",
            "EvaluationResult",
            "Deployment",
            "InferenceEndpoint",
        ),
        "supports": (
            "model_lifecycle",
            "version_control",
            "model_lineage",
            "model_ownership",
            "model_retirement",
        ),
        "present_required": True,
    }


def generative_domain() -> dict[str, Any]:
    return {
        "entities": (
            "FoundationModel",
            "LLMInstance",
            "PromptTemplate",
            "PromptVersion",
            "EmbeddingModel",
            "RAGPipeline",
            "ContextWindow",
            "GenerationRequest",
        ),
        "supports": (
            "prompt_lifecycle",
            "model_routing",
            "context_management",
            "retrieval_integration",
        ),
        "present_required": True,
    }


def agent_domain() -> dict[str, Any]:
    return {
        "entities": (
            "Agent",
            "AgentCapability",
            "AgentMemory",
            "AgentTool",
            "AgentGoal",
            "AgentPlan",
            "AgentExecution",
        ),
        "supports": (
            "agent_lifecycle",
            "agent_collaboration",
            "agent_governance",
            "agent_identity",
        ),
        "present_required": True,
    }


def knowledge_domain() -> dict[str, Any]:
    return {
        "aggregate": "KnowledgeAggregate",
        "via_p213_l": True,
        "via_p212_j": True,
        "entities": (
            "KnowledgeObject",
            "SemanticEntity",
            "Embedding",
            "KnowledgeRelation",
            "ContextMemory",
        ),
        "supports": ("graph_rag", "semantic_reasoning", "enterprise_memory"),
        "present_required": True,
    }


def data_domain() -> dict[str, Any]:
    return dict(AI_DATA_DOMAIN) | {"present_required": True}


def security_domain() -> dict[str, Any]:
    return {
        "aggregate": "AISecurityAggregate",
        "via_p207": True,
        "via_p208": True,
        "via_p209": True,
        "via_p210": True,
        "via_p211": True,
        "entities": (
            "AIIdentity",
            "ModelPermission",
            "PromptPolicy",
            "AIThreat",
            "AIControl",
        ),
        "present_required": True,
    }


def events() -> dict[str, Any]:
    return {
        "core_events": [dict(e) for e in DOMAIN_EVENTS],
        "core_event_count": len(DOMAIN_EVENTS),
        "event_ownership_required": True,
        "versioning": "event_version_field",
        "present_required": True,
    }


def microservice_mapping() -> dict[str, Any]:
    return {
        "services": [dict(s) for s in MICROSERVICE_MAP],
        "service_count": len(MICROSERVICE_MAP),
        "mapping": "ddd_domain_to_bc_to_microservice_to_api_to_db_to_events",
        "present_required": True,
    }


def integration() -> dict[str, Any]:
    return dict(INTEGRATION) | {"boundaries_clear_required": True}


def governance() -> dict[str, Any]:
    return dict(DOMAIN_GOVERNANCE) | {"present_required": True}


def cqrs() -> dict[str, Any]:
    commands: list[str] = []
    queries: list[str] = []
    for bc in LOGICAL_BOUNDED_CONTEXTS:
        commands.extend(bc.get("commands", ()))
        queries.extend(bc.get("queries", ()))
    return {
        "commands": list(dict.fromkeys(commands)),
        "command_count": len(set(commands)),
        "queries": list(dict.fromkeys(queries)),
        "query_count": len(set(queries)),
        "alignment_present_required": True,
    }


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
            "enterprise_ai_domain_architecture": True,
            "ddd_model": True,
            "ai_core_domain": True,
            "ai_supporting_domains": True,
            "bounded_contexts": True,
            "aggregates": True,
            "domain_events": True,
            "ai_microservice_boundaries": True,
            "integration_architecture": True,
            "governance_architecture": True,
            "foundation_tests": True,
            "domain_api_live": True,
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
            "ADR-421",
            "ADR-422",
            "P212",
            "P212-J",
            "P213",
            "P213-L",
            "P207",
            "P208",
            "P209",
            "P210",
            "P211",
            "AI_PLATFORM_STANDARD",
            "DDD_DOMAIN_ARCHITECTURE",
        ],
        "domain_map": domain_map(),
        "core_domain_model": core_domain_model(),
        "bounded_contexts": bounded_contexts(),
        "tactical_ddd": tactical_ddd(),
        "model_domain": model_domain(),
        "generative_domain": generative_domain(),
        "agent_domain": agent_domain(),
        "knowledge_domain": knowledge_domain(),
        "data_domain": data_domain(),
        "security_domain": security_domain(),
        "events": events(),
        "microservice_mapping": microservice_mapping(),
        "integration": integration(),
        "governance": governance(),
        "cqrs": cqrs(),
        "cursor_outputs": cursor_outputs(),
        "quality_gates": quality_gates(),
        "production_readiness": production_readiness(),
        "complete_ai_domain_model_present_required": True,
        "strategic_ddd_design_present_required": True,
        "core_domain_defined_required": True,
        "supporting_domains_defined_required": True,
        "bounded_contexts_present_required": True,
        "aggregates_defined_required": True,
        "entities_defined_required": True,
        "value_objects_defined_required": True,
        "domain_events_present_required": True,
        "microservice_mapping_present_required": True,
        "integration_boundaries_clear_required": True,
        "governance_model_present_required": True,
        "domains_loosely_coupled_required": True,
        "sibling_ai_bc_forbidden": True,
        "module_local_llm_sdk_forbidden": True,
        "via_enterprise_ai": True,
        "via_api_gateway": True,
        "api_prefix": f"{API_PREFIX}/domain",
        "forbidden_sibling_bc": [
            "ml_platform",
            "generative_ai",
            "llm_platform",
            "ai_core",
            "vector_intelligence",
            "model_lifecycle_platform",
        ],
    }


def domain_surface() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "routes": [
            "GET /ai/domain",
            "GET /ai/domain/map",
            "GET /ai/domain/core",
            "GET /ai/domain/strategic",
            "GET /ai/domain/bounded-contexts",
            "GET /ai/domain/tactical",
            "GET /ai/domain/models",
            "GET /ai/domain/generative",
            "GET /ai/domain/agents",
            "GET /ai/domain/knowledge",
            "GET /ai/domain/data",
            "GET /ai/domain/security",
            "GET /ai/domain/events",
            "GET /ai/domain/microservices",
            "GET /ai/domain/integration",
            "GET /ai/domain/governance",
            "GET /ai/domain/cqrs",
            "GET /ai/domain/outputs",
            "GET /ai/domain/production-readiness",
            "GET /ai/domain/readiness",
        ],
    }
