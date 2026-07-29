"""P214-Q Enterprise Autonomous AI Ecosystem / Digital Workforce — immutable catalog."""
from __future__ import annotations

from typing import Any

PROMPT_ID = "P214-Q"
ADR = 437
SOR = "ai"
API_PREFIX = "/api/v1/ai"
PRODUCT = (
    "Enterprise Autonomous AI Ecosystem, AI Digital Workforce & "
    "Self-Improving Intelligence Platform"
)
CAPABILITY = "CAP-PLT-AI-001"

PRINCIPLE = (
    "Enterprise Autonomous AI Ecosystem SHALL transform MEOS from an "
    "AI-enabled platform into a self-improving intelligent enterprise "
    "operating system."
)

FABRIC = "meos_autonomous_intelligence_ecosystem"

CORE_DOMAIN = "enterprise_autonomous_intelligence_management"

SUPPORTING_DOMAINS: tuple[dict[str, str], ...] = (
    {"id": "ai_digital_workforce", "purpose": "Digital employees, roles, responsibilities."},
    {"id": "autonomous_agent", "purpose": "Agent lifecycle, coordination, collaboration."},
    {"id": "ai_organization", "purpose": "AI departments, teams, authority models."},
    {"id": "cognitive_workflow", "purpose": "Autonomous business execution and exception handling."},
    {"id": "ai_collaboration", "purpose": "Human and agent collaboration workflows."},
    {"id": "self_learning", "purpose": "Learning loops, capability enhancement, feedback."},
    {"id": "ai_decision_autonomy", "purpose": "Decision confidence, escalation, execution."},
    {"id": "ai_evolution", "purpose": "Improvement plans, evolution scoring, optimization."},
    {"id": "human_ai_interaction", "purpose": "Oversight, approvals, collaboration boundaries."},
)

AGGREGATE = {
    "name": "EnterpriseAutonomousIntelligenceAggregate",
    "root": "EnterpriseAutonomousIntelligence",
    "entities": (
        "AIDigitalEmployee",
        "AutonomousAgent",
        "AgentTeam",
        "AIOrganizationUnit",
        "CognitiveWorkflow",
        "AutonomousDecision",
        "LearningCycle",
        "AgentMemory",
        "AgentCapability",
        "AIImprovementPlan",
    ),
    "value_objects": (
        "AgentIdentifier",
        "CapabilityScore",
        "AutonomyLevel",
        "TrustLevel",
        "DecisionConfidence",
        "LearningScore",
        "PerformanceScore",
        "HumanApprovalLevel",
    ),
    "events": (
        "AIAgentCreatedEvent",
        "DigitalEmployeeActivatedEvent",
        "AgentCollaborationStartedEvent",
        "AutonomousDecisionExecutedEvent",
        "LearningCycleCompletedEvent",
        "CapabilityImprovedEvent",
        "AutonomyLevelChangedEvent",
        "AIImprovementPlanCreatedEvent",
    ),
}

LOGICAL_BOUNDED_CONTEXTS: tuple[dict[str, Any], ...] = (
    {
        "id": "ai_digital_workforce",
        "bc": "BC-01",
        "name": "AI Digital Workforce Context",
        "purpose": "Digital employees, AI roles, responsibilities, workforce management.",
    },
    {
        "id": "autonomous_agent_ecosystem",
        "bc": "BC-02",
        "name": "Autonomous Agent Ecosystem Context",
        "purpose": "Agent lifecycle, coordination, collaboration, delegation.",
    },
    {
        "id": "ai_organization",
        "bc": "BC-03",
        "name": "AI Organization Context",
        "purpose": "AI departments, teams, structures, authority models.",
    },
    {
        "id": "cognitive_workflow",
        "bc": "BC-04",
        "name": "Cognitive Workflow Context",
        "purpose": "Autonomous processes, business execution, workflow intelligence.",
    },
    {
        "id": "self_learning_intelligence",
        "bc": "BC-05",
        "name": "Self-Learning Intelligence Context",
        "purpose": "Learning loops, improvement cycles, capability evolution.",
    },
    {
        "id": "ai_decision_autonomy",
        "bc": "BC-06",
        "name": "AI Decision Autonomy Context",
        "purpose": "Autonomous decisions, confidence scoring, human escalation.",
    },
    {
        "id": "human_ai_collaboration",
        "bc": "BC-07",
        "name": "Human AI Collaboration Context",
        "purpose": "Human oversight, collaboration workflows, approval management.",
    },
)

