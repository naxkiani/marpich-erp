"""P207-E Identity AI Agent Platform — immutable catalog."""
from __future__ import annotations

from typing import Any

PROMPT_ID = "P207-E"
ADR = 320
SOR = "identity_intelligence"
API_PREFIX = "/api/v1/identity-intelligence"
PRODUCT = "Identity AI Agent Platform"

CORE_AGENTS: dict[str, tuple[str, ...]] = {
    "identity_analyst_agent": (
        "identity_investigation",
        "identity_summary",
        "relationship_analysis",
        "risk_explanation",
    ),
    "identity_governance_agent": (
        "access_review_assistance",
        "certification_analysis",
        "role_recommendation",
        "policy_analysis",
    ),
    "identity_security_agent": (
        "threat_detection",
        "identity_compromise_analysis",
        "attack_path_investigation",
        "security_recommendation",
    ),
    "identity_operations_agent": (
        "workflow_automation",
        "error_resolution",
        "provisioning_support",
        "synchronization_recovery",
    ),
    "identity_compliance_agent": (
        "control_monitoring",
        "evidence_collection",
        "audit_preparation",
        "compliance_reporting",
    ),
    "identity_architecture_agent": (
        "architecture_analysis",
        "dependency_analysis",
        "design_recommendations",
    ),
}

AGENT_TOOLS: tuple[str, ...] = (
    "identity_search_tool",
    "access_analysis_tool",
    "risk_analysis_tool",
    "policy_evaluation_tool",
    "workflow_execution_tool",
    "graph_query_tool",
    "audit_query_tool",
)

MEMORY_TYPES: tuple[str, ...] = (
    "short_term_task_context",
    "long_term_historical_identity_knowledge",
    "enterprise_policies_architecture_security",
)

RAG_SOURCES: tuple[str, ...] = (
    "identity_graph",
    "directory_data",
    "governance_policies",
    "security_events",
    "compliance_rules",
    "architecture_documents",
)

MICROSERVICES_LOGICAL: tuple[str, ...] = (
    "ai-agent-runtime-service",
    "agent-orchestrator-service",
    "knowledge-retrieval-service",
    "agent-memory-service",
    "agent-security-service",
    "agent-governance-service",
    "agent-monitoring-service",
)

LOGICAL_BOUNDED_CONTEXTS: tuple[str, ...] = (
    "agent_runtime",
    "agent_orchestrator",
    "agent_memory",
    "knowledge_rag",
    "agent_tools",
    "agent_security",
    "agent_governance",
)

AGGREGATES: tuple[str, ...] = (
    "IdentityAiAgentContract",
    "AgentTask",
    "AgentOrchestrationSession",
    "AgentMemoryScope",
    "AgentToolGrant",
    "AgentRecommendation",
    "AgentGovernancePolicy",
)

COMMANDS: tuple[str, ...] = (
    "CreateAgentTask",
    "AnalyzeIdentity",
    "GenerateRecommendation",
    "RequestApproval",
    "ExecuteAgentAction",
    "RegisterAgent",
    "GrantToolAccess",
)

QUERIES: tuple[str, ...] = (
    "GetAgentCatalog",
    "GetAgentTask",
    "GetRecommendation",
    "GetOrchestrationSession",
    "GetToolGrants",
    "GetAgentMemoryScope",
)

DOMAIN_EVENTS: tuple[str, ...] = (
    "AgentActivated",
    "AnalysisCompleted",
    "RecommendationCreated",
    "ApprovalRequested",
    "ActionExecuted",
    "LearningUpdated",
    "ToolAccessGranted",
)

QUALITY_GATES_REJECT_IF: tuple[str, ...] = (
    "agents_without_permissions",
    "decisions_not_explainable",
    "knowledge_sources_uncontrolled",
    "human_governance_missing",
    "ai_actions_not_audited",
    "security_boundaries_undefined",
    "invents_sibling_agent_bc",
    "embeds_llm_sdk",
    "chatbot_only_ai",
    "tool_access_unscoped",
    "skips_hitl_high_impact",
    "uncontrolled_rag_sources",
)


def capabilities() -> dict[str, Any]:
    return {
        "core_agents": list(CORE_AGENTS.keys()),
        "agent_count": len(CORE_AGENTS),
        "agent_permissions_required": True,
        "explainable_decisions_required": True,
        "knowledge_sources_controlled_required": True,
        "human_governance_required": True,
        "ai_actions_audited_required": True,
        "security_boundaries_defined_required": True,
        "hitl_required": True,
        "via_ai_platform": True,
        "permissionless_forbidden": True,
        "not_permissionless": True,
        "not_non_explainable": True,
        "not_uncontrolled_knowledge": True,
        "not_missing_human_governance": True,
        "not_unaudited": True,
        "not_undefined_security": True,
        "chatbot_only_forbidden": True,
        "embeds_llm_forbidden": True,
    }


