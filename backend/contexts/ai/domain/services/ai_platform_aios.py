"""P214-T Enterprise AI Operating System / Control Plane — immutable catalog."""
from __future__ import annotations

from typing import Any

PROMPT_ID = "P214-T"
ADR = 440
SOR = "ai"
API_PREFIX = "/api/v1/ai"
PRODUCT = (
    "Enterprise AI Operating System, AI Control Plane & Autonomous "
    "Intelligence Governance Layer"
)
CAPABILITY = "CAP-PLT-AI-001"

PRINCIPLE = (
    "Enterprise AI Operating System SHALL become the intelligent control plane "
    "that manages, coordinates, governs and evolves all AI capabilities across MEOS."
)

FABRIC = "meos_ai_operating_system_layer"

CORE_DOMAIN = "enterprise_ai_operating_system_management"

SUPPORTING_DOMAINS: tuple[dict[str, str], ...] = (
    {"id": "ai_control_plane", "purpose": "AI ecosystem management and coordination."},
    {"id": "ai_orchestration", "purpose": "Workflow execution and autonomous coordination."},
    {"id": "ai_capability_management", "purpose": "Capability registry, state, lifecycle metadata."},
    {"id": "ai_governance_operations", "purpose": "Policy enforcement and trust operations."},
    {"id": "ai_decision_control", "purpose": "Decision routing, approval, and escalation."},
    {"id": "ai_lifecycle_management", "purpose": "Capability lifecycle from creation to retirement."},
    {"id": "ai_resource_coordination", "purpose": "Resource prioritization and allocation orchestration."},
    {"id": "ai_intelligence_monitoring", "purpose": "Health, performance, intelligence metrics."},
    {"id": "ai_evolution_management", "purpose": "Continuous improvement and future adaptation."},
)

AGGREGATE = {
    "name": "EnterpriseAIOperatingSystemAggregate",
    "root": "EnterpriseAIOperatingSystem",
    "entities": (
        "AIControlPlane",
        "AIServiceRegistry",
        "AICapabilityRegistry",
        "AIOrchestrator",
        "AIPolicyController",
        "AIDecisionController",
        "AIWorkflowManager",
        "AIIntelligenceRuntime",
        "AICommandCenter",
        "AIEvolutionManager",
    ),
    "value_objects": (
        "AIControlIdentifier",
        "CapabilityState",
        "AutonomyLevel",
        "GovernanceState",
        "ExecutionPriority",
        "TrustLevel",
        "IntelligenceScore",
    ),
    "events": (
        "AIControlPlaneCreatedEvent",
        "AICapabilityRegisteredEvent",
        "AIWorkflowExecutedEvent",
        "AIPolicyAppliedEvent",
        "AIDecisionApprovedEvent",
        "AIStateChangedEvent",
        "AIEvolutionTriggeredEvent",
        "AIOptimizationTriggeredEvent",
    ),
}

LOGICAL_BOUNDED_CONTEXTS: tuple[dict[str, Any], ...] = (
    {"id": "ai_control_plane", "bc": "BC-01", "name": "AI Control Plane Context", "purpose": "AI ecosystem management, capability coordination, system control."},
    {"id": "ai_orchestration", "bc": "BC-02", "name": "AI Orchestration Context", "purpose": "Workflow execution, agent coordination, process orchestration."},
    {"id": "ai_governance_operations", "bc": "BC-03", "name": "AI Governance Operations Context", "purpose": "Policy enforcement, compliance operations, trust management."},
    {"id": "ai_lifecycle_management", "bc": "BC-04", "name": "AI Lifecycle Management Context", "purpose": "Capability lifecycle, model lifecycle, agent lifecycle."},
    {"id": "ai_decision_control", "bc": "BC-05", "name": "AI Decision Control Context", "purpose": "Decision approval, routing, and governance."},
    {"id": "ai_intelligence_monitoring", "bc": "BC-06", "name": "AI Intelligence Monitoring Context", "purpose": "Intelligence metrics, AI health, AI performance."},
    {"id": "ai_evolution_management", "bc": "BC-07", "name": "AI Evolution Management Context", "purpose": "Continuous improvement, capability evolution, future adaptation."},
)

CONTROL_PLANE = {
    "present_required": True,
    "layer": "enterprise_ai_command_and_control_layer",
    "manages": (
        "ai_assets",
        "ai_agents",
        "ai_models",
        "ai_services",
        "ai_workflows",
        "ai_policies",
        "ai_infrastructure",
        "ai_knowledge",
    ),
    "capabilities": (
        "discovery",
        "registration",
        "control",
        "coordination",
        "governance",
        "optimization",
    ),
}

