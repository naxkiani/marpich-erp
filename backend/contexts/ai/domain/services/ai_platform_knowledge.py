"""P214-G Enterprise AI Knowledge, RAG & Cognitive Intelligence — immutable catalog."""
from __future__ import annotations

from typing import Any

PROMPT_ID = "P214-G"
ADR = 427
SOR = "ai"
API_PREFIX = "/api/v1/ai"
PRODUCT = "Enterprise AI Knowledge, RAG & Cognitive Intelligence Platform"
CAPABILITY = "CAP-PLT-AI-001"

PRINCIPLE = (
    "Enterprise AI Knowledge Platform SHALL provide the trusted cognitive "
    "foundation allowing AI systems to understand enterprise context, retrieve "
    "relevant knowledge, reason accurately and generate reliable intelligence."
)

FABRIC = "meos_enterprise_cognitive_knowledge_fabric"

CORE_DOMAIN = "enterprise_cognitive_knowledge_management"

SUPPORTING_DOMAINS: tuple[dict[str, str], ...] = (
    {"id": "knowledge_acquisition", "purpose": "Ingest and register knowledge sources."},
    {"id": "knowledge_processing", "purpose": "Chunk, classify, enrich documents."},
    {"id": "knowledge_graph", "purpose": "Entities, relations, semantic reasoning."},
    {"id": "vector_intelligence", "purpose": "Embeddings, indexes, similarity search."},
    {"id": "rag_pipeline", "purpose": "Retrieval, ranking, grounded generation."},
    {"id": "semantic_search", "purpose": "Meaning-aware enterprise search."},
    {"id": "context_management", "purpose": "Context assembly, compression, security."},
    {"id": "ai_memory", "purpose": "Short/long-term and enterprise memory."},
    {"id": "knowledge_governance", "purpose": "Ownership, quality, security, compliance."},
)

AGGREGATE = {
    "name": "EnterpriseKnowledgeIntelligenceAggregate",
    "root": "EnterpriseKnowledgeIntelligence",
    "entities": (
        "KnowledgeAsset",
        "KnowledgeSource",
        "KnowledgeDocument",
        "KnowledgeEntity",
        "KnowledgeRelation",
        "KnowledgeGraph",
        "Embedding",
        "VectorIndex",
        "RetrievalPipeline",
        "ContextWindow",
        "KnowledgeMemory",
        "RAGApplication",
    ),
    "value_objects": (
        "KnowledgeIdentifier",
        "DocumentIdentifier",
        "EmbeddingVector",
        "SemanticScore",
        "RelevanceScore",
        "ContextIdentifier",
        "KnowledgeConfidence",
        "SourceTrustLevel",
    ),
    "events": (
        "KnowledgeAssetCreatedEvent",
        "KnowledgeIndexedEvent",
        "EmbeddingGeneratedEvent",
        "KnowledgeRetrievedEvent",
        "ContextCreatedEvent",
        "RAGResponseGeneratedEvent",
        "KnowledgeUpdatedEvent",
    ),
}

LOGICAL_BOUNDED_CONTEXTS: tuple[dict[str, Any], ...] = (
    {
        "id": "knowledge_acquisition",
        "bc": "BC-01",
        "name": "Knowledge Acquisition Context",
        "purpose": "Knowledge ingestion, document acquisition, source registration.",
    },
    {
        "id": "knowledge_processing",
        "bc": "BC-02",
        "name": "Knowledge Processing Context",
        "purpose": "Document processing, chunking, classification, enrichment.",
    },
    {
        "id": "knowledge_graph",
        "bc": "BC-03",
        "name": "Knowledge Graph Context",
        "purpose": "Entity modeling, relationships, semantic reasoning.",
    },
    {
        "id": "vector_intelligence",
        "bc": "BC-04",
        "name": "Vector Intelligence Context",
        "purpose": "Embedding generation, vector storage, similarity search.",
    },
    {
        "id": "rag_intelligence",
        "bc": "BC-05",
        "name": "RAG Intelligence Context",
        "purpose": "Retrieval pipelines, context construction, grounded generation.",
    },
    {
        "id": "knowledge_memory",
        "bc": "BC-06",
        "name": "Knowledge Memory Context",
        "purpose": "Enterprise memory, AI memory, historical context.",
    },
    {
        "id": "knowledge_governance",
        "bc": "BC-07",
        "name": "Knowledge Governance Context",
        "purpose": "Ownership, quality, security, compliance.",
    },
)

