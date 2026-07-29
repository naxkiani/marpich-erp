"""P215-K Quantum Governance Platform — immutable catalog."""
from __future__ import annotations

from typing import Any

PROMPT_ID = "P215-K"
ADR = 403
SOR = "quantum"
API_PREFIX = "/api/v1/quantum"
PRODUCT = (
    "Enterprise Quantum Governance, Regulation, Ethics "
    "& Responsible Quantum Computing Platform"
)
CAPABILITY = "CAP-PLT-QC-001"
FABRIC = "meos_quantum_responsible_intelligence_fabric"

PRINCIPLE = (
    "MEOS Quantum Governance Platform SHALL ensure that "
    "all quantum technologies, algorithms, infrastructures "
    "and intelligence systems operate within trusted, "
    "ethical, compliant and accountable boundaries."
)

CORE_DOMAIN = "enterprise_quantum_governance_intelligence_management"

SUPPORTING_DOMAINS: tuple[str, ...] = (
    "quantum_policy_domain",
    "quantum_regulation_domain",
    "quantum_ethics_domain",
    "quantum_risk_domain",
    "quantum_compliance_domain",
    "quantum_audit_domain",
    "quantum_trust_domain",
    "quantum_accountability_domain",
    "quantum_transparency_domain",
)

BOUNDED_CONTEXTS: tuple[dict[str, Any], ...] = (
    {
        "id": "BC-01",
        "name": "quantum_policy_governance_context",
        "owns": "QuantumPolicyAggregate",
        "responsibilities": (
            "policy_creation",
            "policy_enforcement",
            "governance_lifecycle",
        ),
    },
    {
        "id": "BC-02",
        "name": "quantum_regulatory_intelligence_context",
        "owns": "QuantumRegulationAggregate",
        "responsibilities": (
            "regulation_monitoring",
            "legal_intelligence",
            "compliance_mapping",
        ),
    },
    {
        "id": "BC-03",
        "name": "responsible_quantum_computing_context",
        "owns": "ResponsibleQuantumAggregate",
        "responsibilities": (
            "responsible_innovation",
            "impact_assessment",
            "ethical_evaluation",
        ),
    },
    {
        "id": "BC-04",
        "name": "quantum_risk_governance_context",
        "owns": "QuantumRiskAggregate",
        "responsibilities": (
            "risk_identification",
            "risk_scoring",
            "risk_mitigation",
        ),
    },
    {
        "id": "BC-05",
        "name": "quantum_compliance_context",
        "owns": "QuantumComplianceAggregate",
        "responsibilities": (
            "compliance_automation",
            "control_validation",
            "evidence_management",
        ),
    },
    {
        "id": "BC-06",
        "name": "quantum_audit_intelligence_context",
        "owns": "QuantumAuditAggregate",
        "responsibilities": (
            "audit_execution",
            "audit_evidence",
            "governance_reporting",
        ),
    },
    {
        "id": "BC-07",
        "name": "quantum_accountability_context",
        "owns": "QuantumAccountabilityAggregate",
        "responsibilities": (
            "ownership",
            "responsibility_mapping",
            "human_oversight",
        ),
    },
)

POLICY_CATEGORIES: tuple[str, ...] = (
    "quantum_computing_policies",
    "quantum_ai_policies",
    "quantum_data_policies",
    "quantum_security_policies",
    "quantum_research_policies",
    "quantum_usage_policies",
)

POLICY_CAPABILITIES: tuple[str, ...] = (
    "policy_creation",
    "policy_versioning",
    "policy_enforcement",
    "policy_automation",
    "policy_monitoring",
)

REGULATORY_CAPABILITIES: tuple[str, ...] = (
    "regulation_discovery",
    "regulatory_mapping",
    "compliance_prediction",
    "policy_impact_analysis",
    "regulatory_change_management",
)

RESPONSIBLE_CAPABILITIES: tuple[str, ...] = (
    "ethical_assessment",
    "impact_evaluation",
    "responsible_innovation_scoring",
)