DIGITAL_WORKFORCE = {
    "present_required": True,
    "operating_model": "meos_ai_workforce_operating_model",
    "roles": (
        "ai_employees",
        "ai_managers",
        "ai_specialists",
        "ai_analysts",
        "ai_operators",
        "ai_advisors",
    ),
    "defines": (
        "ai_role",
        "ai_responsibility",
        "ai_capability",
        "ai_authority",
        "ai_governance_boundary",
    ),
}

AGENT_ECOSYSTEM = {
    "present_required": True,
    "via_p214_f": True,
    "platform": "enterprise_multi_agent_intelligence_platform",
    "supports": (
        "agent_discovery",
        "agent_registration",
        "agent_communication",
        "agent_collaboration",
        "agent_negotiation",
        "agent_delegation",
        "agent_coordination",
    ),
}

AI_ORGANIZATION = {
    "present_required": True,
    "model": "enterprise_ai_organization_model",
    "departments": (
        "ai_finance_team",
        "ai_security_team",
        "ai_operations_team",
        "ai_research_team",
        "ai_customer_intelligence_team",
        "ai_data_team",
        "ai_governance_team",
    ),
    "defines": (
        "organizational_structure",
        "responsibilities",
        "authority_model",
        "communication_model",
    ),
}

COGNITIVE_WORKFLOW = {
    "present_required": True,
    "via_workflow_engine": True,
    "engine": "autonomous_business_process_intelligence_engine",
    "supports": (
        "process_discovery",
        "process_automation",
        "decision_automation",
        "task_delegation",
        "exception_handling",
        "continuous_improvement",
    ),
}

SELF_LEARNING = {
    "present_required": True,
    "via_p214_o": True,
    "via_p214_l": True,
    "engine": "enterprise_continuous_learning_engine",
    "supports": (
        "learning_loops",
        "feedback_collection",
        "performance_analysis",
        "knowledge_improvement",
        "capability_enhancement",
    ),
    "score": "ai_evolution_score",
}

DECISION_AUTONOMY = {
    "present_required": True,
    "via_p214_p": True,
    "framework": "enterprise_ai_decision_autonomy_framework",
    "manages": (
        "decision_context",
        "decision_reasoning",
        "decision_confidence",
        "decision_approval",
        "decision_execution",
        "decision_review",
    ),
    "supports": (
        "human_in_the_loop",
        "human_on_the_loop",
        "autonomous_execution",
    ),
}

MEMORY_PLATFORM = {
    "present_required": True,
    "via_p214_g": True,
    "system": "enterprise_ai_long_term_memory_system",
    "manages": (
        "agent_memory",
        "enterprise_knowledge",
        "past_decisions",
        "experiences",
        "lessons_learned",
    ),
}

EVOLUTION_MANAGEMENT = {
    "present_required": True,
    "via_p214_j": True,
    "engine": "self_improving_ai_intelligence_engine",
    "monitors": (
        "capability_growth",
        "learning_progress",
        "performance_improvement",
        "knowledge_expansion",
        "autonomy_development",
    ),
    "enables": (
        "ai_evolution_planning",
        "capability_upgrades",
        "autonomous_optimization",
    ),
}

AUTONOMOUS_KNOWLEDGE_GRAPH = {
    "present_required": True,
    "via_p214_g": True,
    "represents": (
        "agents",
        "digital_employees",
        "capabilities",
        "tasks",
        "decisions",
        "knowledge",
        "experiences",
        "dependencies",
    ),
    "enables": (
        "agent_discovery",
        "collaboration_optimization",
        "capability_matching",
        "intelligence_evolution",
    ),
}

AUTONOMOUS_DIGITAL_TWIN = {
    "present_required": True,
    "represents": (
        "ai_employees",
        "agent_state",
        "capability_state",
        "learning_state",
        "decision_state",
        "performance_state",
    ),
    "enables": (
        "simulation",
        "workforce_planning",
        "optimization",
        "autonomy_forecasting",
    ),
}