ORCHESTRATION = {
    "present_required": True,
    "via_p214_q": True,
    "engine": "enterprise_autonomous_ai_orchestrator",
    "supports": (
        "multi_agent_coordination",
        "ai_workflow_execution",
        "business_process_intelligence",
        "task_distribution",
        "decision_routing",
        "exception_management",
    ),
}

CAPABILITY_MANAGEMENT = {
    "present_required": True,
    "registry": "enterprise_ai_capability_operating_registry",
    "manages": (
        "ai_capabilities",
        "ai_services",
        "ai_models",
        "ai_agents",
        "ai_products",
        "ai_skills",
    ),
    "tracks": (
        "version",
        "performance",
        "trust",
        "usage",
        "lifecycle",
    ),
}

COMMAND_CENTER = {
    "present_required": True,
    "platform": "meos_enterprise_ai_command_center",
    "provides": (
        "ai_ecosystem_visibility",
        "operational_intelligence",
        "governance_monitoring",
        "risk_monitoring",
        "performance_analytics",
        "strategic_intelligence",
    ),
}

POLICY_CONTROL = {
    "present_required": True,
    "via_p214_p": True,
    "engine": "enterprise_ai_policy_enforcement_layer",
    "manages": (
        "security_policies",
        "governance_policies",
        "operational_policies",
        "autonomy_policies",
        "compliance_policies",
    ),
}

DECISION_CONTROL = {
    "present_required": True,
    "system": "enterprise_ai_decision_governance_system",
    "manages": (
        "decision_context",
        "decision_confidence",
        "decision_authority",
        "approval_workflow",
        "decision_history",
    ),
    "supports": (
        "human_approval",
        "autonomous_approval",
        "escalation_management",
    ),
}

LIFECYCLE = {
    "present_required": True,
    "engine": "enterprise_ai_capability_lifecycle_engine",
    "manages": (
        "creation",
        "training",
        "deployment",
        "operation",
        "monitoring",
        "improvement",
        "retirement",
    ),
}

OS_KNOWLEDGE_GRAPH = {
    "present_required": True,
    "via_p214_g": True,
    "represents": (
        "ai_systems",
        "capabilities",
        "agents",
        "models",
        "policies",
        "decisions",
        "dependencies",
        "operations",
    ),
    "enables": (
        "global_ai_understanding",
        "impact_analysis",
        "optimization",
        "autonomous_management",
    ),
}

OS_DIGITAL_TWIN = {
    "present_required": True,
    "represents": (
        "ai_ecosystem_state",
        "capability_state",
        "governance_state",
        "decision_state",
        "operational_state",
        "evolution_state",
    ),
    "enables": (
        "simulation",
        "prediction",
        "optimization",
        "autonomous_control",
    ),
}

COMMANDS: tuple[str, ...] = (
    "CreateAIControlPlaneCommand",
    "RegisterCapabilityCommand",
    "ExecuteAIWorkflowCommand",
    "ApplyPolicyCommand",
    "ApproveDecisionCommand",
    "TriggerEvolutionCommand",
)

QUERIES: tuple[str, ...] = (
    "GetAIStateQuery",
    "GetCapabilityStatusQuery",
    "GetGovernanceStatusQuery",
    "GetDecisionHistoryQuery",
    "GetEvolutionStatusQuery",
)

CORE_EVENTS: tuple[dict[str, str], ...] = (
    {"name": "ControlPlaneCreatedEvent", "owner": "ai", "consumers": "audit,analytics"},
    {"name": "CapabilityRegisteredEvent", "owner": "ai", "consumers": "analytics,search"},
    {"name": "WorkflowExecutedEvent", "owner": "ai", "consumers": "aiops,analytics"},
    {"name": "PolicyAppliedEvent", "owner": "ai", "consumers": "governance,audit"},
    {"name": "DecisionCompletedEvent", "owner": "ai", "consumers": "audit,analytics"},
    {"name": "OptimizationTriggeredEvent", "owner": "ai", "consumers": "aiops,infra"},
    {"name": "EvolutionStartedEvent", "owner": "ai", "consumers": "research,marketplace"},
    {"name": "AIStateChangedEvent", "owner": "ai", "consumers": "command_center,analytics"},
)

