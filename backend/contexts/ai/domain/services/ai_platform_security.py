"""P214-I Enterprise AI Security, Adversarial Defense & Protection — immutable catalog."""
from __future__ import annotations

from typing import Any

PROMPT_ID = "P214-I"
ADR = 429
SOR = "ai"
API_PREFIX = "/api/v1/ai"
PRODUCT = "Enterprise AI Security, Adversarial Defense & AI Protection Platform"
CAPABILITY = "CAP-PLT-AI-001"

PRINCIPLE = (
    "Enterprise AI Security SHALL protect the intelligence layer of MEOS by "
    "securing models, data, agents, prompts, knowledge and autonomous actions "
    "against internal and external threats."
)

FABRIC = "meos_ai_security_fabric"

CORE_DOMAIN = "enterprise_ai_security_management"

SUPPORTING_DOMAINS: tuple[dict[str, str], ...] = (
    {"id": "ai_identity_security", "purpose": "Secure AI system and agent identities."},
    {"id": "ai_model_security", "purpose": "Protect model confidentiality and integrity."},
    {"id": "llm_security", "purpose": "LLM firewall, abuse and leakage prevention."},
    {"id": "prompt_security", "purpose": "Prompt injection and leakage defense."},
    {"id": "agent_security", "purpose": "Agent zero trust and tool authorization."},
    {"id": "ai_runtime_security", "purpose": "Runtime monitoring and behavior analysis."},
    {"id": "adversarial_defense", "purpose": "Attack detection, simulation, defense."},
    {"id": "ai_threat_intelligence", "purpose": "AI threat indicators and patterns."},
    {"id": "ai_security_operations", "purpose": "AI-SOC, IR, threat hunting."},
)

AGGREGATE = {
    "name": "EnterpriseAISecurityAggregate",
    "root": "EnterpriseAISecurity",
    "entities": (
        "AISystem",
        "AIModel",
        "LLMInstance",
        "AIAgent",
        "AIPrompt",
        "AIDataAsset",
        "AIKnowledgeAsset",
        "AIRuntime",
        "AIThreat",
        "AISecurityPolicy",
        "AIControl",
        "AIIncident",
    ),
    "value_objects": (
        "AIAssetIdentifier",
        "ThreatIdentifier",
        "RiskLevel",
        "SecurityScore",
        "TrustLevel",
        "AttackVector",
        "ProtectionPolicy",
        "SecurityStatus",
    ),
    "events": (
        "AIThreatDetectedEvent",
        "AIModelCompromisedEvent",
        "PromptAttackDetectedEvent",
        "AgentViolationDetectedEvent",
        "AIIncidentCreatedEvent",
        "AISecurityControlTriggeredEvent",
        "AIProtectionCompletedEvent",
    ),
}

LOGICAL_BOUNDED_CONTEXTS: tuple[dict[str, Any], ...] = (
    {
        "id": "ai_asset_security",
        "bc": "BC-01",
        "name": "AI Asset Security Context",
        "purpose": "AI inventory, discovery, classification, protection mapping.",
    },
    {
        "id": "ai_model_security",
        "bc": "BC-02",
        "name": "AI Model Security Context",
        "purpose": "Model protection, integrity, access, vulnerability management.",
    },
    {
        "id": "llm_security",
        "bc": "BC-03",
        "name": "LLM Security Context",
        "purpose": "LLM protection, context/output security, abuse prevention.",
    },
    {
        "id": "prompt_security",
        "bc": "BC-04",
        "name": "Prompt Security Context",
        "purpose": "Prompt validation, injection defense, leakage prevention.",
    },
    {
        "id": "ai_agent_security",
        "bc": "BC-05",
        "name": "AI Agent Security Context",
        "purpose": "Agent identity, authorization, action and tool security.",
    },
    {
        "id": "adversarial_defense",
        "bc": "BC-06",
        "name": "Adversarial Defense Context",
        "purpose": "Attack detection, simulation, defense automation.",
    },
    {
        "id": "ai_runtime_security",
        "bc": "BC-07",
        "name": "AI Runtime Security Context",
        "purpose": "Runtime monitoring, execution protection, behavior analysis.",
    },
    {
        "id": "ai_security_operations",
        "bc": "BC-08",
        "name": "AI Security Operations Context",
        "purpose": "AI-SOC, incident response, threat hunting.",
    },
)