KNOWLEDGE_FABRIC = {
    "present_required": True,
    "includes": (
        "structured_knowledge",
        "unstructured_knowledge",
        "enterprise_documents",
        "business_rules",
        "policies",
        "processes",
        "events",
        "metadata",
        "ontologies",
        "taxonomies",
    ),
}

KNOWLEDGE_LIFECYCLE: tuple[str, ...] = (
    "create",
    "capture",
    "process",
    "enrich",
    "validate",
    "publish",
    "consume",
    "improve",
)

RAG_PIPELINE: tuple[str, ...] = (
    "knowledge_sources",
    "data_ingestion",
    "document_processing",
    "chunk_generation",
    "embedding_creation",
    "vector_storage",
    "retrieval",
    "ranking",
    "context_assembly",
    "llm_generation",
    "response_validation",
)

INGESTION = {
    "present_required": True,
    "sources": (
        "enterprise_documents",
        "databases",
        "data_warehouses",
        "lakehouse",
        "apis",
        "applications",
        "emails",
        "knowledge_bases",
        "business_processes",
        "iot_sources",
        "events",
    ),
    "capabilities": (
        "connectors",
        "parsers",
        "metadata_extraction",
        "classification",
        "validation",
    ),
}

VECTOR_INTELLIGENCE = {
    "present_required": True,
    "capabilities": (
        "embedding_models",
        "vector_database",
        "similarity_search",
        "hybrid_search",
        "semantic_retrieval",
        "vector_optimization",
        "index_management",
    ),
    "lifecycle": (
        "generate",
        "store",
        "index",
        "search",
        "update",
        "retire",
    ),
}

SEMANTIC_INTELLIGENCE = {
    "present_required": True,
    "via_p213_l": True,
    "capabilities": (
        "ontologies",
        "taxonomies",
        "entity_resolution",
        "semantic_mapping",
        "concept_extraction",
        "meaning_understanding",
    ),
}

GRAPH_RAG = {
    "present_required": True,
    "via_p213_l": True,
    "capabilities": (
        "graph_retrieval",
        "relationship_reasoning",
        "entity_context",
        "multi_hop_reasoning",
        "enterprise_knowledge_discovery",
    ),
}

AI_MEMORY = {
    "present_required": True,
    "via_p214_f": True,
    "types": (
        "short_term_memory",
        "conversation_memory",
        "agent_memory",
        "operational_memory",
        "semantic_memory",
        "historical_memory",
        "enterprise_memory",
    ),
}

CONTEXT_ENGINE = {
    "present_required": True,
    "capabilities": (
        "context_collection",
        "context_ranking",
        "context_compression",
        "context_validation",
        "context_personalization",
        "context_security",
    ),
}

COGNITIVE_REASONING = {
    "present_required": True,
    "capabilities": (
        "reasoning_chains",
        "knowledge_based_reasoning",
        "semantic_reasoning",
        "decision_support",
        "explanation_generation",
        "confidence_assessment",
    ),
}

KNOWLEDGE_GOVERNANCE = {
    "present_required": True,
    "via_p212": True,
    "controls": (
        "knowledge_ownership",
        "knowledge_stewardship",
        "knowledge_quality",
        "knowledge_classification",
        "knowledge_security",
        "knowledge_compliance",
    ),
}

DATA_VS_KNOWLEDGE = {
    "data": "Raw facts and records without interpretive structure.",
    "knowledge": "Trusted, contextualized, related meaning ready for reasoning.",
}

COMMANDS: tuple[str, ...] = (
    "CreateKnowledgeAssetCommand",
    "RegisterKnowledgeSourceCommand",
    "GenerateEmbeddingCommand",
    "BuildRAGPipelineCommand",
    "PublishKnowledgeCommand",
    "UpdateKnowledgeCommand",
)

QUERIES: tuple[str, ...] = (
    "GetKnowledgeQuery",
    "SearchKnowledgeQuery",
    "RetrieveContextQuery",
    "GetKnowledgeGraphQuery",
    "GetRAGHistoryQuery",
)

