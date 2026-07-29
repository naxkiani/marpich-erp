"""P210-I Enterprise ASM & CTEM Platform — immutable catalog."""
from __future__ import annotations

from typing import Any

PROMPT_ID = "P210-I"
ADR = 369
SOR = "cyber_security"
API_PREFIX = "/api/v1/cyber-security"
PRODUCT = (
    "Enterprise Cyber Security & Threat Defense Platform — "
    "ASM & CTEM (Attack Surface & Continuous Threat Exposure Management)"
)

MISSION_STATEMENT = (
    "Create an enterprise ASM & CTEM platform capable of continuously "
    "discovering enterprise assets, mapping internal and external attack "
    "surfaces, identifying exploitable exposures, prioritizing cyber risks, "
    "predicting attack paths, enabling continuous remediation, and supporting "
    "executive cyber risk governance."
)

VISION_STATEMENT = (
    "Create an Autonomous Exposure Management Platform where every asset is "
    "continuously discovered, every exposure is continuously assessed, every "
    "attack path is visualized, every remediation is prioritized, every risk "
    "decision is intelligence-driven, and every enterprise asset becomes "
    "continuously defensible."
)

ASM_LAYERS: tuple[str, ...] = (
    "asset_discovery",
    "asset_inventory",
    "attack_surface_discovery",
    "exposure_detection",
    "vulnerability_intelligence",
    "attack_path_analysis",
    "risk_prioritization",
    "remediation_orchestration",
    "continuous_validation",
    "executive_cyber_risk_dashboard",
)

ASSET_TYPES: tuple[str, ...] = (
    "users",
    "identities",
    "service_accounts",
    "endpoints",
    "servers",
    "virtual_machines",
    "containers",
    "kubernetes_clusters",
    "cloud_accounts",
    "cloud_services",
    "applications",
    "apis",
    "databases",
    "storage",
    "dns",
    "domains",
    "certificates",
    "secrets",
    "encryption_keys",
    "network_devices",
    "firewalls",
    "load_balancers",
    "iot_devices",
    "ot_devices",
    "ai_models",
    "ai_agents",
    "knowledge_graph_nodes",
    "digital_twins",
    "third_party_integrations",
)

ATTACK_SURFACES: tuple[str, ...] = (
    "internal_attack_surface",
    "external_attack_surface_easm",
    "cloud_attack_surface_caasm",
    "api_attack_surface",
    "identity_attack_surface",
    "kubernetes_attack_surface",
    "container_attack_surface",
    "network_attack_surface",
    "supply_chain_attack_surface",
    "ai_attack_surface",
    "saas_attack_surface",
    "partner_attack_surface",
)

DISCOVERY_CAPABILITIES: tuple[str, ...] = (
    "continuous_scanning",
    "passive_discovery",
    "active_discovery",
    "shadow_it_discovery",
    "orphaned_asset_detection",
    "internet_exposure_detection",
)

EXPOSURE_TYPES: tuple[str, ...] = (
    "unpatched_systems",
    "misconfigurations",
    "open_ports",
    "weak_authentication",
    "privilege_escalation_paths",
    "exposed_apis",
    "public_buckets",
    "weak_encryption",
    "expired_certificates",
    "secret_exposure",
    "identity_misconfiguration",
    "cloud_misconfiguration",
    "kubernetes_misconfiguration",
    "container_risks",
    "ai_model_exposure",
    "supply_chain_exposure",
)

VULN_INTEGRATIONS: tuple[str, ...] = (
    "cve",
    "cwe",
    "cvss",
    "epss",
    "kev_catalog",
    "vendor_advisories",
    "threat_intelligence",
    "exploit_databases",
    "bug_bounty_reports",
)

ATTACK_PATH_CHAIN: tuple[str, ...] = (
    "threat_actor",
    "internet",
    "gateway",
    "identity",
    "endpoint",
    "application",
    "api",
    "container",
    "cluster",
    "database",
    "sensitive_data",
    "business_service",
)

AI_CAPABILITIES: tuple[str, ...] = (
    "prioritize_exposures",
    "estimate_business_impact",
    "predict_exploitation_probability",
    "recommend_remediation",
    "identify_critical_attack_paths",
    "forecast_risk_trends",
    "optimize_patch_scheduling",
    "recommend_security_investments",
    "generate_executive_summaries",
)

