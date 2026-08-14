"""P214-F Enterprise AI Agent & Autonomous Intelligence — immutable catalog."""
from __future__ import annotations

from typing import Any

PROMPT_ID = "P214-F"
ADR = 426
SOR = "ai"
API_PREFIX = "/api/v1/ai"
PRODUCT = "Enterprise AI Agent & Autonomous Intelligence Platform"
CAPABILITY = "CAP-PLT-AI-001"

PRINCIPLE = (
    "Enterprise AI Agents SHALL become intelligent digital workers capable of "
    "understanding goals, reasoning over enterprise knowledge, executing "
    "approved actions and continuously improving enterprise operations."
)

FABRIC = "meos_autonomous_intelligence_fabric"

CORE_DOMAIN = "enterprise_autonomous_intelligence_management"

SUPPORTING_DOMAINS: tuple[dict[str, str], ...] = (
    {"id": "agent_lifecycle_management", "purpose": "Register, version, deploy, retire agents."},
    {"id": "agent_identity_management", "purpose": "Agent identity, certs, trust levels."},
    {"id": "agent_memory_management", "purpose": "Short/long-term and enterprise memory."},
    {"id": "agent_reasoning_management", "purpose": "Planning, reasoning, decision selection."},
    {"id": "agent_tool_management", "purpose": "Tool registry, permissions, execution."},
    {"id": "agent_workflow_management", "purpose": "Autonomous workflow orchestration."},
    {"id": "agent_governance_management", "purpose": "Policies, compliance, risk, audit."},
    {"id": "agent_monitoring_management", "purpose": "Performance, health, cost, quality."},
    {"id": "agent_marketplace_management", "purpose": "Discover, publish, reuse agents."},
)

AGGREGATE = {
    "name": "EnterpriseAgentPlatformAggregate",
    "root": "EnterpriseAgentPlatform",
    "entities": (
        "AIAgent",
        "AgentVersion",
        "AgentCapability",
        "AgentGoal",
        "AgentPlan",
        "AgentMemory",
        "AgentTool",
        "AgentWorkflow",
        "AgentExecution",
        "AgentPolicy",
        "AgentIdentity",
        "AgentConversation",
    ),
    "value_objects": (
        "AgentIdentifier",
        "AgentType",
        "AgentCapabilityType",
        "GoalDefinition",
        "ExecutionContext",
        "ReasoningTrace",
        "ConfidenceScore",
        "PermissionScope",
        "MemoryReference",
    ),
    "events": (
        "AgentCreatedEvent",
        "AgentActivatedEvent",
        "GoalAssignedEvent",
        "PlanGeneratedEvent",
        "TaskExecutedEvent",
        "ToolInvokedEvent",
        "AgentCompletedEvent",
        "AgentPolicyViolationEvent",
    ),
}

LOGICAL_BOUNDED_CONTEXTS: tuple[dict[str, Any], ...] = (
    {
        "id": "agent_platform_management",
        "bc": "BC-01",
        "name": "Agent Platform Management Context",
        "purpose": "Agent lifecycle, registration, deployment, versioning.",
    },
    {
        "id": "agent_reasoning",
        "bc": "BC-02",
        "name": "Agent Reasoning Context",
        "purpose": "Planning, decision making, reasoning chains, goal decomposition.",
    },
    {
        "id": "agent_memory",
        "bc": "BC-03",
        "name": "Agent Memory Context",
        "purpose": "Short-term, long-term, enterprise memory, context management.",
    },
    {
        "id": "agent_tool_integration",
        "bc": "BC-04",
        "name": "Agent Tool Integration Context",
        "purpose": "API access, system integration, tool execution.",
    },
    {
        "id": "agent_workflow",
        "bc": "BC-05",
        "name": "Agent Workflow Context",
        "purpose": "Task orchestration, process automation, human approval.",
    },
    {
        "id": "multi_agent_collaboration",
        "bc": "BC-06",
        "name": "Multi-Agent Collaboration Context",
        "purpose": "Communication, negotiation, delegation, team intelligence.",
    },
    {
        "id": "agent_governance",
        "bc": "BC-07",
        "name": "Agent Governance Context",
        "purpose": "Policies, compliance, risk, audit.",
    },
    {
        "id": "agent_marketplace",
        "bc": "BC-08",
        "name": "Agent Marketplace Context",
        "purpose": "Agent discovery, publishing, reuse.",
    },
)

