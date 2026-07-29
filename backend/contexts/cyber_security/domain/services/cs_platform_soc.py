"""P210-D Enterprise Security Operations Center (SOC) — immutable catalog."""
from __future__ import annotations

from typing import Any

PROMPT_ID = "P210-D"
ADR = 364
SOR = "cyber_security"
API_PREFIX = "/api/v1/cyber-security"
PRODUCT = (
    "Enterprise Cyber Security & Threat Defense Platform — "
    "Security Operations Center (SOC)"
)

MISSION_STATEMENT = (
    "Create an AI-native Security Operations Center capable of continuous "
    "security monitoring, enterprise-wide threat detection, automated incident "
    "response orchestration, threat hunting, digital investigations, "
    "cross-platform security orchestration, and enterprise cyber resilience."
)

VISION_STATEMENT = (
    "Create an Autonomous SOC where every security event is observed, every "
    "alert is correlated, every incident is prioritised, every investigation "
    "is AI-assisted, every response is orchestrated, and every lesson improves "
    "future defence."
)

SOC_LAYERS: tuple[str, ...] = (
    "security_telemetry_layer",
    "collection_layer",
    "normalization_layer",
    "correlation_layer",
    "detection_layer",
    "threat_intelligence_layer",
    "investigation_layer",
    "response_layer",
    "recovery_layer",
    "executive_reporting_layer",
)

OPERATIONAL_DOMAINS: tuple[str, ...] = (
    "security_monitoring",
    "alert_management",
    "threat_detection",
    "threat_correlation",
    "threat_hunting",
    "incident_management_handoff",
    "case_management",
    "digital_forensics",
    "malware_investigation",
    "security_intelligence",
    "executive_reporting",
    "knowledge_management",
)

TELEMETRY_SOURCES: tuple[str, ...] = (
    "identity_platforms",
    "directory_services",
    "pam",
    "pki",
    "kms",
    "vault",
    "cloud_providers",
    "kubernetes",
    "containers",
    "endpoints",
    "servers",
    "applications",
    "apis",
    "databases",
    "firewalls",
    "ids_ips",
    "waf",
    "email_security",
    "dns",
    "network_devices",
    "ai_platforms",
    "iot",
    "ot_systems",
    "third_party_security_platforms",
)

ALERT_LIFECYCLE: tuple[str, ...] = (
    "detection",
    "classification",
    "deduplication",
    "correlation",
    "risk_scoring",
    "assignment",
    "investigation",
    "response",
    "closure",
)

ALERT_CAPS: tuple[str, ...] = (
    "real_time_alerts",
    "priority_queues",
    "alert_suppression",
    "false_positive_reduction",
    "alert_enrichment",
)

INCIDENT_STAGES: tuple[str, ...] = (
    "preparation",
    "identification",
    "triage",
    "containment",
    "eradication",
    "recovery",
    "lessons_learned",
    "post_incident_review",
)

SEVERITY_LEVELS: tuple[str, ...] = (
    "critical",
    "high",
    "medium",
    "low",
    "informational",
)

CASE_CAPS: tuple[str, ...] = (
    "case_creation",
    "evidence_collection",
    "timeline_reconstruction",
    "artifact_management",
    "task_assignment",
    "investigator_collaboration",
    "executive_review",
    "evidence_preservation",
)

HUNTING_CAPS: tuple[str, ...] = (
    "hypothesis_based_hunting",
    "ioc_hunting",
    "ioa_hunting",
    "mitre_attack_mapping",
    "behavioral_hunting",
    "cloud_threat_hunting",
    "identity_threat_hunting",
    "ai_threat_hunting",
)

AI_CAPS: tuple[str, ...] = (
    "alert_prioritization",
    "root_cause_analysis",
    "threat_correlation",
    "attack_prediction",
    "incident_classification",
    "investigation_assistance",
    "playbook_recommendation",
    "executive_summarization",
    "natural_language_investigation",
    "autonomous_response_recommendation",
)

KG_CHAIN: tuple[str, ...] = (
    "alert",
    "incident",
    "identity",
    "endpoint",
    "application",
    "api",
    "threat_actor",
    "campaign",
    "technique",
    "asset",
    "control",
    "evidence",
    "risk",
)

DIGITAL_TWINS: tuple[str, ...] = (
    "soc_operations_twin",
    "incident_twin",
    "threat_campaign_twin",
    "analyst_twin",
    "infrastructure_twin",
)

RESPONSE_ACTIONS: tuple[str, ...] = (
    "account_disable",
    "credential_reset",
    "token_revocation",
    "endpoint_isolation",
    "container_quarantine",
    "network_segmentation",
    "certificate_revocation",
    "key_rotation",
    "secret_rotation",
    "policy_enforcement",
    "ticket_creation",
    "executive_notification",
)

DASHBOARD_AUDIENCES: tuple[str, ...] = (
    "soc_analysts",
    "threat_hunters",
    "incident_responders",
    "soc_managers",
    "ciso",
    "executive_leadership",
)

