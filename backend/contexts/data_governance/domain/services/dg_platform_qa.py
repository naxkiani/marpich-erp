"""P212-O Testing, Governance, Compliance Validation & DoD — immutable catalog."""
from __future__ import annotations

from typing import Any

PROMPT_ID = "P212-O"
ADR = 407
SOR = "data_governance"
API_PREFIX = "/api/v1/data-governance"
PRODUCT = (
    "Enterprise Data Governance Testing, Governance, "
    "Compliance Validation & Definition of Done Platform"
)
CAPABILITY = "CAP-PLT-DG-001"

PRINCIPLE = (
    "Enterprise systems SHALL prove their correctness, "
    "security, compliance, and governance continuously."
)

CORE_DOMAIN = "enterprise_assurance_management"

SUPPORTING_DOMAINS: tuple[str, ...] = (
    "testing_management",
    "compliance_validation",
    "governance_validation",
    "security_assurance",
    "evidence_management",
    "certification_management",
    "definition_of_done_management",
)

BOUNDED_CONTEXTS: tuple[dict[str, Any], ...] = (
    {
        "id": "BC-01",
        "name": "enterprise_testing_context",
        "responsibilities": (
            "test_planning",
            "test_execution",
            "test_automation",
            "result_management",
        ),
    },
    {
        "id": "BC-02",
        "name": "governance_validation_context",
        "responsibilities": (
            "governance_rule_validation",
            "architecture_compliance",
            "policy_verification",
        ),
    },
    {
        "id": "BC-03",
        "name": "compliance_assurance_context",
        "responsibilities": (
            "regulatory_validation",
            "control_verification",
            "evidence_generation",
        ),
    },
    {
        "id": "BC-04",
        "name": "security_assurance_context",
        "responsibilities": (
            "security_testing",
            "zero_trust_validation",
            "vulnerability_verification",
        ),
    },
    {
        "id": "BC-05",
        "name": "certification_context",
        "responsibilities": (
            "approval_workflow",
            "certification_lifecycle",
            "enterprise_acceptance",
        ),
    },
)

TESTING_LAYERS: dict[str, tuple[str, ...]] = {
    "unit_testing": ("domain_logic", "business_rules", "aggregates"),
    "integration_testing": (
        "service_communication",
        "apis",
        "events",
        "databases",
    ),
    "contract_testing": ("api_contracts", "event_contracts", "data_contracts"),
    "performance_testing": ("scalability", "latency", "throughput"),
    "security_testing": (
        "authentication",
        "authorization",
        "encryption",
        "vulnerabilities",
    ),
    "chaos_testing": (
        "resilience",
        "failure_recovery",
        "disaster_handling",
    ),
}

DG_VALIDATION_TARGETS: tuple[str, ...] = (
    "data_ownership",
    "data_stewardship",
    "data_quality",
    "metadata_completeness",
    "data_lineage",
    "policy_enforcement",
    "data_product_compliance",
    "ai_data_governance",
)

DG_VALIDATION_INTEGRATIONS: tuple[str, ...] = (
    "P212-D",
    "P212-E",
    "P212-H",
    "P212-I",
    "P212-K",
)

COMPLIANCE_CAPABILITIES: tuple[str, ...] = (
    "control_mapping",
    "compliance_assessment",
    "evidence_collection",
    "gap_detection",
    "remediation_tracking",
)

COMPLIANCE_SUPPORT: tuple[str, ...] = (
    "regulatory_requirements",
    "internal_policies",
    "enterprise_standards",
    "security_controls",
)

DOD_CRITERIA: tuple[str, ...] = (
    "architecture",
    "development",
    "testing",
    "security",
    "deployment",
    "governance",
    "compliance",
)

DOD_MODEL: tuple[str, ...] = (
    "requirement",
    "validation_rule",
    "evidence",
    "approval",
    "certification",
)

ARCHITECTURE_CONFORMANCE: tuple[str, ...] = (
    "ddd_compliance",
    "bounded_context_integrity",
    "api_first_compliance",
    "microservice_boundaries",
    "cqrs_implementation",
    "event_architecture",
    "cloud_native_standards",
)