AGENT_LIFECYCLE: tuple[dict[str, Any], ...] = (
    {"id": "agent_idea", "owner": "ai_product_owner", "governance": "use_case_intake", "security": "classification", "metrics": ("idea_clarity",), "versioning": "n/a"},
    {"id": "agent_design", "owner": "agent_architect", "governance": "design_review", "security": "threat_model", "metrics": ("design_completeness",), "versioning": "design_rev"},
    {"id": "agent_development", "owner": "agent_engineer", "governance": "code_review", "security": "secure_coding", "metrics": ("dev_velocity",), "versioning": "semver_dev"},
    {"id": "agent_testing", "owner": "qa_ai", "governance": "test_gates", "security": "safety_tests", "metrics": ("pass_rate",), "versioning": "build_id"},
    {"id": "agent_approval", "owner": "ai_risk_owner", "governance": "workflow_approval", "security": "policy_attest", "metrics": ("approval_sla",), "versioning": "approved_tag"},
    {"id": "agent_deployment", "owner": "platform_ops", "governance": "change_control", "security": "signed_release", "metrics": ("deploy_success",), "versioning": "release_tag"},
    {"id": "agent_operation", "owner": "agent_owner", "governance": "runtime_policy", "security": "least_privilege", "metrics": ("task_success",), "versioning": "runtime_rev"},
    {"id": "agent_monitoring", "owner": "ai_ops", "governance": "slo_review", "security": "anomaly_watch", "metrics": ("health_score",), "versioning": "n/a"},
    {"id": "agent_optimization", "owner": "agent_engineer", "governance": "improve_cycle", "security": "regress_check", "metrics": ("cost_quality",), "versioning": "opt_rev"},
    {"id": "agent_retirement", "owner": "agent_owner", "governance": "decommission", "security": "credential_revoke", "metrics": ("retire_complete",), "versioning": "retired"},
)

AGENT_IDENTITY = {
    "present_required": True,
    "via_p207": True,
    "via_p208": True,
    "via_p209": True,
    "attributes": (
        "unique_identity",
        "digital_certificate",
        "permission_profile",
        "capability_profile",
        "trust_level",
        "ownership_record",
    ),
}

REASONING_ENGINE = {
    "present_required": True,
    "capabilities": (
        "goal_understanding",
        "task_planning",
        "reasoning",
        "decision_selection",
        "action_planning",
        "reflection",
        "self_evaluation",
    ),
    "engines": (
        "reasoning_engine",
        "planning_engine",
        "decision_engine",
        "execution_engine",
    ),
}

AGENT_MEMORY = {
    "present_required": True,
    "via_p213_l": True,
    "via_p214_e": True,
    "types": (
        "short_term_memory",
        "long_term_memory",
        "semantic_memory",
        "episodic_memory",
        "operational_memory",
        "enterprise_knowledge_memory",
    ),
}

AGENT_TOOLS = {
    "present_required": True,
    "categories": (
        "internal_tools",
        "erp_apis",
        "crm_apis",
        "analytics_apis",
        "security_apis",
        "data_apis",
        "workflow_apis",
        "external_services",
    ),
    "capabilities": (
        "tool_registry",
        "tool_discovery",
        "tool_permission",
        "tool_execution",
        "tool_monitoring",
    ),
}

MULTI_AGENT = {
    "present_required": True,
    "capabilities": (
        "agent_collaboration",
        "agent_delegation",
        "agent_communication",
        "agent_teams",
        "agent_hierarchies",
        "agent_coordination",
    ),
    "patterns": (
        "supervisor_agent",
        "worker_agents",
        "specialist_agents",
        "coordinator_agents",
        "validator_agents",
    ),
}

AUTONOMOUS_WORKFLOW = {
    "present_required": True,
    "via_workflow_engine": True,
    "capabilities": (
        "business_process_automation",
        "intelligent_workflow",
        "decision_automation",
        "exception_handling",
        "human_approval",
    ),
    "integrates": ("bpm", "erp", "crm", "finance", "hr", "supply_chain"),
}

KNOWLEDGE_INTEGRATION = {
    "via_p212": True,
    "via_p213_l": True,
    "via_p214_e": True,
    "enables": (
        "knowledge_retrieval",
        "semantic_reasoning",
        "context_awareness",
        "enterprise_understanding",
    ),
}

AGENT_DIGITAL_TWIN = {
    "present_required": True,
    "represents": (
        "agent_state",
        "agent_capability",
        "agent_performance",
        "agent_behavior",
        "agent_history",
    ),
    "enables": ("simulation", "optimization", "prediction", "governance"),
}

ASSISTANT_VS_AGENT = {
    "assistant": "Conversational help and recommendations; human remains executor.",
    "agent": "Goal-oriented digital worker; plans, acts via approved tools, learns.",
}

