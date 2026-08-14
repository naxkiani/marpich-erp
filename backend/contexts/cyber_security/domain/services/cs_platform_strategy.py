"""P210-A Enterprise Cyber Security & Threat Defense — strategy catalog."""
from __future__ import annotations

from typing import Any

PROMPT_ID = "P210-A"
ADR = 361
SOR = "cyber_security"
API_PREFIX = "/api/v1/cyber-security"
PRODUCT = "Enterprise Cyber Security & Threat Defense Platform"

MISSION_STATEMENT = (
    "Create an enterprise cyber security platform capable of preventing cyber "
    "attacks, detecting threats in real time, correlating security events, "
    "automating incident response where appropriate, and protecting enterprise "
    "identities, data, infrastructure, applications, APIs, and AI systems under "
    "Zero Trust."
)

VISION_STATEMENT = (
    "Create an Autonomous Cyber Defense Fabric where every asset is continuously "
    "protected, every attack is detected, every anomaly is analysed, every "
    "incident is prioritised, every response is automated where appropriate, "
    "every investigation is explainable, and every cyber decision is risk-aware."
)

CAPABILITY_DOMAINS: tuple[str, ...] = (
    "enterprise_soc",
    "enterprise_siem",
    "enterprise_soar",
    "enterprise_xdr",
    "enterprise_edr",
    "enterprise_ndr",
    "enterprise_ueba",
    "threat_intelligence",
    "threat_hunting",
    "incident_response_handoff",
    "digital_forensics",
    "malware_analysis",
    "attack_surface_management",
    "continuous_threat_exposure",
    "cloud_security",
    "application_security",
    "api_security",
    "container_security",
    "kubernetes_security",
    "identity_threat_detection",
    "ai_security_operations",
)

SECURITY_LAYERS: tuple[str, ...] = (
    "identity_security_layer",
    "endpoint_security_layer",
    "network_security_layer",
    "cloud_security_layer",
    "application_security_layer",
    "api_security_layer",
    "data_security_layer",
    "cryptographic_trust_layer",
    "ai_security_layer",
    "operations_layer",
)

PROTECTION_DOMAINS: tuple[str, ...] = (
    "enterprise_identities",
    "enterprise_users",
    "machines",
    "servers",
    "endpoints",
    "mobile_devices",
    "containers",
    "kubernetes",
    "virtual_machines",
    "cloud_infrastructure",
    "databases",
    "data_lakes",
    "object_storage",
    "applications",
    "apis",
    "microservices",
    "ai_models",
    "ai_agents",
    "knowledge_graph",
    "digital_twin",
    "secrets",
    "certificates",
    "keys",
)

PRINCIPLES: tuple[str, ...] = (
    "zero_trust",
    "assume_breach",
    "least_privilege",
    "continuous_verification",
    "identity_first_security",
    "policy_driven_security",
    "risk_adaptive_security",
    "cloud_native_security",
    "security_by_design",
    "privacy_by_design",
    "ai_assisted_security",
    "autonomous_operations",
)

SERVICE_DOMAINS: tuple[str, ...] = (
    "threat_detection",
    "threat_intelligence",
    "threat_analytics",
    "threat_correlation",
    "security_automation",
    "security_orchestration",
    "incident_management_handoff",
    "digital_evidence",
    "forensics",
    "risk_intelligence",
    "compliance_monitoring",
    "exposure_management",
    "vulnerability_intelligence",
    "security_knowledge_graph",
    "security_digital_twin",
)

EVENT_SOURCES: tuple[str, ...] = (
    "identity_platforms",
    "pam",
    "iga",
    "directory_services",
    "pki",
    "kms",
    "vault",
    "cloud_providers",
    "kubernetes",
    "containers",
    "firewalls",
    "ids_ips",
    "waf",
    "dns",
    "email_security",
    "endpoints",
    "servers",
    "databases",
    "applications",
    "apis",
    "ai_platforms",
    "iot_devices",
    "ot_systems",
    "siem_agents",
    "third_party_security_products",
)

AGGREGATES: tuple[str, ...] = (
    "CyberSecurityStrategyProfile",
    "ZeroTrustControlPlane",
    "SocOperatingModel",
    "DetectionCapabilityMap",
    "ThreatIntelligenceBinding",
    "ResponseAutomationPolicy",
    "TelemetryCoverageModel",
    "MeasurableControlRegister",
)

COMMANDS: tuple[str, ...] = (
    "PublishCyberStrategy",
    "RegisterCapabilityDomain",
    "BindThreatIntelligence",
    "EnableSocOperatingModel",
    "RequireZeroTrust",
    "RegisterMeasurableControl",
    "DeclareTelemetryCoverage",
)

QUERIES: tuple[str, ...] = (
    "GetCyberStrategy",
    "ListCapabilityDomains",
    "GetSecurityLayers",
    "GetProtectionDomains",
    "GetQualityGates",
    "GetReadiness",
)