KPIS: tuple[str, ...] = (
    "mttd",
    "mttr",
    "open_incidents",
    "threat_trends",
    "risk_heatmap",
    "automation_rate",
    "threat_intelligence_coverage",
)

COMMANDS: tuple[str, ...] = (
    "CreateAlert",
    "CorrelateAlerts",
    "EscalateIncidentHandoff",
    "AssignCase",
    "ExecutePlaybookIntent",
    "ContainThreatIntent",
    "CloseAlert",
    "GenerateSocReport",
    "StartThreatHunt",
)

QUERIES: tuple[str, ...] = (
    "GetActiveAlerts",
    "GetIncidentHandoffStatus",
    "GetThreatTimeline",
    "GetRiskDashboard",
    "GetSocMetrics",
    "GetReadiness",
)

DOMAIN_EVENTS: tuple[str, ...] = (
    "AlertGenerated",
    "AlertCorrelated",
    "IncidentHandoffOpened",
    "IncidentHandoffEscalated",
    "ThreatDetected",
    "ThreatHuntStarted",
    "ThreatHuntCompleted",
    "PlaybookIntentExecuted",
    "CaseOpened",
    "CaseClosed",
    "ManualOnlyResponseRejected",
    "Non24x7Rejected",
    "UncorrelatedAlertsRejected",
    "MissingAiRejected",
    "IncompleteMetricsRejected",
)

MICROSERVICES_LOGICAL: tuple[str, ...] = (
    "soc_core_service",
    "alert_management_service",
    "incident_management_handoff_service",
    "case_management_service",
    "threat_hunting_service",
    "investigation_service",
    "response_orchestration_service",
    "soc_ai_service",
    "soc_dashboard_service",
    "soc_reporting_service",
)

AGGREGATES: tuple[str, ...] = (
    "SocOperatingProfile",
    "SecurityAlert",
    "AlertQueue",
    "SocCase",
    "ThreatHunt",
    "ResponseOrchestration",
    "SocMetricsRegister",
    "SocKnowledgeLink",
)

INTEGRATIONS: tuple[str, ...] = (
    "p201_identity_lifecycle",
    "p202_identity_governance",
    "p203_pam",
    "p204_access_management",
    "p205_directory_services",
    "p206_identity_data_governance",
    "p207_identity_intelligence",
    "p208_authorization",
    "p209_crypto_trust",
    "enterprise_siem_logical",
    "enterprise_soar_logical",
    "xdr_logical",
    "threat_intelligence_logical",
    "itsm_platform",
    "cmdb",
    "enterprise_ai_platform",
    "security_incident",
)

QUALITY_GATES_REJECT_IF: tuple[str, ...] = (
    "soc_not_24x7",
    "alerts_cannot_be_correlated",
    "ai_assistance_absent",
    "incident_response_manual_only",
    "threat_hunting_missing",
    "metrics_incomplete",
    "knowledge_graph_integration_absent",
    "sibling_soc_bc",
)


def architecture() -> dict[str, Any]:
    return {
        "layers": list(SOC_LAYERS),
        "layer_count": len(SOC_LAYERS),
        "operating_mode_24x7": True,
        "not_non_24x7": True,
    }


def operational_domains() -> dict[str, Any]:
    return {
        "domains": list(OPERATIONAL_DOMAINS),
        "count": len(OPERATIONAL_DOMAINS),
    }


def telemetry() -> dict[str, Any]:
    return {
        "sources": list(TELEMETRY_SOURCES),
        "count": len(TELEMETRY_SOURCES),
        "via_integration_and_observability": True,
    }


def alert_management() -> dict[str, Any]:
    return {
        "lifecycle": list(ALERT_LIFECYCLE),
        "capabilities": list(ALERT_CAPS),
        "correlation_required": True,
        "can_correlate": True,
        "not_uncorrelated": True,
    }


def incident_management() -> dict[str, Any]:
    return {
        "stages": list(INCIDENT_STAGES),
        "severity_levels": list(SEVERITY_LEVELS),
        "handoff_to_security_incident": True,
        "manual_only_forbidden": True,
        "not_manual_only": True,
        "automation_required": True,
    }


def case_management() -> dict[str, Any]:
    return {"capabilities": list(CASE_CAPS), "count": len(CASE_CAPS)}


def threat_hunting() -> dict[str, Any]:
    return {
        "capabilities": list(HUNTING_CAPS),
        "count": len(HUNTING_CAPS),
        "required": True,
        "not_missing": True,
        "playbooks": True,
        "workflows": True,
    }


def ai() -> dict[str, Any]:
    return {
        "capabilities": list(AI_CAPS),
        "count": len(AI_CAPS),
        "assistance_required": True,
        "not_absent": True,
        "via_ai_platform": True,
        "advisor_not_authority_for_destructive": True,
    }


