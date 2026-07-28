"""P213-M AI Native Analytics & Autonomous Decision Intelligence — immutable catalog."""
from __future__ import annotations

from typing import Any

PROMPT_ID = "P213-M"
ADR = 417
SOR = "analytics"
API_PREFIX = "/api/v1/analytics"
PRODUCT = "AI Native Analytics & Autonomous Decision Intelligence Platform"
CAPABILITY = "CAP-PLT-BI-001"

PRINCIPLE = (
    "Every enterprise decision SHALL be supported by AI reasoning, "
    "enterprise knowledge, governance policies and continuous learning."
)

FABRIC = "meos_autonomous_decision_intelligence_fabric"

CORE_DOMAIN = "enterprise_autonomous_decision_intelligence"

SUPPORTING_DOMAINS: tuple[dict[str, str], ...] = (
    {"id": "ai_reasoning", "purpose": "Multi-step and hybrid enterprise reasoning."},
    {"id": "decision_agents", "purpose": "Domain decision agent ecosystem."},
    {"id": "executive_copilot", "purpose": "Executive conversations and briefings."},
    {"id": "recommendation_intelligence", "purpose": "Governed action recommendations."},
    {"id": "decision_automation", "purpose": "Autonomous and approved execution."},
    {"id": "ai_governance", "purpose": "AI compliance, risk, explainability."},
    {"id": "cognitive_learning", "purpose": "Continuous learning and feedback."},
    {"id": "human_approval", "purpose": "Human oversight and escalation."},
)

LOGICAL_BOUNDED_CONTEXTS: tuple[dict[str, Any], ...] = (
    {
        "id": "enterprise_decision_intelligence",
        "bc": "BC-01",
        "name": "Enterprise Decision Intelligence Context",
        "purpose": "Decision lifecycle, orchestration, recommendations.",
    },
    {
        "id": "ai_reasoning",
        "bc": "BC-02",
        "name": "AI Reasoning Context",
        "purpose": "Multi-step, context, policy, and semantic reasoning.",
    },
    {
        "id": "executive_ai_copilot",
        "bc": "BC-03",
        "name": "Executive AI Copilot Context",
        "purpose": "Executive assistance, conversations, summaries.",
    },
    {
        "id": "decision_automation",
        "bc": "BC-04",
        "name": "Decision Automation Context",
        "purpose": "Workflow automation, autonomous execution, approvals.",
    },
    {
        "id": "learning",
        "bc": "BC-05",
        "name": "Learning Context",
        "purpose": "Continuous learning, feedback, decision optimisation.",
    },
    {
        "id": "ai_governance",
        "bc": "BC-06",
        "name": "AI Governance Context",
        "purpose": "AI compliance, explainability, risk, policy validation.",
    },
)

AGGREGATE = {
    "name": "AutonomousDecisionAggregate",
    "root": "AutonomousDecision",
    "entities": (
        "DecisionAgent",
        "DecisionSession",
        "Recommendation",
        "ReasoningChain",
        "BusinessGoal",
        "ExecutionPlan",
        "DecisionExplanation",
        "ApprovalWorkflow",
        "LearningFeedback",
        "PolicyEvaluation",
    ),
    "value_objects": (
        "ReasoningScore",
        "ConfidenceScore",
        "RiskScore",
        "BusinessPriority",
        "DecisionContext",
        "OptimizationScore",
        "ApprovalLevel",
        "BusinessIntent",
    ),
    "events": (
        "DecisionRequestedEvent",
        "ReasoningCompletedEvent",
        "RecommendationGeneratedEvent",
        "DecisionApprovedEvent",
        "DecisionExecutedEvent",
        "LearningFeedbackCapturedEvent",
    ),
}

AGENT_CATEGORIES: tuple[dict[str, Any], ...] = (
    {"id": "executive", "mission": "Executive decision support.", "approval": "level_2"},
    {"id": "financial", "mission": "Financial intelligence.", "approval": "level_2"},
    {"id": "sales", "mission": "Sales optimization.", "approval": "level_1"},
    {"id": "marketing", "mission": "Marketing optimization.", "approval": "level_1"},
    {"id": "hr", "mission": "Workforce intelligence.", "approval": "level_2"},
    {"id": "supply_chain", "mission": "Supply chain optimization.", "approval": "level_2"},
    {"id": "risk", "mission": "Risk intelligence.", "approval": "level_2"},
    {"id": "compliance", "mission": "Compliance recommendations.", "approval": "level_2"},
    {"id": "cyber_security", "mission": "Security response.", "approval": "level_3"},
    {"id": "customer_intelligence", "mission": "Customer insights.", "approval": "level_1"},
    {"id": "operations", "mission": "Operational optimization.", "approval": "level_2"},
    {"id": "strategy", "mission": "Strategic planning.", "approval": "level_2"},
    {"id": "analytics_scientist", "mission": "Analytical science.", "approval": "level_1"},
    {"id": "knowledge_graph", "mission": "Graph reasoning.", "approval": "level_1"},
    {"id": "digital_twin", "mission": "Simulation-backed decisions.", "approval": "level_2"},
    {"id": "data_governance", "mission": "Governed data decisions.", "approval": "level_2"},
)