AI_ASSET_SECURITY = {
    "present_required": True,
    "assets": (
        "ai_models",
        "llm_instances",
        "ai_agents",
        "prompts",
        "datasets",
        "knowledge_assets",
        "ai_applications",
        "inference_services",
    ),
    "capabilities": (
        "discovery",
        "classification",
        "ownership",
        "risk_assessment",
        "security_controls",
    ),
}

MODEL_SECURITY = {
    "present_required": True,
    "via_p209": True,
    "protects": (
        "model_confidentiality",
        "model_integrity",
        "model_availability",
        "model_intellectual_property",
    ),
    "controls": (
        "model_encryption",
        "model_signing",
        "model_access_control",
        "model_verification",
        "model_integrity_monitoring",
    ),
}

LLM_SECURITY = {
    "present_required": True,
    "via_p214_e": True,
    "threats": (
        "prompt_injection",
        "jailbreak_attacks",
        "data_leakage",
        "model_extraction",
        "sensitive_information_disclosure",
        "unsafe_generation",
    ),
    "controls": (
        "llm_firewall",
        "input_validation",
        "output_filtering",
        "context_protection",
        "safety_guardrails",
    ),
}

PROMPT_SECURITY = {
    "present_required": True,
    "via_p214_e": True,
    "via_p214_h": True,
    "capabilities": (
        "prompt_validation",
        "prompt_classification",
        "prompt_risk_analysis",
        "prompt_injection_detection",
        "prompt_monitoring",
        "prompt_governance",
    ),
}

AGENT_SECURITY = {
    "present_required": True,
    "via_p214_f": True,
    "protects": (
        "agent_identity",
        "agent_memory",
        "agent_goals",
        "agent_tools",
        "agent_actions",
        "agent_communication",
    ),
    "controls": (
        "agent_zero_trust",
        "least_privilege",
        "action_approval",
        "tool_authorization",
        "execution_monitoring",
    ),
}

ADVERSARIAL_DEFENSE = {
    "present_required": True,
    "threats": (
        "data_poisoning",
        "model_manipulation",
        "evasion_attacks",
        "prompt_attacks",
        "model_theft",
        "ai_abuse",
    ),
    "capabilities": (
        "attack_simulation",
        "red_team_testing",
        "defense_automation",
        "threat_modeling",
    ),
}

THREAT_INTELLIGENCE = {
    "present_required": True,
    "via_p210": True,
    "collects": (
        "ai_vulnerabilities",
        "attack_patterns",
        "threat_indicators",
        "adversarial_techniques",
        "security_events",
    ),
}

RUNTIME_PROTECTION = {
    "present_required": True,
    "monitors": (
        "inference_requests",
        "model_behavior",
        "agent_actions",
        "api_traffic",
        "resource_usage",
        "output_quality",
    ),
    "controls": (
        "runtime_policy_enforcement",
        "behavior_analysis",
        "anomaly_detection",
        "automatic_response",
    ),
}

SECURITY_KG = {
    "present_required": True,
    "via_p214_g": True,
    "represents": (
        "ai_assets",
        "threats",
        "vulnerabilities",
        "controls",
        "incidents",
        "relationships",
    ),
    "enables": ("threat_reasoning", "risk_prediction", "attack_simulation"),
}

SECURITY_DIGITAL_TWIN = {
    "present_required": True,
    "represents": (
        "ai_system_state",
        "security_posture",
        "threat_landscape",
        "protection_controls",
        "attack_surface",
    ),
    "enables": ("simulation", "prediction", "optimization", "autonomous_defense"),
}

AI_SOC = {
    "present_required": True,
    "via_p210": True,
    "capabilities": (
        "ai_threat_monitoring",
        "ai_threat_hunting",
        "incident_response",
        "automated_remediation",
        "security_analytics",
        "threat_intelligence",
    ),
}

COMMANDS: tuple[str, ...] = (
    "RegisterAIAssetCommand",
    "ScanAIModelCommand",
    "ValidatePromptCommand",
    "BlockThreatCommand",
    "ProtectAgentCommand",
    "UpdateSecurityPolicyCommand",
)