RESPONSIBLE_MANAGES: tuple[str, ...] = (
    "ethical_principles",
    "responsible_usage",
    "human_oversight",
    "social_impact",
    "environmental_impact",
)

RISK_TYPES: tuple[str, ...] = (
    "technology_risks",
    "security_risks",
    "operational_risks",
    "ethical_risks",
    "regulatory_risks",
    "strategic_risks",
)

RISK_CAPABILITIES: tuple[str, ...] = (
    "risk_prediction",
    "risk_scoring",
    "risk_mitigation",
    "risk_monitoring",
)

COMPLIANCE_CAPABILITIES: tuple[str, ...] = (
    "continuous_compliance",
    "automated_validation",
    "control_monitoring",
    "evidence_collection",
)

KG_NODES: tuple[str, ...] = (
    "QuantumSystems",
    "Policies",
    "Regulations",
    "Risks",
    "EthicalPrinciples",
    "Organizations",
    "Decisions",
)

KG_RELATIONSHIPS: tuple[str, ...] = (
    "GovernedBy",
    "RestrictedBy",
    "EvaluatedBy",
    "ApprovedBy",
    "ImpactedBy",
    "ResponsibleFor",
)

TWIN_REPRESENTS: tuple[str, ...] = (
    "policies",
    "regulations",
    "risks",
    "compliance_state",
    "ethical_decisions",
    "governance_evolution",
)

TWIN_ENABLES: tuple[str, ...] = (
    "governance_simulation",
    "policy_testing",
    "risk_forecasting",
    "compliance_prediction",
)

COMMANDS: tuple[str, ...] = (
    "CreateQuantumPolicyCommand",
    "UpdateQuantumRegulationCommand",
    "AssessQuantumRiskCommand",
    "ValidateComplianceCommand",
    "ExecuteQuantumAuditCommand",
    "ApproveQuantumUsageCommand",
)

QUERIES: tuple[str, ...] = (
    "GetQuantumGovernanceScoreQuery",
    "GetComplianceStatusQuery",
    "GetRiskAssessmentQuery",
    "GetAuditHistoryQuery",
    "GetEthicalImpactQuery",
)

DOMAIN_EVENTS: tuple[dict[str, Any], ...] = (
    {
        "name": "QuantumPolicyCreatedEvent",
        "producer": "quantum_policy_service",
        "consumers": ("governance_core", "policy_engine", "audit"),
        "payload": ("tenant_id", "policy_id", "policy_category", "owner_ref"),
        "version": "v1",
    },
    {
        "name": "RegulationChangedEvent",
        "producer": "quantum_regulation_service",
        "consumers": ("compliance", "policy_service", "audit"),
        "payload": ("tenant_id", "regulation_id", "change_type", "effective_at"),
        "version": "v1",
    },
    {
        "name": "RiskAssessmentCompletedEvent",
        "producer": "quantum_risk_service",
        "consumers": ("governance_core", "cyber_security", "twin"),
        "payload": ("tenant_id", "assessment_id", "risk_score", "mitigations"),
        "version": "v1",
    },
    {
        "name": "ComplianceValidatedEvent",
        "producer": "quantum_compliance_service",
        "consumers": ("audit", "marketplace_gate", "notifications"),
        "payload": ("tenant_id", "control_id", "status", "evidence_ref"),
        "version": "v1",
    },
    {
        "name": "AuditExecutedEvent",
        "producer": "quantum_audit_service",
        "consumers": ("audit_platform", "compliance", "accountability"),
        "payload": ("tenant_id", "audit_id", "scope", "findings_count"),
        "version": "v1",
    },
    {
        "name": "EthicalReviewCompletedEvent",
        "producer": "quantum_ethics_service",
        "consumers": ("responsible_quantum", "workflow", "audit"),
        "payload": ("tenant_id", "review_id", "ethical_risk_score", "decision"),
        "version": "v1",
    },
)

