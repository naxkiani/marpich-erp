"""P219-T Civilization Intelligence Governance & Alignment Core — immutable catalog."""
from __future__ import annotations
from typing import Any

PROMPT_ID = "P219-T"
ADR = 573
SOR = "civilization"
API_PREFIX = "/api/v1/civilization"
PRODUCT = (
    "Enterprise Civilization Operating System Civilization Intelligence Governance, "
    "Strategic Alignment Intelligence, Enterprise Policy Intelligence, Civilization Trust & Compliance Framework, "
    "Global Decision Assurance Platform & MEOS Civilization Governance & Alignment Intelligence Core"
)
CAPABILITY = "CAP-PLT-CIV-001"
PRIMARY_CAPABILITY = (
    "Create a civilization-scale governance intelligence platform capable of "
    "continuously aligning strategy, policy, execution and decision-making while "
    "maintaining transparency, accountability, resilience and trust across the MEOS ecosystem."
)
FABRIC = "meos_civilization_os_civilization_governance_alignment_intelligence_framework"
FOUNDATION_GATE = "P219"
MISSION_GATE = "P219-A"
STRATEGY_GATE = "P219-B"
DOMAIN_GATE = "P219-C"
PLANETARY_GATE = "P219-D"
AI_OS_GATE = "P219-E"
SIMULATION_GATE = "P219-F"
RESOURCES_GATE = "P219-G"
ECONOMY_GATE = "P219-H"
KNOWLEDGE_GATE = "P219-I"
HUMAN_GATE = "P219-J"
GOVERNANCE_GATE = "P219-K"
INNOVATION_GATE = "P219-L"
SECURITY_GATE = "P219-M"
SUSTAINABILITY_GATE = "P219-N"
PROSPERITY_GATE = "P219-O"
COLLABORATION_GATE = "P219-P"
CONSCIOUSNESS_GATE = "P219-Q"
EVOLUTION_GATE = "P219-R"
FUTURES_GATE = "P219-S"
INTELLIGENCE_NEXUS_GATE = "P218-Z"
SPACE_GATE = "P218"
BIO_GATE = "P217-Z"
ROBOTICS_GATE = "P216-Z"
QUANTUM_GATE = "P215-Z"
AI_GATE = "P214-Z"