AI_AGENTS: tuple[str, ...] = (
    "ai_test_analyst",
    "ai_compliance_auditor",
    "ai_architecture_reviewer",
    "ai_security_validator",
    "ai_governance_inspector",
)

GRAPH_NODES: tuple[str, ...] = (
    "Requirement",
    "Test",
    "Control",
    "Policy",
    "Evidence",
    "Service",
    "Component",
    "Risk",
)

GRAPH_RELATIONSHIPS: tuple[str, ...] = (
    "Test_VALIDATES_Requirement",
    "Evidence_SUPPORTS_Compliance",
    "Control_PROTECTS_Asset",
)

TWIN_CAPABILITIES: tuple[str, ...] = (
    "validation_simulation",
    "compliance_prediction",
    "failure_prediction",
    "governance_impact_testing",
)

COMMANDS: tuple[str, ...] = (
    "CreateValidationPlanCommand",
    "ExecuteTestCommand",
    "ValidateComplianceCommand",
    "GenerateEvidenceCommand",
    "IssueCertificationCommand",
)

QUERIES: tuple[str, ...] = (
    "GetValidationStatusQuery",
    "GetComplianceScoreQuery",
    "GetEvidenceQuery",
    "GetCertificationQuery",
)

QA_EVENTS: tuple[dict[str, Any], ...] = (
    {
        "name": "ValidationStartedEvent",
        "producer": "testing_management_service",
        "consumers": ("governance", "audit", "observability"),
        "payload": ("tenant_id", "assessment_id", "plan_ref"),
        "version": "v1",
    },
    {
        "name": "TestExecutedEvent",
        "producer": "testing_management_service",
        "consumers": ("evidence", "ai_quality", "audit"),
        "payload": ("tenant_id", "execution_id", "result"),
        "version": "v1",
    },
    {
        "name": "CompliancePassedEvent",
        "producer": "compliance_validation_service",
        "consumers": ("certification", "audit", "graph"),
        "payload": ("tenant_id", "assessment_id", "score"),
        "version": "v1",
    },
    {
        "name": "ComplianceFailedEvent",
        "producer": "compliance_validation_service",
        "consumers": ("remediation", "audit", "notifications"),
        "payload": ("tenant_id", "assessment_id", "gaps"),
        "version": "v1",
    },
    {
        "name": "EvidenceGeneratedEvent",
        "producer": "evidence_management_service",
        "consumers": ("audit", "certification", "compliance"),
        "payload": ("tenant_id", "evidence_id", "artifact_ref"),
        "version": "v1",
    },
    {
        "name": "CertificationIssuedEvent",
        "producer": "certification_service",
        "consumers": ("audit", "dashboard", "twin"),
        "payload": ("tenant_id", "certification_id", "level"),
        "version": "v1",
    },
)

MICROSERVICES: tuple[dict[str, Any], ...] = (
    {
        "name": "testing-management-service",
        "responsibility": "Test planning, execution, automation",
        "database_boundary": "data_governance_qa_testing",
        "api_boundary": "/api/v1/data-governance/qa/tests",
        "events": "data_governance.qa.testing.*",
        "security_model": "zero_trust_via_p208",
        "scaling_strategy": "async_workers",
    },
    {
        "name": "compliance-validation-service",
        "responsibility": "Continuous compliance assessment",
        "database_boundary": "data_governance_qa_compliance",
        "api_boundary": "/api/v1/data-governance/qa/compliance",
        "events": "data_governance.qa.compliance.*",
        "security_model": "via_compliance_framework",
        "scaling_strategy": "horizontal_stateless",
    },
    {
        "name": "governance-assurance-service",
        "responsibility": "Governance rule and architecture validation",
        "database_boundary": "data_governance_qa_governance",
        "api_boundary": "/api/v1/data-governance/qa/validation",
        "events": "data_governance.qa.governance.*",
        "security_model": "via_policy_engine",
        "scaling_strategy": "horizontal_stateless",
    },
    {
        "name": "security-validation-service",
        "responsibility": "Security and zero-trust validation",
        "database_boundary": "data_governance_qa_security",
        "api_boundary": "/api/v1/data-governance/qa/security",
        "events": "data_governance.qa.security.*",
        "security_model": "via_p207_p211",
        "scaling_strategy": "async_workers",
    },
    {
        "name": "evidence-management-service",
        "responsibility": "Evidence artifacts via Audit Platform",
        "database_boundary": "data_governance_qa_evidence",
        "api_boundary": "/api/v1/data-governance/qa/evidence",
        "events": "data_governance.qa.evidence.*",
        "security_model": "via_audit_platform",
        "scaling_strategy": "append_only",
    },
    {
        "name": "certification-service",
        "responsibility": "Certification lifecycle and acceptance",
        "database_boundary": "data_governance_qa_certification",
        "api_boundary": "/api/v1/data-governance/qa/certification",
        "events": "data_governance.qa.certification.*",
        "security_model": "via_workflow_engine",
        "scaling_strategy": "horizontal_stateless",
    },
    {
        "name": "ai-quality-intelligence-service",
        "responsibility": "AI quality agents via Enterprise AI",
        "database_boundary": "data_governance_qa_ai",
        "api_boundary": "/api/v1/data-governance/qa/quality-assistant",
        "events": "data_governance.qa.ai.*",
        "security_model": "via_enterprise_ai",
        "scaling_strategy": "async_workers",
    },
)