COMMANDS: tuple[str, ...] = (
    "CreateDigitalEmployeeCommand",
    "ActivateAgentCommand",
    "CreateAgentTeamCommand",
    "ExecuteAutonomousDecisionCommand",
    "StartLearningCycleCommand",
    "ImproveCapabilityCommand",
)

QUERIES: tuple[str, ...] = (
    "GetAgentStatusQuery",
    "GetDigitalWorkforceQuery",
    "GetDecisionHistoryQuery",
    "GetLearningProgressQuery",
    "GetCapabilityScoreQuery",
)

CORE_EVENTS: tuple[dict[str, str], ...] = (
    {"name": "AgentCreatedEvent", "owner": "ai", "consumers": "audit,analytics,agents"},
    {"name": "EmployeeActivatedEvent", "owner": "ai", "consumers": "audit,identity"},
    {"name": "TaskAssignedEvent", "owner": "ai", "consumers": "workflow,analytics"},
    {"name": "DecisionExecutedEvent", "owner": "ai", "consumers": "audit,governance"},
    {"name": "LearningCompletedEvent", "owner": "ai", "consumers": "aiqa,modelintel"},
    {"name": "CapabilityImprovedEvent", "owner": "ai", "consumers": "analytics,aiops"},
    {"name": "AutonomyChangedEvent", "owner": "ai", "consumers": "governance,aisec"},
    {"name": "HumanApprovalRequestedEvent", "owner": "ai", "consumers": "workflow,notifications,audit"},
)

MICROSERVICES: tuple[dict[str, Any], ...] = (
    {
        "id": "digital_workforce_service",
        "responsibility": "digital employee registry, role design, authority boundaries",
        "api": "/ai/aiworkforce/workforce",
        "db": "ai_*",
        "events": ("EmployeeActivatedEvent",),
        "security": ("ai.assist.read",),
        "scaling": "control_plane_replicas",
    },
    {
        "id": "agent_management_service",
        "responsibility": "agent lifecycle and activation for workforce execution",
        "api": "/ai/aiworkforce/ecosystem",
        "db": "ai_*",
        "events": ("AgentCreatedEvent",),
        "security": ("ai.assist.infer",),
        "scaling": "stateless_replicas",
    },
    {
        "id": "agent_collaboration_service",
        "responsibility": "agent communication, negotiation, and delegation",
        "api": "/ai/aiworkforce/collaboration",
        "db": "ai_*",
        "events": ("TaskAssignedEvent",),
        "security": ("ai.assist.infer",),
        "scaling": "message_driven",
    },
    {
        "id": "ai_organization_service",
        "responsibility": "AI departments, teams, reporting lines, authority model",
        "api": "/ai/aiworkforce/organization",
        "db": "ai_*",
        "events": ("EmployeeActivatedEvent",),
        "security": ("ai.assist.read",),
        "scaling": "control_plane",
    },
    {
        "id": "workflow_intelligence_service",
        "responsibility": "cognitive workflow automation and exception handling",
        "api": "/ai/aiworkforce/workflows",
        "db": "ai_*",
        "events": ("TaskAssignedEvent", "HumanApprovalRequestedEvent"),
        "security": ("ai.assist.infer",),
        "scaling": "orchestrator_replicas",
    },
    {
        "id": "decision_autonomy_service",
        "responsibility": "decision reasoning, confidence, approvals, execution",
        "api": "/ai/aiworkforce/decisions",
        "db": "ai_*",
        "events": ("DecisionExecutedEvent",),
        "security": ("ai.assist.infer",),
        "scaling": "async_workers",
    },
    {
        "id": "learning_service",
        "responsibility": "continuous learning loops and feedback processing",
        "api": "/ai/aiworkforce/learning",
        "db": "ai_*",
        "events": ("LearningCompletedEvent",),
        "security": ("ai.assist.infer",),
        "scaling": "analytics_pipeline",
    },
    {
        "id": "memory_service",
        "responsibility": "memory retrieval, experience retention, lessons learned",
        "api": "/ai/aiworkforce/memory",
        "db": "ai_*",
        "events": ("LearningCompletedEvent",),
        "security": ("ai.assist.read",),
        "scaling": "memory_shards",
    },
    {
        "id": "evolution_service",
        "responsibility": "capability upgrades, optimization plans, evolution scoring",
        "api": "/ai/aiworkforce/evolution",
        "db": "ai_*",
        "events": ("CapabilityImprovedEvent", "AutonomyChangedEvent"),
        "security": ("ai.assist.infer",),
        "scaling": "worker_pools",
    },
    {
        "id": "human_collaboration_service",
        "responsibility": "human oversight, approval management, escalation workflows",
        "api": "/ai/aiworkforce/human-collaboration",
        "db": "ai_*",
        "events": ("HumanApprovalRequestedEvent",),
        "security": ("ai.assist.read",),
        "scaling": "control_plane",
    },
)