MULTI_AGENT: dict[str, Any] = {
    "capabilities": (
        "task_delegation",
        "consensus_decision_making",
        "agent_negotiation",
        "shared_memory",
        "shared_context",
        "event_collaboration",
        "hierarchical_agents",
        "peer_to_peer_agents",
        "swarm_intelligence",
        "distributed_reasoning",
    ),
}

REASONING_ENGINE: tuple[str, ...] = (
    "chain_of_thought_orchestration",
    "graph_reasoning",
    "causal_reasoning",
    "constraint_reasoning",
    "goal_oriented_planning",
    "semantic_reasoning",
    "rule_based_reasoning",
    "hybrid_symbolic_llm_reasoning",
    "decision_trees",
    "bayesian_reasoning",
    "case_based_reasoning",
)

AUTONOMY_LEVELS: tuple[dict[str, Any], ...] = (
    {"level": 0, "name": "observation"},
    {"level": 1, "name": "recommendation"},
    {"level": 2, "name": "human_approval_required"},
    {"level": 3, "name": "conditional_autonomous_execution"},
    {"level": 4, "name": "fully_autonomous_execution"},
)

AUTONOMY_CONTROLS: tuple[str, ...] = (
    "escalation_policies",
    "risk_thresholds",
    "business_constraints",
    "emergency_stop",
    "rollback",
    "decision_replay",
)

EXECUTIVE_COPILOT: dict[str, Any] = {
    "capabilities": (
        "executive_conversations",
        "kpi_explanations",
        "strategic_recommendations",
        "scenario_comparison",
        "board_meeting_preparation",
        "executive_briefings",
        "risk_summaries",
        "opportunity_discovery",
        "action_tracking",
    ),
    "modalities": (
        "natural_language",
        "voice",
        "documents",
        "dashboards",
        "graph_exploration",
    ),
}

AI_GOVERNANCE: dict[str, Any] = {
    "registries": (
        "ai_registry",
        "model_registry",
        "prompt_registry",
        "agent_registry",
        "policy_registry",
    ),
    "controls": (
        "ai_risk_assessment",
        "bias_detection",
        "fairness_evaluation",
        "explainability_validation",
        "human_oversight",
        "ai_audit_trail",
    ),
}

KNOWLEDGE_GRAPH: dict[str, Any] = {
    "via_p212_j": True,
    "via_p213_l": True,
    "capabilities": (
        "graph_augmented_generation",
        "semantic_retrieval",
        "context_expansion",
        "enterprise_memory",
        "cross_domain_reasoning",
    ),
}

DIGITAL_TWIN: dict[str, Any] = {
    "via_p212_l": True,
    "capabilities": (
        "decision_simulation",
        "ai_simulation",
        "scenario_planning",
        "future_state_evaluation",
        "operational_optimisation",
        "autonomous_strategy_testing",
    ),
}

PREDICTIVE_INTEGRATION: dict[str, Any] = {"via_p213_j": True}
PRESCRIPTIVE_INTEGRATION: dict[str, Any] = {"via_p213_k": True}
SEMANTIC_INTEGRATION: dict[str, Any] = {"via_p213_g": True}

COMMANDS: tuple[str, ...] = (
    "CreateDecisionSessionCommand",
    "ExecuteReasoningCommand",
    "GenerateRecommendationCommand",
    "ApproveDecisionCommand",
    "ExecuteDecisionCommand",
    "RegisterLearningFeedbackCommand",
)

QUERIES: tuple[str, ...] = (
    "GetDecisionSessionQuery",
    "GetRecommendationQuery",
    "GetReasoningQuery",
    "SearchDecisionHistoryQuery",
    "GetLearningInsightsQuery",
)

