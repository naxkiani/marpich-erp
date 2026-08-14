"""P214-B Enterprise AI mission/vision/strategic intelligence scope — immutable catalog."""
from __future__ import annotations

from typing import Any

PROMPT_ID = "P214-B"
ADR = 422
SOR = "ai"
API_PREFIX = "/api/v1/ai"
PRODUCT = (
    "Enterprise AI — Mission, Vision & Strategic Intelligence Scope"
)
CAPABILITY = "CAP-PLT-AI-001"

MISSION_STATEMENT = (
    "Enterprise AI SHALL transform MEOS from a traditional enterprise "
    "platform into an adaptive, intelligent, autonomous and continuously "
    "learning operating system."
)

VISION_STATEMENT = (
    "MEOS Enterprise AI SHALL become the intelligence layer that "
    "continuously learns, reasons, predicts, optimizes and improves "
    "every enterprise capability."
)

FABRIC = "meos_enterprise_ai_strategic_intelligence_framework"

FABRIC_FLOW: tuple[str, ...] = (
    "business_strategy",
    "enterprise_data",
    "enterprise_knowledge",
    "ai_capabilities",
    "human_expertise",
    "autonomous_intelligence",
    "ai_powered_enterprise_transformation",
    "intelligent_operations",
    "strategic_decision_advantage",
    "autonomous_business_capabilities",
    "continuous_enterprise_evolution",
)

STRATEGIC_OBJECTIVES: tuple[dict[str, Any], ...] = (
    {
        "id": "SO-01",
        "name": "enterprise_intelligence_enhancement",
        "business_purpose": "Raise enterprise cognitive capacity across domains.",
        "ai_capability": "unified_ai_paas_and_analytics",
        "data_requirement": "governed_data_products",
        "success_metrics": ("intelligence_coverage_pct", "insight_latency"),
        "governance_requirement": "ai_governance_board_oversight",
    },
    {
        "id": "SO-02",
        "name": "ai_driven_decision_excellence",
        "business_purpose": "Improve decision quality and speed.",
        "ai_capability": "decision_support_and_prescriptive_ai",
        "data_requirement": "decision_context_and_outcomes",
        "success_metrics": ("decision_improvement_rate", "time_to_decision"),
        "governance_requirement": "explainability_and_human_oversight",
    },
    {
        "id": "SO-03",
        "name": "autonomous_operations_enablement",
        "business_purpose": "Automate safe operational loops.",
        "ai_capability": "agents_and_automation",
        "data_requirement": "event_streams_and_runbooks",
        "success_metrics": ("ai_automation_rate", "mttr_reduction"),
        "governance_requirement": "autonomy_levels_and_kill_switches",
    },
    {
        "id": "SO-04",
        "name": "enterprise_knowledge_expansion",
        "business_purpose": "Grow reusable enterprise memory.",
        "ai_capability": "rag_graph_embeddings",
        "data_requirement": "knowledge_graph_and_documents",
        "success_metrics": ("knowledge_coverage", "retrieval_precision"),
        "governance_requirement": "knowledge_stewardship",
    },
    {
        "id": "SO-05",
        "name": "business_process_intelligence",
        "business_purpose": "Instrument and optimize processes with AI.",
        "ai_capability": "process_mining_and_optimization",
        "data_requirement": "process_events_and_kpis",
        "success_metrics": ("process_efficiency_gain", "cycle_time"),
        "governance_requirement": "process_owner_approval",
    },
    {
        "id": "SO-06",
        "name": "ai_innovation_acceleration",
        "business_purpose": "Shorten idea-to-production for AI products.",
        "ai_capability": "experimentation_and_marketplace",
        "data_requirement": "sandbox_datasets",
        "success_metrics": ("time_to_model_production", "portfolio_throughput"),
        "governance_requirement": "coe_portfolio_gating",
    },
    {
        "id": "SO-07",
        "name": "operational_efficiency_improvement",
        "business_purpose": "Reduce cost-to-serve via AI.",
        "ai_capability": "forecasting_and_resource_optimization",
        "data_requirement": "ops_and_cost_telemetry",
        "success_metrics": ("cost_reduction", "productivity_index"),
        "governance_requirement": "finops_and_ai_roi_review",
    },
    {
        "id": "SO-08",
        "name": "enterprise_risk_reduction",
        "business_purpose": "Detect and mitigate operational and AI risks.",
        "ai_capability": "anomaly_and_risk_models",
        "data_requirement": "security_and_compliance_signals",
        "success_metrics": ("risk_score_delta", "incident_prevention_rate"),
        "governance_requirement": "ai_risk_committee",
    },
    {
        "id": "SO-09",
        "name": "customer_intelligence_improvement",
        "business_purpose": "Personalize and anticipate customer needs.",
        "ai_capability": "customer_ai_and_recommendations",
        "data_requirement": "crm_consent_aware_profiles",
        "success_metrics": ("nps_delta", "conversion_lift"),
        "governance_requirement": "privacy_by_design",
    },
    {
        "id": "SO-10",
        "name": "continuous_organizational_learning",
        "business_purpose": "Close feedback loops into models and policies.",
        "ai_capability": "retraining_and_outcome_learning",
        "data_requirement": "outcome_labels_and_feedback",
        "success_metrics": ("model_accuracy_trend", "learning_cycle_time"),
        "governance_requirement": "continuous_governance",
    },
)