API_SURFACES: tuple[str, ...] = (
    "/api/v1/ai/aiworkforce/workforce",
    "/api/v1/ai/aiworkforce/ecosystem",
    "/api/v1/ai/aiworkforce/organization",
    "/api/v1/ai/aiworkforce/workflows",
    "/api/v1/ai/aiworkforce/learning",
    "/api/v1/ai/aiworkforce/decisions",
    "/api/v1/ai/aiworkforce/memory",
    "/api/v1/ai/aiworkforce/evolution",
)

API_STYLES: tuple[str, ...] = ("REST", "GraphQL", "gRPC", "Streaming", "Event")

SECURITY = {
    "present_required": True,
    "zero_trust": True,
    "integrates": ("P207", "P208", "P209", "P210", "P214-I", "P214-P"),
    "controls": (
        "autonomy_policy_enforcement",
        "human_approval_gates",
        "decision_authorization",
        "memory_protection",
        "workforce_identity_boundaries",
    ),
}

DEPLOYMENT = {
    "present_required": True,
    "cloud_native": True,
    "via_p214_n": True,
    "components": (
        "kubernetes",
        "agent_runtime_cluster",
        "ai_memory_infrastructure",
        "workflow_engine",
        "knowledge_graph_platform",
        "digital_twin_platform",
        "observability_platform",
        "governance_layer",
    ),
}

TESTING: tuple[str, ...] = (
    "agent_testing",
    "autonomy_testing",
    "decision_testing",
    "learning_testing",
    "collaboration_testing",
    "safety_testing",
    "governance_testing",
    "performance_testing",
    "evolution_testing",
)

CURSOR_OUTPUTS: tuple[str, ...] = (
    "enterprise_autonomous_ai_vision",
    "ddd_domain_model",
    "bounded_context_map",
    "ai_digital_workforce",
    "autonomous_agent_ecosystem",
    "ai_organization_model",
    "cognitive_workflow_automation",
    "self_learning_engine",
    "decision_autonomy_framework",
    "ai_memory_platform",
    "ai_evolution_management",
    "autonomous_knowledge_graph",
    "autonomous_digital_twin",
    "cqrs_commands_queries",
    "event_sourcing_schema",
    "microservice_boundaries",
    "integration_architecture",
    "cloud_native_deployment",
    "testing_architecture",
    "quality_gates_dod",
    "adr_437",
    "enterprise_ai_aiworkforce_law",
)

QUALITY_GATES_REJECT_IF: tuple[str, ...] = (
    "enterprise_autonomous_ai_ecosystem_is_missing",
    "ai_digital_workforce_is_missing",
    "multi_agent_platform_is_missing",
    "ai_organization_model_is_missing",
    "autonomous_workflow_platform_is_missing",
    "self_learning_intelligence_is_missing",
    "autonomous_decision_framework_is_missing",
    "ai_memory_platform_is_missing",
    "ai_evolution_management_is_missing",
    "knowledge_graph_integration_is_missing",
    "digital_twin_integration_is_missing",
    "cqrs_architecture_is_missing",
    "event_architecture_is_missing",
    "microservices_architecture_is_missing",
    "api_first_architecture_is_missing",
    "zero_trust_ai_security_is_missing",
    "cloud_native_deployment_is_missing",
    "sibling_ai_bc",
)