MICROSERVICES: tuple[dict[str, Any], ...] = (
    {"id": "ai_control_plane_service", "responsibility": "global control plane registry and coordination", "api": "/ai/aios/control-plane", "db": "ai_*", "events": ("ControlPlaneCreatedEvent", "CapabilityRegisteredEvent"), "security": ("ai.assist.read",), "scaling": "control_plane_replicas"},
    {"id": "orchestration_service", "responsibility": "workflow execution and autonomous orchestration", "api": "/ai/aios/orchestration", "db": "ai_*", "events": ("WorkflowExecutedEvent",), "security": ("ai.assist.infer",), "scaling": "orchestrator_replicas"},
    {"id": "capability_management_service", "responsibility": "capability state, versioning, usage, lifecycle metadata", "api": "/ai/aios/capabilities", "db": "ai_*", "events": ("CapabilityRegisteredEvent",), "security": ("ai.assist.read",), "scaling": "metadata_shards"},
    {"id": "policy_control_service", "responsibility": "policy enforcement and governance operations", "api": "/ai/aios/policies", "db": "ai_*", "events": ("PolicyAppliedEvent",), "security": ("ai.assist.read",), "scaling": "control_plane"},
    {"id": "decision_service", "responsibility": "decision governance, routing, approval, escalation", "api": "/ai/aios/decisions", "db": "ai_*", "events": ("DecisionCompletedEvent",), "security": ("ai.assist.read",), "scaling": "control_plane"},
    {"id": "lifecycle_service", "responsibility": "capability lifecycle transitions and retirement orchestration", "api": "/ai/aios/lifecycle", "db": "ai_*", "events": ("AIStateChangedEvent",), "security": ("ai.assist.infer",), "scaling": "worker_pools"},
    {"id": "monitoring_service", "responsibility": "intelligence metrics, health, and performance visibility", "api": "/ai/aios/monitoring", "db": "ai_*", "events": ("AIStateChangedEvent",), "security": ("ai.assist.read",), "scaling": "analytics_pipeline"},
    {"id": "evolution_service", "responsibility": "continuous improvement and controlled evolution triggers", "api": "/ai/aios/evolution", "db": "ai_*", "events": ("EvolutionStartedEvent", "OptimizationTriggeredEvent"), "security": ("ai.assist.infer",), "scaling": "control_plane"},
    {"id": "command_center_service", "responsibility": "enterprise command center dashboards and strategic oversight", "api": "/ai/aios/command-center", "db": "ai_*", "events": ("AIStateChangedEvent", "DecisionCompletedEvent"), "security": ("ai.assist.read",), "scaling": "analytics_replicas"},
)

API_SURFACES: tuple[str, ...] = (
    "/api/v1/ai/aios/control-plane",
    "/api/v1/ai/aios/orchestration",
    "/api/v1/ai/aios/capabilities",
    "/api/v1/ai/aios/policies",
    "/api/v1/ai/aios/decisions",
    "/api/v1/ai/aios/lifecycle",
    "/api/v1/ai/aios/monitoring",
    "/api/v1/ai/aios/evolution",
)

API_STYLES: tuple[str, ...] = ("REST", "GraphQL", "gRPC", "Streaming", "Event")

SECURITY = {
    "present_required": True,
    "zero_trust": True,
    "integrates": ("P207", "P208", "P209", "P210", "P214-P"),
    "controls": (
        "control_plane_authorization",
        "policy_enforced_coordination",
        "decision_approval_guards",
        "command_center_access_control",
        "autonomy_boundary_enforcement",
    ),
}

DEPLOYMENT = {
    "present_required": True,
    "cloud_native": True,
    "via_p214_n": True,
    "components": (
        "kubernetes",
        "ai_control_plane_cluster",
        "orchestration_engine",
        "policy_engine",
        "knowledge_graph",
        "digital_twin",
        "observability_platform",
        "security_layer",
    ),
}

TESTING: tuple[str, ...] = (
    "control_plane_testing",
    "orchestration_testing",
    "policy_testing",
    "decision_testing",
    "lifecycle_testing",
    "security_testing",
    "governance_testing",
    "autonomy_testing",
    "scalability_testing",
)

CURSOR_OUTPUTS: tuple[str, ...] = (
    "enterprise_ai_operating_system_vision",
    "ddd_domain_model",
    "bounded_context_map",
    "ai_control_plane",
    "ai_orchestration_engine",
    "ai_capability_management",
    "ai_command_center",
    "ai_policy_control",
    "ai_decision_governance",
    "ai_lifecycle_management",
    "ai_os_knowledge_graph",
    "ai_os_digital_twin",
    "cqrs_commands_queries",
    "event_sourcing_schema",
    "microservice_boundaries",
    "integration_architecture",
    "cloud_native_deployment",
    "testing_architecture",
    "quality_gates_dod",
    "adr_440",
    "enterprise_ai_aios_law",
)