API_CATEGORIES: dict[str, tuple[str, ...]] = {
    "testing": (
        "/api/v1/data-governance/qa/tests",
        "/api/v1/data-governance/qa/executions",
        "/api/v1/data-governance/qa/results",
    ),
    "compliance": (
        "/api/v1/data-governance/qa/compliance",
        "/api/v1/data-governance/qa/controls",
        "/api/v1/data-governance/qa/evidence",
    ),
    "governance": (
        "/api/v1/data-governance/qa/validation",
        "/api/v1/data-governance/qa/certification",
        "/api/v1/data-governance/qa/definition-of-done",
    ),
    "ai": (
        "/api/v1/data-governance/qa/quality-assistant",
        "/api/v1/data-governance/qa/compliance-ai",
    ),
}

SECURITY_VALIDATE: tuple[str, ...] = (
    "identity_controls",
    "access_policies",
    "encryption",
    "auditability",
    "security_evidence",
)

DEPLOY_VALIDATE: tuple[str, ...] = (
    "kubernetes_deployment",
    "devsecops_pipeline",
    "infrastructure_as_code",
    "observability",
    "scalability",
    "reliability",
)

CONTINUOUS_GOVERNANCE_CYCLE: tuple[str, ...] = (
    "observe",
    "validate",
    "detect_gap",
    "remediate",
    "verify",
    "certify",
)

DASHBOARD_SCORES: tuple[str, ...] = (
    "compliance_score",
    "governance_score",
    "quality_score",
    "security_score",
    "ai_readiness_score",
    "architecture_maturity_score",
)

CURSOR_OUTPUTS: tuple[str, ...] = (
    "enterprise_assurance_vision",
    "enterprise_assurance_domain_model_ddd",
    "assurance_bounded_context_architecture",
    "enterprise_testing_framework",
    "data_governance_validation_engine",
    "automated_compliance_validation_platform",
    "definition_of_done_engine",
    "architecture_conformance_validation",
    "ai_native_quality_intelligence",
    "knowledge_graph_validation_integration",
    "digital_twin_validation_integration",
    "cqrs_architecture",
    "event_sourcing_architecture",
    "microservice_architecture",
    "api_first_architecture",
    "security_assurance_architecture",
    "deployment_validation_architecture",
    "continuous_governance_operations",
    "enterprise_reporting_certification",
    "production_readiness_checklist",
)

QUALITY_GATES_REJECT_IF: tuple[str, ...] = (
    "complete_enterprise_testing_architecture_is_missing",
    "governance_validation_platform_is_missing",
    "compliance_automation_is_missing",
    "security_assurance_is_missing",
    "definition_of_done_engine_is_missing",
    "ai_quality_intelligence_is_missing",
    "knowledge_graph_integration_is_missing",
    "digital_twin_integration_is_missing",
    "cqrs_architecture_is_missing",
    "event_sourcing_architecture_is_missing",
    "microservices_architecture_is_missing",
    "api_first_architecture_is_missing",
    "continuous_governance_is_missing",
    "sibling_data_governance_qa_bc",
)