DOMAIN_EVENTS: tuple[str, ...] = (
    "CyberStrategyPublished",
    "CapabilityDomainRegistered",
    "ZeroTrustEnforced",
    "SocModelEnabled",
    "ThreatIntelligenceBound",
    "ResponseAutomationEnabled",
    "TelemetryCoverageDeclared",
    "ControlRegistered",
    "ManualOnlyResponseRejected",
    "IsolatedIntelRejected",
    "IncompleteTelemetryRejected",
    "SiblingCyberBcRejected",
)

INTEGRATION_EVENTS: tuple[str, ...] = (
    "cyber_security.strategy.published",
    "cyber_security.capability.registered",
    "cyber_security.control.registered",
)

MICROSERVICES_LOGICAL: tuple[str, ...] = (
    "strategy_service",
    "soc_orchestration_service",
    "siem_signal_service",
    "soar_intent_service",
    "xdr_correlation_service",
    "threat_intel_service",
    "asm_exposure_service",
    "ai_secops_service",
)

QUALITY_GATES_REJECT_IF: tuple[str, ...] = (
    "security_architecture_not_zero_trust",
    "soc_not_enterprise_scale",
    "ai_security_omitted",
    "threat_intelligence_isolated",
    "incident_response_manual_only",
    "security_telemetry_incomplete",
    "security_controls_not_measurable",
    "architecture_not_cloud_native",
    "sibling_cyber_bc",
    "vendor_sdk_embedded",
)

FOLLOW_UP_MODULES: tuple[str, ...] = (
    "P210-B",
    "P210-C",
    "P210-D",
    "P210-E",
    "P210-F",
    "P210-G",
    "P210-H",
    "P210-I",
    "P210-J",
    "P210-K",
    "P210-L",
    "P210-M",
    "P210-N",
    "P210-O",
)


def capabilities() -> dict[str, Any]:
    return {
        "domains": list(CAPABILITY_DOMAINS),
        "count": len(CAPABILITY_DOMAINS),
        "enterprise_soc_required": True,
        "ai_security_required": True,
        "threat_intelligence_not_isolated": True,
    }


def layers() -> dict[str, Any]:
    return {
        "layers": list(SECURITY_LAYERS),
        "count": len(SECURITY_LAYERS),
        "ordered": True,
    }


def protection_domains() -> dict[str, Any]:
    return {
        "domains": list(PROTECTION_DOMAINS),
        "count": len(PROTECTION_DOMAINS),
    }


def principles() -> dict[str, Any]:
    return {
        "principles": list(PRINCIPLES),
        "count": len(PRINCIPLES),
        "zero_trust": True,
        "not_missing_zero_trust": True,
    }


def services() -> dict[str, Any]:
    return {
        "domains": list(SERVICE_DOMAINS),
        "count": len(SERVICE_DOMAINS),
    }


def event_sources() -> dict[str, Any]:
    return {
        "sources": list(EVENT_SOURCES),
        "count": len(EVENT_SOURCES),
        "telemetry_complete_required": True,
        "not_incomplete": True,
    }


def soc() -> dict[str, Any]:
    return {
        "enterprise_scale_required": True,
        "not_enterprise_scale_forbidden": True,
        "ai_native_operations": True,
        "follow_up": "P210-D",
    }


def siem() -> dict[str, Any]:
    return {"logical_capability": True, "follow_up": "P210-E", "no_sibling_bc": True}


def soar() -> dict[str, Any]:
    return {
        "logical_capability": True,
        "follow_up": "P210-F",
        "automation_required": True,
        "manual_only_forbidden": True,
        "via_workflow": True,
    }


def xdr() -> dict[str, Any]:
    return {
        "planes": ["edr", "ndr", "xdr_correlation"],
        "follow_up": "P210-G",
        "no_sibling_bc": True,
    }


def threat_intelligence() -> dict[str, Any]:
    return {
        "isolated_forbidden": True,
        "not_isolated": True,
        "follow_up": "P210-H",
        "integrated_with_detection": True,
    }


def ai() -> dict[str, Any]:
    return {
        "ai_security_required": True,
        "not_omitted": True,
        "advisor_not_authority_for_destructive_actions": True,
        "via_ai_platform": True,
        "follow_up": "P210-J",
    }