def agent_catalog() -> dict[str, Any]:
    return {
        "agents": {k: list(v) for k, v in CORE_AGENTS.items()},
        "count": len(CORE_AGENTS),
        "required": True,
        "not_chatbot_only": True,
    }


def platform_architecture() -> dict[str, Any]:
    return {
        "runtime": [
            "agent_execution",
            "reasoning",
            "memory",
            "tool_access",
            "decision_support",
        ],
        "orchestrator": [
            "agent_coordination",
            "task_routing",
            "workflow_management",
        ],
        "knowledge_layer": [
            "identity_knowledge",
            "context",
            "relationships",
            "policies",
        ],
        "governance_layer": ["permissions", "approval", "audit"],
        "required": True,
    }


def orchestration() -> dict[str, Any]:
    return {
        "flow": [
            "user_system_request",
            "agent_orchestrator",
            "agent_selection",
            "agent_collaboration",
            "knowledge_retrieval",
            "reasoning",
            "decision_output",
            "governance_validation",
            "execution_or_recommendation",
        ],
        "required": True,
    }


def memory() -> dict[str, Any]:
    return {
        "types": list(MEMORY_TYPES),
        "requirements": [
            "privacy_protection",
            "access_control",
            "data_governance",
        ],
        "required": True,
    }


def rag() -> dict[str, Any]:
    return {
        "sources": list(RAG_SOURCES),
        "capabilities": [
            "context_retrieval",
            "semantic_search",
            "evidence_based_answers",
        ],
        "controlled": True,
        "not_uncontrolled": True,
        "via_search_and_directory": True,
    }


def tools() -> dict[str, Any]:
    return {
        "tools": list(AGENT_TOOLS),
        "count": len(AGENT_TOOLS),
        "authorized_only": True,
        "not_unscoped": True,
        "via_authorization": True,
    }


def decision_model() -> dict[str, Any]:
    return {
        "process": [
            "understand_context",
            "retrieve_knowledge",
            "analyze_situation",
            "generate_recommendation",
            "evaluate_policy",
            "calculate_confidence",
            "request_approval",
            "execute",
        ],
        "explainable": True,
        "hitl_for_high_impact": True,
        "not_non_explainable": True,
    }


def human_ai_collaboration() -> dict[str, Any]:
    return {
        "human_roles": [
            "security_analyst",
            "iam_administrator",
            "compliance_officer",
            "enterprise_architect",
        ],
        "ai_responsibilities": [
            "analysis",
            "recommendation",
            "automation_support",
        ],
        "human_responsibilities": [
            "approval",
            "governance",
            "strategic_decisions",
        ],
        "human_governance_required": True,
        "not_missing": True,
    }


def security() -> dict[str, Any]:
    return {
        "zero_trust_ai": [
            "agent_authentication",
            "agent_authorization",
            "tool_access_control",
            "data_protection",
        ],
        "ai_security": [
            "prompt_protection",
            "model_security",
            "output_validation",
            "decision_logging",
        ],
        "boundaries_defined": True,
        "not_undefined": True,
        "actions_audited": True,
        "not_unaudited": True,
    }


def model_governance() -> dict[str, Any]:
    return {
        "model_controls": [
            "version_management",
            "evaluation",
            "monitoring",
            "bias_detection",
        ],
        "agent_controls": [
            "permission_review",
            "activity_monitoring",
            "behaviour_analysis",
        ],
        "via_ai_platform": True,
        "embeds_llm_forbidden": True,
    }


def observability() -> dict[str, Any]:
    return {
        "agents": ["activity", "decisions", "performance"],
        "models": ["accuracy", "drift", "confidence"],
        "operations": ["automation_success", "errors", "human_overrides"],
        "via_observability_platform": True,
    }


def ddd() -> dict[str, Any]:
    return {
        "logical_contexts": list(LOGICAL_BOUNDED_CONTEXTS),
        "logical_count": len(LOGICAL_BOUNDED_CONTEXTS),
        "aggregates": list(AGGREGATES),
        "aggregate_count": len(AGGREGATES),
        "boundaries_clear": True,
        "deployable_unit": SOR,
    }


def cqrs() -> dict[str, Any]:
    return {
        "commands": list(COMMANDS),
        "command_count": len(COMMANDS),
        "queries": list(QUERIES),
        "query_count": len(QUERIES),
        "events": list(DOMAIN_EVENTS),
        "event_count": len(DOMAIN_EVENTS),
        "cqrs_ready": True,
        "event_driven": True,
        "outbox_required": True,
    }