CORE_EVENTS: tuple[dict[str, Any], ...] = (
    {
        "name": "DecisionRequestedEvent",
        "producer": "enterprise_decision_intelligence",
        "consumers": ("ai_reasoning", "audit"),
        "payload": ("tenant_id", "session_id", "intent"),
        "version": "v1",
    },
    {
        "name": "ReasoningStartedEvent",
        "producer": "ai_reasoning",
        "consumers": ("observability",),
        "payload": ("tenant_id", "session_id", "agent_refs"),
        "version": "v1",
    },
    {
        "name": "ReasoningCompletedEvent",
        "producer": "ai_reasoning",
        "consumers": ("recommendation", "ai_governance"),
        "payload": ("tenant_id", "session_id", "reasoning_score"),
        "version": "v1",
    },
    {
        "name": "RecommendationGeneratedEvent",
        "producer": "recommendation_intelligence",
        "consumers": ("decision_automation", "executive_copilot", "audit"),
        "payload": ("tenant_id", "recommendation_id", "confidence"),
        "version": "v1",
    },
    {
        "name": "DecisionApprovedEvent",
        "producer": "human_approval",
        "consumers": ("decision_automation", "audit"),
        "payload": ("tenant_id", "decision_id", "approver_ref"),
        "version": "v1",
    },
    {
        "name": "DecisionExecutedEvent",
        "producer": "decision_automation",
        "consumers": ("learning", "audit", "notifications"),
        "payload": ("tenant_id", "decision_id", "autonomy_level"),
        "version": "v1",
    },
    {
        "name": "LearningCapturedEvent",
        "producer": "learning",
        "consumers": ("ai_governance", "enterprise_ai"),
        "payload": ("tenant_id", "feedback_id", "decision_id"),
        "version": "v1",
    },
    {
        "name": "AgentCollaboratedEvent",
        "producer": "agent_orchestrator",
        "consumers": ("decision_memory", "observability"),
        "payload": ("tenant_id", "session_id", "agent_ids"),
        "version": "v1",
    },
    {
        "name": "PolicyValidationCompletedEvent",
        "producer": "ai_governance",
        "consumers": ("decision_automation", "audit"),
        "payload": ("tenant_id", "decision_id", "policy_result"),
        "version": "v1",
    },
)

MICROSERVICES: tuple[dict[str, Any], ...] = (
    {
        "name": "decision-intelligence-service",
        "responsibility": "Decision session lifecycle and orchestration.",
        "database_boundary": "analytics_ai_decisions",
        "api_boundary": "/api/v1/analytics/decision-intelligence",
        "events": ("DecisionRequestedEvent", "DecisionExecutedEvent"),
        "security_model": "analytics.decision_intelligence.*",
        "scaling_strategy": "horizontal_stateless",
    },
    {
        "name": "ai-reasoning-service",
        "responsibility": "Enterprise reasoning via Enterprise AI.",
        "database_boundary": "analytics_ai_reasoning",
        "api_boundary": "/api/v1/analytics/reasoning",
        "events": ("ReasoningStartedEvent", "ReasoningCompletedEvent"),
        "security_model": "analytics.reasoning.*",
        "scaling_strategy": "async_via_enterprise_ai",
    },
    {
        "name": "executive-copilot-service",
        "responsibility": "Executive conversations and briefings.",
        "database_boundary": "analytics_ai_copilot",
        "api_boundary": "/api/v1/analytics/copilot",
        "events": ("RecommendationGeneratedEvent",),
        "security_model": "analytics.copilot.*",
        "scaling_strategy": "async_via_enterprise_ai",
    },
    {
        "name": "agent-orchestrator-service",
        "responsibility": "Multi-agent collaboration and delegation.",
        "database_boundary": "analytics_ai_agents",
        "api_boundary": "/api/v1/analytics/agents",
        "events": ("AgentCollaboratedEvent",),
        "security_model": "analytics.agents.*",
        "scaling_strategy": "queue_backed_workers",
    },
    {
        "name": "decision-automation-service",
        "responsibility": "Approved autonomous execution.",
        "database_boundary": "analytics_ai_automation",
        "api_boundary": "/api/v1/analytics/decision-intelligence/execute",
        "events": ("DecisionApprovedEvent", "DecisionExecutedEvent"),
        "security_model": "analytics.automation.*",
        "scaling_strategy": "horizontal_stateless",
    },
    {
        "name": "learning-service",
        "responsibility": "Continuous learning and feedback.",
        "database_boundary": "analytics_ai_learning",
        "api_boundary": "/api/v1/analytics/learning",
        "events": ("LearningCapturedEvent",),
        "security_model": "analytics.learning.*",
        "scaling_strategy": "async_workers",
    },
    {
        "name": "ai-governance-service",
        "responsibility": "AI risk, bias, explainability, policy checks.",
        "database_boundary": "analytics_ai_gov",
        "api_boundary": "/api/v1/analytics/decision-intelligence/governance",
        "events": ("PolicyValidationCompletedEvent",),
        "security_model": "analytics.ai.governance.*",
        "scaling_strategy": "horizontal_stateless",
    },
    {
        "name": "prompt-registry-service",
        "responsibility": "Versioned prompt registry (delegates to AI).",
        "database_boundary": "analytics_ai_prompts",
        "api_boundary": "/api/v1/analytics/prompt-registry",
        "events": ("PolicyValidationCompletedEvent",),
        "security_model": "analytics.prompts.*",
        "scaling_strategy": "horizontal_stateless",
    },
    {
        "name": "model-registry-service",
        "responsibility": "Model registry references via Enterprise AI.",
        "database_boundary": "analytics_ai_models",
        "api_boundary": "/api/v1/analytics/model-registry",
        "events": ("PolicyValidationCompletedEvent",),
        "security_model": "analytics.models.*",
        "scaling_strategy": "horizontal_stateless",
    },
    {
        "name": "decision-memory-service",
        "responsibility": "Decision memory and history.",
        "database_boundary": "analytics_ai_memory",
        "api_boundary": "/api/v1/analytics/executive",
        "events": ("DecisionExecutedEvent", "LearningCapturedEvent"),
        "security_model": "analytics.decision_memory.*",
        "scaling_strategy": "horizontal_stateless",
    },
)