QUERIES: tuple[str, ...] = (
    "GetAISecurityStatusQuery",
    "GetThreatQuery",
    "GetModelSecurityQuery",
    "GetAgentSecurityQuery",
    "GetIncidentHistoryQuery",
)

CORE_EVENTS: tuple[dict[str, str], ...] = (
    {"name": "AIAssetRegisteredEvent", "owner": "ai", "consumers": "audit,security"},
    {"name": "ThreatDetectedEvent", "owner": "ai", "consumers": "cyber,notifications"},
    {"name": "PromptAttackDetectedEvent", "owner": "ai", "consumers": "audit,security"},
    {"name": "ModelIntegrityVerifiedEvent", "owner": "ai", "consumers": "audit"},
    {"name": "AgentBlockedEvent", "owner": "ai", "consumers": "audit,agents"},
    {"name": "SecurityPolicyTriggeredEvent", "owner": "ai", "consumers": "policy,audit"},
    {"name": "AIIncidentResolvedEvent", "owner": "ai", "consumers": "audit,cyber"},
    {"name": "AIThreatDetectedEvent", "owner": "ai", "consumers": "ai_soc,cyber"},
)

MICROSERVICES: tuple[dict[str, Any], ...] = (
    {
        "id": "ai_asset_security_service",
        "responsibility": "AI asset inventory and classification",
        "api": "/ai/aisec/assets",
        "db": "ai_*",
        "events": ("AIAssetRegisteredEvent",),
        "security": ("ai.assist.read",),
        "scaling": "control_plane",
    },
    {
        "id": "model_security_service",
        "responsibility": "model signing, integrity, access",
        "api": "/ai/aisec/models",
        "db": "ai_*",
        "events": ("ModelIntegrityVerifiedEvent",),
        "security": ("ai.assist.read", "ai.assist.infer"),
        "scaling": "stateless_replicas",
    },
    {
        "id": "llm_security_service",
        "responsibility": "LLM firewall and guardrails",
        "api": "/ai/aisec/llm",
        "db": "ai_*",
        "events": ("PromptAttackDetectedEvent",),
        "security": ("ai.assist.infer",),
        "scaling": "inline_hpa",
    },
    {
        "id": "prompt_security_service",
        "responsibility": "prompt validation and injection defense",
        "api": "/ai/aisec/prompts",
        "db": "ai_*",
        "events": ("PromptAttackDetectedEvent",),
        "security": ("ai.assist.infer",),
        "scaling": "inline_hpa",
    },
    {
        "id": "agent_security_service",
        "responsibility": "agent zero trust and tool authz",
        "api": "/ai/aisec/agents",
        "db": "ai_*",
        "events": ("AgentBlockedEvent",),
        "security": ("ai.assist.infer",),
        "scaling": "stateless_replicas",
    },
    {
        "id": "threat_intelligence_service",
        "responsibility": "AI threat intel collection and correlation",
        "api": "/ai/aisec/threats",
        "db": "ai_*",
        "events": ("ThreatDetectedEvent", "AIThreatDetectedEvent"),
        "security": ("ai.assist.read",),
        "scaling": "async_workers",
    },
    {
        "id": "runtime_protection_service",
        "responsibility": "runtime policy and anomaly detection",
        "api": "/ai/aisec/runtime",
        "db": "ai_*",
        "events": ("SecurityPolicyTriggeredEvent",),
        "security": ("ai.assist.infer",),
        "scaling": "inline_and_async",
    },
    {
        "id": "security_monitoring_service",
        "responsibility": "AI security telemetry and analytics",
        "api": "/ai/aisec/monitoring",
        "db": "ai_*",
        "events": (),
        "security": ("ai.assist.read",),
        "scaling": "observability_pipeline",
    },
    {
        "id": "incident_response_service",
        "responsibility": "AI incident orchestration via cyber/SOC",
        "api": "/ai/aisec/incidents",
        "db": "ai_*",
        "events": ("AIIncidentResolvedEvent",),
        "security": ("ai.assist.read",),
        "scaling": "control_plane",
    },
    {
        "id": "policy_enforcement_service",
        "responsibility": "AI security policy enforcement hooks",
        "api": "/ai/aisec/policies",
        "db": "ai_*",
        "events": ("SecurityPolicyTriggeredEvent",),
        "security": ("ai.assist.infer",),
        "scaling": "inline_hpa",
    },
)