CAPABILITY_DOMAINS: tuple[dict[str, Any], ...] = (
    {
        "id": "DOMAIN_01",
        "name": "ai_infrastructure_capability",
        "includes": ("ai_compute", "ai_runtime", "gpu_infrastructure", "model_serving"),
    },
    {
        "id": "DOMAIN_02",
        "name": "machine_learning_capability",
        "includes": (
            "ml_engineering",
            "model_training",
            "feature_engineering",
            "model_lifecycle",
        ),
    },
    {
        "id": "DOMAIN_03",
        "name": "generative_ai_capability",
        "includes": ("llm_platform", "prompt_engineering", "rag", "ai_assistants"),
    },
    {
        "id": "DOMAIN_04",
        "name": "autonomous_agent_capability",
        "includes": (
            "ai_agents",
            "agent_memory",
            "agent_planning",
            "agent_collaboration",
        ),
    },
    {
        "id": "DOMAIN_05",
        "name": "ai_governance_capability",
        "includes": ("ai_risk", "ai_compliance", "responsible_ai", "ai_audit"),
    },
    {
        "id": "DOMAIN_06",
        "name": "ai_business_intelligence_capability",
        "includes": (
            "ai_analytics",
            "ai_forecasting",
            "ai_optimization",
            "ai_decision_support",
        ),
    },
)

OPERATING_MODEL_LAYERS: tuple[str, ...] = (
    "ai_strategy_layer",
    "ai_governance_layer",
    "ai_platform_layer",
    "ai_engineering_layer",
    "ai_application_layer",
    "ai_business_consumption_layer",
)

OPERATING_MODEL_ROLES: tuple[str, ...] = (
    "chief_ai_officer",
    "ai_product_owner",
    "ml_engineer",
    "generative_ai_engineer",
    "ai_governance_officer",
    "ai_security_officer",
    "domain_ai_champion",
    "human_oversight_owner",
)

COE_RESPONSIBILITIES: tuple[str, ...] = (
    "ai_strategy",
    "ai_standards",
    "ai_architecture",
    "ai_research",
    "ai_governance",
    "ai_training",
    "ai_innovation",
    "ai_portfolio_management",
)

COE_TEAMS: tuple[str, ...] = (
    "ai_architecture_team",
    "ml_engineering_team",
    "generative_ai_team",
    "ai_governance_team",
    "ai_security_team",
    "ai_research_team",
    "ai_product_team",
)