MATURITY = (
    "Policy", "Control", "Governance", "Strategic Alignment",
    "Adaptive Governance", "Civilization Intelligence Governance",
)
LAYERS = (
    {"id": "L01", "name": "Civilization Governance Layer"},
    {"id": "L02", "name": "Governance Intelligence Layer"},
    {"id": "L03", "name": "Strategic Alignment Layer"},
    {"id": "L04", "name": "Governance Digital Twin"},
    {"id": "L05", "name": "Decision Assurance Layer"},
    {"id": "L06", "name": "Adaptive Governance Layer"},
)
GOVERNANCE_DOMAINS = (
    "policy", "strategy", "compliance", "risk", "ethics",
    "audit", "trust", "performance", "decision", "regulation",
)
INTEL_GOV_DOMAINS = (
    "strategy", "policy", "security", "economy", "infrastructure",
    "innovation", "knowledge", "human_development", "environment", "space",
)
ALIGNMENT_DIMENSIONS = (
    "mission", "vision", "objectives", "capabilities", "programs",
    "projects", "policies", "resources", "execution",
)
POLICY_LIFECYCLE = (
    "Create", "Review", "Approve", "Publish", "Enforce", "Monitor", "Improve",
)
POLICY_DOMAINS = (
    "security", "privacy", "ai", "risk", "finance",
    "hr", "technology", "operations", "governance",
)
TRUST_DOMAINS = (
    "ai_trust", "data_trust", "policy_trust",
    "decision_trust", "operational_trust", "institutional_trust",
)
COMPLIANCE_DOMAINS = (
    "internal_standards", "industry_standards", "regulatory_policies",
    "governance_standards", "enterprise_policies",
)
DECISION_LIFECYCLE = (
    "Proposal", "Evidence Collection", "Simulation", "Risk Evaluation",
    "Policy Verification", "Approval", "Execution", "Continuous Monitoring",
)
GOV_AGENTS = (
    "Governance Intelligence Agent", "Strategic Alignment Agent", "Policy Intelligence Agent",
    "Decision Assurance Agent", "Trust Intelligence Agent",
)
KG_ENTITIES = (
    "Policy", "Decision", "Objective", "Capability", "Organization", "Program",
    "Project", "Risk", "Control", "Audit", "ComplianceRecord",
)
KG_RELATIONSHIPS = (
    "GOVERNS", "SUPPORTS", "ALIGNS_WITH", "DEPENDS_ON",
    "VERIFIES", "MITIGATES", "IMPLEMENTS", "AUDITS",
)
DIGITAL_TWINS = (
    "Policy Twin", "Strategy Twin", "Organization Twin", "Decision Twin", "Governance Twin",
)
BOUNDED_CONTEXTS = (
    {
        "id": "BC-IGOV-01", "name": "Governance Core", "type": "CORE",
        "aggregate": "GovernanceAggregate",
        "entities": ("GovernanceModel", "GovernanceControl", "GovernancePolicy"),
        "value_objects": ("GovernanceScore", "GovernanceLevel", "ControlStrength"),
        "services": ("GovernanceService", "GovernanceAssessmentService"),
        "events": ("GovernanceUpdatedEvent", "ControlValidatedEvent", "GovernanceImprovedEvent"),
    },
    {
        "id": "BC-IGOV-02", "name": "Strategic Alignment Context", "type": "CORE",
        "aggregate": "AlignmentAggregate",
        "entities": ("StrategicObjective", "CapabilityAlignment", "StrategicRoadmap"),
        "value_objects": ("AlignmentScore", "Priority", "DependencyLevel"),
        "services": ("AlignmentService", "CapabilityAlignmentService"),
        "events": ("AlignmentVerifiedEvent", "ObjectiveUpdatedEvent", "CapabilityMappedEvent"),
    },
    {
        "id": "BC-IGOV-03", "name": "Policy Intelligence Context", "type": "CORE",
        "aggregate": "PolicyAggregate",
        "entities": ("Policy", "PolicyVersion", "PolicyReview"),
        "value_objects": ("PolicyStatus", "PolicyRisk", "ApprovalState"),
        "services": ("PolicyManagementService", "PolicyEvaluationService"),
        "events": ("PolicyPublishedEvent", "PolicyUpdatedEvent", "PolicyRetiredEvent"),
    },
    {
        "id": "BC-IGOV-04", "name": "Trust & Compliance Context", "type": "SUPPORTING",
        "aggregate": "ComplianceAggregate",
        "entities": ("ComplianceControl", "AuditRecord", "TrustAssessment"),
        "value_objects": ("ComplianceScore", "TrustIndex", "AuditResult"),
        "services": ("ComplianceService", "TrustAssessmentService"),
        "events": ("ComplianceVerifiedEvent", "AuditCompletedEvent", "TrustImprovedEvent"),
    },
)
PRIMARY_AGGREGATES = (
    "GovernanceAggregate", "GovernanceStateAggregate", "AlignmentAggregate",
    "PolicyAggregate", "ComplianceAggregate",
)
COMMANDS = (
    "CreatePolicyCommand", "ApproveDecisionCommand", "RunGovernanceAssessmentCommand",
    "VerifyAlignmentCommand", "ValidateComplianceCommand", "CalculateTrustCommand",
)
QUERIES = (
    "GetGovernanceDashboardQuery", "GetPolicyRepositoryQuery", "GetStrategicAlignmentQuery",
    "GetDecisionAuditTrailQuery", "GetTrustScoreQuery", "GetComplianceStatusQuery",
)
CORE_EVENTS = (
    {"name": "PolicyPublishedEvent", "owner": "BC-IGOV-03"},
    {"name": "PolicyUpdatedEvent", "owner": "BC-IGOV-03"},
    {"name": "GovernanceChangedEvent", "owner": "BC-IGOV-01"},
    {"name": "AlignmentVerifiedEvent", "owner": "BC-IGOV-02"},
    {"name": "DecisionApprovedEvent", "owner": "BC-IGOV-01"},
    {"name": "DecisionRejectedEvent", "owner": "BC-IGOV-01"},
    {"name": "AuditCompletedEvent", "owner": "BC-IGOV-04"},
    {"name": "ComplianceValidatedEvent", "owner": "BC-IGOV-04"},
    {"name": "TrustCalculatedEvent", "owner": "BC-IGOV-04"},
    {"name": "StrategicObjectiveUpdatedEvent", "owner": "BC-IGOV-02"},
    {"name": "ControlValidatedEvent", "owner": "BC-IGOV-01"},
    {"name": "GovernanceImprovedEvent", "owner": "BC-IGOV-01"},
)
KNOWLEDGE_GRAPH = {
    "present_required": True,
    "entities": KG_ENTITIES,
    "relationships": KG_RELATIONSHIPS,
    "capabilities": (
        "policy_reasoning", "strategic_navigation",
        "governance_analytics", "decision_explainability",
    ),
}
DIGITAL_TWIN = {
    "present_required": True,
    "twins": DIGITAL_TWINS,
    "capabilities": (
        "policy_simulation", "governance_simulation",
        "strategic_stress_testing", "decision_replay", "impact_analysis",
    ),
}
INTEGRATION = {
    "present_required": True,
    "peers": (
        "P214-Z", "P215-Z", "P216-Z", "P217-Z", "P218", "P218-Z",
        "P219", "P219-A", "P219-B", "P219-C", "P219-D", "P219-E", "P219-F",
        "P219-G", "P219-H", "P219-I", "P219-J", "P219-K", "P219-L", "P219-M",
        "P219-N", "P219-O", "P219-P", "P219-Q", "P219-R", "P219-S",
        "Policy Engine", "Workflow", "Audit", "Compliance", "MEOS Core",
    ),
    "integrations": (
        {"peer": "P214-Z", "provides": ("ai_governance",)},
        {"peer": "P215-Z", "provides": ("strategic_optimization",)},
        {"peer": "P216-Z", "provides": ("operational_governance",)},
        {"peer": "P217-Z", "provides": ("bio_governance",)},
        {"peer": "P218", "provides": ("space_governance",)},
        {"peer": "P219-E", "provides": ("governance_reasoning",)},
        {"peer": "P219-F", "provides": ("governance_simulation",)},
        {"peer": "P219-I", "provides": ("knowledge_governance",)},
        {"peer": "P219-K", "provides": ("policy_coordination",)},
        {"peer": "P219-L", "provides": ("innovation_governance",)},
        {"peer": "P219-M", "provides": ("security_governance",)},
        {"peer": "P219-N", "provides": ("esg_governance",)},
        {"peer": "P219-O", "provides": ("prosperity_governance",)},
        {"peer": "P219-P", "provides": ("collaborative_governance",)},
        {"peer": "P219-Q", "provides": ("strategic_awareness_governance",)},
        {"peer": "P219-R", "provides": ("evolution_governance",)},
        {"peer": "P219-S", "provides": ("strategic_foresight_governance",)},
    ),
}
ROADMAP = {
    "phases": (
        {"id": "P01", "name": "Governance Foundation"},
        {"id": "P02", "name": "Strategic Alignment"},
        {"id": "P03", "name": "Adaptive Governance"},
        {"id": "P04", "name": "Civilization Governance Intelligence"},
    ),
}
MICROSERVICES = (
    {"id": "intel_gov_service", "api": "/civilization/intelligence-governance", "bc": "BC-IGOV-01"},
    {"id": "alignment_service", "api": "/civilization/intelligence-governance/alignment", "bc": "BC-IGOV-02"},
    {"id": "policy_intelligence_service", "api": "/civilization/intelligence-governance/policy", "bc": "BC-IGOV-03"},
    {"id": "trust_compliance_service", "api": "/civilization/intelligence-governance/trust", "bc": "BC-IGOV-04"},
    {"id": "decision_assurance_service", "api": "/civilization/intelligence-governance/decision-assurance", "bc": "BC-IGOV-01"},
    {"id": "gov_twin_service", "api": "/civilization/intelligence-governance/digital-twin", "bc": "BC-IGOV-01"},
    {"id": "gov_kg_service", "api": "/civilization/intelligence-governance/knowledge-graph", "bc": "BC-IGOV-01"},
    {"id": "gov_agents_service", "api": "/civilization/intelligence-governance/agents", "bc": "BC-IGOV-01"},
    {"id": "gov_events_service", "api": "/civilization/intelligence-governance/events", "bc": "BC-IGOV-01"},
    {"id": "gov_integration_service", "api": "/civilization/intelligence-governance/integration", "bc": "BC-IGOV-01"},
)


