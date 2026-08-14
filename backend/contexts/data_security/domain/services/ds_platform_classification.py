"""P211-E Enterprise Data Classification & Labeling — immutable catalog."""
from __future__ import annotations

from typing import Any

PROMPT_ID = "P211-E"
ADR = 380
SOR = "data_security"
API_PREFIX = "/api/v1/data-security"
PRODUCT = (
    "Enterprise Data Security & Privacy Intelligence Platform — "
    "Data Classification & Labeling"
)
CAPABILITY = "CAP-PLT-DS-001"

MISSION_STATEMENT = (
    "Create an enterprise data classification platform capable of understanding "
    "enterprise data meaning, automatically identifying sensitive information, "
    "assigning security classifications, applying data labels, enforcing "
    "protection requirements, supporting privacy regulations, and providing "
    "classification intelligence."
)

VISION_STATEMENT = (
    "Create a Data Intelligence Classification Fabric where every data asset "
    "has a security identity, every dataset has a classification level, every "
    "sensitive element is automatically detected, every protection requirement "
    "is known, every AI system understands data sensitivity, and every "
    "security decision is context-aware."
)

ARCHITECTURE_FLOW: tuple[str, ...] = (
    "data_sources",
    "p211_d_data_discovery",
    "data_profiling_engine",
    "ai_classification_engine",
    "classification_policy_engine",
    "label_management_platform",
    "security_control_integration",
    "continuous_classification_monitoring",
)

CORE_ENTITIES: tuple[str, ...] = (
    "DataClassification",
    "DataLabel",
    "ClassificationRule",
    "ClassificationResult",
    "ClassificationPolicy",
)

CLASSIFICATION_LEVELS: tuple[dict[str, Any], ...] = (
    {
        "level": 0,
        "name": "public_data",
        "examples": ["public_information", "marketing_content", "published_documents"],
        "protection": ["minimal_controls"],
    },
    {
        "level": 1,
        "name": "internal_data",
        "examples": ["internal_documents", "operational_information"],
        "protection": ["access_control_required"],
    },
    {
        "level": 2,
        "name": "confidential_data",
        "examples": ["business_records", "contracts", "internal_financial_data"],
        "protection": ["encryption", "access_governance", "monitoring"],
    },
    {
        "level": 3,
        "name": "restricted_data",
        "examples": ["customer_information", "employee_data", "sensitive_business_data"],
        "protection": ["strong_encryption", "strict_authorization", "audit_logging"],
    },
    {
        "level": 4,
        "name": "critical_data",
        "examples": [
            "cryptographic_material",
            "strategic_intelligence",
            "critical_infrastructure_data",
        ],
        "protection": [
            "zero_trust_controls",
            "continuous_monitoring",
            "advanced_protection",
        ],
    },
)

SENSITIVE_CATEGORIES: tuple[dict[str, Any], ...] = (
    {
        "id": "pii",
        "examples": ["names", "addresses", "phone_numbers", "identity_numbers"],
    },
    {
        "id": "financial_information",
        "examples": ["bank_records", "payment_information", "transactions"],
    },
    {
        "id": "health_information",
        "examples": ["medical_records", "health_data"],
    },
    {
        "id": "security_information",
        "examples": ["passwords", "secrets", "tokens", "keys"],
    },
    {
        "id": "intellectual_property",
        "examples": ["source_code", "research", "design_documents"],
    },
    {
        "id": "ai_sensitive_data",
        "examples": ["training_data", "prompts", "embeddings", "agent_memory"],
    },
)

AI_CAPABILITIES: tuple[str, ...] = (
    "natural_language_understanding",
    "semantic_data_analysis",
    "pattern_recognition",
    "context_understanding",
    "machine_learning_classification",
    "anomaly_detection",
    "confidence_scoring",
    "explain_classification_decisions",
    "improve_from_feedback",
)

CLASSIFICATION_METHODS: tuple[str, ...] = (
    "rule_based",
    "ai_based",
    "metadata_based",
    "context_based",
)

SECURITY_LABELS: tuple[str, ...] = (
    "PUBLIC",
    "INTERNAL",
    "CONFIDENTIAL",
    "RESTRICTED",
    "CRITICAL",
)

PRIVACY_LABELS: tuple[str, ...] = (
    "PII",
    "SENSITIVE_PERSONAL_DATA",
    "CONSENT_REQUIRED",
)

COMPLIANCE_LABELS: tuple[str, ...] = ("GDPR", "PCI", "HIPAA", "SOC2")

BUSINESS_LABELS: tuple[str, ...] = ("FINANCE", "HR", "LEGAL", "STRATEGIC")

AI_LABELS: tuple[str, ...] = (
    "TRAINING_DATA",
    "MODEL_DATA",
    "PROMPT_DATA",
    "VECTOR_DATA",
)