QUALITY_GATES_REJECT_IF: tuple[str, ...] = (
    "enterprise_ai_operating_system_is_missing",
    "ai_control_plane_is_missing",
    "autonomous_orchestration_is_missing",
    "ai_command_center_is_missing",
    "ai_capability_management_is_missing",
    "ai_policy_control_is_missing",
    "ai_decision_governance_is_missing",
    "ai_lifecycle_management_is_missing",
    "ai_knowledge_graph_is_missing",
    "ai_digital_twin_is_missing",
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
        "role": "MEOS AI Operating System Layer",
        "principle": PRINCIPLE,
        "equation": (
            "AI Capabilities → AI Control Plane → Autonomous Orchestration → "
            "Policy Enforcement → Intelligent Decisions → Enterprise Execution "
            "→ Continuous Evolution"
        ),
        "pillars": (
            "ai_operating_system_required",
            "centralized_intelligence_control_required",
            "autonomous_systems_require_coordination",
            "governance_requires_operational_layer",
            "ai_evolution_requires_continuous_management",
        ),
        "strategic_role": {
            "operating_system": (
                "Enterprises need an AI operating system to coordinate many AI "
                "subsystems as one governable intelligence fabric."
            ),
            "centralized_control": (
                "Capabilities need a metadata-driven control plane for registry, "
                "state, health, policy, and orchestration decisions."
            ),
            "coordination": (
                "Autonomous models, agents, services, and workflows require "
                "enterprise-wide coordination to avoid conflict and drift."
            ),
            "governance": (
                "Responsible AI becomes operational only when policy, trust, and "
                "approvals are enforced in the runtime control layer."
            ),
            "continuous_management": (
                "AI ecosystems evolve continuously, so orchestration, monitoring, "
                "and adaptation must be native platform capabilities."
            ),
        },
        "deepens_p214_s": (
            "P214-S discovers future capabilities; P214-T becomes the supreme "
            "control plane that coordinates discovery, execution, trust, and evolution."
        ),
        "governed_by_p214_p": True,
    }


def domain_model() -> dict[str, Any]:
    return {"core_domain": CORE_DOMAIN, "supporting_domains": [dict(d) for d in SUPPORTING_DOMAINS], "supporting_count": len(SUPPORTING_DOMAINS), "aggregate": dict(AGGREGATE)}


def bounded_contexts() -> dict[str, Any]:
    return {"contexts": [dict(c) for c in LOGICAL_BOUNDED_CONTEXTS], "context_count": len(LOGICAL_BOUNDED_CONTEXTS), "logical_partitions_same_sor": True}


def control_plane() -> dict[str, Any]:
    return dict(CONTROL_PLANE)


def orchestration() -> dict[str, Any]:
    return dict(ORCHESTRATION)


def capability_management() -> dict[str, Any]:
    return dict(CAPABILITY_MANAGEMENT)


def command_center() -> dict[str, Any]:
    return dict(COMMAND_CENTER)


def policy_control() -> dict[str, Any]:
    return dict(POLICY_CONTROL)


def decision_control() -> dict[str, Any]:
    return dict(DECISION_CONTROL)


def lifecycle() -> dict[str, Any]:
    return dict(LIFECYCLE)


def knowledge_graph() -> dict[str, Any]:
    return dict(OS_KNOWLEDGE_GRAPH)


def digital_twin() -> dict[str, Any]:
    return dict(OS_DIGITAL_TWIN)


def cqrs() -> dict[str, Any]:
    return {"commands": list(COMMANDS), "command_count": len(COMMANDS), "queries": list(QUERIES), "query_count": len(QUERIES), "alignment_present_required": True}


def events() -> dict[str, Any]:
    return {"core_events": [dict(e) for e in CORE_EVENTS], "core_event_count": len(CORE_EVENTS), "event_driven_required": True, "retention_policy": "tenant_scoped_immutable_append", "version_strategy": "event_version_field", "ownership": "ai"}


def microservices() -> dict[str, Any]:
    return {"services": [dict(s) for s in MICROSERVICES], "service_count": len(MICROSERVICES), "logical_decomposition": True}


def api() -> dict[str, Any]:
    return {"surfaces": list(API_SURFACES), "styles": list(API_STYLES), "api_first_present_required": True}


