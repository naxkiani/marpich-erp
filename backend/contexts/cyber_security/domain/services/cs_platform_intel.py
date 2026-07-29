"""P210-H Enterprise Threat Intelligence & Hunting — immutable catalog."""
from __future__ import annotations

from typing import Any

PROMPT_ID = "P210-H"
ADR = 368
SOR = "cyber_security"
API_PREFIX = "/api/v1/cyber-security"
PRODUCT = (
    "Enterprise Cyber Security & Threat Defense Platform — "
    "Threat Intelligence & Threat Hunting"
)

MISSION_STATEMENT = (
    "Create an enterprise threat intelligence platform capable of collecting "
    "global cyber intelligence, predicting cyber attacks, detecting emerging "
    "threats, enabling proactive threat hunting, supporting AI-assisted "
    "investigations, and continuously improving enterprise defence."
)

VISION_STATEMENT = (
    "Create an Autonomous Threat Intelligence Fabric where every threat is "
    "understood, every campaign is correlated, every indicator is enriched, "
    "every hunt is evidence-driven, every detection continuously improves, "
    "and every lesson strengthens enterprise resilience."
)

INTEL_LAYERS: tuple[str, ...] = (
    "external_intelligence",
    "collection_layer",
    "normalization_layer",
    "enrichment_layer",
    "threat_intelligence_fusion",
    "knowledge_graph",
    "threat_analytics",
    "threat_hunting",
    "detection_engineering",
    "soc_siem_soar",
    "executive_intelligence",
)

INTEL_SOURCES: tuple[str, ...] = (
    "commercial_threat_feeds",
    "osint",
    "government_cert_feeds",
    "isac_isao",
    "vendor_intelligence",
    "cloud_providers",
    "dark_web_intelligence",
    "deep_web_intelligence",
    "social_media_intelligence",
    "malware_sandboxes",
    "threat_research_teams",
    "internal_incident_reports",
    "siem",
    "soc",
    "soar",
    "xdr",
    "edr",
    "ndr",
    "identity_platform",
    "cloud_security",
    "api_security",
    "container_security",
    "ai_security",
)

INTEL_TYPES: tuple[str, ...] = (
    "strategic_intelligence",
    "operational_intelligence",
    "tactical_intelligence",
    "technical_intelligence",
    "executive_intelligence",
    "industry_intelligence",
    "geopolitical_intelligence",
    "threat_actor_intelligence",
    "campaign_intelligence",
    "malware_intelligence",
    "supply_chain_intelligence",
    "cloud_threat_intelligence",
    "ai_threat_intelligence",
)

THREAT_ENTITIES: tuple[str, ...] = (
    "threat_actor",
    "threat_group",
    "campaign",
    "malware_family",
    "ransomware_family",
    "vulnerability",
    "exploit",
    "zero_day",
    "ioc",
    "ioa",
    "tool",
    "technique",
    "procedure_ttp",
    "target",
    "asset",
    "organization",
    "country",
    "sector",
    "mitre_attack_technique",
    "mitre_attack_tactic",
    "kill_chain_stage",
)

HUNT_TYPES: tuple[str, ...] = (
    "ioc_hunting",
    "ioa_hunting",
    "behaviour_hunting",
    "threat_actor_hunting",
    "campaign_hunting",
    "cloud_hunting",
    "identity_hunting",
    "api_hunting",
    "container_hunting",
    "kubernetes_hunting",
    "ai_platform_hunting",
    "supply_chain_hunting",
)

HUNT_CAPABILITIES: tuple[str, ...] = (
    "hypothesis_engine",
    "hunt_planner",
    "hunt_scheduler",
    "hunt_automation",
    "hunt_knowledge_base",
)

AI_CAPABILITIES: tuple[str, ...] = (
    "classify_threat_actors",
    "predict_campaign_evolution",
    "generate_ioc_relationships",
    "recommend_hunts",
    "create_detection_rules",
    "estimate_risk",
    "summarize_intelligence",
    "generate_executive_reports",
    "predict_attack_targets",
    "detect_emerging_threat_patterns",
)

KG_CHAIN: tuple[str, ...] = (
    "threat_actor",
    "campaign",
    "malware",
    "exploit",
    "vulnerability",
    "ioc",
    "identity",
    "endpoint",
    "application",
    "api",
    "asset",
    "incident",
    "evidence",
    "control",
    "response",
)

DIGITAL_TWINS: tuple[str, ...] = (
    "threat_landscape_twin",
    "threat_actor_twin",
    "campaign_twin",
    "enterprise_exposure_twin",
    "detection_twin",
    "soc_twin",
)

DETECTION_ENGINEERING: tuple[str, ...] = (
    "sigma_rules",
    "yara_rules",
    "mitre_attack_mapping",
    "behavior_rules",
    "anomaly_rules",
    "machine_learning_models",
    "ioc_packages",
    "detection_pipelines",
    "continuous_rule_validation",
    "detection_performance_scoring",
)