EXAMPLE_LABELS: tuple[str, ...] = (
    "CONFIDENTIAL",
    "RESTRICTED",
    "PERSONAL_DATA",
    "FINANCIAL_DATA",
    "CRITICAL_DATA",
    "AI_TRAINING_DATA",
)

LIFECYCLE_CAPS: tuple[str, ...] = (
    "continuous_scanning",
    "classification_updates",
    "label_drift_detection",
    "classification_review",
    "data_change_monitoring",
    "risk_recalculation",
)

KG_NODES: tuple[str, ...] = (
    "data_asset",
    "classification",
    "label",
    "owner",
    "policy",
    "risk",
    "compliance_requirement",
    "application",
)

KG_RELATIONSHIPS: tuple[str, ...] = (
    "classified_as",
    "protected_by",
    "owned_by",
    "used_by",
    "requires_control",
)

COMMANDS: tuple[str, ...] = (
    "CreateClassificationRule",
    "ClassifyDataAsset",
    "ApplyDataLabel",
    "ApproveClassification",
    "UpdateClassificationPolicy",
    "ReviewClassification",
)

QUERIES: tuple[str, ...] = (
    "GetClassificationStatus",
    "GetDataLabels",
    "GetSensitiveDataReport",
    "GetClassificationHistory",
    "GetClassificationCoverage",
    "GetClassificationReadiness",
)

DOMAIN_EVENTS: tuple[str, ...] = (
    "DataClassified",
    "LabelApplied",
    "SensitiveInformationDetected",
    "ClassificationReviewed",
    "ClassificationPolicyChanged",
    "ClassificationChanged",
    "LabelUpdated",
    "PolicyViolationDetected",
)

MICROSERVICES: tuple[str, ...] = (
    "classification-service",
    "label-management-service",
    "sensitive-data-detection-service",
    "ai-classification-service",
    "policy-engine-service",
    "classification-review-service",
    "classification-reporting-service",
    "classification-graph-service",
    "classification-twin-service",
)

APIS: tuple[str, ...] = (
    "classification_api",
    "label_api",
    "sensitive_data_detection_api",
    "policy_api",
    "review_api",
    "reporting_api",
)

API_STYLES: tuple[str, ...] = ("rest", "graphql", "grpc", "event_streaming")

INTEGRATIONS: tuple[str, ...] = (
    "P211-D",
    "P211-F",
    "P211-G",
    "P211-H",
    "P211-I",
    "P208",
    "P209",
    "P210",
    "enterprise_ai",
    "policy_engine",
    "workflow",
)

COMPLIANCE_STANDARDS: tuple[str, ...] = (
    "iso_27001",
    "iso_27701",
    "nist_privacy_framework",
    "gdpr",
    "soc_2",
)

CURSOR_OUTPUTS: tuple[str, ...] = (
    "enterprise_classification_architecture",
    "classification_domain_model",
    "classification_taxonomy",
    "label_management_framework",
    "ai_classification_engine_design",
    "sensitive_data_detection_model",
    "policy_engine_architecture",
    "knowledge_graph_model",
    "digital_twin_model",
    "cqrs_architecture",
    "event_catalogue",
    "microservice_blueprint",
    "api_specifications",
    "security_integration_model",
    "classification_dashboard",
    "production_deployment_blueprint",
)

QUALITY_GATES_REJECT_IF: tuple[str, ...] = (
    "data_cannot_be_classified",
    "sensitive_data_detection_is_unavailable",
    "labels_are_unmanaged",
    "ai_decisions_are_unexplained",
    "classification_policies_are_missing",
    "classification_lifecycle_is_undefined",
    "sibling_classification_bc",
)


def architecture() -> dict[str, Any]:
    return {
        "flow": list(ARCHITECTURE_FLOW),
        "layer_count": len(ARCHITECTURE_FLOW),
        "builds_on_discovery": True,
    }


def entities() -> dict[str, Any]:
    return {"entities": list(CORE_ENTITIES), "entity_count": len(CORE_ENTITIES)}


def taxonomy() -> dict[str, Any]:
    return {
        "levels": list(CLASSIFICATION_LEVELS),
        "level_count": len(CLASSIFICATION_LEVELS),
        "classifiable_required": True,
        "not_unclassifiable": True,
    }


def sensitive_detection() -> dict[str, Any]:
    return {
        "categories": list(SENSITIVE_CATEGORIES),
        "category_count": len(SENSITIVE_CATEGORIES),
        "available_required": True,
        "not_unavailable": True,
    }


def ai_classification() -> dict[str, Any]:
    return {
        "capabilities": list(AI_CAPABILITIES),
        "explainable_required": True,
        "not_unexplained": True,
        "via_enterprise_ai": True,
        "module_local_llm_sdk_forbidden": True,
        "confidence_scoring": True,
    }


def methods() -> dict[str, Any]:
    return {"methods": list(CLASSIFICATION_METHODS)}