COMMANDS: tuple[str, ...] = (
    "CreateAgentCommand",
    "DeployAgentCommand",
    "AssignGoalCommand",
    "ExecuteTaskCommand",
    "ApproveAgentCommand",
    "UpdateAgentPolicyCommand",
)

QUERIES: tuple[str, ...] = (
    "GetAgentQuery",
    "GetAgentExecutionQuery",
    "GetAgentPerformanceQuery",
    "GetAgentMemoryQuery",
    "GetAgentAuditQuery",
)

CORE_EVENTS: tuple[dict[str, str], ...] = (
    {"name": "AgentCreatedEvent", "owner": "ai", "consumers": "audit,analytics"},
    {"name": "AgentDeployedEvent", "owner": "ai", "consumers": "audit,observability"},
    {"name": "GoalReceivedEvent", "owner": "ai", "consumers": "observability"},
    {"name": "PlanCreatedEvent", "owner": "ai", "consumers": "audit"},
    {"name": "ActionExecutedEvent", "owner": "ai", "consumers": "audit,analytics"},
    {"name": "ToolCalledEvent", "owner": "ai", "consumers": "audit,security"},
    {"name": "AgentLearningEvent", "owner": "ai", "consumers": "analytics"},
    {"name": "AgentRetiredEvent", "owner": "ai", "consumers": "audit,identity"},
)

MICROSERVICES: tuple[dict[str, Any], ...] = (
    {
        "id": "agent_management_service",
        "responsibility": "agent lifecycle and catalog",
        "api": "/ai/agents",
        "db": "ai_*",
        "events": ("AgentCreatedEvent", "AgentDeployedEvent", "AgentRetiredEvent"),
        "security": ("ai.assist.read", "ai.assist.infer"),
        "scaling": "control_plane_replicas",
    },
    {
        "id": "reasoning_service",
        "responsibility": "reasoning chains and reflection",
        "api": "/ai/agents/reasoning",
        "db": "ai_*",
        "events": ("PlanCreatedEvent",),
        "security": ("ai.assist.infer",),
        "scaling": "gpu_optional_hpa",
    },
    {
        "id": "planning_service",
        "responsibility": "goal decomposition and plans",
        "api": "/ai/agents/planning",
        "db": "ai_*",
        "events": ("PlanCreatedEvent", "GoalReceivedEvent"),
        "security": ("ai.assist.infer",),
        "scaling": "stateless_replicas",
    },
    {
        "id": "memory_service",
        "responsibility": "agent memory stores",
        "api": "/ai/agents/{id}/memory",
        "db": "ai_*",
        "events": ("AgentLearningEvent",),
        "security": ("ai.assist.read", "ai.assist.infer"),
        "scaling": "memory_shards",
    },
    {
        "id": "tool_registry_service",
        "responsibility": "tool catalog and permissions",
        "api": "/ai/agents/{id}/tools",
        "db": "ai_*",
        "events": ("ToolCalledEvent",),
        "security": ("ai.assist.infer",),
        "scaling": "stateless_replicas",
    },
    {
        "id": "execution_service",
        "responsibility": "task and tool execution",
        "api": "/ai/agents/{id}/execution",
        "db": "ai_*",
        "events": ("ActionExecutedEvent", "ToolCalledEvent"),
        "security": ("ai.assist.infer",),
        "scaling": "worker_pools",
    },
    {
        "id": "workflow_service",
        "responsibility": "autonomous workflow orchestration",
        "api": "/ai/agents/workflows",
        "db": "ai_*",
        "events": ("ActionExecutedEvent",),
        "security": ("ai.assist.infer",),
        "scaling": "orchestrator_replicas",
    },
    {
        "id": "collaboration_service",
        "responsibility": "multi-agent coordination",
        "api": "/ai/agents/collaboration",
        "db": "ai_*",
        "events": ("GoalReceivedEvent",),
        "security": ("ai.assist.infer",),
        "scaling": "message_driven",
    },
    {
        "id": "governance_service",
        "responsibility": "policies and compliance",
        "api": "/ai/agents/{id}/governance",
        "db": "ai_*",
        "events": ("AgentPolicyViolationEvent",),
        "security": ("ai.assist.read",),
        "scaling": "control_plane",
    },
    {
        "id": "monitoring_service",
        "responsibility": "agent health and ops analytics",
        "api": "/ai/agents/monitoring",
        "db": "ai_*",
        "events": ("ActionExecutedEvent",),
        "security": ("ai.assist.read", "analytics.dashboard.read"),
        "scaling": "observability_pipeline",
    },
)