API_SURFACES: tuple[str, ...] = (
    "/api/v1/ai/aisec",
    "/api/v1/ai/aisec/assets",
    "/api/v1/ai/aisec/models",
    "/api/v1/ai/aisec/llm",
    "/api/v1/ai/aisec/prompts",
    "/api/v1/ai/aisec/agents",
    "/api/v1/ai/aisec/threats",
    "/api/v1/ai/aisec/runtime",
    "/api/v1/ai/aisec/incidents",
)

API_STYLES: tuple[str, ...] = ("REST", "GraphQL", "gRPC", "Event", "Streaming")

SECURITY = {
    "present_required": True,
    "zero_trust": True,
    "integrates": ("P207", "P208", "P209", "P210", "P211"),
    "controls": (
        "ai_zero_trust",
        "model_access_governance",
        "agent_governance",
        "prompt_governance",
        "data_protection",
        "policy_enforcement",
        "runtime_protection",
        "adversarial_defense",
    ),
}

DEPLOYMENT = {
    "present_required": True,
    "cloud_native": True,
    "via_p213_o": True,
    "components": (
        "kubernetes_security",
        "ai_firewall",
        "security_gateway",
        "policy_engine",
        "threat_detection_engine",
        "monitoring_platform",
        "siem_integration",
        "soar_integration",
    ),
}

TESTING: tuple[str, ...] = (
    "ai_security_testing",
    "adversarial_testing",
    "red_team_testing",
    "prompt_attack_testing",
    "model_security_testing",
    "agent_security_testing",
    "runtime_testing",
    "compliance_testing",
)

CURSOR_OUTPUTS: tuple[str, ...] = (
    "enterprise_ai_security_vision",
    "ddd_domain_model",
    "bounded_context_map",
    "ai_asset_security",
    "model_security_platform",
    "llm_security_platform",
    "prompt_security_platform",
    "agent_security_platform",
    "adversarial_defense",
    "threat_intelligence",
    "runtime_protection",
    "security_knowledge_graph",
    "security_digital_twin",
    "ai_soc",
    "cqrs_commands_queries",
    "event_sourcing_schema",
    "microservice_boundaries",
    "integration_architecture",
    "cloud_native_deployment",
    "testing_architecture",
    "quality_gates_dod",
    "adr_429",
    "enterprise_ai_security_law",
)