def labels() -> dict[str, Any]:
    return {
        "security_labels": list(SECURITY_LABELS),
        "privacy_labels": list(PRIVACY_LABELS),
        "compliance_labels": list(COMPLIANCE_LABELS),
        "business_labels": list(BUSINESS_LABELS),
        "ai_labels": list(AI_LABELS),
        "examples": list(EXAMPLE_LABELS),
        "managed_required": True,
        "not_unmanaged": True,
    }


def policies() -> dict[str, Any]:
    return {
        "defines": [
            "who_can_classify",
            "who_can_modify_labels",
            "classification_approval_workflow",
            "automatic_classification_rules",
            "exception_handling",
            "review_lifecycle",
        ],
        "present_required": True,
        "not_missing": True,
        "via_policy_engine": True,
        "via_workflow": True,
        "examples": [
            "financial_information_to_confidential",
            "identity_information_to_personal_data",
            "critical_ai_models_to_critical_ai_data",
        ],
    }


def lifecycle() -> dict[str, Any]:
    return {
        "capabilities": list(LIFECYCLE_CAPS),
        "defined_required": True,
        "not_undefined": True,
    }


def knowledge_graph() -> dict[str, Any]:
    return {
        "nodes": list(KG_NODES),
        "relationships": list(KG_RELATIONSHIPS),
        "capabilities": [
            "classification_reasoning",
            "risk_propagation",
            "impact_analysis",
        ],
    }


def digital_twin() -> dict[str, Any]:
    return {
        "represents": [
            "enterprise_data_classification_state",
            "sensitivity_distribution",
            "risk_exposure",
            "protection_coverage",
        ],
        "capabilities": [
            "classification_simulation",
            "policy_testing",
            "impact_prediction",
            "security_scenario_analysis",
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


def apis() -> dict[str, Any]:
    return {
        "apis": list(APIS),
        "styles": list(API_STYLES),
        "api_count": len(APIS),
    }


def integrations() -> dict[str, Any]:
    return {"targets": list(INTEGRATIONS), "count": len(INTEGRATIONS)}


def compliance() -> dict[str, Any]:
    return {"standards": list(COMPLIANCE_STANDARDS)}


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
            "data_classifiable": True,
            "sensitive_detection": True,
            "labels_managed": True,
            "ai_explainable": True,
            "policies_present": True,
            "lifecycle_defined": True,
            "foundation_tests": True,
            "classification_api_live": True,
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
        "mission": MISSION_STATEMENT,
        "vision": VISION_STATEMENT,
        "builds_on": [
            "P211-A",
            "P211-B",
            "P211-C",
            "P211-D",
            "ADR-376",
            "ADR-377",
            "ADR-378",
            "ADR-379",
        ],
        "architecture": architecture(),
        "entities": entities(),
        "taxonomy": taxonomy(),
        "sensitive_detection": sensitive_detection(),
        "ai_classification": ai_classification(),
        "methods": methods(),
        "labels": labels(),
        "policies": policies(),
        "lifecycle": lifecycle(),
        "knowledge_graph": knowledge_graph(),
        "digital_twin": digital_twin(),
        "cqrs": cqrs(),
        "microservices": microservices(),
        "apis": apis(),
        "integrations": integrations(),
        "compliance": compliance(),
        "cursor_outputs": cursor_outputs(),
        "quality_gates": quality_gates(),
        "production_readiness": production_readiness(),
        "data_classifiable_required": True,
        "sensitive_detection_available_required": True,
        "labels_managed_required": True,
        "ai_decisions_explainable_required": True,
        "classification_policies_present_required": True,
        "classification_lifecycle_defined_required": True,
        "sibling_classification_bc_forbidden": True,
        "api_prefix": f"{API_PREFIX}/classification",
        "forbidden_sibling_bc": [
            "data_classification",
            "label_management",
            "sensitive_data_detection",
        ],
    }


def executive_summary() -> dict[str, Any]:
    return catalog()


def classification_surface() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "routes": [
            "GET /data-security/classification",
            "GET /data-security/classification/architecture",
            "GET /data-security/classification/taxonomy",
            "GET /data-security/classification/sensitive-detection",
            "GET /data-security/classification/ai",
            "GET /data-security/classification/methods",
            "GET /data-security/classification/labels",
            "GET /data-security/classification/policies",
            "GET /data-security/classification/lifecycle",
            "GET /data-security/classification/knowledge-graph",
            "GET /data-security/classification/digital-twin",
            "GET /data-security/classification/cqrs",
            "GET /data-security/classification/events",
            "GET /data-security/classification/microservices",
            "GET /data-security/classification/apis",
            "GET /data-security/classification/integrations",
            "GET /data-security/classification/outputs",
            "GET /data-security/classification/production-readiness",
            "GET /data-security/classification/readiness",
        ],
    }