MATURITY_LEVELS: tuple[dict[str, Any], ...] = (
    {
        "level": 1,
        "name": "ai_awareness",
        "capabilities": ("education", "pilot_identification"),
        "technology": ("sandbox_access",),
        "governance": ("policy_awareness",),
        "outcomes": ("shared_vocabulary",),
    },
    {
        "level": 2,
        "name": "ai_adoption",
        "capabilities": ("assisted_use_cases", "prompt_libraries"),
        "technology": ("managed_llm_assist",),
        "governance": ("use_case_intake",),
        "outcomes": ("measured_productivity_gains",),
    },
    {
        "level": 3,
        "name": "ai_integration",
        "capabilities": ("embedded_ai_in_workflows", "rag"),
        "technology": ("model_registry", "feature_store"),
        "governance": ("model_approval",),
        "outcomes": ("cross_module_ai_surfaces",),
    },
    {
        "level": 4,
        "name": "ai_optimization",
        "capabilities": ("continuous_retraining", "cost_performance_tuning"),
        "technology": ("mlops_pipelines", "observability"),
        "governance": ("slo_and_drift_controls",),
        "outcomes": ("reliable_production_ai",),
    },
    {
        "level": 5,
        "name": "ai_automation",
        "capabilities": ("closed_loop_automation", "agent_tools"),
        "technology": ("agent_runtime", "event_driven_triggers"),
        "governance": ("autonomy_levels",),
        "outcomes": ("reduced_manual_toil",),
    },
    {
        "level": 6,
        "name": "autonomous_intelligence",
        "capabilities": ("multi_agent_collaboration", "self_improving_systems"),
        "technology": ("knowledge_graph", "digital_twin", "enterprise_ai"),
        "governance": ("continuous_governance", "ethics_board"),
        "outcomes": ("adaptive_operating_system",),
    },
)

VALUE_CATEGORIES: tuple[dict[str, Any], ...] = (
    {
        "id": "revenue_growth",
        "opportunity": "AI-driven offers and conversion",
        "measurement": "incremental_revenue",
        "kpi": "ai_attributed_revenue",
        "impact": "top_line_growth",
    },
    {
        "id": "cost_reduction",
        "opportunity": "Automate repetitive work",
        "measurement": "cost_avoidance",
        "kpi": "ai_cost_savings",
        "impact": "opex_reduction",
    },
    {
        "id": "operational_efficiency",
        "opportunity": "Optimize cycles and queues",
        "measurement": "throughput_and_cycle_time",
        "kpi": "process_efficiency_gain",
        "impact": "higher_capacity",
    },
    {
        "id": "risk_reduction",
        "opportunity": "Earlier detection and controls",
        "measurement": "loss_prevented",
        "kpi": "risk_score_delta",
        "impact": "lower_residual_risk",
    },
    {
        "id": "innovation_acceleration",
        "opportunity": "Faster experimentation",
        "measurement": "time_to_value",
        "kpi": "portfolio_throughput",
        "impact": "competitive_pace",
    },
    {
        "id": "customer_experience",
        "opportunity": "Personalized journeys",
        "measurement": "satisfaction_and_retention",
        "kpi": "nps_delta",
        "impact": "loyalty",
    },
    {
        "id": "employee_productivity",
        "opportunity": "Copilots and assistants",
        "measurement": "hours_saved",
        "kpi": "ai_adoption_rate",
        "impact": "focus_on_high_value_work",
    },
    {
        "id": "strategic_advantage",
        "opportunity": "Unique intelligence moats",
        "measurement": "capability_differentiation",
        "kpi": "business_impact_score",
        "impact": "enterprise_advantage",
    },
)