CORE_EVENTS: tuple[dict[str, str], ...] = (
    {"name": "KnowledgeCreatedEvent", "owner": "ai", "consumers": "audit,search"},
    {"name": "KnowledgeProcessedEvent", "owner": "ai", "consumers": "observability"},
    {"name": "EmbeddingGeneratedEvent", "owner": "ai", "consumers": "analytics"},
    {"name": "KnowledgeIndexedEvent", "owner": "ai", "consumers": "search,audit"},
    {"name": "RetrievalExecutedEvent", "owner": "ai", "consumers": "audit,analytics"},
    {"name": "ContextGeneratedEvent", "owner": "ai", "consumers": "observability"},
    {"name": "RAGCompletedEvent", "owner": "ai", "consumers": "audit,analytics"},
    {"name": "KnowledgeQualityChangedEvent", "owner": "ai", "consumers": "governance,audit"},
)

MICROSERVICES: tuple[dict[str, Any], ...] = (
    {
        "id": "knowledge_ingestion_service",
        "responsibility": "source registration and ingestion",
        "api": "/ai/knowledge/assets",
        "db": "ai_*",
        "events": ("KnowledgeCreatedEvent",),
        "security": ("ai.assist.read", "ai.assist.infer"),
        "scaling": "async_ingestion_workers",
    },
    {
        "id": "document_processing_service",
        "responsibility": "chunking, classification, enrichment",
        "api": "/ai/knowledge/processing",
        "db": "ai_*",
        "events": ("KnowledgeProcessedEvent",),
        "security": ("ai.assist.infer",),
        "scaling": "cpu_workers",
    },
    {
        "id": "embedding_service",
        "responsibility": "embedding generation",
        "api": "/ai/knowledge/embeddings",
        "db": "ai_*",
        "events": ("EmbeddingGeneratedEvent",),
        "security": ("ai.assist.infer",),
        "scaling": "batch_and_online_pools",
    },
    {
        "id": "vector_search_service",
        "responsibility": "similarity and hybrid search",
        "api": "/ai/knowledge/search",
        "db": "ai_*",
        "events": ("RetrievalExecutedEvent",),
        "security": ("ai.assist.read",),
        "scaling": "vector_index_shards",
    },
    {
        "id": "knowledge_graph_service",
        "responsibility": "graph entities and multi-hop retrieval",
        "api": "/ai/knowledge/graph",
        "db": "ai_*",
        "events": ("KnowledgeIndexedEvent",),
        "security": ("ai.assist.read",),
        "scaling": "graph_query_pool",
    },
    {
        "id": "rag_orchestration_service",
        "responsibility": "RAG pipeline orchestration",
        "api": "/ai/knowledge/rag",
        "db": "ai_*",
        "events": ("RAGCompletedEvent", "ContextGeneratedEvent"),
        "security": ("ai.assist.infer",),
        "scaling": "stateless_replicas",
    },
    {
        "id": "context_service",
        "responsibility": "context assembly and compression",
        "api": "/ai/knowledge/context",
        "db": "ai_*",
        "events": ("ContextGeneratedEvent",),
        "security": ("ai.assist.infer",),
        "scaling": "stateless_replicas",
    },
    {
        "id": "memory_service",
        "responsibility": "enterprise and AI memory",
        "api": "/ai/knowledge/memory",
        "db": "ai_*",
        "events": ("KnowledgeUpdatedEvent",),
        "security": ("ai.assist.read", "ai.assist.infer"),
        "scaling": "memory_shards",
    },
    {
        "id": "knowledge_governance_service",
        "responsibility": "ownership, quality, compliance",
        "api": "/ai/knowledge/governance",
        "db": "ai_*",
        "events": ("KnowledgeQualityChangedEvent",),
        "security": ("ai.assist.read",),
        "scaling": "control_plane",
    },
    {
        "id": "analytics_service",
        "responsibility": "RAG quality metrics via Analytics SoR",
        "api": "/analytics (delegated)",
        "db": "analytics_*",
        "events": ("RAGCompletedEvent",),
        "security": ("analytics.dashboard.read",),
        "scaling": "analytics_platform",
    },
)