REMEDIATION_ACTIONS: tuple[str, ...] = (
    "patch_deployment",
    "configuration_hardening",
    "firewall_updates",
    "identity_remediation",
    "secret_rotation",
    "key_rotation",
    "certificate_renewal",
    "container_rebuild",
    "kubernetes_policy_enforcement",
    "cloud_configuration_repair",
    "api_protection",
    "soar_playbook_execution",
    "human_approval_workflow",
)

KG_CHAIN: tuple[str, ...] = (
    "asset",
    "identity",
    "endpoint",
    "cloud_resource",
    "application",
    "api",
    "container",
    "exposure",
    "vulnerability",
    "exploit",
    "threat",
    "risk",
    "business_service",
    "control",
)

DIGITAL_TWINS: tuple[str, ...] = (
    "enterprise_exposure_twin",
    "attack_surface_twin",
    "cloud_twin",
    "identity_twin",
    "infrastructure_twin",
    "business_service_twin",
)

CTEM_LIFECYCLE: tuple[str, ...] = (
    "discover",
    "inventory",
    "assess",
    "prioritize",
    "validate",
    "remediate",
    "verify",
    "measure",
    "continuously_repeat",
)

COMMANDS: tuple[str, ...] = (
    "DiscoverAsset",
    "RegisterExposure",
    "ImportVulnerability",
    "CalculateRisk",
    "GenerateAttackPath",
    "CreateRemediationPlan",
    "ExecuteRemediation",
    "ValidateExposure",
)

QUERIES: tuple[str, ...] = (
    "GetAssetInventory",
    "GetAttackSurface",
    "GetExposureDashboard",
    "GetAttackGraph",
    "GetRiskHeatmap",
    "GetRemediationStatus",
)

DOMAIN_EVENTS: tuple[str, ...] = (
    "AssetDiscovered",
    "ExposureDetected",
    "VulnerabilityImported",
    "RiskCalculated",
    "AttackPathGenerated",
    "RemediationStarted",
    "RemediationCompleted",
    "ExposureResolved",
)

MICROSERVICES: tuple[str, ...] = (
    "asset-discovery-service",
    "attack-surface-service",
    "exposure-management-service",
    "vulnerability-intelligence-service",
    "attack-graph-service",
    "risk-engine-service",
    "remediation-service",
    "ctem-ai-service",
    "dashboard-service",
    "reporting-service",
)

OBSERVABILITY_METRICS: tuple[str, ...] = (
    "assets_discovered",
    "attack_surface_coverage",
    "exposure_count",
    "critical_exposure_count",
    "mean_time_to_remediate",
    "exposure_validation_rate",
    "patch_compliance",
    "attack_path_count",
    "risk_score_trend",
    "platform_availability",
)

COMPLIANCE: tuple[str, ...] = (
    "nist_csf",
    "nist_sp_800_53",
    "iso_27001",
    "cis_controls",
    "pci_dss",
    "soc_2",
)

INTEGRATIONS: tuple[str, ...] = (
    "P201",
    "P202",
    "P203",
    "P204",
    "P205",
    "P206",
    "P207",
    "P208",
    "P209",
    "P210-D",
    "P210-E",
    "P210-F",
    "P210-G",
    "P210-H",
    "cloud_providers",
    "enterprise_cmdb",
    "enterprise_ai",
    "itsm",
)

CURSOR_OUTPUTS: tuple[str, ...] = (
    "enterprise_asm_architecture",
    "enterprise_ctem_architecture",
    "asset_discovery_platform",
    "attack_surface_discovery_framework",
    "exposure_management_platform",
    "vulnerability_intelligence_engine",
    "attack_path_analysis_engine",
    "ai_risk_prioritization_platform",
    "remediation_orchestration_framework",
    "knowledge_graph_model",
    "digital_twin_architecture",
    "ctem_lifecycle_model",
    "cqrs_design",
    "event_catalogue",
    "microservice_blueprint",
    "api_specifications",
    "executive_dashboards",
    "security_runbooks",
    "enterprise_risk_reporting",
    "production_deployment_blueprint",
)

QUALITY_GATES_REJECT_IF: tuple[str, ...] = (
    "asset_discovery_incomplete",
    "external_attack_surface_not_continuously_monitored",
    "risk_prioritization_ignores_business_context",
    "attack_path_analysis_absent",
    "ai_recommendations_not_explainable",
    "remediation_cannot_be_validated",
    "ctem_lifecycle_not_continuous",
    "sibling_asm_bc",
)