def vision() -> dict[str, Any]:
    return {
        "role": "MEOS Autonomous Intelligence Ecosystem",
        "principle": PRINCIPLE,
        "equation": (
            "AI Agents + Knowledge Systems + Enterprise Data + AI Models + "
            "Business Processes + Human Expertise → Digital Workforce → "
            "Autonomous Collaboration → Intelligent Execution → Continuous "
            "Learning → Enterprise Self Improvement"
        ),
        "pillars": (
            "digital_ai_workforce_required",
            "assistants_vs_autonomous_agents",
            "ai_organizations_required",
            "self_improving_intelligence_required",
            "autonomous_systems_require_governance",
            "human_ai_collaboration_is_essential",
        ),
        "strategic_role": {
            "digital_workforce": (
                "Enterprises need AI employees and specialist agents that operate "
                "with explicit roles, authority boundaries, and measurable outcomes."
            ),
            "assistants_vs_agents": (
                "Assistants advise humans; autonomous agents plan, coordinate, "
                "and execute approved work as digital employees."
            ),
            "ai_organizations": (
                "As agent populations scale, enterprises need AI teams, reporting "
                "lines, and collaboration models to avoid ad hoc sprawl."
            ),
            "self_improving": (
                "Learning loops and experience memory convert each execution into "
                "better future performance."
            ),
            "governance": (
                "Autonomy without policy, trust, and oversight becomes an enterprise "
                "risk, so P214-P remains the governing control plane."
            ),
            "human_ai_collaboration": (
                "Human-in-the-loop and human-on-the-loop remain essential for "
                "approval, escalation, and accountability."
            ),
        },
        "deepens_p214_f": (
            "P214-F owns autonomous agent foundations; P214-Q organizes agents "
            "into digital workforce, AI organizations, self-learning loops, and "
            "enterprise execution models."
        ),
        "governed_by_p214_p": True,
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


def digital_workforce() -> dict[str, Any]:
    return dict(DIGITAL_WORKFORCE)


def ecosystem() -> dict[str, Any]:
    return dict(AGENT_ECOSYSTEM)


def organization() -> dict[str, Any]:
    return dict(AI_ORGANIZATION)


def workflows() -> dict[str, Any]:
    return dict(COGNITIVE_WORKFLOW)


def learning() -> dict[str, Any]:
    return dict(SELF_LEARNING)


def decision_autonomy() -> dict[str, Any]:
    return dict(DECISION_AUTONOMY)


def memory() -> dict[str, Any]:
    return dict(MEMORY_PLATFORM)


def evolution() -> dict[str, Any]:
    return dict(EVOLUTION_MANAGEMENT)


def knowledge_graph() -> dict[str, Any]:
    return dict(AUTONOMOUS_KNOWLEDGE_GRAPH)


def digital_twin() -> dict[str, Any]:
    return dict(AUTONOMOUS_DIGITAL_TWIN)


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


def integrations() -> dict[str, Any]:
    return {
        "peers": (
            "P214-F",
            "P214-G",
            "P214-J",
            "P214-L",
            "P214-M",
            "P214-N",
            "P214-O",
            "P214-P",
            "workflow",
            "audit",
            "policy_engine",
        ),
        "via_events_and_acl": True,
        "autonomy_policies": True,
        "trust_boundaries": True,
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
            "enterprise_autonomous_ai_ecosystem": True,
            "ai_digital_workforce": True,
            "autonomous_agent_ecosystem": True,
            "ai_organization_model": True,
            "cognitive_workflow_platform": True,
            "self_learning_engine": True,
            "autonomous_decision_platform": True,
            "ai_memory_platform": True,
            "ai_evolution_platform": True,
            "knowledge_graph": True,
            "digital_twin": True,
            "cqrs_architecture": True,
            "event_architecture": True,
            "microservice_architecture": True,
            "api_platform": True,
            "security_architecture": True,
            "governance_architecture": True,
            "deployment_architecture": True,
            "testing_architecture": True,
            "foundation_tests": True,
            "aiworkforce_api_live": True,
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
            "P214-G",
            "P214-H",
            "P214-I",
            "P214-J",
            "P214-K",
            "P214-L",
            "P214-M",
            "P214-N",
            "P214-O",
            "P214-P",
            "ADR-421",
            "ADR-426",
            "ADR-436",
            "P207",
            "P208",
            "P209",
            "P210",
            "P211",
            "P212",
            "P213",
            "AI_PLATFORM_STANDARD",
            "ENTERPRISE_POLICY_ENGINE",
            "ENTERPRISE_AUDIT_PLATFORM",
            "ENTERPRISE_WORKFLOW_ENGINE",
        ],
        "vision": vision(),
        "domain_model": domain_model(),
        "bounded_contexts": bounded_contexts(),
        "digital_workforce": digital_workforce(),
        "ecosystem": ecosystem(),
        "organization": organization(),
        "workflows": workflows(),
        "learning": learning(),
        "decision_autonomy": decision_autonomy(),
        "memory": memory(),
        "evolution": evolution(),
        "knowledge_graph": knowledge_graph(),
        "digital_twin": digital_twin(),
        "cqrs": cqrs(),
        "events": events(),
        "microservices": microservices(),
        "api": api(),
        "integrations": integrations(),
        "security": security(),
        "deployment": deployment(),
        "testing": testing(),
        "cursor_outputs": cursor_outputs(),
        "quality_gates": quality_gates(),
        "production_readiness": production_readiness(),
        "enterprise_autonomous_ai_ecosystem_present_required": True,
        "ai_digital_workforce_present_required": True,
        "multi_agent_platform_present_required": True,
        "ai_organization_model_present_required": True,
        "autonomous_workflow_platform_present_required": True,
        "self_learning_intelligence_present_required": True,
        "autonomous_decision_framework_present_required": True,
        "ai_memory_platform_present_required": True,
        "ai_evolution_management_present_required": True,
        "knowledge_graph_integration_present_required": True,
        "digital_twin_integration_present_required": True,
        "cqrs_architecture_present_required": True,
        "event_architecture_present_required": True,
        "microservices_architecture_present_required": True,
        "api_first_architecture_present_required": True,
        "zero_trust_ai_security_present_required": True,
        "cloud_native_deployment_present_required": True,
        "sibling_ai_bc_forbidden": True,
        "module_local_ai_workforce_forbidden": True,
        "deepens_p214_f_digital_workforce": True,
        "governed_by_p214_p": True,
        "via_enterprise_ai": True,
        "via_api_gateway": True,
        "api_prefix": f"{API_PREFIX}/aiworkforce",
        "forbidden_sibling_bc": [
            "autonomous_ai_ecosystem",
            "ai_digital_workforce",
            "digital_workforce_platform",
            "autonomous_agent_ecosystem",
            "ai_organization_platform",
            "self_improving_intelligence",
            "generative_ai",
            "llm_platform",
            "ai_core",
            "vector_intelligence",
            "ml_platform",
        ],
    }