API_SURFACES: tuple[str, ...] = (
    "/api/v1/ai/knowledge/assets",
    "/api/v1/ai/knowledge/search",
    "/api/v1/ai/knowledge/retrieve",
    "/api/v1/ai/knowledge/context",
    "/api/v1/ai/knowledge/rag/pipelines",
    "/api/v1/ai/knowledge/rag/query",
    "/api/v1/ai/knowledge/memory",
)

API_STYLES: tuple[str, ...] = ("REST", "GraphQL", "gRPC", "Streaming", "Event")

SECURITY = {
    "present_required": True,
    "zero_trust": True,
    "integrates": ("P207", "P208", "P209", "P210", "P211"),
    "controls": (
        "knowledge_access_control",
        "retrieval_authorization",
        "data_protection",
        "prompt_context_security",
        "knowledge_audit_trail",
        "ai_trust_scoring",
    ),
}

DEPLOYMENT = {
    "present_required": True,
    "cloud_native": True,
    "via_p213_o": True,
    "components": (
        "kubernetes",
        "vector_database_cluster",
        "knowledge_graph_database",
        "ai_runtime",
        "rag_services",
        "api_gateway",
        "observability",
        "auto_scaling",
    ),
}

TESTING: tuple[str, ...] = (
    "knowledge_quality_testing",
    "retrieval_accuracy_testing",
    "embedding_testing",
    "rag_evaluation_testing",
    "hallucination_testing",
    "security_testing",
    "performance_testing",
    "regression_testing",
    "human_evaluation_testing",
)

CURSOR_OUTPUTS: tuple[str, ...] = (
    "enterprise_knowledge_vision",
    "data_vs_knowledge",
    "ddd_domain_model",
    "bounded_context_map",
    "knowledge_fabric",
    "knowledge_lifecycle",
    "rag_pipeline",
    "ingestion_platform",
    "vector_intelligence",
    "semantic_intelligence",
    "graph_enhanced_rag",
    "ai_memory_architecture",
    "context_intelligence_engine",
    "cognitive_reasoning",
    "knowledge_governance",
    "cqrs_commands_queries",
    "event_sourcing_schema",
    "microservice_boundaries",
    "api_first_surfaces",
    "security_trust",
    "cloud_native_deployment",
    "testing_architecture",
    "quality_gates_dod",
    "adr_427",
    "enterprise_ai_knowledge_law",
)

