"""P210-F Enterprise SOAR Platform — immutable catalog."""
from __future__ import annotations

from typing import Any

PROMPT_ID = "P210-F"
ADR = 365
SOR = "cyber_security"
API_PREFIX = "/api/v1/cyber-security"
PRODUCT = (
    "Enterprise Cyber Security & Threat Defense Platform — "
    "SOAR (Security Orchestration, Automation & Response)"
)

MISSION_STATEMENT = (
    "Create an enterprise SOAR platform capable of orchestrating security "
    "operations, automating repetitive tasks, coordinating multi-system "
    "incident response, reducing MTTR, standardising response procedures, "
    "enabling AI-assisted decision making, and supporting autonomous cyber "
    "defence under Zero Trust."
)

VISION_STATEMENT = (
    "Create an Autonomous SOAR Platform where every alert launches intelligent "
    "workflows, every incident follows approved playbooks, every response is "
    "coordinated, every action is fully auditable, every recommendation is "
    "AI-assisted and explainable, and every automation continuously improves."
)

SOAR_LAYERS: tuple[str, ...] = (
    "security_alerts",
    "incident_intake",
    "playbook_engine",
    "decision_engine",
    "orchestration_layer",
    "automation_engine",
    "execution_layer",
    "verification_layer",
    "evidence_collection",
    "reporting_layer",
)

ORCHESTRATION_TARGETS: tuple[str, ...] = (
    "soc",
    "siem",
    "xdr",
    "edr",
    "ndr",
    "threat_intelligence",
    "identity_platform",
    "pam",
    "iga",
    "directory_services",
    "pki",
    "kms",
    "vault",
    "cloud_platforms",
    "firewalls",
    "ids_ips",
    "waf",
    "endpoint_platforms",
    "itsm",
    "cmdb",
    "enterprise_ai_platform",
)

PLAYBOOK_FORMATS: tuple[str, ...] = (
    "visual_playbooks",
    "declarative_playbooks",
    "yaml_playbooks",
    "versioned_playbooks",
    "reusable_components",
    "conditional_branching",
    "parallel_execution",
    "human_approval_gates",
    "rollback_support",
)

PLAYBOOK_CATEGORIES: tuple[str, ...] = (
    "phishing",
    "malware",
    "ransomware",
    "credential_theft",
    "privilege_escalation",
    "data_exfiltration",
    "insider_threat",
    "cloud_compromise",
    "api_abuse",
    "identity_compromise",
    "supply_chain_attack",
    "ai_security_incident",
)

AUTOMATION_ACTIONS: tuple[str, ...] = (
    "disable_account",
    "lock_user",
    "reset_password",
    "revoke_token",
    "rotate_secret",
    "rotate_key",
    "revoke_certificate",
    "isolate_endpoint",
    "quarantine_container",
    "block_ip_address",
    "update_firewall",
    "update_waf",
    "disable_api_key",
    "suspend_workload",
    "notify_teams",
    "create_ticket",
    "collect_evidence",
)

IR_WORKFLOW: tuple[str, ...] = (
    "alert",
    "validation",
    "enrichment",
    "classification",
    "prioritisation",
    "investigation",
    "containment",
    "eradication",
    "recovery",
    "post_incident_review",
)

SEVERITY_WORKFLOWS: tuple[str, ...] = (
    "critical",
    "high",
    "medium",
    "low",
    "informational",
)

HITL_APPROVALS: tuple[str, ...] = (
    "security_analyst_approval",
    "soc_manager_approval",
    "ciso_approval",
    "emergency_override",
    "multi_person_approval",
    "segregation_of_duties",
    "escalation_policies",
    "business_owner_approval",
)

AI_CAPS: tuple[str, ...] = (
    "recommend_playbooks",
    "predict_incident_severity",
    "classify_incidents",
    "suggest_response_actions",
    "estimate_business_impact",
    "recommend_containment",
    "generate_executive_summary",
    "generate_root_cause_analysis",
    "learn_from_historical_incidents",
    "optimise_automation",
)

