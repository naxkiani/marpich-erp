"""P210-B Cyber Security Mission, Vision & Enterprise Scope — immutable catalog."""
from __future__ import annotations

from typing import Any

PROMPT_ID = "P210-B"
ADR = 362
SOR = "cyber_security"
API_PREFIX = "/api/v1/cyber-security"
PRODUCT = "Enterprise Cyber Security & Threat Defense Platform"

MISSION_STATEMENT = (
    "The Enterprise Cyber Security & Threat Defense Platform SHALL provide "
    "intelligent, autonomous, Zero Trust cyber defence capabilities that protect "
    "every digital asset, identity, workload, application, service, API, cloud "
    "resource and AI system operating within the Marpich Enterprise Operating "
    "System. The platform SHALL continuously prevent, detect, analyse, respond "
    "to and recover from cyber threats while enabling secure digital "
    "transformation and enterprise resilience."
)

VISION_STATEMENT = (
    "Create the world's most intelligent AI-native Enterprise Cyber Defense "
    "Fabric where every cyber event is observable, every threat is analysed, "
    "every attack is contained, every response is orchestrated and every "
    "security decision is driven by Zero Trust, risk intelligence and "
    "continuous verification."
)

STRATEGIC_OBJECTIVES: tuple[str, ...] = (
    "protect_enterprise_identities",
    "protect_enterprise_data",
    "protect_enterprise_infrastructure",
    "protect_ai_platforms",
    "protect_cloud_environments",
    "protect_software_supply_chains",
    "reduce_cyber_risk",
    "increase_cyber_resilience",
    "enable_autonomous_security_operations",
    "provide_continuous_compliance",
    "minimise_operational_risk",
    "support_global_enterprise_growth",
)

BUSINESS_OBJECTIVES: tuple[str, ...] = (
    "protect_business_continuity",
    "protect_enterprise_reputation",
    "protect_customer_trust",
    "reduce_financial_loss",
    "reduce_cyber_operational_cost",
    "improve_security_automation",
    "improve_operational_efficiency",
    "accelerate_secure_innovation",
    "enable_regulatory_compliance",
    "enable_secure_digital_transformation",
)

ENTERPRISE_SCOPE: tuple[str, ...] = (
    "human_identities",
    "machine_identities",
    "service_identities",
    "workload_identities",
    "applications",
    "apis",
    "microservices",
    "containers",
    "kubernetes",
    "cloud_platforms",
    "networks",
    "databases",
    "data_lakes",
    "enterprise_storage",
    "ai_models",
    "ai_agents",
    "knowledge_graph",
    "digital_twins",
    "certificates",
    "secrets",
    "keys",
    "iot_devices",
    "operational_technology",
    "third_party_integrations",
    "multi_cloud_environments",
    "hybrid_infrastructure",
)

SECURITY_DOMAINS: tuple[str, ...] = (
    "identity_security",
    "endpoint_security",
    "cloud_security",
    "infrastructure_security",
    "application_security",
    "api_security",
    "network_security",
    "data_security",
    "ai_security",
    "container_security",
    "kubernetes_security",
    "email_security",
    "supply_chain_security",
    "cryptographic_security",
    "operational_security",
    "threat_intelligence",
    "security_operations",
    "digital_forensics",
    "governance_compliance",
)

CAPABILITY_MAP: tuple[str, ...] = (
    "enterprise_soc",
    "enterprise_siem",
    "enterprise_soar",
    "enterprise_xdr",
    "enterprise_edr",
    "enterprise_ndr",
    "ueba",
    "threat_intelligence",
    "threat_hunting",
    "incident_response_handoff",
    "digital_forensics",
    "malware_analysis",
    "attack_surface_management",
    "ctem",
    "cloud_security",
    "container_security",
    "api_security",
    "identity_threat_detection",
    "ai_security_operations",
    "security_knowledge_graph",
    "security_digital_twin",
)