QUALITY_GATES_REJECT_IF: tuple[str, ...] = (
    "enterprise_ai_knowledge_platform_is_missing",
    "rag_platform_is_missing",
    "vector_intelligence_platform_is_missing",
    "knowledge_graph_integration_is_missing",
    "semantic_intelligence_is_missing",
    "ai_memory_platform_is_missing",
    "context_intelligence_is_missing",
    "cognitive_reasoning_is_missing",
    "knowledge_governance_is_missing",
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
        "role": "MEOS Enterprise Cognitive Knowledge Fabric",
        "principle": PRINCIPLE,
        "equation": (
            "Enterprise Data + Documents + Applications + Processes + "
            "Knowledge Graph + Vector Intelligence + LLMs + AI Agents → "
            "Grounded Enterprise Intelligence"
        ),
        "loop": (
            "context_understanding",
            "knowledge_retrieval",
            "reasoning",
            "decision_support",
            "autonomous_intelligence",
        ),
        "pillars": (
            "trusted_knowledge",
            "enterprise_memory",
            "knowledge_driven_decisions",
            "hallucination_reduction",
            "context_aware_intelligence",
            "knowledge_lifecycle",
        ),
        "data_vs_knowledge": dict(DATA_VS_KNOWLEDGE),
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


def knowledge_fabric() -> dict[str, Any]:
    return {
        **dict(KNOWLEDGE_FABRIC),
        "lifecycle": list(KNOWLEDGE_LIFECYCLE),
        "lifecycle_stage_count": len(KNOWLEDGE_LIFECYCLE),
    }


def rag_platform() -> dict[str, Any]:
    return {
        "present_required": True,
        "via_p214_e": True,
        "pipeline": list(RAG_PIPELINE),
        "pipeline_count": len(RAG_PIPELINE),
    }


def ingestion() -> dict[str, Any]:
    return dict(INGESTION)


def vector_intelligence() -> dict[str, Any]:
    return dict(VECTOR_INTELLIGENCE)


def semantic() -> dict[str, Any]:
    return dict(SEMANTIC_INTELLIGENCE)


def graph_rag() -> dict[str, Any]:
    return dict(GRAPH_RAG)


def memory() -> dict[str, Any]:
    return dict(AI_MEMORY)


def context_engine() -> dict[str, Any]:
    return dict(CONTEXT_ENGINE)


def cognitive() -> dict[str, Any]:
    return dict(COGNITIVE_REASONING)


def governance() -> dict[str, Any]:
    return dict(KNOWLEDGE_GOVERNANCE)


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
            "enterprise_knowledge_platform": True,
            "rag_platform": True,
            "knowledge_ingestion": True,
            "vector_intelligence": True,
            "semantic_intelligence": True,
            "knowledge_graph_integration": True,
            "ai_memory": True,
            "context_engine": True,
            "cognitive_reasoning": True,
            "knowledge_governance": True,
            "cqrs_architecture": True,
            "event_architecture": True,
            "microservice_architecture": True,
            "api_platform": True,
            "security_architecture": True,
            "deployment_architecture": True,
            "testing_architecture": True,
            "foundation_tests": True,
            "knowledge_api_live": True,
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
            "P214-E",
            "P214-F",
            "ADR-421",
            "ADR-422",
            "ADR-423",
            "ADR-424",
            "ADR-425",
            "ADR-426",
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
        "knowledge_fabric": knowledge_fabric(),
        "rag_platform": rag_platform(),
        "ingestion": ingestion(),
        "vector_intelligence": vector_intelligence(),
        "semantic": semantic(),
        "graph_rag": graph_rag(),
        "memory": memory(),
        "context_engine": context_engine(),
        "cognitive": cognitive(),
        "governance": governance(),
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
        "enterprise_ai_knowledge_platform_present_required": True,
        "rag_platform_present_required": True,
        "vector_intelligence_platform_present_required": True,
        "knowledge_graph_integration_present_required": True,
        "semantic_intelligence_present_required": True,
        "ai_memory_platform_present_required": True,
        "context_intelligence_present_required": True,
        "cognitive_reasoning_present_required": True,
        "knowledge_governance_present_required": True,
        "cqrs_architecture_present_required": True,
        "event_architecture_present_required": True,
        "microservices_architecture_present_required": True,
        "api_first_architecture_present_required": True,
        "zero_trust_security_present_required": True,
        "cloud_native_deployment_present_required": True,
        "sibling_ai_bc_forbidden": True,
        "module_local_vector_sdk_forbidden": True,
        "via_enterprise_ai": True,
        "via_api_gateway": True,
        "api_prefix": f"{API_PREFIX}/knowledge",
        "forbidden_sibling_bc": [
            "ai_knowledge",
            "rag_platform",
            "vector_intelligence",
            "cognitive_intelligence",
            "knowledge_graph_platform",
            "semantic_intelligence",
            "ai_memory_platform",
            "generative_ai",
            "llm_platform",
            "ai_core",
        ],
    }


def knowledge_surface() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "routes": [
            "GET /ai/knowledge",
            "GET /ai/knowledge/vision",
            "GET /ai/knowledge/domain",
            "GET /ai/knowledge/bounded-contexts",
            "GET /ai/knowledge/fabric",
            "GET /ai/knowledge/rag",
            "GET /ai/knowledge/ingestion",
            "GET /ai/knowledge/vectors",
            "GET /ai/knowledge/semantic",
            "GET /ai/knowledge/graph-rag",
            "GET /ai/knowledge/memory",
            "GET /ai/knowledge/context",
            "GET /ai/knowledge/cognitive",
            "GET /ai/knowledge/governance",
            "GET /ai/knowledge/cqrs",
            "GET /ai/knowledge/events",
            "GET /ai/knowledge/microservices",
            "GET /ai/knowledge/api",
            "GET /ai/knowledge/security",
            "GET /ai/knowledge/deployment",
            "GET /ai/knowledge/testing",
            "GET /ai/knowledge/outputs",
            "GET /ai/knowledge/production-readiness",
            "GET /ai/knowledge/readiness",
        ],
    }