def integrations() -> dict[str, Any]:
    return {
        "peers": (
            "P214-F", "P214-G", "P214-J", "P214-L", "P214-M", "P214-N", "P214-O", "P214-P", "P214-Q", "P214-R", "P214-S", "audit", "policy_engine",
        ),
        "via_events_and_acl": True,
        "control_contracts": True,
        "governance_boundaries": True,
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
    return {"reject_if": list(QUALITY_GATES_REJECT_IF), "count": len(QUALITY_GATES_REJECT_IF)}


def production_readiness() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "checklist": {
            "ai_operating_system": True,
            "ai_control_plane": True,
            "ai_orchestration": True,
            "ai_command_center": True,
            "ai_capability_management": True,
            "ai_policy_control": True,
            "ai_decision_control": True,
            "ai_lifecycle_management": True,
            "ai_knowledge_graph": True,
            "ai_digital_twin": True,
            "cqrs_architecture": True,
            "event_architecture": True,
            "microservice_architecture": True,
            "api_platform": True,
            "governance_architecture": True,
            "security_architecture": True,
            "deployment_architecture": True,
            "testing_architecture": True,
            "foundation_tests": True,
            "aios_api_live": True,
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
            "P214-A", "P214-B", "P214-C", "P214-D", "P214-E", "P214-F", "P214-G", "P214-H", "P214-I", "P214-J", "P214-K", "P214-L", "P214-M", "P214-N", "P214-O", "P214-P", "P214-Q", "P214-R", "P214-S", "ADR-421", "ADR-436", "ADR-437", "ADR-438", "ADR-439", "AI_PLATFORM_STANDARD", "ENTERPRISE_POLICY_ENGINE", "ENTERPRISE_AUDIT_PLATFORM",
        ],
        "vision": vision(),
        "domain_model": domain_model(),
        "bounded_contexts": bounded_contexts(),
        "control_plane": control_plane(),
        "orchestration": orchestration(),
        "capability_management": capability_management(),
        "command_center": command_center(),
        "policy_control": policy_control(),
        "decision_control": decision_control(),
        "lifecycle": lifecycle(),
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
        "enterprise_ai_operating_system_present_required": True,
        "ai_control_plane_present_required": True,
        "autonomous_orchestration_present_required": True,
        "ai_command_center_present_required": True,
        "ai_capability_management_present_required": True,
        "ai_policy_control_present_required": True,
        "ai_decision_governance_present_required": True,
        "ai_lifecycle_management_present_required": True,
        "ai_knowledge_graph_present_required": True,
        "ai_digital_twin_present_required": True,
        "cqrs_architecture_present_required": True,
        "event_architecture_present_required": True,
        "microservices_architecture_present_required": True,
        "api_first_architecture_present_required": True,
        "zero_trust_ai_security_present_required": True,
        "cloud_native_deployment_present_required": True,
        "sibling_ai_bc_forbidden": True,
        "module_local_aios_forbidden": True,
        "deepens_p214_s_control_plane": True,
        "governed_by_p214_p": True,
        "via_enterprise_ai": True,
        "via_api_gateway": True,
        "api_prefix": f"{API_PREFIX}/aios",
        "forbidden_sibling_bc": [
            "ai_operating_system", "ai_control_plane", "autonomous_intelligence_governance", "ai_orchestration_platform", "ai_capability_management_platform", "ai_command_center_platform", "ai_decision_control_platform", "generative_ai", "llm_platform", "vector_intelligence", "ai_core", "ml_platform",
        ],
    }


def aios_surface() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "routes": [
            "GET /ai/aios",
            "GET /ai/aios/vision",
            "GET /ai/aios/domain",
            "GET /ai/aios/bounded-contexts",
            "GET /ai/aios/control-plane",
            "GET /ai/aios/orchestration",
            "GET /ai/aios/capabilities",
            "GET /ai/aios/command-center",
            "GET /ai/aios/policies",
            "GET /ai/aios/decisions",
            "GET /ai/aios/lifecycle",
            "GET /ai/aios/knowledge-graph",
            "GET /ai/aios/digital-twin",
            "GET /ai/aios/cqrs",
            "GET /ai/aios/events",
            "GET /ai/aios/microservices",
            "GET /ai/aios/integrations",
            "GET /ai/aios/api",
            "GET /ai/aios/security",
            "GET /ai/aios/deployment",
            "GET /ai/aios/testing",
            "GET /ai/aios/outputs",
            "GET /ai/aios/production-readiness",
            "GET /ai/aios/readiness",
        ],
    }