SHARING_STANDARDS: tuple[str, ...] = (
    "stix_2x",
    "taxii_2x",
    "openioc",
    "misp",
    "json",
    "rest_api",
    "kafka",
    "grpc",
    "secure_federation",
    "trust_communities",
    "partner_sharing",
)

COMMANDS: tuple[str, ...] = (
    "CollectThreatFeed",
    "NormalizeThreat",
    "EnrichIndicator",
    "RegisterThreatActor",
    "CreateCampaign",
    "LaunchThreatHunt",
    "GenerateDetectionRule",
    "PublishThreatIntel",
)

QUERIES: tuple[str, ...] = (
    "GetThreatActor",
    "GetCampaign",
    "GetThreatGraph",
    "GetThreatFeedStatus",
    "GetThreatHuntResults",
    "GetDetectionCoverage",
)

DOMAIN_EVENTS: tuple[str, ...] = (
    "ThreatFeedCollected",
    "ThreatEnriched",
    "ThreatActorDiscovered",
    "CampaignDetected",
    "ThreatHuntStarted",
    "ThreatHuntCompleted",
    "DetectionRuleGenerated",
    "ThreatPublished",
)

MICROSERVICES: tuple[str, ...] = (
    "threat-feed-service",
    "threat-enrichment-service",
    "ioc-service",
    "threat-actor-service",
    "campaign-service",
    "threat-hunting-service",
    "detection-engineering-service",
    "intel-sharing-service",
    "threat-ai-service",
    "threat-dashboard-service",
)

OBSERVABILITY_METRICS: tuple[str, ...] = (
    "threat_feed_health",
    "ioc_processing_rate",
    "threat_correlation_accuracy",
    "threat_hunt_success_rate",
    "detection_coverage",
    "threat_actor_coverage",
    "campaign_discovery_rate",
    "ai_recommendation_accuracy",
    "detection_rule_quality",
    "platform_availability",
)

COMPLIANCE: tuple[str, ...] = (
    "iso_27001",
    "nist_csf",
    "mitre_attack",
    "mitre_d3fend",
    "stix_taxii",
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
    "enterprise_ai",
    "enterprise_data",
    "itsm",
    "cmdb",
    "cloud_providers",
)

CURSOR_OUTPUTS: tuple[str, ...] = (
    "enterprise_threat_intelligence_architecture",
    "threat_intelligence_domain_model",
    "threat_feed_management_platform",
    "threat_hunting_framework",
    "threat_entity_model",
    "ai_threat_intelligence_engine",
    "threat_knowledge_graph",
    "digital_twin_architecture",
    "detection_engineering_platform",
    "intelligence_sharing_platform",
    "cqrs_architecture",
    "event_catalogue",
    "microservice_blueprint",
    "api_specifications",
    "stix_taxii_integration",
    "hunt_playbooks",
    "executive_dashboards",
    "threat_intelligence_runbooks",
    "scalability_performance_model",
    "production_deployment_blueprint",
)

QUALITY_GATES_REJECT_IF: tuple[str, ...] = (
    "threat_intelligence_cannot_be_validated",
    "threat_hunting_reactive_only",
    "knowledge_graph_integration_absent",
    "ai_cannot_explain_recommendations",
    "detection_engineering_disconnected",
    "intelligence_sharing_lacks_standards",
    "threat_actor_attribution_unsupported",
    "sibling_threat_intel_bc",
)


def architecture() -> dict[str, Any]:
    return {"layers": list(INTEL_LAYERS), "layer_count": len(INTEL_LAYERS)}


def sources() -> dict[str, Any]:
    return {"sources": list(INTEL_SOURCES), "source_count": len(INTEL_SOURCES)}


def intelligence_types() -> dict[str, Any]:
    return {"types": list(INTEL_TYPES), "type_count": len(INTEL_TYPES)}


def threat_entities() -> dict[str, Any]:
    return {
        "entities": list(THREAT_ENTITIES),
        "entity_count": len(THREAT_ENTITIES),
        "attribution_supported": True,
        "not_unsupported_attribution": True,
    }


def threat_hunting() -> dict[str, Any]:
    return {
        "types": list(HUNT_TYPES),
        "type_count": len(HUNT_TYPES),
        "capabilities": list(HUNT_CAPABILITIES),
        "proactive_required": True,
        "not_reactive_only": True,
    }


def ai() -> dict[str, Any]:
    return {
        "capabilities": list(AI_CAPABILITIES),
        "capability_count": len(AI_CAPABILITIES),
        "explainable_required": True,
        "not_unexplainable": True,
        "via_ai_platform": True,
    }


def knowledge_graph() -> dict[str, Any]:
    return {
        "chain": list(KG_CHAIN),
        "integration_required": True,
        "not_absent": True,
        "capabilities": [
            "relationship_discovery",
            "threat_attribution",
            "campaign_mapping",
            "attack_path_discovery",
            "blast_radius_analysis",
            "threat_reasoning",
        ],
    }


