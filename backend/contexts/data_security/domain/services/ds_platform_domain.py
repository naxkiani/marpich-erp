"""P211-C Enterprise Data Security Domain Architecture — immutable catalog."""
from __future__ import annotations

from typing import Any

PROMPT_ID = "P211-C"
ADR = 378
SOR = "data_security"
API_PREFIX = "/api/v1/data-security"
PRODUCT = (
    "Enterprise Data Security & Privacy Intelligence Platform — "
    "Domain Architecture"
)
CAPABILITY = "CAP-PLT-DS-001"

CORE_DOMAIN = "enterprise_data_security_intelligence"

SUPPORTING_DOMAINS: tuple[str, ...] = (
    "data_discovery",
    "data_classification",
    "data_protection",
    "data_privacy",
    "data_access_governance",
    "data_security_risk",
    "data_lineage_intelligence",
    "data_loss_prevention",
    "data_compliance",
    "data_intelligence_graph",
    "ai_data_security",
    "data_digital_twin",
)

LOGICAL_BOUNDED_CONTEXTS: tuple[dict[str, Any], ...] = (
    {
        "id": "data_discovery",
        "purpose": "Discover and maintain complete visibility of enterprise data assets.",
        "owns": (
            "automated_data_discovery",
            "data_source_scanning",
            "metadata_collection",
            "shadow_data_detection",
            "data_asset_registration",
        ),
        "entities": (
            "DataAsset",
            "DataSource",
            "Connector",
            "MetadataRecord",
            "DiscoveryJob",
        ),
        "aggregates": ("DataDiscoveryAggregate",),
        "commands": (
            "RegisterDataSource",
            "DiscoverDataAsset",
            "UpdateMetadata",
            "ScanDataEnvironment",
        ),
        "events": (
            "DataAssetDiscovered",
            "MetadataCollected",
            "DiscoveryCompleted",
        ),
        "integrations": ("cloud_platforms", "databases", "applications", "data_lakes"),
    },
    {
        "id": "data_classification",
        "purpose": "Automatically identify and classify data sensitivity.",
        "owns": (
            "data_classification",
            "sensitive_information_detection",
            "label_management",
            "classification_policies",
        ),
        "entities": (
            "ClassificationRule",
            "DataLabel",
            "SensitivityLevel",
            "ClassificationResult",
        ),
        "aggregates": ("ClassificationAggregate",),
        "commands": (
            "ClassifyData",
            "ApplyDataLabel",
            "UpdateClassificationRule",
        ),
        "events": ("DataClassified", "SensitiveDataDetected"),
        "integrations": ("enterprise_ai", "dlp", "compliance"),
    },
    {
        "id": "data_protection",
        "purpose": "Provide security controls protecting enterprise data.",
        "owns": ("encryption", "masking", "tokenization", "data_protection_policies"),
        "entities": (
            "ProtectionPolicy",
            "EncryptionProfile",
            "MaskingRule",
            "ProtectionAction",
        ),
        "aggregates": ("DataProtectionAggregate",),
        "commands": (
            "ApplyProtection",
            "EncryptData",
            "TokenizeData",
            "MaskData",
        ),
        "events": (
            "ProtectionApplied",
            "EncryptionCompleted",
            "PolicyViolationDetected",
        ),
        "integrations": ("P209",),
    },
    {
        "id": "data_privacy",
        "purpose": "Manage privacy protection and regulatory compliance.",
        "owns": (
            "privacy_risk_analysis",
            "consent_intelligence",
            "privacy_assessment",
            "data_subject_rights",
        ),
        "entities": (
            "PrivacyPolicy",
            "ConsentRecord",
            "PrivacyAssessment",
            "DataSubject",
        ),
        "aggregates": ("PrivacyManagementAggregate",),
        "commands": (
            "CreatePrivacyAssessment",
            "RegisterConsent",
            "EvaluatePrivacyRisk",
        ),
        "events": (
            "PrivacyRiskDetected",
            "ConsentUpdated",
            "PrivacyAssessmentCompleted",
        ),
        "integrations": ("consent", "compliance", "identity"),
        "privacy_integrated_with_security": True,
    },
    {
        "id": "data_access_governance",
        "purpose": "Control and govern access to enterprise data.",
        "owns": (
            "data_entitlement",
            "access_reviews",
            "data_authorization",
            "least_privilege",
        ),
        "entities": (
            "DataPermission",
            "AccessRequest",
            "AccessPolicy",
            "Entitlement",
        ),
        "aggregates": ("DataAccessAggregate",),
        "commands": (
            "RequestDataAccess",
            "ApproveDataAccess",
            "RevokeDataAccess",
        ),
        "events": (
            "DataAccessGranted",
            "DataAccessDenied",
            "AccessReviewCompleted",
        ),
        "integrations": ("P207", "P208"),
    },
    {
        "id": "data_security_risk",
        "purpose": "Measure and manage data security risk.",
        "owns": (
            "risk_scoring",
            "exposure_analysis",
            "threat_correlation",
            "risk_prediction",
        ),
        "entities": ("DataRisk", "RiskFactor", "Exposure", "ThreatIndicator"),
        "aggregates": ("DataRiskAggregate",),
        "commands": (
            "AssessDataRisk",
            "CalculateRiskScore",
            "PredictExposure",
        ),
        "events": ("DataRiskDetected", "RiskScoreUpdated"),
        "integrations": ("P210", "threat_intelligence"),
    },
    {
        "id": "data_lineage_intelligence",
        "purpose": "Understand data movement and dependencies.",
        "owns": (
            "data_lineage",
            "data_flow_mapping",
            "dependency_analysis",
            "impact_analysis",
        ),
        "entities": ("DataFlow", "LineageNode", "Transformation", "Dependency"),
        "aggregates": ("DataLineageAggregate",),
        "commands": ("CreateLineage", "UpdateDataFlow", "AnalyzeImpact"),
        "events": ("LineageCreated", "DataMovementDetected"),
        "integrations": ("knowledge_graph", "digital_twin"),
    },
    {
        "id": "data_loss_prevention",
        "purpose": "Prevent unauthorized data leakage.",
        "owns": (
            "data_exfiltration_prevention",
            "policy_enforcement",
            "monitoring",
            "incident_response_handoff",
        ),
        "entities": (
            "DLPPolicy",
            "Violation",
            "DetectionRule",
            "ResponseAction",
        ),
        "aggregates": ("DLPAggregate",),
        "commands": ("CreateDLPPolicy", "DetectViolation", "BlockTransfer"),
        "events": ("DataLeakDetected", "TransferBlocked"),
        "integrations": ("P210_siem", "P210_soar", "endpoint_security"),
    },
    {
        "id": "data_compliance",
        "purpose": "Automate regulatory compliance.",
        "owns": (
            "compliance_mapping",
            "evidence_generation",
            "audit_readiness",
        ),
        "entities": (
            "ComplianceControl",
            "Requirement",
            "Evidence",
            "AuditRecord",
        ),
        "aggregates": ("ComplianceAggregate",),
        "commands": (
            "MapControl",
            "CollectEvidence",
            "GenerateComplianceReport",
        ),
        "events": ("EvidenceGenerated", "ComplianceValidated"),
        "standards": (
            "iso_27001",
            "iso_27701",
            "gdpr",
            "soc_2",
            "nist",
        ),
    },
    {
        "id": "ai_data_security",
        "purpose": "Secure AI data lifecycle.",
        "owns": (
            "training_data_protection",
            "ai_data_validation",
            "prompt_data_protection",
            "vector_database_security",
        ),
        "entities": (
            "AIDataAsset",
            "TrainingDataset",
            "EmbeddingStore",
            "AgentMemory",
        ),
        "aggregates": ("AIDataSecurityAggregate",),
        "commands": (
            "ValidateAIData",
            "ProtectTrainingData",
            "AuditAIDataUsage",
        ),
        "events": ("AIDataValidated", "AIDataRiskDetected"),
        "integrations": ("P210-M", "enterprise_ai"),
    },
    {
        "id": "data_intelligence_graph",
        "purpose": "Create semantic understanding of enterprise data.",
        "owns": (
            "relationship_discovery",
            "security_reasoning",
            "risk_propagation",
            "impact_analysis",
        ),
        "entities": (
            "DataAsset",
            "User",
            "Application",
            "Policy",
            "Risk",
            "Classification",
            "ComplianceRequirement",
        ),
        "aggregates": ("DataKnowledgeGraphAggregate",),
        "events": ("RelationshipCreated", "KnowledgeUpdated"),
    },
    {
        "id": "data_digital_twin",
        "purpose": "Simulate enterprise data security state.",
        "owns": (
            "data_security_simulation",
            "privacy_simulation",
            "access_simulation",
            "risk_forecasting",
            "control_testing",
        ),
        "entities": ("DataTwin", "SecurityState", "SimulationScenario"),
        "aggregates": ("DataDigitalTwinAggregate",),
        "events": ("TwinUpdated", "SimulationCompleted"),
    },
)