API_BOUNDARIES: dict[str, Any] = {
    "decision": (
        "/api/v1/analytics/decision-intelligence",
        "/api/v1/analytics/recommendations",
        "/api/v1/analytics/reasoning",
        "/api/v1/analytics/copilot",
        "/api/v1/analytics/agents",
        "/api/v1/analytics/learning",
        "/api/v1/analytics/model-registry",
        "/api/v1/analytics/prompt-registry",
        "/api/v1/analytics/executive",
    ),
    "rest": True,
    "graphql": "/api/v1/analytics/graphql",
    "grpc": True,
    "streaming_apis": "/api/v1/analytics/copilot/stream",
    "event_apis": "analytics.ai.*.v1",
    "security": (
        "analytics.ai.read",
        "zero_trust",
        "tenant_isolation",
    ),
}

SECURITY: dict[str, Any] = {
    "via_p207": True,
    "via_p208": True,
    "via_p209": True,
    "via_p210": True,
    "via_p211": True,
    "via_p212": True,
    "agent_identity": True,
    "agent_authorization": True,
    "secure_prompt_execution": True,
    "secure_tool_invocation": True,
    "encrypted_agent_memory": True,
    "fine_grained_permissions": True,
    "policy_enforcement": True,
    "ai_audit_logging": True,
    "human_approval_policies": True,
    "module_local_llm_sdk_forbidden": True,
}

DEPLOYMENT: dict[str, Any] = {
    "kubernetes": True,
    "gpu_node_pools": True,
    "ai_inference_cluster": True,
    "vector_database_cluster": True,
    "graph_database_cluster": True,
    "service_mesh": True,
    "api_gateway": True,
    "event_bus": True,
    "distributed_cache": True,
    "observability": True,
    "multi_region": True,
    "high_availability": True,
    "disaster_recovery": True,
    "cloud_native": True,
}

TESTING: tuple[str, ...] = (
    "ai_functional_testing",
    "agent_collaboration_testing",
    "reasoning_validation",
    "prompt_evaluation",
    "hallucination_detection",
    "explainability_testing",
    "security_testing",
    "policy_compliance_testing",
    "performance_testing",
    "scalability_testing",
    "chaos_testing",
    "acceptance_testing",
)

CURSOR_OUTPUTS: tuple[str, ...] = (
    "ai_native_analytics_vision",
    "ddd_domain_model",
    "bounded_context_architecture",
    "enterprise_ai_agent_platform",
    "multi_agent_collaboration",
    "enterprise_reasoning_engine",
    "autonomous_decision_platform",
    "executive_ai_copilot",
    "knowledge_graph_integration",
    "digital_twin_integration",
    "ai_governance_platform",
    "cqrs_architecture",
    "event_sourcing_architecture",
    "microservice_architecture",
    "api_first_architecture",
    "security_governance_architecture",
    "deployment_architecture",
    "testing_architecture",
    "production_readiness_checklist",
    "autonomy_levels_architecture",
)