USE_CASE_CLASSES: tuple[dict[str, Any], ...] = (
    {
        "id": "strategic_ai",
        "pattern": "executive_scenario_and_portfolio",
        "required_data": "strategy_kpis",
        "model_type": "decision_and_forecast",
        "benefit": "strategic_clarity",
    },
    {
        "id": "operational_ai",
        "pattern": "ops_anomaly_and_automation",
        "required_data": "telemetry_events",
        "model_type": "anomaly_and_rl",
        "benefit": "reliability",
    },
    {
        "id": "customer_ai",
        "pattern": "personalization_and_support",
        "required_data": "crm_interactions",
        "model_type": "llm_and_recommenders",
        "benefit": "experience",
    },
    {
        "id": "employee_ai",
        "pattern": "workplace_copilot",
        "required_data": "knowledge_base",
        "model_type": "rag_llm",
        "benefit": "productivity",
    },
    {
        "id": "security_ai",
        "pattern": "threat_detection",
        "required_data": "security_signals",
        "model_type": "classification_and_graph",
        "benefit": "cyber_resilience",
    },
    {
        "id": "financial_ai",
        "pattern": "fraud_forecast_treasury",
        "required_data": "ledger_and_transactions",
        "model_type": "time_series_and_risk",
        "benefit": "financial_control",
    },
    {
        "id": "supply_chain_ai",
        "pattern": "demand_and_logistics",
        "required_data": "inventory_and_orders",
        "model_type": "forecast_and_optimization",
        "benefit": "service_level",
    },
    {
        "id": "healthcare_ai",
        "pattern": "clinical_and_ops_assist",
        "required_data": "clinical_events",
        "model_type": "nlp_and_risk",
        "benefit": "care_quality",
    },
    {
        "id": "manufacturing_ai",
        "pattern": "quality_and_predictive_maintenance",
        "required_data": "sensor_streams",
        "model_type": "cv_and_anomaly",
        "benefit": "uptime",
    },
    {
        "id": "government_ai",
        "pattern": "citizen_services_and_compliance",
        "required_data": "case_records",
        "model_type": "classification_and_llm",
        "benefit": "public_service",
    },
    {
        "id": "knowledge_ai",
        "pattern": "enterprise_memory_and_rag",
        "required_data": "documents_and_graph",
        "model_type": "embeddings_and_graph_rag",
        "benefit": "institutional_memory",
    },
)

GOVERNANCE_BODIES: tuple[str, ...] = (
    "enterprise_ai_governance_board",
    "ai_architecture_review_board",
    "ai_risk_committee",
    "ai_ethics_committee",
    "ai_security_committee",
)

GOVERNANCE_RESPONSIBILITIES: tuple[str, ...] = (
    "ai_approval",
    "ai_risk_assessment",
    "ai_policy_management",
    "ai_compliance",
    "ai_investment_decisions",
)

MEOS_DOMAIN_ALIGNMENT: tuple[str, ...] = (
    "erp_intelligence",
    "crm_intelligence",
    "finance_intelligence",
    "hr_intelligence",
    "supply_chain_intelligence",
    "cyber_intelligence",
    "data_intelligence",
    "knowledge_intelligence",
    "digital_twin_intelligence",
    "decision_intelligence",
)

KNOWLEDGE_STRATEGY: tuple[str, ...] = (
    "knowledge_acquisition",
    "knowledge_representation",
    "knowledge_retrieval",
    "knowledge_reasoning",
    "knowledge_evolution",
)

TRANSFORMATION_ROADMAP: tuple[dict[str, Any], ...] = (
    {
        "phase": 1,
        "name": "ai_foundation",
        "capabilities": ("ai_paas", "registry", "governance_baseline"),
        "technology": ("kubernetes", "gpu_pools", "otel"),
        "governance": ("board_charter", "responsible_ai_policy"),
        "outcomes": ("platform_ready",),
    },
    {
        "phase": 2,
        "name": "ai_adoption",
        "capabilities": ("assistants", "prompt_registry", "pilot_use_cases"),
        "technology": ("managed_llm", "embeddings"),
        "governance": ("use_case_intake",),
        "outcomes": ("measured_adoption",),
    },
    {
        "phase": 3,
        "name": "ai_integration",
        "capabilities": ("module_ai_surfaces", "rag", "ml_pipelines"),
        "technology": ("feature_store", "vector_db"),
        "governance": ("model_approval_gates"),
        "outcomes": ("cross_domain_ai",),
    },
    {
        "phase": 4,
        "name": "ai_optimization",
        "capabilities": ("drift_mgmt", "cost_optimization", "retraining"),
        "technology": ("mlops", "autoscaling"),
        "governance": ("slo_error_budgets"),
        "outcomes": ("reliable_roi",),
    },
    {
        "phase": 5,
        "name": "autonomous_enterprise",
        "capabilities": ("multi_agent", "closed_loops", "twin_simulation"),
        "technology": ("agent_fabric", "graph_rag", "twin"),
        "governance": ("autonomy_and_ethics"),
        "outcomes": ("adaptive_meos",),
    },
)