def vision_pack() -> dict[str, Any]:
    return {
        "primary_capability": PRIMARY_CAPABILITY,
        "foundation_gate": FOUNDATION_GATE, "mission_gate": MISSION_GATE,
        "strategy_gate": STRATEGY_GATE, "domain_gate": DOMAIN_GATE,
        "planetary_gate": PLANETARY_GATE, "ai_os_gate": AI_OS_GATE,
        "simulation_gate": SIMULATION_GATE, "resources_gate": RESOURCES_GATE,
        "economy_gate": ECONOMY_GATE, "knowledge_gate": KNOWLEDGE_GATE,
        "human_gate": HUMAN_GATE, "governance_gate": GOVERNANCE_GATE,
        "innovation_gate": INNOVATION_GATE, "security_gate": SECURITY_GATE,
        "sustainability_gate": SUSTAINABILITY_GATE, "prosperity_gate": PROSPERITY_GATE,
        "collaboration_gate": COLLABORATION_GATE, "consciousness_gate": CONSCIOUSNESS_GATE,
        "evolution_gate": EVOLUTION_GATE, "futures_gate": FUTURES_GATE,
        "intelligence_nexus_gate": INTELLIGENCE_NEXUS_GATE, "space_gate": SPACE_GATE,
        "bio_gate": BIO_GATE, "robotics_gate": ROBOTICS_GATE,
        "quantum_gate": QUANTUM_GATE, "ai_gate": AI_GATE,
        "never_replace_p219_e_ai_os": True,
        "never_replace_p219_f_simulation": True,
        "never_replace_p219_k_governance": True,
        "never_replace_p219_s_futures": True,
        "never_replace_policy_engine": True,
        "never_ungated_governance_decision_execution": True,
        "never_opaque_unexplainable_governance_decisions": True,
        "never_bypass_human_accountability": True,
        "never_bypass_human_supervision_governance": True,
        "foundation_for_p219_u": True,
    }