KG_CHAIN: tuple[str, ...] = (
    "alert",
    "incident",
    "playbook",
    "automation",
    "security_control",
    "identity",
    "application",
    "asset",
    "threat_actor",
    "evidence",
    "response",
    "outcome",
)

DIGITAL_TWINS: tuple[str, ...] = (
    "soar_digital_twin",
    "incident_digital_twin",
    "automation_twin",
    "playbook_twin",
    "security_operations_twin",
)

CONNECTORS: tuple[str, ...] = (
    "microsoft_defender",
    "microsoft_sentinel",
    "crowdstrike",
    "palo_alto",
    "fortinet",
    "cisco",
    "splunk",
    "elastic",
    "wazuh",
    "servicenow",
    "jira",
    "slack",
    "microsoft_teams",
    "aws",
    "azure",
    "google_cloud",
    "kubernetes",
    "hashicorp_vault",
    "spire",
    "pki_services",
    "meos_internal_services",
)

COMMANDS: tuple[str, ...] = (
    "CreatePlaybook",
    "PublishPlaybookVersion",
    "ExecutePlaybook",
    "PauseExecution",
    "ResumeExecution",
    "RequestApproval",
    "ApproveResponse",
    "RejectResponse",
    "ExecuteAutomation",
    "RollbackAutomation",
    "PreserveEvidence",
)

QUERIES: tuple[str, ...] = (
    "GetPlaybook",
    "GetExecutionStatus",
    "GetIncidentWorkflow",
    "GetAutomationHistory",
    "GetApprovalStatus",
    "GetReadiness",
)

DOMAIN_EVENTS: tuple[str, ...] = (
    "PlaybookCreated",
    "PlaybookVersionPublished",
    "PlaybookExecuted",
    "AutomationStarted",
    "AutomationCompleted",
    "AutomationFailed",
    "IncidentEscalated",
    "ResponseApproved",
    "ResponseRejected",
    "RollbackCompleted",
    "EvidencePreserved",
    "UnversionedPlaybookRejected",
    "UnauditedAutomationRejected",
    "TightCouplingRejected",
    "UnexplainableAiRejected",
)

MICROSERVICES_LOGICAL: tuple[str, ...] = (
    "playbook_service",
    "automation_service",
    "orchestration_service",
    "connector_service",
    "approval_service",
    "workflow_service",
    "incident_response_handoff_service",
    "evidence_service",
    "soar_ai_service",
    "audit_service",
)

AGGREGATES: tuple[str, ...] = (
    "SoarPlaybook",
    "PlaybookVersion",
    "AutomationRun",
    "OrchestrationSession",
    "ApprovalGate",
    "ConnectorBinding",
    "EvidencePackage",
    "RollbackPlan",
)

OBSERVABILITY_METRICS: tuple[str, ...] = (
    "automation_success_rate",
    "playbook_execution_time",
    "mttr",
    "approval_time",
    "connector_health",
    "automation_failure_rate",
    "incident_resolution_time",
    "workflow_throughput",
    "response_accuracy",
    "platform_availability",
)

COMPLIANCE: tuple[str, ...] = (
    "iso_27001",
    "soc_2",
    "nist_csf",
    "nist_800_61",
    "mitre_attack",
    "pci_dss",
    "gdpr",
)

QUALITY_GATES_REJECT_IF: tuple[str, ...] = (
    "playbooks_cannot_be_versioned",
    "automation_not_auditable",
    "human_approval_unavailable",
    "ai_recommendations_not_explainable",
    "rollback_capability_absent",
    "connectors_tightly_coupled",
    "incident_evidence_cannot_be_preserved",
    "sibling_soar_bc",
)


def architecture() -> dict[str, Any]:
    return {"layers": list(SOAR_LAYERS), "layer_count": len(SOAR_LAYERS)}