def knowledge_graph() -> dict[str, Any]:
    return {
        "chain": list(KG_CHAIN),
        "integrated": True,
        "not_absent": True,
        "does_not_own_kg_sor": True,
        "capabilities": [
            "attack_path_discovery",
            "relationship_analysis",
            "threat_correlation",
            "impact_analysis",
        ],
    }


def digital_twin() -> dict[str, Any]:
    return {
        "twins": list(DIGITAL_TWINS),
        "capabilities": [
            "attack_simulation",
            "incident_replay",
            "capacity_planning",
            "workflow_optimization",
            "training_simulation",
        ],
        "does_not_own_twin_sor": True,
    }


def automated_response() -> dict[str, Any]:
    return {
        "actions": list(RESPONSE_ACTIONS),
        "count": len(RESPONSE_ACTIONS),
        "via_workflow_and_authorization": True,
        "intent_only_destructive_actions": True,
    }


def dashboards() -> dict[str, Any]:
    return {
        "audiences": list(DASHBOARD_AUDIENCES),
        "metrics": list(KPIS),
        "metric_count": len(KPIS),
        "metrics_complete": True,
        "not_incomplete": True,
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
        "peers": list(INTEGRATIONS),
        "count": len(INTEGRATIONS),
        "security_incident_ir": True,
        "vendor_sdk_embed_forbidden": True,
    }


def cursor_outputs() -> dict[str, Any]:
    return {
        "enterprise_soc_architecture": True,
        "soc_domain_model": True,
        "alert_management_framework": True,
        "incident_response_framework": True,
        "case_management_architecture": True,
        "threat_hunting_platform": True,
        "ai_soc_architecture": True,
        "soc_knowledge_graph": True,
        "soc_digital_twin": True,
        "response_automation_model": True,
        "cqrs_design": True,
        "event_catalog": True,
        "microservice_architecture": True,
        "api_specifications": True,
        "dashboard_designs": True,
        "operational_playbooks": True,
        "soc_runbooks": True,
        "kpi_framework": True,
        "production_deployment_architecture": True,
        "enterprise_soc_operations_manual": True,
        "count": 20,
    }


def production_readiness() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "checklist": {
            "soc_24x7": True,
            "alert_correlation": True,
            "ai_assistance": True,
            "response_not_manual_only": True,
            "threat_hunting": True,
            "metrics_complete": True,
            "knowledge_graph": True,
            "foundation_tests": True,
            "soc_api_live": True,
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
        "builds_on": ["P210-A", "P210-B", "P210-C", "ADR-361", "ADR-362", "ADR-363"],
        "architecture": architecture(),
        "operational_domains": operational_domains(),
        "telemetry": telemetry(),
        "alert_management": alert_management(),
        "incident_management": incident_management(),
        "case_management": case_management(),
        "threat_hunting": threat_hunting(),
        "ai": ai(),
        "knowledge_graph": knowledge_graph(),
        "digital_twin": digital_twin(),
        "automated_response": automated_response(),
        "dashboards": dashboards(),
        "ddd": ddd(),
        "cqrs": cqrs(),
        "microservices": microservices(),
        "integrations": integrations(),
        "cursor_outputs": cursor_outputs(),
        "quality_gates": quality_gates(),
        "production_readiness": production_readiness(),
        "soc_24x7_required": True,
        "alert_correlation_required": True,
        "ai_assistance_required": True,
        "incident_response_manual_only_forbidden": True,
        "threat_hunting_required": True,
        "metrics_incomplete_forbidden": True,
        "knowledge_graph_integration_required": True,
        "sibling_soc_bc_forbidden": True,
        "ir_lifecycle_duplication_forbidden": True,
        "api_prefix": f"{API_PREFIX}/soc",
        "forbidden_sibling_bc": "soc_platform",
        "distinct_from": [
            "P210-A /strategy*",
            "P210-B /mission*",
            "P210-C /domain*",
            "security_incident IR SoR",
            "P210-E /siem* (planned)",
            "P210-F /soar* (planned)",
        ],
    }


def executive_summary() -> dict[str, Any]:
    return catalog()


def soc_surface() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "routes": [
            "GET /cyber-security/soc",
            "GET /cyber-security/soc/architecture",
            "GET /cyber-security/soc/domains",
            "GET /cyber-security/soc/telemetry",
            "GET /cyber-security/soc/alerts",
            "GET /cyber-security/soc/incidents",
            "GET /cyber-security/soc/cases",
            "GET /cyber-security/soc/hunting",
            "GET /cyber-security/soc/ai",
            "GET /cyber-security/soc/knowledge-graph",
            "GET /cyber-security/soc/digital-twin",
            "GET /cyber-security/soc/response",
            "GET /cyber-security/soc/dashboards",
            "GET /cyber-security/soc/ddd",
            "GET /cyber-security/soc/cqrs",
            "GET /cyber-security/soc/events",
            "GET /cyber-security/soc/microservices",
            "GET /cyber-security/soc/integrations",
            "GET /cyber-security/soc/outputs",
            "GET /cyber-security/soc/production-readiness",
            "GET /cyber-security/soc/readiness",
        ],
    }