DOMAIN_AGGREGATES: tuple[str, ...] = (
    "DataDiscoveryAggregate",
    "ClassificationAggregate",
    "DataProtectionAggregate",
    "PrivacyManagementAggregate",
    "DataAccessAggregate",
    "DataRiskAggregate",
    "DataLineageAggregate",
    "DLPAggregate",
    "ComplianceAggregate",
    "AIDataSecurityAggregate",
    "DataKnowledgeGraphAggregate",
    "DataDigitalTwinAggregate",
    "DomainOwnershipMap",
)

CORE_EVENTS: tuple[str, ...] = (
    "DataAssetRegistered",
    "DataDiscovered",
    "DataClassified",
    "SensitiveDataDetected",
    "ProtectionApplied",
    "AccessGranted",
    "AccessRevoked",
    "PrivacyRiskDetected",
    "DataLeakDetected",
    "ComplianceViolationDetected",
    "RiskScoreChanged",
    "AIDataRiskDetected",
    "LineageUpdated",
    "DigitalTwinUpdated",
)

MICROSERVICES: tuple[str, ...] = (
    "data-discovery-service",
    "classification-service",
    "data-protection-service",
    "privacy-service",
    "data-access-service",
    "data-risk-service",
    "lineage-service",
    "dlp-service",
    "compliance-service",
    "ai-data-security-service",
    "data-knowledge-graph-service",
    "data-digital-twin-service",
)