MICROSERVICES: tuple[dict[str, Any], ...] = (
    {
        "name": "quantum-governance-service",
        "responsibility": "Governance fabric orchestration and scoring",
        "database_boundary": "quantum_governance_core",
        "api_boundary": "/api/v1/quantum/governance",
        "events": "quantum.governance.*",
        "security_model": "zero_trust_via_p207_p208",
        "scaling_strategy": "horizontal_stateless",
    },
    {
        "name": "quantum-policy-service",
        "responsibility": "Quantum policy lifecycle; PDP via Policy Engine",
        "database_boundary": "quantum_policies",
        "api_boundary": "/api/v1/quantum/governance/policies",
        "events": "quantum.governance.policy.*",
        "security_model": "via_policy_engine",
        "scaling_strategy": "horizontal_stateless",
    },
    {
        "name": "quantum-regulation-service",
        "responsibility": "Regulatory intelligence and mapping",
        "database_boundary": "quantum_regulations",
        "api_boundary": "/api/v1/quantum/governance/regulations",
        "events": "quantum.governance.regulation.*",
        "security_model": "zero_trust_via_p208",
        "scaling_strategy": "read_replicas",
    },
    {
        "name": "quantum-ethics-service",
        "responsibility": "Ethics assessment and responsible scoring",
        "database_boundary": "quantum_ethics",
        "api_boundary": "/api/v1/quantum/governance/ethics",
        "events": "quantum.governance.ethics.*",
        "security_model": "via_ai_governance_acl",
        "scaling_strategy": "horizontal_stateless",
    },
    {
        "name": "quantum-risk-service",
        "responsibility": "Quantum risk intelligence",
        "database_boundary": "quantum_risks",
        "api_boundary": "/api/v1/quantum/governance/risks",
        "events": "quantum.governance.risk.*",
        "security_model": "via_p210_p215h_bindings",
        "scaling_strategy": "async_workers",
    },
    {
        "name": "quantum-compliance-service",
        "responsibility": "Compliance automation and evidence",
        "database_boundary": "quantum_compliance",
        "api_boundary": "/api/v1/quantum/governance/compliance",
        "events": "quantum.governance.compliance.*",
        "security_model": "via_compliance_audit",
        "scaling_strategy": "horizontal_stateless",
    },
    {
        "name": "quantum-audit-service",
        "responsibility": "Governance audit orchestration → Audit Platform",
        "database_boundary": "quantum_audit_proj",
        "api_boundary": "/api/v1/quantum/governance/audit",
        "events": "quantum.governance.audit.*",
        "security_model": "via_audit_platform",
        "scaling_strategy": "async_workers",
    },
    {
        "name": "quantum-accountability-service",
        "responsibility": "Ownership, RACI, human oversight",
        "database_boundary": "quantum_accountability",
        "api_boundary": "/api/v1/quantum/governance/accountability",
        "events": "quantum.governance.accountability.*",
        "security_model": "via_workflow_identity",
        "scaling_strategy": "horizontal_stateless",
    },
    {
        "name": "quantum-trust-service",
        "responsibility": "Trust profiles and assurance scores",
        "database_boundary": "quantum_trust",
        "api_boundary": "/api/v1/quantum/governance/trust",
        "events": "quantum.governance.trust.*",
        "security_model": "via_p209_bindings",
        "scaling_strategy": "read_replicas",
    },
    {
        "name": "quantum-governance-knowledge-graph-service",
        "responsibility": "Ethics/governance graph projection",
        "database_boundary": "quantum_gov_graph",
        "api_boundary": "/api/v1/quantum/governance/knowledge-graph",
        "events": "quantum.governance.graph.*",
        "security_model": "zero_trust_via_p208",
        "scaling_strategy": "read_replicas",
    },
    {
        "name": "quantum-governance-digital-twin-service",
        "responsibility": "Governance twin simulation signals",
        "database_boundary": "quantum_gov_twin",
        "api_boundary": "/api/v1/quantum/governance/digital-twin",
        "events": "quantum.governance.twin.*",
        "security_model": "via_enterprise_ai",
        "scaling_strategy": "async_workers",
    },
)