def aiworkforce_surface() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "routes": [
            "GET /ai/aiworkforce",
            "GET /ai/aiworkforce/vision",
            "GET /ai/aiworkforce/domain",
            "GET /ai/aiworkforce/bounded-contexts",
            "GET /ai/aiworkforce/workforce",
            "GET /ai/aiworkforce/ecosystem",
            "GET /ai/aiworkforce/organization",
            "GET /ai/aiworkforce/workflows",
            "GET /ai/aiworkforce/learning",
            "GET /ai/aiworkforce/decisions",
            "GET /ai/aiworkforce/memory",
            "GET /ai/aiworkforce/evolution",
            "GET /ai/aiworkforce/knowledge-graph",
            "GET /ai/aiworkforce/digital-twin",
            "GET /ai/aiworkforce/cqrs",
            "GET /ai/aiworkforce/events",
            "GET /ai/aiworkforce/microservices",
            "GET /ai/aiworkforce/integrations",
            "GET /ai/aiworkforce/api",
            "GET /ai/aiworkforce/security",
            "GET /ai/aiworkforce/deployment",
            "GET /ai/aiworkforce/testing",
            "GET /ai/aiworkforce/outputs",
            "GET /ai/aiworkforce/production-readiness",
            "GET /ai/aiworkforce/readiness",
        ],
    }