def testing_architecture() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "principle": PRINCIPLE,
        "core_domain": CORE_DOMAIN,
        "supporting_domains": list(SUPPORTING_DOMAINS),
        "aggregate": "EnterpriseValidationAssessment",
        "layers": {k: list(v) for k, v in TESTING_LAYERS.items()},
        "layer_count": len(TESTING_LAYERS),
        "fabric": "meos_enterprise_assurance_intelligence_fabric",
        "transforms": "manual_review_to_continuous_automated_evidence_driven",
    }


def governance_validation() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "bounded_contexts": [dict(bc) for bc in BOUNDED_CONTEXTS],
        "bc_count": len(BOUNDED_CONTEXTS),
        "dg_targets": list(DG_VALIDATION_TARGETS),
        "integrations": list(DG_VALIDATION_INTEGRATIONS),
        "architecture_conformance": list(ARCHITECTURE_CONFORMANCE),
        "compliance_score_generated": True,
    }


def compliance_automation() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "capabilities": list(COMPLIANCE_CAPABILITIES),
        "supports": list(COMPLIANCE_SUPPORT),
        "capability_count": len(COMPLIANCE_CAPABILITIES),
        "via_compliance_framework": True,
        "module_local_compliance_tables_forbidden": True,
    }


def security_assurance() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "validates": list(SECURITY_VALIDATE),
        "validate_count": len(SECURITY_VALIDATE),
        "via_p207": True,
        "via_p208": True,
        "via_p209": True,
        "via_p210": True,
        "via_p211": True,
    }


def definition_of_done() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "criteria": list(DOD_CRITERIA),
        "criteria_count": len(DOD_CRITERIA),
        "model": list(DOD_MODEL),
        "model_step_count": len(DOD_MODEL),
    }


def ai_quality_intelligence() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "agents": list(AI_AGENTS),
        "agent_count": len(AI_AGENTS),
        "capabilities": (
            "generate_test_scenarios",
            "predict_failures",
            "detect_compliance_gaps",
            "recommend_improvements",
            "generate_validation_reports",
        ),
        "via_enterprise_ai": True,
    }


def knowledge_graph_integration() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "via_p212_j": True,
        "nodes": list(GRAPH_NODES),
        "relationships": list(GRAPH_RELATIONSHIPS),
        "node_count": len(GRAPH_NODES),
    }


def digital_twin_integration() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "via_p212_l": True,
        "capabilities": list(TWIN_CAPABILITIES),
        "capability_count": len(TWIN_CAPABILITIES),
    }


def cqrs_architecture() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "commands": list(COMMANDS),
        "queries": list(QUERIES),
        "command_count": len(COMMANDS),
        "query_count": len(QUERIES),
    }


def event_sourcing() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "events": [dict(e) for e in QA_EVENTS],
        "event_count": len(QA_EVENTS),
        "via_enterprise_event_bus": True,
        "versioning_strategy": "append_only_vN",
        "outbox_required": True,
    }


def microservices() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "services": [dict(s) for s in MICROSERVICES],
        "service_count": len(MICROSERVICES),
    }


def api_first() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "categories": {k: list(v) for k, v in API_CATEGORIES.items()},
        "category_count": len(API_CATEGORIES),
        "rest": True,
        "graphql": True,
        "event_apis": True,
        "streaming_apis": True,
        "via_api_gateway": True,
        "module_local_gateway_forbidden": True,
        "api_security": (
            "data_governance.read",
            "zero_trust",
            "tenant_isolation",
            "rate_limiting",
            "audit_logging",
        ),
    }


def continuous_governance() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "cycle": list(CONTINUOUS_GOVERNANCE_CYCLE),
        "cycle_step_count": len(CONTINUOUS_GOVERNANCE_CYCLE),
        "dashboard_scores": list(DASHBOARD_SCORES),
        "score_count": len(DASHBOARD_SCORES),
    }


def deployment_validation() -> dict[str, Any]:
    return {
        "via_p212_n": True,
        "validates": list(DEPLOY_VALIDATE),
        "validate_count": len(DEPLOY_VALIDATE),
    }