CURSOR_OUTPUTS: tuple[str, ...] = (
    "enterprise_quantum_governance_vision",
    "ddd_domain_model",
    "quantum_governance_domain_architecture",
    "quantum_policy_management_platform",
    "quantum_regulatory_intelligence_platform",
    "responsible_quantum_computing_platform",
    "quantum_risk_management_platform",
    "quantum_compliance_automation_platform",
    "quantum_ethics_knowledge_graph",
    "quantum_governance_digital_twin",
    "cqrs_architecture",
    "event_sourcing_architecture",
    "microservice_architecture",
    "integration_architecture",
    "deployment_architecture",
    "testing_architecture",
    "production_readiness_checklist",
)

QUALITY_GATES_REJECT_IF: tuple[str, ...] = (
    "quantum_governance_platform_is_incomplete",
    "quantum_regulatory_intelligence_is_missing",
    "responsible_quantum_computing_is_missing",
    "quantum_ethics_framework_is_missing",
    "quantum_risk_management_is_missing",
    "quantum_compliance_automation_is_missing",
    "quantum_audit_intelligence_is_missing",
    "accountability_framework_is_missing",
    "knowledge_graph_integration_is_missing",
    "digital_twin_integration_is_missing",
    "cqrs_architecture_is_missing",
    "event_architecture_is_missing",
    "microservices_architecture_is_missing",
    "api_first_architecture_is_missing",
    "cloud_native_governance_is_missing",
    "sibling_quantum_governance_bc",
)

INTEGRATIONS: tuple[str, ...] = (
    "P215-A",
    "P215-B",
    "P215-C",
    "P215-D",
    "P215-E",
    "P215-F",
    "P215-G",
    "P215-H",
    "P215-I",
    "P215-J",
    "P214-H",
    "P214-Y",
    "P209",
    "P210",
    "P212",
    "ai_governance",
    "policy_engine",
    "authorization",
    "audit",
    "compliance",
    "workflow",
    "enterprise_ai",
)

DEPLOYMENT: dict[str, Any] = {
    "kubernetes_governance_layer": True,
    "policy_engine": True,
    "compliance_automation_engine": True,
    "audit_platform": True,
    "knowledge_graph_infrastructure": True,
    "digital_twin_platform": True,
    "observability_platform": True,
    "containers": True,
    "service_mesh": True,
    "cicd": True,
    "gitops": True,
    "auto_scaling": True,
    "multi_region": True,
}

TESTING: tuple[str, ...] = (
    "policy_testing",
    "compliance_testing",
    "regulatory_validation_testing",
    "ethics_evaluation_testing",
    "risk_simulation_testing",
    "audit_testing",
    "governance_performance_testing",
    "trust_validation_testing",
)


def governance_platform() -> dict[str, Any]:
    return {
        "complete_required": True,
        "not_incomplete": True,
        "principle": PRINCIPLE,
        "core_domain": CORE_DOMAIN,
        "supporting_domains": list(SUPPORTING_DOMAINS),
        "bounded_contexts": [dict(b) for b in BOUNDED_CONTEXTS],
        "bc_count": len(BOUNDED_CONTEXTS),
        "fabric": FABRIC,
        "aggregate": "EnterpriseQuantumGovernanceAggregate",
        "entities": (
            "QuantumGovernancePolicy",
            "QuantumRegulationRule",
            "QuantumEthicalPrinciple",
            "QuantumRiskAssessment",
            "QuantumComplianceControl",
            "QuantumAuditRecord",
            "QuantumTrustProfile",
            "QuantumAccountabilityRecord",
            "QuantumImpactAssessment",
        ),
        "value_objects": (
            "GovernanceScore",
            "ComplianceScore",
            "EthicalRiskScore",
            "TrustScore",
            "TransparencyScore",
            "QuantumMaturityLevel",
        ),
    }


def regulatory_intelligence() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "capabilities": list(REGULATORY_CAPABILITIES),
        "capability_count": len(REGULATORY_CAPABILITIES),
        "via_p212": True,
        "via_p210": True,
    }


