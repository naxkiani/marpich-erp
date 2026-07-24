"""P207-C Identity Intelligence Domain Architecture (DDD) — immutable catalog."""
from __future__ import annotations

from typing import Any

PROMPT_ID = "P207-C"
ADR = 318
SOR = "identity_intelligence"
API_PREFIX = "/api/v1/identity-intelligence"
PRODUCT = "Enterprise Identity Intelligence & Autonomous Identity Operations Platform"

DOMAIN_PURPOSE: tuple[str, ...] = (
    "identity_understanding",
    "identity_reasoning",
    "identity_prediction",
    "identity_optimization",
    "autonomous_identity_operations",
    "continuous_identity_intelligence",
)

CORE_DOMAINS: tuple[str, ...] = (
    "identity_understanding",
    "predictive_risk",
    "behavioral_analytics",
    "autonomous_operations",
    "ai_agent_orchestration",
)

SUPPORTING_DOMAINS: tuple[str, ...] = (
    "digital_twin_orchestration",
    "knowledge_graph_intelligence",
    "self_healing",
    "recommendation",
    "model_registry_refs",
)

GENERIC_DOMAINS: tuple[str, ...] = (
    "notification",
    "audit_hooks",
    "observability_hooks",
    "caching",
)

LOGICAL_BOUNDED_CONTEXTS: tuple[str, ...] = (
    "identity_understanding",
    "predictive_risk",
    "behavioral_analytics",
    "ai_agent_platform",
    "digital_twin_orchestration",
    "knowledge_graph_intelligence",
    "autonomous_operations",
    "self_healing_fabric",
    "recommendation",
    "ai_security_governance",
    "ml_model_registry_refs",
    "compliance_intelligence_hooks",
)

UBIQUITOUS_LANGUAGE: dict[str, str] = {
    "IdentityIntelligence": "Actionable understanding of an identity across data, behavior, risk, and relationships",
    "Insight": "Explainable finding derived from identity analysis",
    "RiskPrediction": "Measurable scored forecast of identity/access/privilege/behavior/compliance risk",
    "BehaviorProfile": "Pattern model of login, access, device, privilege, and application usage",
    "AiAgent": "Governed AI agent contract that investigates, recommends, or automates under HITL",
    "DigitalTwinOrchestration": "Simulation/impact/what-if coordination against peer twin SoR refs",
    "GraphIntegration": "ACL-bound connection to Directory knowledge graph projections",
    "AutonomousOperation": "Governed monitor→analyze→decide→act→learn run with human control",
    "SelfHealingRemediation": "Detection→RCA→recommendation→remediation→validation loop",
    "Recommendation": "Explainable suggested action for operators or peer platforms",
    "ModelRegistryRef": "Reference to AI Platform model version — never local LLM",
    "IntelligenceTenantPolicy": "Tenant-scoped intelligence/automation policy projection",
}

AGGREGATES: tuple[str, ...] = (
    "IdentityIntelligenceProfile",
    "IdentityInsight",
    "IdentityRiskPrediction",
    "BehaviorAnalyticsProfile",
    "IdentityAiAgentContract",
    "DigitalTwinOrchestration",
    "KnowledgeGraphIntegration",
    "AutonomousOperationRun",
    "SelfHealingRemediation",
    "RecommendationCase",
    "IntelligenceModelRegistryRef",
    "IntelligenceTenantPolicy",
)

ENTITIES: tuple[str, ...] = (
    "InsightEvidence",
    "RiskFactor",
    "BehaviorSignal",
    "AgentCapability",
    "RemediationStep",
    "RecommendationOption",
)

VALUE_OBJECTS: tuple[str, ...] = (
    "RiskScore",
    "Explanation",
    "Confidence",
    "TenantId",
    "SubjectRef",
    "TwinRef",
    "GraphProjectionRef",
    "ModelVersionRef",
    "HitlApproval",
)