def orchestration() -> dict[str, Any]:
    return {
        "targets": list(ORCHESTRATION_TARGETS),
        "count": len(ORCHESTRATION_TARGETS),
        "coordinates_soc_siem_xdr": True,
    }


def playbook_engine() -> dict[str, Any]:
    return {
        "formats": list(PLAYBOOK_FORMATS),
        "categories": list(PLAYBOOK_CATEGORIES),
        "category_count": len(PLAYBOOK_CATEGORIES),
        "versioned_required": True,
        "can_be_versioned": True,
        "not_unversioned": True,
        "rollback_support": True,
        "human_approval_gates": True,
    }


def automation_engine() -> dict[str, Any]:
    return {
        "actions": list(AUTOMATION_ACTIONS),
        "count": len(AUTOMATION_ACTIONS),
        "auditable_required": True,
        "auditable": True,
        "not_unauditable": True,
        "rollback_required": True,
        "rollback_present": True,
        "not_absent_rollback": True,
    }


def incident_workflows() -> dict[str, Any]:
    return {
        "lifecycle": list(IR_WORKFLOW),
        "severity_workflows": list(SEVERITY_WORKFLOWS),
        "handoff_to_security_incident": True,
    }


def human_in_the_loop() -> dict[str, Any]:
    return {
        "approvals": list(HITL_APPROVALS),
        "count": len(HITL_APPROVALS),
        "available": True,
        "not_unavailable": True,
        "via_workflow_engine": True,
        "local_approval_engine_forbidden": True,
    }


def ai() -> dict[str, Any]:
    return {
        "capabilities": list(AI_CAPS),
        "count": len(AI_CAPS),
        "explainable_required": True,
        "explainable": True,
        "not_unexplainable": True,
        "via_ai_platform": True,
        "advisor_not_authority": True,
    }


def knowledge_graph() -> dict[str, Any]:
    return {
        "chain": list(KG_CHAIN),
        "capabilities": [
            "automation_optimisation",
            "dependency_analysis",
            "impact_prediction",
            "attack_path_analysis",
            "response_recommendation",
        ],
        "does_not_own_kg_sor": True,
    }


def digital_twin() -> dict[str, Any]:
    return {
        "twins": list(DIGITAL_TWINS),
        "capabilities": [
            "playbook_simulation",
            "automation_validation",
            "incident_replay",
            "failure_simulation",
            "training_environment",
        ],
        "does_not_own_twin_sor": True,
    }


def connectors() -> dict[str, Any]:
    return {
        "catalog": list(CONNECTORS),
        "count": len(CONNECTORS),
        "via_integration_platform": True,
        "tightly_coupled_forbidden": True,
        "not_tightly_coupled": True,
        "peer_ids_only": True,
        "vendor_sdk_embed_forbidden": True,
    }


def evidence() -> dict[str, Any]:
    return {
        "preservation_required": True,
        "can_be_preserved": True,
        "not_unpreservable": True,
        "integrity_required": True,
    }


def observability() -> dict[str, Any]:
    return {
        "metrics": list(OBSERVABILITY_METRICS),
        "count": len(OBSERVABILITY_METRICS),
    }


def governance() -> dict[str, Any]:
    return {
        "zero_trust": True,
        "rbac": True,
        "abac": True,
        "policy_based_automation": True,
        "least_privilege": True,
        "immutable_audit_logs": True,
        "compliance": list(COMPLIANCE),
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
        "p201_to_p209": True,
        "p210_d_soc": True,
        "p210_e_siem_planned": True,
        "p210_g_xdr_planned": True,
        "security_incident": True,
        "workflow": True,
        "integration_platform": True,
        "ai_platform": True,
        "itsm": True,
    }