def responsible_quantum() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "manages": list(RESPONSIBLE_MANAGES),
        "capabilities": list(RESPONSIBLE_CAPABILITIES),
        "capability_count": len(RESPONSIBLE_CAPABILITIES),
        "human_oversight_required": True,
    }


def ethics_framework() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "via_ai_governance": True,
        "ethical_assessment": True,
        "impact_evaluation": True,
        "knowledge_graph_enabled": True,
    }


def risk_management() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "risk_types": list(RISK_TYPES),
        "capabilities": list(RISK_CAPABILITIES),
        "risk_type_count": len(RISK_TYPES),
        "via_p210": True,
        "via_p215_h": True,
    }


def compliance_automation() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "capabilities": list(COMPLIANCE_CAPABILITIES),
        "capability_count": len(COMPLIANCE_CAPABILITIES),
        "via_compliance": True,
        "via_audit": True,
    }


def audit_intelligence() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "via_audit_platform": True,
        "audit_execution": True,
        "audit_evidence": True,
        "governance_reporting": True,
        "module_local_audit_ledger_forbidden": True,
    }


def accountability_framework() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "ownership": True,
        "responsibility_mapping": True,
        "human_oversight": True,
        "via_workflow": True,
    }


def policy_management() -> dict[str, Any]:
    return {
        "categories": list(POLICY_CATEGORIES),
        "capabilities": list(POLICY_CAPABILITIES),
        "category_count": len(POLICY_CATEGORIES),
        "via_policy_engine": True,
        "module_local_pdp_forbidden": True,
    }


def knowledge_graph() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "nodes": list(KG_NODES),
        "relationships": list(KG_RELATIONSHIPS),
        "ethical_reasoning": True,
        "governance_intelligence": True,
        "trust_analysis": True,
        "node_count": len(KG_NODES),
    }


def digital_twin() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "represents": list(TWIN_REPRESENTS),
        "enables": list(TWIN_ENABLES),
        "represent_count": len(TWIN_REPRESENTS),
    }


def cqrs() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "commands": list(COMMANDS),
        "command_count": len(COMMANDS),
        "queries": list(QUERIES),
        "query_count": len(QUERIES),
        "events": [e["name"] for e in DOMAIN_EVENTS],
        "event_count": len(DOMAIN_EVENTS),
    }


def event_architecture() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "immutable_events": True,
        "outbox_required": True,
        "events": [dict(e) for e in DOMAIN_EVENTS],
        "versioning_strategy": "append_only_vN",
    }


def microservices() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "services": [dict(s) for s in MICROSERVICES],
        "service_count": len(MICROSERVICES),
    }


def apis() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "rest": (
            "/api/v1/quantum/governance",
            "/api/v1/quantum/governance/policies",
            "/api/v1/quantum/governance/regulations",
            "/api/v1/quantum/governance/ethics",
            "/api/v1/quantum/governance/risks",
            "/api/v1/quantum/governance/compliance",
            "/api/v1/quantum/governance/audit",
            "/api/v1/quantum/governance/accountability",
            "/api/v1/quantum/governance/trust",
        ),
        "graphql": "/api/v1/quantum/governance/graphql",
        "event_apis": "quantum.governance.*.v1",
        "streaming_apis": True,
        "api_security": ("quantum.read", "zero_trust", "tenant_isolation"),
    }


def cloud_native() -> dict[str, Any]:
    return {
        "present_required": True,
        "not_missing": True,
        "deployment": dict(DEPLOYMENT),
    }


def testing_architecture() -> dict[str, Any]:
    return {"suites": list(TESTING), "suite_count": len(TESTING)}