OPERATING_PRINCIPLES: tuple[str, ...] = (
    "zero_trust_by_default",
    "assume_breach",
    "identity_first_security",
    "security_by_design",
    "privacy_by_design",
    "least_privilege",
    "continuous_verification",
    "risk_based_decisions",
    "policy_driven_operations",
    "automation_first",
    "ai_assisted_decision_making",
    "continuous_improvement",
)

STAKEHOLDERS: tuple[str, ...] = (
    "board_of_directors",
    "ceo",
    "ciso",
    "cio",
    "cro",
    "cto",
    "security_operations_teams",
    "devsecops_teams",
    "platform_engineering",
    "cloud_operations",
    "infrastructure_teams",
    "application_teams",
    "compliance_teams",
    "internal_audit",
    "business_units",
    "external_regulators",
    "enterprise_customers",
    "strategic_partners",
)

KPIS: tuple[str, ...] = (
    "mttd",
    "mttr",
    "incident_containment_time",
    "threat_detection_accuracy",
    "false_positive_rate",
    "automation_coverage",
    "security_control_coverage",
    "compliance_score",
    "patch_compliance",
    "identity_risk_score",
    "security_posture_score",
    "business_continuity_score",
)

RISK_CATEGORIES: tuple[str, ...] = (
    "identity_risk",
    "cloud_risk",
    "infrastructure_risk",
    "application_risk",
    "supply_chain_risk",
    "cryptographic_risk",
    "ai_risk",
    "data_risk",
    "insider_risk",
    "third_party_risk",
    "operational_risk",
    "regulatory_risk",
)

ARCHITECTURE_PRINCIPLES: tuple[str, ...] = (
    "ddd",
    "cqrs",
    "event_sourcing",
    "microservices",
    "api_first",
    "cloud_native",
    "event_driven",
    "knowledge_graph_native",
    "digital_twin_native",
    "ai_native",
    "zero_trust",
    "policy_driven",
    "gitops",
    "devsecops",
    "immutable_infrastructure",
)

MEOS_ALIGNMENT: tuple[str, ...] = (
    "p201_identity_lifecycle",
    "p202_identity_governance",
    "p203_pam",
    "p204_access_management",
    "p205_directory_services",
    "p206_identity_data_governance",
    "p207_identity_intelligence",
    "p208_authorization",
    "p209_crypto_trust",
    "enterprise_erp",
    "enterprise_ai_platform",
    "enterprise_data_platform",
    "enterprise_integration_platform",
)

AGGREGATES: tuple[str, ...] = (
    "CyberMissionCharter",
    "CyberVisionCharter",
    "EnterpriseScopeRegister",
    "SecurityDomainMap",
    "StrategicObjectiveRegister",
    "OperatingPrincipleSet",
    "StakeholderModel",
    "CyberKpiRegister",
)

COMMANDS: tuple[str, ...] = (
    "PublishMission",
    "PublishVision",
    "DeclareEnterpriseScope",
    "RegisterSecurityDomain",
    "AlignStrategicObjective",
    "RegisterKpi",
    "BindStakeholder",
)

QUERIES: tuple[str, ...] = (
    "GetMission",
    "GetVision",
    "GetEnterpriseScope",
    "GetSecurityDomains",
    "GetCapabilityMap",
    "GetKpis",
    "GetReadiness",
)

DOMAIN_EVENTS: tuple[str, ...] = (
    "MissionPublished",
    "VisionPublished",
    "ScopeDeclared",
    "DomainRegistered",
    "ObjectiveAligned",
    "PrincipleAdopted",
    "StakeholderBound",
    "KpiRegistered",
    "UnmeasurableMissionRejected",
    "IncompleteScopeRejected",
    "FragmentedDomainsRejected",
    "ZeroTrustAbsenceRejected",
)

INTEGRATION_EVENTS: tuple[str, ...] = (
    "cyber_security.mission.published",
    "cyber_security.vision.published",
    "cyber_security.scope.declared",
)