def architecture() -> dict[str, Any]:
    return {
        "present_required": True,
        "maturity": list(MATURITY),
        "maturity_stage_count": len(MATURITY),
        "layers": [dict(l) for l in LAYERS],
        "layer_count": len(LAYERS),
        "governance_domains": list(GOVERNANCE_DOMAINS),
        "governance_domain_count": len(GOVERNANCE_DOMAINS),
        "intelligence_governance_domains": list(INTEL_GOV_DOMAINS),
        "intelligence_governance_domain_count": len(INTEL_GOV_DOMAINS),
        "alignment_dimensions": list(ALIGNMENT_DIMENSIONS),
        "alignment_dimension_count": len(ALIGNMENT_DIMENSIONS),
        "policy_lifecycle": list(POLICY_LIFECYCLE),
        "policy_lifecycle_step_count": len(POLICY_LIFECYCLE),
        "policy_domains": list(POLICY_DOMAINS),
        "policy_domain_count": len(POLICY_DOMAINS),
        "trust_domains": list(TRUST_DOMAINS),
        "trust_domain_count": len(TRUST_DOMAINS),
        "compliance_domains": list(COMPLIANCE_DOMAINS),
        "compliance_domain_count": len(COMPLIANCE_DOMAINS),
        "decision_lifecycle": list(DECISION_LIFECYCLE),
        "decision_lifecycle_step_count": len(DECISION_LIFECYCLE),
    }