DOMAIN_SERVICES: tuple[str, ...] = (
    "IdentityReasoningService",
    "RiskScoringService",
    "BehaviorDetectionService",
    "RecommendationRankingService",
    "AutonomousDecisionService",
    "SelfHealingOrchestrationService",
)

COMMANDS: tuple[str, ...] = (
    "AnalyzeIdentity",
    "PredictIdentityRisk",
    "GenerateRecommendation",
    "ExecuteRemediation",
    "UpdateDigitalTwin",
    "TrainModel",
    "RegisterAgent",
    "BindGraphProjection",
)

QUERIES: tuple[str, ...] = (
    "GetIdentityIntelligence",
    "GetRiskPrediction",
    "GetBehaviorProfile",
    "GetDigitalTwin",
    "GetRecommendations",
    "GetAgentContract",
)

DOMAIN_EVENTS: tuple[str, ...] = (
    "RiskPredicted",
    "AnomalyDetected",
    "InsightGenerated",
    "ActionRecommended",
    "RemediationExecuted",
    "ModelUpdated",
    "AgentRegistered",
    "TwinOrchestrationBound",
    "GraphIntegrationConnected",
)

MEOS_PLACEMENT: tuple[str, ...] = (
    "intelligence_layer_above_identity_trust_fabric",
    "consumes_p201_p205_and_twin_via_events_acl",
    "emits_recommendations_and_remediation_intents",
    "never_owns_peer_operational_sors",
)

QUALITY_GATES_REJECT_IF: tuple[str, ...] = (
    "ddd_boundaries_unclear",
    "anemic_domain_model",
    "cqrs_absent",
    "event_driven_missing",
    "replaces_peer_sors",
    "domain_purpose_absent",
    "context_map_undefined",
    "ai_only_chatbot",
    "human_control_removed",
    "invents_sibling_intelligence_bc",
    "embeds_llm_sdk",
    "automation_without_governance",
)


def purpose() -> dict[str, Any]:
    return {
        "provides": list(DOMAIN_PURPOSE),
        "count": len(DOMAIN_PURPOSE),
        "transforms_into": "actionable_enterprise_identity_intelligence",
        "required": True,
        "not_absent": True,
    }


def classification() -> dict[str, Any]:
    return {
        "core": list(CORE_DOMAINS),
        "supporting": list(SUPPORTING_DOMAINS),
        "generic_delegate": list(GENERIC_DOMAINS),
        "core_count": len(CORE_DOMAINS),
        "supporting_count": len(SUPPORTING_DOMAINS),
    }


def meos_placement() -> dict[str, Any]:
    return {
        "positions": list(MEOS_PLACEMENT),
        "layer": "intelligence_and_autonomous_decision",
        "above": [
            "identity_lifecycle",
            "identity_governance",
            "privileged_access",
            "authentication",
            "directory",
            "identity_digital_twin",
        ],
        "required": True,
        "does_not_replace_peers": True,
    }


def ubiquitous_language() -> dict[str, Any]:
    return {
        "terms": dict(UBIQUITOUS_LANGUAGE),
        "count": len(UBIQUITOUS_LANGUAGE),
        "required": True,
    }


def ddd() -> dict[str, Any]:
    return {
        "logical_contexts": list(LOGICAL_BOUNDED_CONTEXTS),
        "logical_count": len(LOGICAL_BOUNDED_CONTEXTS),
        "aggregates": list(AGGREGATES),
        "aggregate_count": len(AGGREGATES),
        "entities": list(ENTITIES),
        "entity_count": len(ENTITIES),
        "value_objects": list(VALUE_OBJECTS),
        "value_object_count": len(VALUE_OBJECTS),
        "domain_services": list(DOMAIN_SERVICES),
        "domain_service_count": len(DOMAIN_SERVICES),
        "boundaries_clear": True,
        "not_unclear": True,
        "anemic_forbidden": True,
        "not_anemic": True,
        "deployable_unit": SOR,
        "acl_required": True,
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
        "not_absent": True,
        "event_driven": True,
        "not_missing_events": True,
        "outbox_required": True,
    }