RESPONSIBLE_AI_RISKS: tuple[str, ...] = (
    "bias",
    "hallucination",
    "privacy",
    "security",
    "explainability",
    "transparency",
    "accountability",
    "human_oversight",
)

INVESTMENT_MODEL: tuple[str, ...] = (
    "ai_infrastructure_cost",
    "model_development_cost",
    "ai_operation_cost",
    "ai_benefit_measurement",
    "ai_roi_model",
    "ai_portfolio_prioritization",
)

SECURITY_STRATEGY: dict[str, Any] = {
    "via_p210": True,
    "via_p211": True,
    "controls": (
        "ai_threat_management",
        "model_security",
        "prompt_security",
        "data_security",
        "agent_security",
        "ai_supply_chain_security",
    ),
}

SUCCESS_METRICS: tuple[str, ...] = (
    "ai_adoption_rate",
    "ai_automation_rate",
    "model_accuracy",
    "business_impact_score",
    "ai_roi",
    "decision_improvement_rate",
    "process_efficiency_gain",
    "ai_reliability_score",
    "ai_governance_compliance_score",
)

COMMANDS: tuple[str, ...] = (
    "PublishAiMissionCommand",
    "PublishAiVisionCommand",
    "RegisterStrategicObjectiveCommand",
    "ApproveAiCapabilityDomainCommand",
    "AdvanceMaturityAssessmentCommand",
    "ApproveTransformationPhaseCommand",
)

QUERIES: tuple[str, ...] = (
    "GetAiMissionQuery",
    "GetAiVisionQuery",
    "GetStrategicObjectivesQuery",
    "GetCapabilityMapQuery",
    "GetMaturityStatusQuery",
    "GetTransformationRoadmapQuery",
)

EVENTS: tuple[str, ...] = (
    "AiMissionPublishedEvent",
    "AiVisionPublishedEvent",
    "AiStrategicObjectiveRegisteredEvent",
    "AiMaturityLevelAssessedEvent",
    "AiTransformationPhaseApprovedEvent",
    "AiGovernanceStrategyValidatedEvent",
)

CURSOR_OUTPUTS: tuple[str, ...] = (
    "enterprise_ai_mission",
    "enterprise_ai_vision",
    "ai_strategic_objectives",
    "ai_capability_map",
    "ai_operating_model",
    "ai_center_of_excellence",
    "ai_maturity_model",
    "ai_value_realization_framework",
    "ai_use_case_framework",
    "ai_strategic_governance_model",
    "ai_meos_alignment",
    "ai_knowledge_strategy",
    "ai_digital_transformation_roadmap",
    "ai_risk_responsible_strategy",
    "ai_economics_investment_model",
    "ai_security_strategy",
    "ai_success_metrics",
    "production_readiness_checklist",
)

QUALITY_GATES_REJECT_IF: tuple[str, ...] = (
    "mission_is_undefined",
    "vision_is_undefined",
    "ai_strategic_scope_is_undefined",
    "ai_capability_map_is_missing",
    "ai_operating_model_is_missing",
    "ai_maturity_model_is_missing",
    "ai_governance_strategy_is_undefined",
    "ai_transformation_roadmap_is_missing",
    "ai_value_framework_is_missing",
    "responsible_ai_strategy_is_undefined",
    "ai_security_strategy_is_missing",
    "sibling_ai_bc",
)


def mission() -> dict[str, Any]:
    return {
        "statement": MISSION_STATEMENT,
        "defined_required": True,
        "why": "adaptive_intelligent_autonomous_os",
        "value_creation": (
            "human_ai_collaboration",
            "autonomous_operations",
            "innovation_acceleration",
        ),
    }