def intel_gov_platform() -> dict[str, Any]:
    return {
        "present_required": True,
        "domains": list(INTEL_GOV_DOMAINS),
        "domain_count": len(INTEL_GOV_DOMAINS),
        "capabilities": (
            "governance_intelligence", "policy_coordination",
            "decision_oversight", "execution_monitoring", "strategic_evaluation",
        ),
        "never_replace_p219_k_governance": True,
    }


def alignment() -> dict[str, Any]:
    return {
        "present_required": True,
        "dimensions": list(ALIGNMENT_DIMENSIONS),
        "dimension_count": len(ALIGNMENT_DIMENSIONS),
        "capabilities": (
            "alignment_analysis", "gap_detection", "dependency_mapping",
            "portfolio_optimization", "strategic_synchronization",
        ),
    }


def policy_intelligence() -> dict[str, Any]:
    return {
        "present_required": True,
        "lifecycle": list(POLICY_LIFECYCLE),
        "lifecycle_step_count": len(POLICY_LIFECYCLE),
        "domains": list(POLICY_DOMAINS),
        "domain_count": len(POLICY_DOMAINS),
        "never_replace_policy_engine": True,
    }


def trust_compliance() -> dict[str, Any]:
    return {
        "present_required": True,
        "trust_domains": list(TRUST_DOMAINS),
        "trust_domain_count": len(TRUST_DOMAINS),
        "compliance_domains": list(COMPLIANCE_DOMAINS),
        "compliance_domain_count": len(COMPLIANCE_DOMAINS),
        "capabilities": (
            "continuous_compliance", "evidence_collection",
            "trust_scoring", "control_validation", "audit_intelligence",
        ),
    }


def decision_assurance() -> dict[str, Any]:
    return {
        "present_required": True,
        "lifecycle": list(DECISION_LIFECYCLE),
        "lifecycle_step_count": len(DECISION_LIFECYCLE),
        "capabilities": (
            "decision_explainability", "decision_confidence",
            "risk_assessment", "impact_validation", "audit_traceability",
        ),
        "never_ungated_governance_decision_execution": True,
        "never_opaque_unexplainable_governance_decisions": True,
    }


def digital_twin() -> dict[str, Any]:
    return dict(DIGITAL_TWIN) | {
        "twin_count": len(DIGITAL_TWINS),
        "capability_count": len(DIGITAL_TWIN["capabilities"]),
    }


def agents() -> dict[str, Any]:
    return {"present_required": True, "agents": list(GOV_AGENTS), "agent_count": len(GOV_AGENTS)}


def knowledge_graph() -> dict[str, Any]:
    return dict(KNOWLEDGE_GRAPH) | {
        "entity_count": len(KG_ENTITIES),
        "relationship_count": len(KG_RELATIONSHIPS),
        "capability_count": len(KNOWLEDGE_GRAPH["capabilities"]),
    }


def bounded_contexts() -> dict[str, Any]:
    return {
        "present_required": True,
        "contexts": [dict(c) for c in BOUNDED_CONTEXTS],
        "context_count": len(BOUNDED_CONTEXTS),
    }