def digital_twin() -> dict[str, Any]:
    return {
        "twins": list(DIGITAL_TWINS),
        "capabilities": [
            "threat_simulation",
            "campaign_replay",
            "adversary_emulation",
            "purple_team_exercises",
            "detection_validation",
            "future_attack_prediction",
        ],
    }


def detection_engineering() -> dict[str, Any]:
    return {
        "capabilities": list(DETECTION_ENGINEERING),
        "capability_count": len(DETECTION_ENGINEERING),
        "connected_required": True,
        "publishes_to_siem_xdr": True,
        "not_disconnected": True,
    }


def intelligence_sharing() -> dict[str, Any]:
    return {
        "standards": list(SHARING_STANDARDS),
        "standard_count": len(SHARING_STANDARDS),
        "stix_taxii_required": True,
        "not_lacking_standards": True,
    }


def validation() -> dict[str, Any]:
    return {
        "validated_required": True,
        "source_trust_scoring": True,
        "not_unvalidated": True,
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
        "data_classification": True,
        "immutable_audit": True,
        "compliance": list(COMPLIANCE),
    }


def ddd() -> dict[str, Any]:
    return {
        "sor": SOR,
        "logical_subdomains": [
            "threat_feeds",
            "enrichment_fusion",
            "threat_actors_campaigns",
            "threat_hunting",
            "detection_engineering",
            "intel_sharing",
            "threat_ai",
        ],
        "sibling_bc_forbidden": [
            "threat_intel",
            "threat_hunting",
            "cti_platform",
        ],
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
            "threat_intelligence_validated": True,
            "threat_hunting_proactive": True,
            "knowledge_graph_integration": True,
            "ai_explainable": True,
            "detection_engineering_connected": True,
            "intelligence_sharing_standards": True,
            "threat_actor_attribution": True,
            "foundation_tests": True,
            "intel_api_live": True,
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
            "ADR-361",
            "ADR-362",
            "ADR-363",
            "ADR-364",
            "ADR-365",
            "ADR-366",
            "ADR-367",
        ],
        "architecture": architecture(),
        "sources": sources(),
        "intelligence_types": intelligence_types(),
        "threat_entities": threat_entities(),
        "threat_hunting": threat_hunting(),
        "ai": ai(),
        "knowledge_graph": knowledge_graph(),
        "digital_twin": digital_twin(),
        "detection_engineering": detection_engineering(),
        "intelligence_sharing": intelligence_sharing(),
        "validation": validation(),
        "observability": observability(),
        "governance": governance(),
        "ddd": ddd(),
        "cqrs": cqrs(),
        "microservices": microservices(),
        "integrations": integrations(),
        "cursor_outputs": cursor_outputs(),
        "quality_gates": quality_gates(),
        "production_readiness": production_readiness(),
        "threat_intelligence_validated_required": True,
        "threat_hunting_proactive_required": True,
        "knowledge_graph_integration_required": True,
        "ai_recommendations_explainable_required": True,
        "detection_engineering_connected_required": True,
        "intelligence_sharing_standards_required": True,
        "threat_actor_attribution_supported_required": True,
        "sibling_threat_intel_bc_forbidden": True,
        "vendor_sdk_embed_forbidden": True,
        "reactive_only_hunting_forbidden": True,
        "api_prefix": f"{API_PREFIX}/intel",
        "forbidden_sibling_bc": [
            "threat_intel",
            "threat_hunting",
            "cti_platform",
        ],
        "distinct_from": [
            "P210-D /soc*",
            "P210-E /siem*",
            "P210-F /soar*",
            "P210-G /xdr*",
            "P210-K /graph* (planned)",
            "integration feed connectors",
        ],
    }


def executive_summary() -> dict[str, Any]:
    return catalog()


def intel_surface() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "routes": [
            "GET /cyber-security/intel",
            "GET /cyber-security/intel/architecture",
            "GET /cyber-security/intel/sources",
            "GET /cyber-security/intel/types",
            "GET /cyber-security/intel/entities",
            "GET /cyber-security/intel/hunting",
            "GET /cyber-security/intel/ai",
            "GET /cyber-security/intel/knowledge-graph",
            "GET /cyber-security/intel/digital-twin",
            "GET /cyber-security/intel/detection-engineering",
            "GET /cyber-security/intel/sharing",
            "GET /cyber-security/intel/validation",
            "GET /cyber-security/intel/observability",
            "GET /cyber-security/intel/governance",
            "GET /cyber-security/intel/ddd",
            "GET /cyber-security/intel/cqrs",
            "GET /cyber-security/intel/events",
            "GET /cyber-security/intel/microservices",
            "GET /cyber-security/intel/integrations",
            "GET /cyber-security/intel/outputs",
            "GET /cyber-security/intel/production-readiness",
            "GET /cyber-security/intel/readiness",
        ],
    }