def evidence_and_certification() -> dict[str, Any]:
    return {
        "via_audit_platform": True,
        "module_local_certification_store_forbidden": True,
        "dashboard_scores": list(DASHBOARD_SCORES),
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
            "enterprise_testing_platform": True,
            "governance_validation": True,
            "compliance_validation": True,
            "security_assurance": True,
            "evidence_management": True,
            "certification_platform": True,
            "definition_of_done_engine": True,
            "ai_validation": True,
            "knowledge_graph_integration": True,
            "digital_twin_integration": True,
            "cqrs_architecture": True,
            "event_architecture": True,
            "microservice_architecture": True,
            "api_architecture": True,
            "deployment_validation": True,
            "foundation_tests": True,
            "qa_api_live": True,
            "p212_series_complete": True,
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
        "principle": PRINCIPLE,
        "builds_on": [
            "P212-A",
            "P212-B",
            "P212-D",
            "P212-E",
            "P212-F",
            "P212-G",
            "P212-H",
            "P212-J",
            "P212-K",
            "P212-L",
            "P212-M",
            "P212-N",
            "ADR-392",
            "ADR-397",
            "ADR-398",
            "ADR-399",
            "ADR-400",
            "ADR-401",
            "ADR-402",
            "ADR-404",
            "ADR-405",
            "ADR-406",
        ],
        "testing_architecture": testing_architecture(),
        "governance_validation": governance_validation(),
        "compliance_automation": compliance_automation(),
        "security_assurance": security_assurance(),
        "definition_of_done": definition_of_done(),
        "ai_quality_intelligence": ai_quality_intelligence(),
        "knowledge_graph_integration": knowledge_graph_integration(),
        "digital_twin_integration": digital_twin_integration(),
        "cqrs_architecture": cqrs_architecture(),
        "event_sourcing": event_sourcing(),
        "microservices": microservices(),
        "api_first": api_first(),
        "continuous_governance": continuous_governance(),
        "deployment_validation": deployment_validation(),
        "evidence_and_certification": evidence_and_certification(),
        "cursor_outputs": cursor_outputs(),
        "quality_gates": quality_gates(),
        "production_readiness": production_readiness(),
        "complete_enterprise_testing_architecture_present_required": True,
        "governance_validation_platform_present_required": True,
        "compliance_automation_present_required": True,
        "security_assurance_present_required": True,
        "definition_of_done_engine_present_required": True,
        "ai_quality_intelligence_present_required": True,
        "knowledge_graph_integration_present_required": True,
        "digital_twin_integration_present_required": True,
        "cqrs_architecture_present_required": True,
        "event_sourcing_architecture_present_required": True,
        "microservices_architecture_present_required": True,
        "api_first_architecture_present_required": True,
        "continuous_governance_present_required": True,
        "sibling_data_governance_qa_bc_forbidden": True,
        "api_prefix": f"{API_PREFIX}/qa",
        "forbidden_sibling_bc": [
            "data_governance_qa",
            "dg_assurance_platform",
            "governance_certification_platform",
            "data_mesh",
            "data_marketplace",
            "metadata_governance_platform",
        ],
    }


def executive_summary() -> dict[str, Any]:
    return catalog()


def qa_surface() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "routes": [
            "GET /data-governance/qa",
            "GET /data-governance/qa/testing",
            "GET /data-governance/qa/governance",
            "GET /data-governance/qa/compliance",
            "GET /data-governance/qa/security",
            "GET /data-governance/qa/dod",
            "GET /data-governance/qa/ai",
            "GET /data-governance/qa/graph",
            "GET /data-governance/qa/twin",
            "GET /data-governance/qa/cqrs",
            "GET /data-governance/qa/events",
            "GET /data-governance/qa/microservices",
            "GET /data-governance/qa/apis",
            "GET /data-governance/qa/continuous",
            "GET /data-governance/qa/deploy-validation",
            "GET /data-governance/qa/evidence",
            "GET /data-governance/qa/outputs",
            "GET /data-governance/qa/production-readiness",
            "GET /data-governance/qa/readiness",
        ],
    }