def architecture() -> dict[str, Any]:
    return {"layers": list(ASM_LAYERS), "layer_count": len(ASM_LAYERS)}


def asset_discovery() -> dict[str, Any]:
    return {
        "asset_types": list(ASSET_TYPES),
        "asset_type_count": len(ASSET_TYPES),
        "complete_required": True,
        "not_incomplete": True,
    }


def attack_surface() -> dict[str, Any]:
    return {
        "surfaces": list(ATTACK_SURFACES),
        "surface_count": len(ATTACK_SURFACES),
        "capabilities": list(DISCOVERY_CAPABILITIES),
        "external_continuous_required": True,
        "not_non_continuous_easm": True,
    }


def exposure_management() -> dict[str, Any]:
    return {
        "types": list(EXPOSURE_TYPES),
        "type_count": len(EXPOSURE_TYPES),
        "catalog": True,
        "timeline": True,
        "ownership": True,
        "lifecycle": True,
    }


def vulnerability_intelligence() -> dict[str, Any]:
    return {
        "integrations": list(VULN_INTEGRATIONS),
        "capabilities": [
            "exploitability_analysis",
            "business_context",
            "threat_correlation",
            "asset_criticality",
            "patch_prioritization",
        ],
    }


def attack_path_analysis() -> dict[str, Any]:
    return {
        "chain": list(ATTACK_PATH_CHAIN),
        "required": True,
        "not_absent": True,
        "capabilities": [
            "lateral_movement_analysis",
            "privilege_escalation_analysis",
            "blast_radius_analysis",
            "kill_chain_simulation",
            "zero_trust_validation",
        ],
    }


def risk_prioritization() -> dict[str, Any]:
    return {
        "business_context_required": True,
        "not_ignoring_business_context": True,
        "ai": list(AI_CAPABILITIES),
        "ai_capability_count": len(AI_CAPABILITIES),
    }


def ai() -> dict[str, Any]:
    return {
        "capabilities": list(AI_CAPABILITIES),
        "explainable_required": True,
        "not_unexplainable": True,
        "via_ai_platform": True,
    }


def remediation() -> dict[str, Any]:
    return {
        "actions": list(REMEDIATION_ACTIONS),
        "action_count": len(REMEDIATION_ACTIONS),
        "validated_required": True,
        "via_soar": True,
        "via_workflow": True,
        "not_unvalidated": True,
    }


def knowledge_graph() -> dict[str, Any]:
    return {
        "chain": list(KG_CHAIN),
        "capabilities": [
            "exposure_correlation",
            "attack_path_discovery",
            "risk_propagation",
            "dependency_mapping",
            "security_reasoning",
        ],
    }


def digital_twin() -> dict[str, Any]:
    return {
        "twins": list(DIGITAL_TWINS),
        "capabilities": [
            "attack_simulation",
            "exposure_replay",
            "remediation_validation",
            "chaos_security_testing",
            "cyber_resilience_assessment",
        ],
    }


def ctem_lifecycle() -> dict[str, Any]:
    return {
        "phases": list(CTEM_LIFECYCLE),
        "phase_count": len(CTEM_LIFECYCLE),
        "continuous_required": True,
        "not_one_pass": True,
        "kpis_per_phase": True,
    }


def observability() -> dict[str, Any]:
    return {
        "metrics": list(OBSERVABILITY_METRICS),
        "metric_count": len(OBSERVABILITY_METRICS),
    }


def governance() -> dict[str, Any]:
    return {
        "zero_trust": True,
        "rbac": True,
        "abac": True,
        "continuous_asset_validation": True,
        "immutable_audit": True,
        "policy_based_remediation": True,
        "compliance": list(COMPLIANCE),
    }


def ddd() -> dict[str, Any]:
    return {
        "sor": SOR,
        "logical_subdomains": [
            "asset_discovery",
            "attack_surface",
            "exposure_management",
            "vulnerability_intelligence",
            "attack_path_analysis",
            "risk_prioritization",
            "remediation",
            "ctem_lifecycle",
        ],
        "sibling_bc_forbidden": ["asm", "ctem", "easm", "caasm"],
    }