API_SURFACES: tuple[str, ...] = (
    "/api/v1/ai/agents",
    "/api/v1/ai/agents/{id}/goals",
    "/api/v1/ai/agents/{id}/tasks",
    "/api/v1/ai/agents/{id}/memory",
    "/api/v1/ai/agents/{id}/tools",
    "/api/v1/ai/agents/{id}/execution",
    "/api/v1/ai/agents/{id}/governance",
)

API_STYLES: tuple[str, ...] = ("REST", "GraphQL", "gRPC", "Event", "Streaming")

SECURITY = {
    "present_required": True,
    "zero_trust": True,
    "integrates": ("P207", "P208", "P209", "P210", "P211"),
    "controls": (
        "agent_zero_trust",
        "least_privilege",
        "tool_authorization",
        "action_approval",
        "agent_audit_trail",
        "prompt_protection",
        "memory_security",
        "execution_governance",
    ),
}

OBSERVABILITY = {
    "present_required": True,
    "monitors": (
        "agent_performance",
        "reasoning_quality",
        "task_success_rate",
        "execution_cost",
        "tool_usage",
        "decision_accuracy",
        "policy_violations",
        "human_escalations",
    ),
    "supports": (
        "ai_operations_center",
        "agent_analytics",
        "agent_health_monitoring",
        "autonomous_incident_detection",
    ),
}

DEPLOYMENT = {
    "present_required": True,
    "cloud_native": True,
    "via_p213_o": True,
    "components": (
        "kubernetes",
        "agent_runtime",
        "tool_gateway",
        "memory_store",
        "api_gateway",
        "observability",
        "auto_scaling",
        "workflow_engine",
    ),
    "modes": ("cloud", "private_cloud", "on_premise", "hybrid"),
}

TESTING: tuple[str, ...] = (
    "agent_behavior_testing",
    "reasoning_testing",
    "tool_testing",
    "workflow_testing",
    "safety_testing",
    "security_testing",
    "performance_testing",
    "human_evaluation_testing",
    "simulation_testing",
)

CURSOR_OUTPUTS: tuple[str, ...] = (
    "enterprise_agent_vision",
    "assistant_vs_agent",
    "ddd_domain_model",
    "bounded_context_map",
    "agent_lifecycle_platform",
    "agent_identity_platform",
    "reasoning_engine",
    "agent_memory_architecture",
    "agent_tool_ecosystem",
    "multi_agent_orchestration",
    "autonomous_workflow",
    "knowledge_integration",
    "agent_digital_twin",
    "cqrs_commands_queries",
    "event_sourcing_schema",
    "microservice_boundaries",
    "api_first_surfaces",
    "security_governance",
    "observability_operations",
    "testing_architecture",
    "quality_gates_dod",
    "adr_426",
    "enterprise_ai_agents_law",
)

QUALITY_GATES_REJECT_IF: tuple[str, ...] = (
    "enterprise_ai_agent_platform_is_missing",
    "autonomous_intelligence_platform_is_missing",
    "agent_identity_is_missing",
    "agent_memory_is_missing",
    "agent_reasoning_is_missing",
    "agent_tool_ecosystem_is_missing",
    "multi_agent_architecture_is_missing",
    "workflow_automation_is_missing",
    "agent_governance_is_missing",
    "agent_security_is_missing",
    "cqrs_architecture_is_missing",
    "event_architecture_is_missing",
    "microservices_architecture_is_missing",
    "api_first_architecture_is_missing",
    "cloud_native_deployment_is_missing",
    "sibling_ai_bc",
)