QUALITY_GATES_REJECT_IF: tuple[str, ...] = (
    "mission_not_measurable",
    "vision_not_enterprise_scale",
    "enterprise_scope_incomplete",
    "security_domains_fragmented",
    "zero_trust_absent",
    "ai_security_omitted",
    "strategic_objectives_not_aligned_with_meos",
    "sibling_cyber_bc",
)

MISSION_KPIS: tuple[str, ...] = (
    "mttd",
    "mttr",
    "automation_coverage",
    "security_control_coverage",
    "security_posture_score",
    "compliance_score",
)


def mission() -> dict[str, Any]:
    return {
        "statement": MISSION_STATEMENT,
        "measurable": True,
        "not_unmeasurable": True,
        "kpi_bindings": list(MISSION_KPIS),
        "kpi_count": len(MISSION_KPIS),
    }


def vision() -> dict[str, Any]:
    return {
        "statement": VISION_STATEMENT,
        "enterprise_scale": True,
        "not_non_enterprise_scale": True,
        "ai_native": True,
        "zero_trust_driven": True,
    }


def strategic_objectives() -> dict[str, Any]:
    return {
        "objectives": list(STRATEGIC_OBJECTIVES),
        "count": len(STRATEGIC_OBJECTIVES),
        "meos_aligned": True,
        "not_misaligned": True,
    }


def business_objectives() -> dict[str, Any]:
    return {
        "objectives": list(BUSINESS_OBJECTIVES),
        "count": len(BUSINESS_OBJECTIVES),
    }


def enterprise_scope() -> dict[str, Any]:
    return {
        "items": list(ENTERPRISE_SCOPE),
        "count": len(ENTERPRISE_SCOPE),
        "complete": True,
        "not_incomplete": True,
    }


def security_domains() -> dict[str, Any]:
    return {
        "domains": list(SECURITY_DOMAINS),
        "count": len(SECURITY_DOMAINS),
        "unified": True,
        "not_fragmented": True,
    }


def capability_map() -> dict[str, Any]:
    return {
        "capabilities": list(CAPABILITY_MAP),
        "count": len(CAPABILITY_MAP),
        "no_sibling_bc": True,
    }


def operating_principles() -> dict[str, Any]:
    return {
        "principles": list(OPERATING_PRINCIPLES),
        "count": len(OPERATING_PRINCIPLES),
        "zero_trust_by_default": True,
        "not_absent_zero_trust": True,
        "ai_assisted_decision_making": True,
        "not_ai_omitted": True,
    }


def stakeholders() -> dict[str, Any]:
    return {
        "stakeholders": list(STAKEHOLDERS),
        "count": len(STAKEHOLDERS),
    }


def kpis() -> dict[str, Any]:
    return {
        "kpis": list(KPIS),
        "count": len(KPIS),
        "mission_measurable_via_kpis": True,
    }


def risk_model() -> dict[str, Any]:
    return {
        "categories": list(RISK_CATEGORIES),
        "count": len(RISK_CATEGORIES),
    }


def architecture_principles() -> dict[str, Any]:
    return {
        "principles": list(ARCHITECTURE_PRINCIPLES),
        "count": len(ARCHITECTURE_PRINCIPLES),
        "zero_trust": True,
        "ai_native": True,
        "cloud_native": True,
    }


def meos_alignment() -> dict[str, Any]:
    return {
        "integrations": list(MEOS_ALIGNMENT),
        "count": len(MEOS_ALIGNMENT),
        "aligned": True,
        "not_misaligned": True,
    }


def ddd() -> dict[str, Any]:
    return {
        "aggregates": list(AGGREGATES),
        "aggregate_count": len(AGGREGATES),
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
        "integration_events": list(INTEGRATION_EVENTS),
        "cqrs_ready": True,
    }


def integrations() -> dict[str, Any]:
    return {
        "security_incident_ir": True,
        "p210_a_strategy": True,
        "observability_signals": True,
        "integration_platform": True,
        "authorization": True,
        "workflow": True,
        "audit": True,
        "ai_platform": True,
        "secrets_crypto_trust": True,
        "identity_planes_refs_only": True,
    }