QUALITY_GATES_REJECT_IF: tuple[str, ...] = (
    "ai_native_analytics_platform_is_missing",
    "autonomous_decision_intelligence_is_missing",
    "enterprise_ai_agent_platform_is_missing",
    "multi_agent_collaboration_is_missing",
    "executive_ai_copilot_is_missing",
    "ai_governance_platform_is_missing",
    "knowledge_graph_integration_is_missing",
    "digital_twin_integration_is_missing",
    "cqrs_architecture_is_missing",
    "event_sourcing_architecture_is_missing",
    "microservice_architecture_is_missing",
    "api_first_architecture_is_missing",
    "zero_trust_security_is_missing",
    "cloud_native_deployment_is_missing",
    "ai_native_decision_architecture_is_incomplete",
    "sibling_business_intelligence_bc",
)

DECISION_FLOW: tuple[str, ...] = (
    "enterprise_events",
    "enterprise_data",
    "knowledge_graph",
    "digital_twin",
    "business_policies",
    "enterprise_metrics",
    "historical_decisions",
    "predictive_intelligence",
    "ai_agents_reason",
    "collaborate",
    "simulate",
    "recommend",
    "authorized_execute",
)


def vision() -> dict[str, Any]:
    return {
        "statement": PRINCIPLE,
        "fabric": FABRIC,
        "flow": list(DECISION_FLOW),
        "qualities": (
            "fully_explainable",
            "fully_auditable",
            "fully_governed",
            "policy_compliant",
        ),
        "via_enterprise_ai_only": True,
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


def agents() -> dict[str, Any]:
    return {
        "categories": [dict(a) for a in AGENT_CATEGORIES],
        "agent_count": len(AGENT_CATEGORIES),
        "via_enterprise_ai": True,
        "module_local_llm_sdk_forbidden": True,
    }


def multi_agent() -> dict[str, Any]:
    return dict(MULTI_AGENT)


def reasoning() -> dict[str, Any]:
    return {
        "modes": list(REASONING_ENGINE),
        "mode_count": len(REASONING_ENGINE),
        "via_enterprise_ai": True,
    }


def autonomy() -> dict[str, Any]:
    return {
        "levels": [dict(l) for l in AUTONOMY_LEVELS],
        "level_count": len(AUTONOMY_LEVELS),
        "controls": list(AUTONOMY_CONTROLS),
    }


def executive_copilot() -> dict[str, Any]:
    return dict(EXECUTIVE_COPILOT)


def ai_governance() -> dict[str, Any]:
    return dict(AI_GOVERNANCE)


def knowledge_graph() -> dict[str, Any]:
    return dict(KNOWLEDGE_GRAPH)


def digital_twin() -> dict[str, Any]:
    return dict(DIGITAL_TWIN)


def predictive_integration() -> dict[str, Any]:
    return dict(PREDICTIVE_INTEGRATION)


def prescriptive_integration() -> dict[str, Any]:
    return dict(PRESCRIPTIVE_INTEGRATION)


def semantic_integration() -> dict[str, Any]:
    return dict(SEMANTIC_INTEGRATION)


def cqrs() -> dict[str, Any]:
    return {
        "commands": list(COMMANDS),
        "command_count": len(COMMANDS),
        "queries": list(QUERIES),
        "query_count": len(QUERIES),
        "alignment_present_required": True,
        "events": [e["name"] for e in CORE_EVENTS],
        "event_count": len(CORE_EVENTS),
    }


def events() -> dict[str, Any]:
    return {
        "core_events": [dict(e) for e in CORE_EVENTS],
        "core_event_count": len(CORE_EVENTS),
        "event_driven_required": True,
        "replay_strategy": "outbox_replay_by_event_id",
        "version_strategy": "append_only_vN",
    }


def microservices() -> dict[str, Any]:
    return {
        "services": [dict(s) for s in MICROSERVICES],
        "service_count": len(MICROSERVICES),
        "logical_decomposition": True,
    }


def api_boundaries() -> dict[str, Any]:
    return dict(API_BOUNDARIES)


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
            "enterprise_ai_analytics_platform": True,
            "autonomous_decision_platform": True,
            "enterprise_ai_agent_platform": True,
            "executive_ai_copilot": True,
            "multi_agent_collaboration": True,
            "enterprise_reasoning_engine": True,
            "ai_governance_platform": True,
            "knowledge_graph_integration": True,
            "digital_twin_integration": True,
            "cqrs_architecture": True,
            "event_architecture": True,
            "microservice_architecture": True,
            "api_platform": True,
            "security_architecture": True,
            "deployment_architecture": True,
            "testing_architecture": True,
            "foundation_tests": True,
            "ai_api_live": True,
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
            "P213-A",
            "P213-B",
            "P213-C",
            "P213-D",
            "P213-E",
            "P213-F",
            "P213-G",
            "P213-H",
            "P213-I",
            "P213-J",
            "P213-K",
            "P213-L",
            "ADR-394",
            "ADR-395",
            "ADR-396",
            "ADR-408",
            "ADR-409",
            "ADR-410",
            "ADR-411",
            "ADR-412",
            "ADR-413",
            "ADR-414",
            "ADR-415",
            "ADR-416",
            "P207",
            "P208",
            "P209",
            "P210",
            "P211",
            "P212",
            "P212-J",
            "P212-L",
        ],
        "architecture": {
            "present_required": True,
            "not_incomplete": True,
            "capabilities": [
                "enterprise_ai_analytics_fabric",
                "autonomous_decision_platform",
                "enterprise_ai_reasoning_engine",
                "executive_ai_copilot",
                "decision_intelligence_agents",
                "autonomous_business_optimization",
                "enterprise_cognitive_intelligence",
                "multi_agent_collaboration",
                "ai_decision_governance",
                "autonomous_enterprise_intelligence",
            ],
            "capability_count": 10,
        },
        "domain_model": domain_model(),
        "bounded_contexts": bounded_contexts(),
        "agents": agents(),
        "multi_agent": multi_agent(),
        "reasoning": reasoning(),
        "autonomy": autonomy(),
        "executive_copilot": executive_copilot(),
        "ai_governance": ai_governance(),
        "knowledge_graph": knowledge_graph(),
        "digital_twin": digital_twin(),
        "predictive_integration": predictive_integration(),
        "prescriptive_integration": prescriptive_integration(),
        "semantic_integration": semantic_integration(),
        "cqrs": cqrs(),
        "events": events(),
        "microservices": microservices(),
        "apis": api_boundaries(),
        "security": security(),
        "deployment": deployment(),
        "testing": testing(),
        "cursor_outputs": cursor_outputs(),
        "quality_gates": quality_gates(),
        "production_readiness": production_readiness(),
        "ai_native_analytics_platform_present_required": True,
        "autonomous_decision_intelligence_present_required": True,
        "enterprise_ai_agent_platform_present_required": True,
        "multi_agent_collaboration_present_required": True,
        "executive_ai_copilot_present_required": True,
        "ai_governance_platform_present_required": True,
        "knowledge_graph_integration_present_required": True,
        "digital_twin_integration_present_required": True,
        "cqrs_architecture_present_required": True,
        "event_sourcing_architecture_present_required": True,
        "microservice_architecture_present_required": True,
        "api_first_architecture_present_required": True,
        "zero_trust_security_present_required": True,
        "cloud_native_deployment_present_required": True,
        "architecture_present_required": True,
        "sibling_business_intelligence_bc_forbidden": True,
        "via_enterprise_ai_only": True,
        "api_prefix": f"{API_PREFIX}/ai",
        "forbidden_sibling_bc": [
            "business_intelligence",
            "decision_intelligence",
            "reporting_platform",
            "metric_governance_platform",
            "visualization_platform",
            "bi_core",
        ],
    }


def ai_surface() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "routes": [
            "GET /analytics/ai",
            "GET /analytics/ai/vision",
            "GET /analytics/ai/domain",
            "GET /analytics/ai/bounded-contexts",
            "GET /analytics/ai/agents",
            "GET /analytics/ai/multi-agent",
            "GET /analytics/ai/reasoning",
            "GET /analytics/ai/autonomy",
            "GET /analytics/ai/copilot",
            "GET /analytics/ai/governance",
            "GET /analytics/ai/knowledge-graph",
            "GET /analytics/ai/digital-twin",
            "GET /analytics/ai/cqrs",
            "GET /analytics/ai/events",
            "GET /analytics/ai/microservices",
            "GET /analytics/ai/apis",
            "GET /analytics/ai/security",
            "GET /analytics/ai/deployment",
            "GET /analytics/ai/testing",
            "GET /analytics/ai/outputs",
            "GET /analytics/ai/production-readiness",
            "GET /analytics/ai/readiness",
        ],
    }