def vision() -> dict[str, Any]:
    return {
        "statement": VISION_STATEMENT,
        "defined_required": True,
        "future_state": (
            "ai_powered_enterprise_ecosystem",
            "autonomous_business_operations",
            "intelligent_decision_making",
            "ai_driven_innovation",
            "enterprise_cognitive_capabilities",
            "predictive_and_prescriptive_intelligence",
            "human_ai_collaboration_model",
        ),
        "fabric": FABRIC,
        "fabric_flow": list(FABRIC_FLOW),
    }


def strategic_objectives() -> dict[str, Any]:
    return {
        "objectives": [dict(o) for o in STRATEGIC_OBJECTIVES],
        "count": len(STRATEGIC_OBJECTIVES),
        "defined_required": True,
    }


def capability_map() -> dict[str, Any]:
    return {
        "domains": [dict(d) for d in CAPABILITY_DOMAINS],
        "domain_count": len(CAPABILITY_DOMAINS),
        "present_required": True,
    }


def operating_model() -> dict[str, Any]:
    return {
        "layers": list(OPERATING_MODEL_LAYERS),
        "layer_count": len(OPERATING_MODEL_LAYERS),
        "roles": list(OPERATING_MODEL_ROLES),
        "role_count": len(OPERATING_MODEL_ROLES),
        "decision_rights_required": True,
        "present_required": True,
    }


def center_of_excellence() -> dict[str, Any]:
    return {
        "name": "meos_ai_center_of_excellence",
        "responsibilities": list(COE_RESPONSIBILITIES),
        "responsibility_count": len(COE_RESPONSIBILITIES),
        "teams": list(COE_TEAMS),
        "team_count": len(COE_TEAMS),
        "present_required": True,
    }


def maturity_model() -> dict[str, Any]:
    return {
        "levels": [dict(l) for l in MATURITY_LEVELS],
        "level_count": len(MATURITY_LEVELS),
        "present_required": True,
    }


def value_framework() -> dict[str, Any]:
    return {
        "categories": [dict(c) for c in VALUE_CATEGORIES],
        "category_count": len(VALUE_CATEGORIES),
        "present_required": True,
    }


def use_case_framework() -> dict[str, Any]:
    return {
        "classes": [dict(c) for c in USE_CASE_CLASSES],
        "class_count": len(USE_CASE_CLASSES),
        "present_required": True,
    }


def governance_model() -> dict[str, Any]:
    return {
        "bodies": list(GOVERNANCE_BODIES),
        "body_count": len(GOVERNANCE_BODIES),
        "responsibilities": list(GOVERNANCE_RESPONSIBILITIES),
        "defined_required": True,
    }


def meos_alignment() -> dict[str, Any]:
    return {
        "domains": list(MEOS_DOMAIN_ALIGNMENT),
        "domain_count": len(MEOS_DOMAIN_ALIGNMENT),
        "present_required": True,
        "builds_on_p212_p213": True,
    }


def knowledge_strategy() -> dict[str, Any]:
    return {
        "via_p213_l": True,
        "via_p212_j": True,
        "pillars": list(KNOWLEDGE_STRATEGY),
        "pillar_count": len(KNOWLEDGE_STRATEGY),
        "present_required": True,
    }


def transformation_roadmap() -> dict[str, Any]:
    return {
        "phases": [dict(p) for p in TRANSFORMATION_ROADMAP],
        "phase_count": len(TRANSFORMATION_ROADMAP),
        "present_required": True,
    }


def responsible_ai() -> dict[str, Any]:
    return {
        "risks": list(RESPONSIBLE_AI_RISKS),
        "risk_count": len(RESPONSIBLE_AI_RISKS),
        "defined_required": True,
    }


def investment_model() -> dict[str, Any]:
    return {
        "components": list(INVESTMENT_MODEL),
        "component_count": len(INVESTMENT_MODEL),
        "present_required": True,
    }


def security_strategy() -> dict[str, Any]:
    return dict(SECURITY_STRATEGY) | {"present_required": True}