def vision() -> dict[str, Any]:
    return {
        "role": "MEOS Autonomous Intelligence Fabric",
        "principle": PRINCIPLE,
        "equation": (
            "Enterprise Knowledge + Data + Applications + APIs + Events + "
            "LLM Intelligence + AI Agents → Autonomous Enterprise Capability"
        ),
        "loop": (
            "reasoning",
            "planning",
            "execution",
            "learning",
            "optimization",
            "continuous_improvement",
        ),
        "pillars": (
            "autonomous_task_execution",
            "goal_oriented_intelligence",
            "enterprise_process_automation",
            "human_ai_collaboration",
            "multi_agent_cooperation",
            "autonomous_decision_support",
        ),
        "assistant_vs_agent": dict(ASSISTANT_VS_AGENT),
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


def lifecycle() -> dict[str, Any]:
    return {
        "present_required": True,
        "stages": [dict(s) for s in AGENT_LIFECYCLE],
        "stage_count": len(AGENT_LIFECYCLE),
    }


def identity() -> dict[str, Any]:
    return dict(AGENT_IDENTITY)


def reasoning() -> dict[str, Any]:
    return dict(REASONING_ENGINE)


def memory() -> dict[str, Any]:
    return dict(AGENT_MEMORY)


def tools() -> dict[str, Any]:
    return dict(AGENT_TOOLS)


def multi_agent() -> dict[str, Any]:
    return dict(MULTI_AGENT)


def workflow() -> dict[str, Any]:
    return dict(AUTONOMOUS_WORKFLOW)


def knowledge() -> dict[str, Any]:
    return dict(KNOWLEDGE_INTEGRATION)


def digital_twin() -> dict[str, Any]:
    return dict(AGENT_DIGITAL_TWIN)


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


def observability() -> dict[str, Any]:
    return dict(OBSERVABILITY)


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
            "enterprise_ai_agent_platform": True,
            "agent_lifecycle_management": True,
            "agent_identity": True,
            "agent_memory": True,
            "agent_reasoning": True,
            "agent_tool_platform": True,
            "multi_agent_collaboration": True,
            "autonomous_workflow": True,
            "agent_governance": True,
            "agent_security": True,
            "agent_digital_twin": True,
            "cqrs_architecture": True,
            "event_architecture": True,
            "microservice_architecture": True,
            "api_platform": True,
            "deployment_architecture": True,
            "testing_architecture": True,
            "foundation_tests": True,
            "agents_api_live": True,
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
            "ADR-421",
            "ADR-422",
            "ADR-423",
            "ADR-424",
            "ADR-425",
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
        "lifecycle": lifecycle(),
        "identity": identity(),
        "reasoning": reasoning(),
        "memory": memory(),
        "tools": tools(),
        "multi_agent": multi_agent(),
        "workflow": workflow(),
        "knowledge": knowledge(),
        "digital_twin": digital_twin(),
        "cqrs": cqrs(),
        "events": events(),
        "microservices": microservices(),
        "api": api(),
        "security": security(),
        "observability": observability(),
        "deployment": deployment(),
        "testing": testing(),
        "cursor_outputs": cursor_outputs(),
        "quality_gates": quality_gates(),
        "production_readiness": production_readiness(),
        "enterprise_ai_agent_platform_present_required": True,
        "autonomous_intelligence_platform_present_required": True,
        "agent_identity_present_required": True,
        "agent_memory_present_required": True,
        "agent_reasoning_present_required": True,
        "agent_tool_ecosystem_present_required": True,
        "multi_agent_architecture_present_required": True,
        "workflow_automation_present_required": True,
        "agent_governance_present_required": True,
        "agent_security_present_required": True,
        "agent_digital_twin_present_required": True,
        "cqrs_architecture_present_required": True,
        "event_architecture_present_required": True,
        "microservices_architecture_present_required": True,
        "api_first_architecture_present_required": True,
        "cloud_native_deployment_present_required": True,
        "sibling_ai_bc_forbidden": True,
        "module_local_agent_runtime_forbidden": True,
        "via_enterprise_ai": True,
        "via_api_gateway": True,
        "api_prefix": f"{API_PREFIX}/agents",
        "forbidden_sibling_bc": [
            "ai_agent_platform",
            "agent_platform",
            "autonomous_intelligence",
            "multi_agent_platform",
            "agent_runtime",
            "generative_ai",
            "llm_platform",
            "vector_intelligence",
            "ml_platform",
            "ai_core",
        ],
    }


def agents_surface() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "routes": [
            "GET /ai/agents",
            "GET /ai/agents/vision",
            "GET /ai/agents/domain",
            "GET /ai/agents/bounded-contexts",
            "GET /ai/agents/lifecycle",
            "GET /ai/agents/identity",
            "GET /ai/agents/reasoning",
            "GET /ai/agents/memory",
            "GET /ai/agents/tools",
            "GET /ai/agents/multi-agent",
            "GET /ai/agents/workflow",
            "GET /ai/agents/knowledge",
            "GET /ai/agents/digital-twin",
            "GET /ai/agents/cqrs",
            "GET /ai/agents/events",
            "GET /ai/agents/microservices",
            "GET /ai/agents/api",
            "GET /ai/agents/security",
            "GET /ai/agents/observability",
            "GET /ai/agents/deployment",
            "GET /ai/agents/testing",
            "GET /ai/agents/outputs",
            "GET /ai/agents/production-readiness",
            "GET /ai/agents/readiness",
        ],
    }