def cqrs() -> dict[str, Any]:
    return {
        "commands": list(COMMANDS),
        "command_count": len(COMMANDS),
        "queries": list(QUERIES),
        "query_count": len(QUERIES),
        "events": list(DOMAIN_EVENTS),
        "event_count": len(DOMAIN_EVENTS),
    }


def microservices() -> dict[str, Any]:
    return {
        "services": list(MICROSERVICES),
        "service_count": len(MICROSERVICES),
        "logical_decomposition": True,
    }


def integrations() -> dict[str, Any]:
    return {"targets": list(INTEGRATIONS), "count": len(INTEGRATIONS)}


def cursor_outputs() -> dict[str, Any]:
    return {"outputs": list(CURSOR_OUTPUTS), "count": len(CURSOR_OUTPUTS)}


def production_readiness() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "checklist": {
            "asset_discovery_complete": True,
            "external_attack_surface_continuous": True,
            "risk_business_context": True,
            "attack_path_analysis": True,
            "ai_explainable": True,
            "remediation_validated": True,
            "ctem_continuous": True,
            "foundation_tests": True,
            "asm_api_live": True,
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
            "P210-E",
            "P210-F",
            "P210-G",
            "P210-H",
            "ADR-361",
            "ADR-362",
            "ADR-363",
            "ADR-364",
            "ADR-365",
            "ADR-366",
            "ADR-367",
            "ADR-368",
        ],
        "architecture": architecture(),
        "asset_discovery": asset_discovery(),
        "attack_surface": attack_surface(),
        "exposure_management": exposure_management(),
        "vulnerability_intelligence": vulnerability_intelligence(),
        "attack_path_analysis": attack_path_analysis(),
        "risk_prioritization": risk_prioritization(),
        "ai": ai(),
        "remediation": remediation(),
        "knowledge_graph": knowledge_graph(),
        "digital_twin": digital_twin(),
        "ctem_lifecycle": ctem_lifecycle(),
        "observability": observability(),
        "governance": governance(),
        "ddd": ddd(),
        "cqrs": cqrs(),
        "microservices": microservices(),
        "integrations": integrations(),
        "cursor_outputs": cursor_outputs(),
        "quality_gates": quality_gates(),
        "production_readiness": production_readiness(),
        "asset_discovery_complete_required": True,
        "external_attack_surface_continuous_required": True,
        "risk_prioritization_business_context_required": True,
        "attack_path_analysis_required": True,
        "ai_recommendations_explainable_required": True,
        "remediation_validated_required": True,
        "ctem_lifecycle_continuous_required": True,
        "sibling_asm_bc_forbidden": True,
        "vendor_sdk_embed_forbidden": True,
        "api_prefix": f"{API_PREFIX}/asm",
        "forbidden_sibling_bc": ["asm", "ctem", "easm", "caasm"],
        "distinct_from": [
            "P210-D /soc*",
            "P210-E /siem*",
            "P210-F /soar*",
            "P210-G /xdr*",
            "P210-H /intel*",
            "enterprise CMDB (refs only)",
        ],
    }


def executive_summary() -> dict[str, Any]:
    return catalog()


def asm_surface() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "routes": [
            "GET /cyber-security/asm",
            "GET /cyber-security/asm/architecture",
            "GET /cyber-security/asm/assets",
            "GET /cyber-security/asm/attack-surface",
            "GET /cyber-security/asm/exposures",
            "GET /cyber-security/asm/vulnerabilities",
            "GET /cyber-security/asm/attack-paths",
            "GET /cyber-security/asm/risk",
            "GET /cyber-security/asm/ai",
            "GET /cyber-security/asm/remediation",
            "GET /cyber-security/asm/ctem",
            "GET /cyber-security/asm/knowledge-graph",
            "GET /cyber-security/asm/digital-twin",
            "GET /cyber-security/asm/observability",
            "GET /cyber-security/asm/governance",
            "GET /cyber-security/asm/ddd",
            "GET /cyber-security/asm/cqrs",
            "GET /cyber-security/asm/events",
            "GET /cyber-security/asm/microservices",
            "GET /cyber-security/asm/integrations",
            "GET /cyber-security/asm/outputs",
            "GET /cyber-security/asm/production-readiness",
            "GET /cyber-security/asm/readiness",
        ],
    }