def aggregates() -> dict[str, Any]:
    return {
        "present_required": True,
        "primary_aggregates": list(PRIMARY_AGGREGATES),
        "aggregate_count": len(PRIMARY_AGGREGATES),
    }


def events() -> dict[str, Any]:
    return {
        "present_required": True,
        "core_events": [dict(e) for e in CORE_EVENTS],
        "core_event_count": len(CORE_EVENTS),
    }


def cqrs() -> dict[str, Any]:
    return {
        "present_required": True,
        "commands": list(COMMANDS), "command_count": len(COMMANDS),
        "queries": list(QUERIES), "query_count": len(QUERIES),
    }


def integration() -> dict[str, Any]:
    return dict(INTEGRATION)


def microservices() -> dict[str, Any]:
    return {
        "present_required": True,
        "services": [dict(s) for s in MICROSERVICES],
        "service_count": len(MICROSERVICES),
    }


def roadmap() -> dict[str, Any]:
    return dict(ROADMAP) | {"phase_count": len(ROADMAP["phases"])}


def production_readiness() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "verdict": "ENTERPRISE_GRADE", "foundation_for_p219_u": True}


def catalog() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID, "adr": ADR, "sor": SOR, "product": PRODUCT, "capability": CAPABILITY,
        "primary_capability": PRIMARY_CAPABILITY, "principle": PRIMARY_CAPABILITY, "fabric": FABRIC,
        "foundation_gate": FOUNDATION_GATE, "mission_gate": MISSION_GATE,
        "strategy_gate": STRATEGY_GATE, "domain_gate": DOMAIN_GATE,
        "planetary_gate": PLANETARY_GATE, "ai_os_gate": AI_OS_GATE,
        "simulation_gate": SIMULATION_GATE, "resources_gate": RESOURCES_GATE,
        "economy_gate": ECONOMY_GATE, "knowledge_gate": KNOWLEDGE_GATE,
        "human_gate": HUMAN_GATE, "governance_gate": GOVERNANCE_GATE,
        "innovation_gate": INNOVATION_GATE, "security_gate": SECURITY_GATE,
        "sustainability_gate": SUSTAINABILITY_GATE, "prosperity_gate": PROSPERITY_GATE,
        "collaboration_gate": COLLABORATION_GATE, "consciousness_gate": CONSCIOUSNESS_GATE,
        "evolution_gate": EVOLUTION_GATE, "futures_gate": FUTURES_GATE,
        "intelligence_nexus_gate": INTELLIGENCE_NEXUS_GATE, "space_gate": SPACE_GATE,
        "bio_gate": BIO_GATE, "robotics_gate": ROBOTICS_GATE,
        "quantum_gate": QUANTUM_GATE, "ai_gate": AI_GATE,
        "builds_on": [
            "P219-S", "P219-R", "P219-Q", "P219-P", "P219-O", "P219-N", "P219-M", "P219-L", "P219-K", "P219-J",
            "P219-I", "P219-H", "P219-G", "P219-F", "P219-E", "P219-D", "P219-C", "P219-B", "P219-A", "P219",
            "P218-Z", "P218", "P217-Z", "P216-Z", "P215-Z", "P214-Z", "ADR-572",
        ],
        "vision": vision_pack(),
        "architecture": architecture(),
        "intel_gov_platform": intel_gov_platform(),
        "alignment": alignment(),
        "policy_intelligence": policy_intelligence(),
        "trust_compliance": trust_compliance(),
        "decision_assurance": decision_assurance(),
        "digital_twin": digital_twin(),
        "agents": agents(),
        "knowledge_graph": knowledge_graph(),
        "bounded_contexts": bounded_contexts(),
        "aggregates": aggregates(),
        "events": events(),
        "cqrs": cqrs(),
        "integration": integration(),
        "microservices": microservices(),
        "roadmap": roadmap(),
        "production_readiness": production_readiness(),
        "civilization_intelligence_governance_platform_present_required": True,
        "strategic_alignment_platform_present_required": True,
        "enterprise_policy_intelligence_present_required": True,
        "trust_and_compliance_framework_present_required": True,
        "decision_assurance_platform_present_required": True,
        "governance_knowledge_graph_present_required": True,
        "governance_digital_twin_present_required": True,
        "meos_civilization_governance_alignment_intelligence_core_present_required": True,
        "intelligence_governance_event_architecture_present_required": True,
        "intelligence_governance_cqrs_model_present_required": True,
        "meos_intelligence_governance_integration_map_present_required": True,
        "never_replace_p219_foundation": True,
        "never_replace_p219_a_mission": True,
        "never_replace_p219_b_strategy": True,
        "never_replace_p219_c_domain": True,
        "never_replace_p219_d_planetary": True,
        "never_replace_p219_e_ai_os": True,
        "never_replace_p219_f_simulation": True,
        "never_replace_p219_g_resources": True,
        "never_replace_p219_h_economy": True,
        "never_replace_p219_i_knowledge": True,
        "never_replace_p219_j_human": True,
        "never_replace_p219_k_governance": True,
        "never_replace_p219_l_innovation": True,
        "never_replace_p219_m_security": True,
        "never_replace_p219_n_sustainability": True,
        "never_replace_p219_o_prosperity": True,
        "never_replace_p219_p_collaboration": True,
        "never_replace_p219_q_consciousness": True,
        "never_replace_p219_r_evolution": True,
        "never_replace_p219_s_futures": True,
        "never_replace_core_platform": True,
        "never_replace_ai_platform": True,
        "never_replace_policy_engine": True,
        "never_replace_workflow": True,
        "never_replace_audit": True,
        "never_replace_compliance_platform": True,
        "never_replace_p215_z": True,
        "never_replace_p216_z": True,
        "never_replace_biotechnology": True,
        "never_replace_space": True,
        "never_replace_p218_z_intelligence_nexus": True,
        "never_merge_p218_t_space_civilization": True,
        "never_cross_context_aggregate_imports": True,
        "never_opaque_unexplainable_governance_decisions": True,
        "never_ungated_governance_decision_execution": True,
        "never_skip_ethical_governance_assurance": True,
        "never_skip_human_authority_governance": True,
        "never_violate_human_sovereignty_governance": True,
        "never_bypass_trusted_governance_validation": True,
        "never_bypass_human_supervision_governance": True,
        "never_bypass_human_accountability": True,
        "no_module_local_llm": True,
        "sibling_civilization_intelligence_governance_bc_forbidden": True,
        "api_prefix": f"{API_PREFIX}/intelligence-governance",
        "forbidden_sibling_bc": [
            "civilization_intelligence_governance_platform",
            "strategic_alignment_platform_bc",
            "global_decision_assurance_bc",
        ],
        "foundation_for_p219_u": True,
    }


def intel_gov_surface() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "routes": [
        "GET /civilization/intelligence-governance",
        "GET /civilization/intelligence-governance/architecture",
        "GET /civilization/intelligence-governance/platform",
        "GET /civilization/intelligence-governance/alignment",
        "GET /civilization/intelligence-governance/policy",
        "GET /civilization/intelligence-governance/trust",
        "GET /civilization/intelligence-governance/decision-assurance",
        "GET /civilization/intelligence-governance/digital-twin",
        "GET /civilization/intelligence-governance/knowledge-graph",
        "GET /civilization/intelligence-governance/agents",
        "GET /civilization/intelligence-governance/bounded-contexts",
        "GET /civilization/intelligence-governance/aggregates",
        "GET /civilization/intelligence-governance/events",
        "GET /civilization/intelligence-governance/cqrs",
        "GET /civilization/intelligence-governance/integration",
        "GET /civilization/intelligence-governance/readiness",
    ]}