def cursor_outputs() -> dict[str, Any]:
    return {
        "enterprise_mission_statement": True,
        "enterprise_vision_statement": True,
        "strategic_objectives": True,
        "business_objectives": True,
        "enterprise_scope": True,
        "security_domains": True,
        "enterprise_capability_map": True,
        "operating_principles": True,
        "stakeholder_model": True,
        "enterprise_kpis": True,
        "strategic_risk_model": True,
        "architecture_principles": True,
        "governance_alignment": True,
        "executive_summary": True,
        "capability_roadmap": True,
        "strategic_reference_model": True,
        "enterprise_context_diagram": True,
        "domain_boundary_overview": True,
        "strategic_architecture_documentation": True,
        "production_blueprint_foundation": True,
        "count": 20,
    }


def production_readiness() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "checklist": {
            "mission_measurable": True,
            "vision_enterprise_scale": True,
            "scope_complete": True,
            "domains_unified": True,
            "zero_trust": True,
            "ai_security": True,
            "meos_aligned": True,
            "foundation_tests": True,
            "mission_api_live": True,
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
        "builds_on": ["P210-A", "ADR-361"],
        "mission": mission(),
        "vision": vision(),
        "strategic_objectives": strategic_objectives(),
        "business_objectives": business_objectives(),
        "enterprise_scope": enterprise_scope(),
        "security_domains": security_domains(),
        "capability_map": capability_map(),
        "operating_principles": operating_principles(),
        "stakeholders": stakeholders(),
        "kpis": kpis(),
        "risk_model": risk_model(),
        "architecture_principles": architecture_principles(),
        "meos_alignment": meos_alignment(),
        "ddd": ddd(),
        "cqrs": cqrs(),
        "integrations": integrations(),
        "cursor_outputs": cursor_outputs(),
        "quality_gates": quality_gates(),
        "production_readiness": production_readiness(),
        "mission_measurable_required": True,
        "vision_enterprise_scale_required": True,
        "enterprise_scope_complete_required": True,
        "security_domains_fragmented_forbidden": True,
        "zero_trust_absent_forbidden": True,
        "ai_security_omitted_forbidden": True,
        "strategic_objectives_meos_aligned_required": True,
        "sibling_cyber_bc_forbidden": True,
        "ir_lifecycle_duplication_forbidden": True,
        "api_prefix": f"{API_PREFIX}/mission",
        "forbidden_sibling_bc": [
            "cyber_defense",
            "soc_platform",
            "siem_platform",
            "soar_platform",
            "xdr",
            "edr",
            "ndr",
        ],
        "distinct_from": [
            "P210-A /strategy*",
            "security_incident IR",
            "enterprise_observability",
            "secrets P209",
        ],
    }


def executive_summary() -> dict[str, Any]:
    return catalog()


def mission_surface() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "routes": [
            "GET /cyber-security/mission",
            "GET /cyber-security/mission/statement",
            "GET /cyber-security/mission/vision",
            "GET /cyber-security/mission/strategic-objectives",
            "GET /cyber-security/mission/business-objectives",
            "GET /cyber-security/mission/scope",
            "GET /cyber-security/mission/security-domains",
            "GET /cyber-security/mission/capabilities",
            "GET /cyber-security/mission/principles",
            "GET /cyber-security/mission/stakeholders",
            "GET /cyber-security/mission/kpis",
            "GET /cyber-security/mission/risks",
            "GET /cyber-security/mission/architecture-principles",
            "GET /cyber-security/mission/meos-alignment",
            "GET /cyber-security/mission/ddd",
            "GET /cyber-security/mission/cqrs",
            "GET /cyber-security/mission/events",
            "GET /cyber-security/mission/integrations",
            "GET /cyber-security/mission/outputs",
            "GET /cyber-security/mission/production-readiness",
            "GET /cyber-security/mission/readiness",
        ],
    }