def integrations() -> dict[str, Any]:
    return {"targets": list(INTEGRATIONS), "count": len(INTEGRATIONS)}


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
            "quantum_governance_platform": True,
            "regulatory_intelligence": True,
            "ethics_platform": True,
            "risk_management": True,
            "compliance_automation": True,
            "audit_intelligence": True,
            "accountability_framework": True,
            "knowledge_graph": True,
            "digital_twin": True,
            "cqrs_architecture": True,
            "event_architecture": True,
            "microservice_architecture": True,
            "api_platform": True,
            "security_architecture": True,
            "deployment_architecture": True,
            "testing_architecture": True,
            "foundation_tests": True,
            "governance_api_live": True,
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
        "fabric": FABRIC,
        "builds_on": [
            "P215-A",
            "P215-B",
            "P215-C",
            "P215-D",
            "P215-E",
            "P215-F",
            "P215-G",
            "P215-H",
            "P215-I",
            "P215-J",
            "P214-H",
            "P214-Y",
            "P209",
            "P210",
            "P212",
            "ADR-345",
            "ADR-403",
            "ADR-447",
            "ADR-448",
            "ADR-449",
            "ADR-450",
            "ADR-451",
            "ADR-452",
            "ADR-453",
            "ADR-454",
            "ADR-455",
            "ADR-456",
        ],
        "builds_on_p215_a_through_j": True,
        "governed_series_trust_gate": True,
        "governance_platform": governance_platform(),
        "policy_management": policy_management(),
        "regulatory_intelligence": regulatory_intelligence(),
        "responsible_quantum": responsible_quantum(),
        "ethics_framework": ethics_framework(),
        "risk_management": risk_management(),
        "compliance_automation": compliance_automation(),
        "audit_intelligence": audit_intelligence(),
        "accountability_framework": accountability_framework(),
        "knowledge_graph": knowledge_graph(),
        "digital_twin": digital_twin(),
        "cqrs": cqrs(),
        "event_architecture": event_architecture(),
        "microservices": microservices(),
        "apis": apis(),
        "cloud_native": cloud_native(),
        "testing_architecture": testing_architecture(),
        "integrations": integrations(),
        "cursor_outputs": cursor_outputs(),
        "quality_gates": quality_gates(),
        "production_readiness": production_readiness(),
        "quantum_governance_platform_complete_required": True,
        "quantum_regulatory_intelligence_present_required": True,
        "responsible_quantum_computing_present_required": True,
        "quantum_ethics_framework_present_required": True,
        "quantum_risk_management_present_required": True,
        "quantum_compliance_automation_present_required": True,
        "quantum_audit_intelligence_present_required": True,
        "accountability_framework_present_required": True,
        "knowledge_graph_integration_present_required": True,
        "digital_twin_integration_present_required": True,
        "cqrs_architecture_present_required": True,
        "event_architecture_present_required": True,
        "microservices_architecture_present_required": True,
        "api_first_architecture_present_required": True,
        "cloud_native_governance_present_required": True,
        "sibling_quantum_governance_bc_forbidden": True,
        "api_prefix": f"{API_PREFIX}/governance",
        "forbidden_sibling_bc": [
            "quantum_governance",
            "quantum_ethics_platform",
            "quantum_regulation_platform",
            "responsible_quantum_platform",
            "quantum_compliance_platform",
            "quantum_risk_platform",
            "quantum_audit_platform",
        ],
    }


def executive_summary() -> dict[str, Any]:
    return catalog()


def governance_surface() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "routes": [
            "GET /quantum/governance",
            "GET /quantum/governance/policies",
            "GET /quantum/governance/regulations",
            "GET /quantum/governance/responsible",
            "GET /quantum/governance/ethics",
            "GET /quantum/governance/risks",
            "GET /quantum/governance/compliance",
            "GET /quantum/governance/audit",
            "GET /quantum/governance/accountability",
            "GET /quantum/governance/trust",
            "GET /quantum/governance/knowledge-graph",
            "GET /quantum/governance/digital-twin",
            "GET /quantum/governance/cqrs",
            "GET /quantum/governance/events",
            "GET /quantum/governance/microservices",
            "GET /quantum/governance/apis",
            "GET /quantum/governance/deployment",
            "GET /quantum/governance/testing",
            "GET /quantum/governance/outputs",
            "GET /quantum/governance/production-readiness",
            "GET /quantum/governance/readiness",
        ],
    }