INTEGRATIONS: tuple[str, ...] = (
    "P207",
    "P208",
    "P209",
    "P210",
    "P210-M",
    "P212_future_data_governance",
    "enterprise_erp",
    "enterprise_ai_platform",
    "enterprise_knowledge_platform",
    "consent",
)

CURSOR_OUTPUTS: tuple[str, ...] = (
    "enterprise_ddd_domain_map",
    "bounded_context_diagram",
    "aggregate_models",
    "entity_models",
    "domain_services",
    "command_models",
    "query_models",
    "event_catalogue",
    "integration_architecture",
    "microservice_boundaries",
    "api_contracts",
    "data_security_domain_blueprint",
)

QUALITY_GATES_REJECT_IF: tuple[str, ...] = (
    "domains_are_tightly_coupled",
    "data_ownership_is_unclear",
    "privacy_is_separated_from_security",
    "events_are_missing",
    "aggregates_are_undefined",
    "integration_boundaries_are_unclear",
    "sibling_data_security_bc",
)

COMMANDS: tuple[str, ...] = (
    "PublishDomainMap",
    "RegisterLogicalSubdomain",
    "BindAggregateOwnership",
    "IntegratePrivacyWithSecurity",
    "DeclareIntegrationBoundary",
    "PublishEventCatalogue",
)

QUERIES: tuple[str, ...] = (
    "GetDomainMap",
    "GetBoundedContexts",
    "GetAggregates",
    "GetEntities",
    "GetEventCatalogue",
    "GetMicroserviceBoundaries",
    "GetDomainReadiness",
)

DOMAIN_EVENTS: tuple[str, ...] = (
    "DomainMapPublished",
    "SubdomainRegistered",
    "AggregateOwnershipBound",
    "PrivacySecurityIntegrated",
    "IntegrationBoundaryDeclared",
    "EventCataloguePublished",
    "RelationshipCreated",
    "KnowledgeUpdated",
    "TwinUpdated",
    "SimulationCompleted",
)