def success_metrics() -> dict[str, Any]:
    return {
        "kpis": list(SUCCESS_METRICS),
        "kpi_count": len(SUCCESS_METRICS),
        "present_required": True,
    }


def cqrs() -> dict[str, Any]:
    return {
        "commands": list(COMMANDS),
        "command_count": len(COMMANDS),
        "queries": list(QUERIES),
        "query_count": len(QUERIES),
        "events": list(EVENTS),
        "event_count": len(EVENTS),
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
            "enterprise_ai_mission": True,
            "enterprise_ai_vision": True,
            "ai_strategic_objectives": True,
            "ai_capability_map": True,
            "ai_operating_model": True,
            "ai_center_of_excellence": True,
            "ai_maturity_model": True,
            "ai_value_framework": True,
            "ai_governance_model": True,
            "ai_transformation_roadmap": True,
            "ai_risk_strategy": True,
            "ai_security_strategy": True,
            "ai_success_metrics": True,
            "foundation_tests": True,
            "mission_api_live": True,
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
        "fabric": FABRIC,
        "builds_on": [
            "P214-A",
            "ADR-421",
            "P212",
            "P212-J",
            "P212-L",
            "P213",
            "P213-L",
            "P213-M",
            "P213-O",
            "P207",
            "P208",
            "P210",
            "P211",
            "AI_PLATFORM_STANDARD",
        ],
        "mission": mission(),
        "vision": vision(),
        "strategic_objectives": strategic_objectives(),
        "capability_map": capability_map(),
        "operating_model": operating_model(),
        "center_of_excellence": center_of_excellence(),
        "maturity_model": maturity_model(),
        "value_framework": value_framework(),
        "use_case_framework": use_case_framework(),
        "governance_model": governance_model(),
        "meos_alignment": meos_alignment(),
        "knowledge_strategy": knowledge_strategy(),
        "transformation_roadmap": transformation_roadmap(),
        "responsible_ai": responsible_ai(),
        "investment_model": investment_model(),
        "security_strategy": security_strategy(),
        "success_metrics": success_metrics(),
        "cqrs": cqrs(),
        "cursor_outputs": cursor_outputs(),
        "quality_gates": quality_gates(),
        "production_readiness": production_readiness(),
        "mission_defined_required": True,
        "vision_defined_required": True,
        "ai_strategic_scope_defined_required": True,
        "ai_capability_map_present_required": True,
        "ai_operating_model_present_required": True,
        "ai_maturity_model_present_required": True,
        "ai_governance_strategy_defined_required": True,
        "ai_transformation_roadmap_present_required": True,
        "ai_value_framework_present_required": True,
        "responsible_ai_strategy_defined_required": True,
        "ai_security_strategy_present_required": True,
        "sibling_ai_bc_forbidden": True,
        "module_local_llm_sdk_forbidden": True,
        "via_enterprise_ai": True,
        "via_api_gateway": True,
        "api_prefix": f"{API_PREFIX}/mission",
        "forbidden_sibling_bc": [
            "ml_platform",
            "generative_ai",
            "llm_platform",
            "ai_core",
            "vector_intelligence",
            "model_lifecycle_platform",
        ],
    }


def mission_surface() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "routes": [
            "GET /ai/mission",
            "GET /ai/mission/statement",
            "GET /ai/mission/vision",
            "GET /ai/mission/objectives",
            "GET /ai/mission/capability-map",
            "GET /ai/mission/operating-model",
            "GET /ai/mission/coe",
            "GET /ai/mission/maturity",
            "GET /ai/mission/value",
            "GET /ai/mission/use-cases",
            "GET /ai/mission/governance",
            "GET /ai/mission/meos-alignment",
            "GET /ai/mission/knowledge",
            "GET /ai/mission/roadmap",
            "GET /ai/mission/responsible-ai",
            "GET /ai/mission/investment",
            "GET /ai/mission/security",
            "GET /ai/mission/metrics",
            "GET /ai/mission/outputs",
            "GET /ai/mission/production-readiness",
            "GET /ai/mission/readiness",
        ],
    }