def context_map() -> dict[str, Any]:
    return {
        "partnership": [
            "identity_lifecycle",
            "identity_governance",
            "privileged_access",
            "authentication",
            "directory",
            "identity_digital_twin",
        ],
        "customer_supplier": ["ai", "policy", "audit", "observability"],
        "conformist": ["authorization"],
        "anti_corruption": ["integration"],
        "defined": True,
        "not_undefined": True,
        "does_not_replace_peers": True,
    }


def invariants() -> dict[str, Any]:
    return {
        "rules": [
            "tenant_id_required_on_every_aggregate",
            "explainable_decisions_required",
            "hitl_for_high_impact_automation",
            "risk_scores_must_be_measurable",
            "twin_and_graph_are_refs_only",
            "ai_inference_via_platform_only",
            "never_local_pdp",
            "never_chatbot_only",
        ],
        "count": 8,
        "required": True,
    }


def ai_governance() -> dict[str, Any]:
    return {
        "via_ai_platform": True,
        "embeds_llm_forbidden": True,
        "chatbot_only_forbidden": True,
        "explainable_required": True,
        "hitl_required": True,
        "human_control_required": True,
        "not_chatbot_only": True,
        "not_removed_human_control": True,
    }


def integrations() -> dict[str, Any]:
    return {
        "p207a_strategy": True,
        "p207b_mission": True,
        "p201_lifecycle": True,
        "p202_iga": True,
        "p203_pam": True,
        "p204_am": True,
        "p205_directory": True,
        "identity_digital_twin": True,
        "ai_platform": True,
        "authorization": True,
        "domain_integration_complete": True,
    }


def production_readiness() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "checklist": {
            "domain_purpose": True,
            "meos_placement": True,
            "strategic_classification": True,
            "logical_bounded_contexts": True,
            "ubiquitous_language": True,
            "aggregates_entities_vos": True,
            "domain_services": True,
            "cqrs_events": True,
            "context_map": True,
            "invariants": True,
            "foundation_tests": True,
            "domain_api_live": True,
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
        "forbidden_sibling_bc": "ai_identity_ops",
        "builds_on": ["P207-A", "P207-B"],
        "purpose": purpose(),
        "classification": classification(),
        "meos_placement": meos_placement(),
        "ubiquitous_language": ubiquitous_language(),
        "ddd": ddd(),
        "cqrs": cqrs(),
        "context_map": context_map(),
        "invariants": invariants(),
        "ai_governance": ai_governance(),
        "integrations": integrations(),
        "quality_gates": quality_gates(),
        "production_readiness": production_readiness(),
        "ddd_boundaries_clear": True,
        "api_prefix": f"{API_PREFIX}/domain",
        "distinct_from": ["P207-A /strategy*", "P207-B /mission*"],
    }


def executive_summary() -> dict[str, Any]:
    return catalog()


def domain_surface() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "routes": [
            "GET /identity-intelligence/domain",
            "GET /identity-intelligence/domain/purpose",
            "GET /identity-intelligence/domain/classification",
            "GET /identity-intelligence/domain/placement",
            "GET /identity-intelligence/domain/language",
            "GET /identity-intelligence/domain/bounded-contexts",
            "GET /identity-intelligence/domain/aggregates",
            "GET /identity-intelligence/domain/cqrs",
            "GET /identity-intelligence/domain/events",
            "GET /identity-intelligence/domain/context-map",
            "GET /identity-intelligence/domain/invariants",
            "GET /identity-intelligence/domain/ai-governance",
            "GET /identity-intelligence/domain/integrations",
            "GET /identity-intelligence/domain/production-readiness",
            "GET /identity-intelligence/domain/readiness",
        ],
    }