QUALITY_GATES_REJECT_IF: tuple[str, ...] = (
    "enterprise_ai_security_platform_is_missing",
    "ai_model_security_is_missing",
    "llm_security_is_missing",
    "prompt_security_is_missing",
    "agent_security_is_missing",
    "adversarial_defense_is_missing",
    "ai_threat_intelligence_is_missing",
    "runtime_protection_is_missing",
    "ai_security_operations_is_missing",
    "security_knowledge_graph_is_missing",
    "ai_security_digital_twin_is_missing",
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
        "role": "MEOS AI Security Fabric",
        "principle": PRINCIPLE,
        "equation": (
            "AI Models + Agents + LLMs + Applications + Data + Knowledge + "
            "Decisions → Identity → Authorization → Encryption → Threat Detection "
            "→ Runtime Protection → Continuous Monitoring → Autonomous Defense"
        ),
        "pillars": (
            "specialized_ai_security",
            "beyond_traditional_cybersecurity",
            "autonomous_intelligence_risks",
            "generative_ai_risks",
            "enterprise_ai_asset_protection",
            "ai_driven_decision_security",
        ),
        "traditional_vs_ai_security": {
            "traditional": "Hosts, networks, apps, identities.",
            "ai_security": "Models, prompts, agents, knowledge, inference behavior.",
        },
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


def assets() -> dict[str, Any]:
    return dict(AI_ASSET_SECURITY)


def models() -> dict[str, Any]:
    return dict(MODEL_SECURITY)


def llm() -> dict[str, Any]:
    return dict(LLM_SECURITY)


def prompts() -> dict[str, Any]:
    return dict(PROMPT_SECURITY)


def agents() -> dict[str, Any]:
    return dict(AGENT_SECURITY)


def adversarial() -> dict[str, Any]:
    return dict(ADVERSARIAL_DEFENSE)


def threats() -> dict[str, Any]:
    return dict(THREAT_INTELLIGENCE)


def runtime() -> dict[str, Any]:
    return dict(RUNTIME_PROTECTION)


def knowledge_graph() -> dict[str, Any]:
    return dict(SECURITY_KG)


def digital_twin() -> dict[str, Any]:
    return dict(SECURITY_DIGITAL_TWIN)


def soc() -> dict[str, Any]:
    return dict(AI_SOC)


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
            "P207",
            "P208",
            "P209",
            "P210",
            "P211",
            "P214-E",
            "P214-F",
            "P214-G",
            "P214-H",
            "policy_engine",
            "siem",
            "soar",
        ),
        "via_events_and_acl": True,
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
            "ai_security_platform": True,
            "ai_asset_protection": True,
            "model_security": True,
            "llm_security": True,
            "prompt_security": True,
            "agent_security": True,
            "adversarial_defense": True,
            "threat_intelligence": True,
            "runtime_protection": True,
            "ai_soc": True,
            "security_knowledge_graph": True,
            "security_digital_twin": True,
            "cqrs_architecture": True,
            "event_architecture": True,
            "microservice_architecture": True,
            "api_platform": True,
            "security_architecture": True,
            "deployment_architecture": True,
            "testing_architecture": True,
            "foundation_tests": True,
            "aisec_api_live": True,
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
            "ADR-421",
            "ADR-422",
            "ADR-423",
            "ADR-424",
            "ADR-425",
            "ADR-426",
            "ADR-427",
            "ADR-428",
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
        "assets": assets(),
        "models": models(),
        "llm": llm(),
        "prompts": prompts(),
        "agents": agents(),
        "adversarial": adversarial(),
        "threats": threats(),
        "runtime": runtime(),
        "knowledge_graph": knowledge_graph(),
        "digital_twin": digital_twin(),
        "soc": soc(),
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
        "enterprise_ai_security_platform_present_required": True,
        "ai_model_security_present_required": True,
        "llm_security_present_required": True,
        "prompt_security_present_required": True,
        "agent_security_present_required": True,
        "adversarial_defense_present_required": True,
        "ai_threat_intelligence_present_required": True,
        "runtime_protection_present_required": True,
        "ai_security_operations_present_required": True,
        "security_knowledge_graph_present_required": True,
        "ai_security_digital_twin_present_required": True,
        "cqrs_architecture_present_required": True,
        "event_architecture_present_required": True,
        "microservices_architecture_present_required": True,
        "api_first_architecture_present_required": True,
        "zero_trust_security_present_required": True,
        "cloud_native_deployment_present_required": True,
        "sibling_ai_bc_forbidden": True,
        "module_local_ai_security_forbidden": True,
        "via_enterprise_ai": True,
        "via_api_gateway": True,
        "api_prefix": f"{API_PREFIX}/aisec",
        "forbidden_sibling_bc": [
            "ai_security",
            "adversarial_defense",
            "llm_security",
            "prompt_security",
            "ai_threat_intel",
            "ai_runtime_protection",
            "generative_ai",
            "llm_platform",
            "ai_core",
            "vector_intelligence",
        ],
    }


def aisec_surface() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "routes": [
            "GET /ai/aisec",
            "GET /ai/aisec/vision",
            "GET /ai/aisec/domain",
            "GET /ai/aisec/bounded-contexts",
            "GET /ai/aisec/assets",
            "GET /ai/aisec/models",
            "GET /ai/aisec/llm",
            "GET /ai/aisec/prompts",
            "GET /ai/aisec/agents",
            "GET /ai/aisec/adversarial",
            "GET /ai/aisec/threats",
            "GET /ai/aisec/runtime",
            "GET /ai/aisec/knowledge-graph",
            "GET /ai/aisec/digital-twin",
            "GET /ai/aisec/soc",
            "GET /ai/aisec/cqrs",
            "GET /ai/aisec/events",
            "GET /ai/aisec/microservices",
            "GET /ai/aisec/integrations",
            "GET /ai/aisec/api",
            "GET /ai/aisec/security",
            "GET /ai/aisec/deployment",
            "GET /ai/aisec/testing",
            "GET /ai/aisec/outputs",
            "GET /ai/aisec/production-readiness",
            "GET /ai/aisec/readiness",
        ],
    }