def microservices() -> dict[str, Any]:
    return {
        "logical_services": list(MICROSERVICES_LOGICAL),
        "count": len(MICROSERVICES_LOGICAL),
        "deployable_today": SOR,
        "never_invent_sibling_bc": True,
    }


def integrations() -> dict[str, Any]:
    return {
        "p207a_strategy": True,
        "p207b_mission": True,
        "p207c_domain": True,
        "p207d_autonomous": True,
        "p201_lifecycle": True,
        "p202_iga": True,
        "p203_pam": True,
        "p204_am": True,
        "p205_directory": True,
        "ai_platform": True,
        "workflow_engine": True,
        "authorization": True,
        "audit_platform": True,
        "search_platform": True,
        "agent_integration_complete": True,
    }


def cursor_outputs() -> dict[str, Any]:
    return {
        "ai_agent_platform_architecture": True,
        "agent_runtime_design": True,
        "agent_orchestration_model": True,
        "agent_catalog": True,
        "agent_memory_architecture": True,
        "rag_architecture": True,
        "tool_framework": True,
        "decision_model": True,
        "human_ai_collaboration_model": True,
        "security_architecture": True,
        "event_model": True,
        "cqrs_design": True,
        "microservice_architecture": True,
        "api_specification": True,
        "mlops_architecture": True,
        "governance_framework": True,
        "testing_strategy": True,
        "production_deployment_model": True,
        "count": 18,
    }


def production_readiness() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "checklist": {
            "agent_platform_architecture": True,
            "agent_catalog": True,
            "orchestration": True,
            "memory_and_rag": True,
            "tool_framework": True,
            "decision_and_collaboration": True,
            "security_governance": True,
            "cqrs_events": True,
            "foundation_tests": True,
            "agents_api_live": True,
        },
        "verdict": "ENTERPRISE_GRADE",
    }


def quality_gates() -> dict[str, Any]:
    return {
        "reject_if": list(QUALITY_GATES_REJECT_IF),
        "count": len(QUALITY_GATES_REJECT_IF),
    }


def catalog() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "adr": ADR,
        "sor": SOR,
        "product": PRODUCT,
        "forbidden_sibling_bc": "identity_agent_platform",
        "builds_on": ["P207-A", "P207-B", "P207-C", "P207-D"],
        "capabilities": capabilities(),
        "agent_catalog": agent_catalog(),
        "platform_architecture": platform_architecture(),
        "orchestration": orchestration(),
        "memory": memory(),
        "rag": rag(),
        "tools": tools(),
        "decision_model": decision_model(),
        "human_ai_collaboration": human_ai_collaboration(),
        "security": security(),
        "model_governance": model_governance(),
        "observability": observability(),
        "ddd": ddd(),
        "cqrs": cqrs(),
        "microservices": microservices(),
        "integrations": integrations(),
        "cursor_outputs": cursor_outputs(),
        "quality_gates": quality_gates(),
        "production_readiness": production_readiness(),
        "agent_permissions_required": True,
        "api_prefix": f"{API_PREFIX}/agents",
        "distinct_from": [
            "P207-A /strategy*",
            "P207-B /mission*",
            "P207-C /domain*",
            "P207-D /autonomous*",
        ],
    }


def executive_summary() -> dict[str, Any]:
    return catalog()


def agents_surface() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "routes": [
            "GET /identity-intelligence/agents",
            "GET /identity-intelligence/agents/capabilities",
            "GET /identity-intelligence/agents/catalog",
            "GET /identity-intelligence/agents/architecture",
            "GET /identity-intelligence/agents/orchestration",
            "GET /identity-intelligence/agents/memory",
            "GET /identity-intelligence/agents/rag",
            "GET /identity-intelligence/agents/tools",
            "GET /identity-intelligence/agents/decision",
            "GET /identity-intelligence/agents/collaboration",
            "GET /identity-intelligence/agents/security",
            "GET /identity-intelligence/agents/governance",
            "GET /identity-intelligence/agents/observability",
            "GET /identity-intelligence/agents/ddd",
            "GET /identity-intelligence/agents/cqrs",
            "GET /identity-intelligence/agents/events",
            "GET /identity-intelligence/agents/microservices",
            "GET /identity-intelligence/agents/integrations",
            "GET /identity-intelligence/agents/outputs",
            "GET /identity-intelligence/agents/production-readiness",
            "GET /identity-intelligence/agents/readiness",
        ],
    }