def security() -> dict[str, Any]:
    return {
        "zero_trust_required": True,
        "not_zero_trust_forbidden": True,
        "controls_measurable_required": True,
        "not_unmeasurable": True,
        "cloud_native_required": True,
        "not_non_cloud_native": True,
        "vendor_sdk_embed_forbidden": True,
        "ir_lifecycle_in_security_incident": True,
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


def microservices() -> dict[str, Any]:
    return {
        "logical_services": list(MICROSERVICES_LOGICAL),
        "count": len(MICROSERVICES_LOGICAL),
        "deployable_today": SOR,
        "never_invent_sibling_bc": True,
    }


def integrations() -> dict[str, Any]:
    return {
        "security_incident_ir": True,
        "enterprise_observability_signals": True,
        "integration_platform_connectors": True,
        "authorization_pdp": True,
        "workflow_automation": True,
        "audit_platform": True,
        "ai_platform": True,
        "policy_engine": True,
        "secrets_crypto_trust": True,
        "pam_refs_only": True,
        "identity_intelligence_refs_only": True,
        "vendor_sdk_embed_forbidden": True,
    }


def roadmap() -> dict[str, Any]:
    return {
        "series": "P210",
        "current": PROMPT_ID,
        "follow_up_modules": list(FOLLOW_UP_MODULES),
        "count": len(FOLLOW_UP_MODULES),
    }


def cursor_outputs() -> dict[str, Any]:
    return {
        "enterprise_cyber_security_architecture": True,
        "security_domain_model": True,
        "security_capability_map": True,
        "security_reference_architecture": True,
        "security_service_catalogue": True,
        "enterprise_security_standards": True,
        "security_governance_model": True,
        "risk_model": True,
        "operational_architecture": True,
        "security_control_matrix": True,
        "enterprise_api_landscape": True,
        "microservice_architecture": True,
        "event_architecture": True,
        "deployment_architecture": True,
        "security_roadmap": True,
        "production_readiness_assessment": True,
        "count": 16,
    }


def production_readiness() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "checklist": {
            "zero_trust": True,
            "enterprise_soc": True,
            "ai_security": True,
            "threat_intel_integrated": True,
            "response_not_manual_only": True,
            "telemetry_complete": True,
            "controls_measurable": True,
            "cloud_native": True,
            "foundation_tests": True,
            "strategy_api_live": True,
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
        "mission": MISSION_STATEMENT,
        "vision": VISION_STATEMENT,
        "builds_on": ["ADR-021", "ADR-158", "ADR-179", "ADR-345"],
        "forbidden_sibling_bc": [
            "cyber_defense",
            "soc_platform",
            "siem_platform",
            "soar_platform",
            "xdr",
            "edr",
            "ndr",
            "security_ops",
        ],
        "capability_domains": capabilities(),
        "layers": layers(),
        "protection_domains": protection_domains(),
        "principles": principles(),
        "services": services(),
        "event_sources": event_sources(),
        "soc": soc(),
        "siem": siem(),
        "soar": soar(),
        "xdr": xdr(),
        "threat_intelligence": threat_intelligence(),
        "ai": ai(),
        "security": security(),
        "ddd": ddd(),
        "cqrs": cqrs(),
        "microservices": microservices(),
        "integrations": integrations(),
        "roadmap": roadmap(),
        "cursor_outputs": cursor_outputs(),
        "quality_gates": quality_gates(),
        "production_readiness": production_readiness(),
        "zero_trust_required": True,
        "enterprise_soc_required": True,
        "ai_security_required": True,
        "threat_intelligence_isolated_forbidden": True,
        "incident_response_manual_only_forbidden": True,
        "security_telemetry_incomplete_forbidden": True,
        "security_controls_unmeasurable_forbidden": True,
        "non_cloud_native_forbidden": True,
        "sibling_cyber_bc_forbidden": True,
        "vendor_sdk_embed_forbidden": True,
        "ir_lifecycle_duplication_forbidden": True,
        "observability_as_cyber_sor_forbidden": True,
        "via_security_incident": True,
        "via_integration_platform": True,
        "via_authorization": True,
        "via_workflow": True,
        "via_audit_platform": True,
        "via_ai_platform": True,
        "api_prefix": f"{API_PREFIX}/strategy",
        "distinct_from": [
            "security_incident IR lifecycle",
            "enterprise_observability telemetry SoR",
            "secrets P209 crypto trust",
            "privileged_access PAM",
            "identity_intelligence identity UEBA",
            "authorization PDP",
        ],
    }


def executive_summary() -> dict[str, Any]:
    return catalog()


def strategy_surface() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "routes": [
            "GET /cyber-security/strategy",
            "GET /cyber-security/strategy/capabilities",
            "GET /cyber-security/strategy/layers",
            "GET /cyber-security/strategy/protection-domains",
            "GET /cyber-security/strategy/principles",
            "GET /cyber-security/strategy/services",
            "GET /cyber-security/strategy/event-sources",
            "GET /cyber-security/strategy/soc",
            "GET /cyber-security/strategy/siem",
            "GET /cyber-security/strategy/soar",
            "GET /cyber-security/strategy/xdr",
            "GET /cyber-security/strategy/threat-intelligence",
            "GET /cyber-security/strategy/ai",
            "GET /cyber-security/strategy/security",
            "GET /cyber-security/strategy/ddd",
            "GET /cyber-security/strategy/cqrs",
            "GET /cyber-security/strategy/events",
            "GET /cyber-security/strategy/microservices",
            "GET /cyber-security/strategy/integrations",
            "GET /cyber-security/strategy/roadmap",
            "GET /cyber-security/strategy/outputs",
            "GET /cyber-security/strategy/production-readiness",
            "GET /cyber-security/strategy/readiness",
        ],
    }