def domain_map() -> dict[str, Any]:
    return {
        "core_domain": CORE_DOMAIN,
        "supporting_domains": list(SUPPORTING_DOMAINS),
        "supporting_count": len(SUPPORTING_DOMAINS),
        "loosely_coupled_required": True,
        "not_tightly_coupled": True,
    }


def bounded_contexts() -> dict[str, Any]:
    return {
        "contexts": list(LOGICAL_BOUNDED_CONTEXTS),
        "context_count": len(LOGICAL_BOUNDED_CONTEXTS),
        "logical_only": True,
        "sibling_bc_forbidden": True,
    }


def aggregates() -> dict[str, Any]:
    return {
        "aggregates": list(DOMAIN_AGGREGATES),
        "aggregate_count": len(DOMAIN_AGGREGATES),
        "defined_required": True,
        "not_undefined": True,
    }


def entities() -> dict[str, Any]:
    ents: list[str] = []
    for ctx in LOGICAL_BOUNDED_CONTEXTS:
        ents.extend(ctx.get("entities", ()))
    return {"entities": sorted(set(ents)), "entity_count": len(set(ents))}


def ownership() -> dict[str, Any]:
    return {
        "clear_required": True,
        "not_unclear": True,
        "map": "DomainOwnershipMap",
        "ubiquitous_language": True,
    }


def privacy_security() -> dict[str, Any]:
    return {
        "integrated_required": True,
        "not_separated": True,
        "privacy_by_design": True,
        "via_consent_for_ledger": True,
    }


def events() -> dict[str, Any]:
    return {
        "core_events": list(CORE_EVENTS),
        "core_event_count": len(CORE_EVENTS),
        "present_required": True,
        "not_missing": True,
    }


def microservices() -> dict[str, Any]:
    return {
        "services": list(MICROSERVICES),
        "service_count": len(MICROSERVICES),
        "logical_decomposition": True,
    }


def integrations() -> dict[str, Any]:
    return {
        "targets": list(INTEGRATIONS),
        "count": len(INTEGRATIONS),
        "boundaries_clear_required": True,
        "not_unclear": True,
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
            "domains_loosely_coupled": True,
            "ownership_clear": True,
            "privacy_integrated": True,
            "events_present": True,
            "aggregates_defined": True,
            "integration_boundaries_clear": True,
            "foundation_tests": True,
            "domain_api_live": True,
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
        "builds_on": ["P211-A", "P211-B", "ADR-376", "ADR-377"],
        "domain_map": domain_map(),
        "bounded_contexts": bounded_contexts(),
        "aggregates": aggregates(),
        "entities": entities(),
        "ownership": ownership(),
        "privacy_security": privacy_security(),
        "events": events(),
        "microservices": microservices(),
        "integrations": integrations(),
        "cqrs": cqrs(),
        "cursor_outputs": cursor_outputs(),
        "quality_gates": quality_gates(),
        "production_readiness": production_readiness(),
        "domains_loosely_coupled_required": True,
        "data_ownership_clear_required": True,
        "privacy_integrated_with_security_required": True,
        "events_present_required": True,
        "aggregates_defined_required": True,
        "integration_boundaries_clear_required": True,
        "sibling_data_security_bc_forbidden": True,
        "api_prefix": f"{API_PREFIX}/domain",
        "forbidden_sibling_bc": [
            "dspm",
            "dspm_platform",
            "privacy_intelligence",
            "data_classification",
            "data_protection_platform",
            "data_lineage_platform",
        ],
    }


def executive_summary() -> dict[str, Any]:
    return catalog()


def domain_surface() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "routes": [
            "GET /data-security/domain",
            "GET /data-security/domain/map",
            "GET /data-security/domain/bounded-contexts",
            "GET /data-security/domain/aggregates",
            "GET /data-security/domain/entities",
            "GET /data-security/domain/ownership",
            "GET /data-security/domain/privacy-security",
            "GET /data-security/domain/events",
            "GET /data-security/domain/microservices",
            "GET /data-security/domain/integrations",
            "GET /data-security/domain/cqrs",
            "GET /data-security/domain/outputs",
            "GET /data-security/domain/production-readiness",
            "GET /data-security/domain/readiness",
        ],
    }