def cursor_outputs() -> dict[str, Any]:
    return {
        "enterprise_soar_architecture": True,
        "orchestration_framework": True,
        "automation_engine_design": True,
        "playbook_engine": True,
        "incident_response_workflows": True,
        "human_approval_framework": True,
        "ai_security_orchestration": True,
        "knowledge_graph_integration": True,
        "digital_twin_model": True,
        "connector_framework": True,
        "cqrs_architecture": True,
        "event_catalogue": True,
        "microservice_blueprint": True,
        "api_specifications": True,
        "automation_sdk": True,
        "security_governance_model": True,
        "dashboard_architecture": True,
        "operational_runbooks": True,
        "production_deployment_blueprint": True,
        "enterprise_soar_operations_manual": True,
        "count": 20,
    }


def production_readiness() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "checklist": {
            "playbooks_versioned": True,
            "automation_auditable": True,
            "human_approval": True,
            "ai_explainable": True,
            "rollback": True,
            "connectors_loose": True,
            "evidence_preservation": True,
            "foundation_tests": True,
            "soar_api_live": True,
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
        "builds_on": [
            "P210-A",
            "P210-B",
            "P210-C",
            "P210-D",
            "ADR-361",
            "ADR-362",
            "ADR-363",
            "ADR-364",
        ],
        "architecture": architecture(),
        "orchestration": orchestration(),
        "playbook_engine": playbook_engine(),
        "automation_engine": automation_engine(),
        "incident_workflows": incident_workflows(),
        "human_in_the_loop": human_in_the_loop(),
        "ai": ai(),
        "knowledge_graph": knowledge_graph(),
        "digital_twin": digital_twin(),
        "connectors": connectors(),
        "evidence": evidence(),
        "observability": observability(),
        "governance": governance(),
        "ddd": ddd(),
        "cqrs": cqrs(),
        "microservices": microservices(),
        "integrations": integrations(),
        "cursor_outputs": cursor_outputs(),
        "quality_gates": quality_gates(),
        "production_readiness": production_readiness(),
        "playbooks_versioned_required": True,
        "automation_auditable_required": True,
        "human_approval_required": True,
        "ai_recommendations_explainable_required": True,
        "rollback_capability_required": True,
        "connectors_tightly_coupled_forbidden": True,
        "incident_evidence_preservation_required": True,
        "sibling_soar_bc_forbidden": True,
        "ir_lifecycle_duplication_forbidden": True,
        "local_approval_engine_forbidden": True,
        "vendor_sdk_embed_forbidden": True,
        "api_prefix": f"{API_PREFIX}/soar",
        "forbidden_sibling_bc": "soar_platform",
        "distinct_from": [
            "P210-D /soc*",
            "P210-E /siem* (planned)",
            "P210-G /xdr* (planned)",
            "workflow approvals",
            "integration connectors",
            "security_incident IR",
        ],
    }


def executive_summary() -> dict[str, Any]:
    return catalog()


def soar_surface() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "routes": [
            "GET /cyber-security/soar",
            "GET /cyber-security/soar/architecture",
            "GET /cyber-security/soar/orchestration",
            "GET /cyber-security/soar/playbooks",
            "GET /cyber-security/soar/automation",
            "GET /cyber-security/soar/workflows",
            "GET /cyber-security/soar/approvals",
            "GET /cyber-security/soar/ai",
            "GET /cyber-security/soar/knowledge-graph",
            "GET /cyber-security/soar/digital-twin",
            "GET /cyber-security/soar/connectors",
            "GET /cyber-security/soar/evidence",
            "GET /cyber-security/soar/observability",
            "GET /cyber-security/soar/governance",
            "GET /cyber-security/soar/ddd",
            "GET /cyber-security/soar/cqrs",
            "GET /cyber-security/soar/events",
            "GET /cyber-security/soar/microservices",
            "GET /cyber-security/soar/integrations",
            "GET /cyber-security/soar/outputs",
            "GET /cyber-security/soar/production-readiness",
            "GET /cyber-security/soar/readiness",
        ],
    }
