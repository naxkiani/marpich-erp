"""P210-O Testing, Security Validation & Definition of Done — immutable catalog."""
from __future__ import annotations

from typing import Any

PROMPT_ID = "P210-O"
ADR = 375
SOR = "cyber_security"
API_PREFIX = "/api/v1/cyber-security"
PRODUCT = (
    "Enterprise Cyber Security & Threat Defense Platform — "
    "Enterprise Testing, Security Validation, Quality Assurance & Definition of Done"
)

MISSION_STATEMENT = (
    "Create an enterprise security validation platform capable of continuously "
    "testing cyber capabilities, validating security controls, detecting "
    "architectural weaknesses, performing adversarial simulations, ensuring "
    "production readiness, automating compliance verification, and providing "
    "measurable security confidence."
)

VISION_STATEMENT = (
    "Create a Continuous Security Assurance Fabric where every service is "
    "tested, every deployment is validated, every security control is verified, "
    "every vulnerability is measured, every AI capability is governed, and "
    "every release is trustworthy."
)

QA_PIPELINE: tuple[str, ...] = (
    "development_environment",
    "security_testing_pipeline",
    "automated_validation",
    "integration_testing",
    "adversarial_testing",
    "compliance_validation",
    "production_readiness_gate",
    "continuous_security_assurance",
)

TEST_DOMAINS: tuple[str, ...] = (
    "application_testing",
    "api_testing",
    "microservice_testing",
    "infrastructure_testing",
    "cloud_security_testing",
    "kubernetes_security_testing",
    "container_security_testing",
    "network_security_testing",
    "identity_security_testing",
    "authorization_testing",
    "cryptographic_testing",
    "ai_security_testing",
    "data_security_testing",
    "compliance_testing",
    "performance_testing",
    "resilience_testing",
)

SECURITY_TESTING: tuple[str, ...] = (
    "sast",
    "dast",
    "iast",
    "sca",
    "container_security_testing",
    "infrastructure_security_testing",
    "cloud_security_posture_testing",
    "configuration_validation",
    "secret_detection_testing",
    "supply_chain_security_testing",
)

PENTEST: tuple[str, ...] = (
    "external_penetration_testing",
    "internal_penetration_testing",
    "web_application_testing",
    "api_penetration_testing",
    "mobile_security_testing",
    "cloud_penetration_testing",
    "network_penetration_testing",
    "identity_attack_testing",
    "privilege_escalation_testing",
    "social_engineering_simulation",
)

RED_TEAM: tuple[str, ...] = (
    "threat_actor_simulation",
    "apt_simulation",
    "ransomware_simulation",
    "insider_threat_simulation",
    "cloud_attack_simulation",
    "identity_attack_simulation",
    "supply_chain_attack_simulation",
    "ai_attack_simulation",
    "mitre_attack",
    "mitre_caldera",
    "atomic_red_team",
    "purple_team_exercises",
)

BLUE_TEAM: tuple[str, ...] = (
    "detection_rules",
    "siem_correlations",
    "soar_playbooks",
    "xdr_detection",
    "threat_intelligence_feeds",
    "incident_response_procedures",
    "security_controls",
    "security_policies",
    "monitoring_coverage",
)

PURPLE_TEAM: tuple[str, ...] = (
    "attack_simulation",
    "detection_validation",
    "response_testing",
    "control_improvement",
    "threat_hunting_validation",
    "detection_engineering",
    "lessons_learned",
    "security_improvement_cycle",
)

AI_SECURITY_TESTS: tuple[str, ...] = (
    "llm_security",
    "prompt_injection",
    "jailbreak_resistance",
    "model_leakage",
    "data_exposure",
    "model_poisoning",
    "adversarial_inputs",
    "agent_security",
    "autonomous_action_safety",
    "ai_policy_enforcement",
    "ai_explainability",
    "ai_governance_controls",
)

AI_VALIDATE: tuple[str, ...] = (
    "ai_model_behaviour",
    "ai_agent_decisions",
    "ai_security_boundaries",
    "ai_risk_controls",
)

AUTO_VALIDATION: tuple[str, ...] = (
    "control_testing",
    "policy_testing",
    "configuration_testing",
    "compliance_testing",
    "security_regression_testing",
    "vulnerability_retesting",
    "deployment_validation",
    "runtime_validation",
    "continuous_verification",
)

CHAOS: tuple[str, ...] = (
    "service_failure",
    "network_failure",
    "database_failure",
    "cloud_failure",
    "security_control_failure",
    "identity_provider_failure",
    "certificate_failure",
    "key_rotation_failure",
    "ai_service_failure",
)

CHAOS_VALIDATE: tuple[str, ...] = (
    "recovery",
    "self_healing",
    "failover",
    "business_continuity",
)

PERFORMANCE: tuple[str, ...] = (
    "api_performance",
    "event_processing",
    "message_streaming",
    "database_scaling",
    "graph_queries",
    "ai_inference",
    "security_analytics",
    "threat_processing",
    "soc_workloads",
)

PERF_METRICS: tuple[str, ...] = (
    "latency",
    "throughput",
    "availability",
    "resource_utilization",
    "scalability",
)

COMPLIANCE_FRAMEWORKS: tuple[str, ...] = (
    "iso_27001",
    "nist_csf",
    "nist_zero_trust",
    "nist_ai_rmf",
    "soc_2",
    "pci_dss",
    "gdpr",
    "cis_controls",
    "mitre_attack_coverage",
)

TEST_AUTOMATION: tuple[str, ...] = (
    "cicd_integration",
    "gitops_integration",
    "security_pipeline_integration",
    "automated_test_execution",
    "test_result_analysis",
    "risk_based_testing",
    "ai_test_generation",
    "regression_testing",
)

KG_CHAIN: tuple[str, ...] = (
    "application",
    "service",
    "api",
    "asset",
    "vulnerability",
    "threat",
    "test_case",
    "security_control",
    "evidence",
    "compliance_requirement",
)

DIGITAL_TWIN: tuple[str, ...] = (
    "security_scenario_simulation",
    "attack_replay",
    "deployment_simulation",
    "control_testing",
    "architecture_validation",
    "failure_simulation",
    "production_readiness_testing",
)

OBSERVABILITY: tuple[str, ...] = (
    "test_execution",
    "security_findings",
    "coverage_percentage",
    "risk_score",
    "compliance_score",
    "false_positive_rate",
    "remediation_progress",
    "release_quality",
    "security_regression",
)

COMMANDS: tuple[str, ...] = (
    "CreateTestPlan",
    "ExecuteSecurityTest",
    "LaunchPenetrationTest",
    "StartRedTeamExercise",
    "ValidateControl",
    "GenerateComplianceEvidence",
    "ApproveRelease",
)

QUERIES: tuple[str, ...] = (
    "GetTestCoverage",
    "GetSecurityScore",
    "GetVulnerabilityStatus",
    "GetComplianceStatus",
    "GetProductionReadiness",
    "GetSecurityValidationReport",
)

DOMAIN_EVENTS: tuple[str, ...] = (
    "TestStarted",
    "TestCompleted",
    "VulnerabilityDiscovered",
    "ControlValidated",
    "SecurityFailureDetected",
    "ComplianceEvidenceGenerated",
    "ReleaseApproved",
)

MICROSERVICES: tuple[str, ...] = (
    "testing-platform-service",
    "security-validation-service",
    "penetration-testing-service",
    "red-team-service",
    "purple-team-service",
    "compliance-validation-service",
    "performance-testing-service",
    "chaos-engineering-service",
    "ai-security-testing-service",
    "reporting-service",
)

INTEGRATIONS: tuple[str, ...] = (
    "P207",
    "P208",
    "P209",
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
    "cicd_platforms",
    "git_platforms",
    "cloud_platforms",
    "security_tools",
    "compliance_platforms",
    "enterprise_ai_platform",
)

CURSOR_OUTPUTS: tuple[str, ...] = (
    "enterprise_testing_architecture",
    "security_validation_framework",
    "test_domain_model",
    "automated_security_testing_platform",
    "penetration_testing_framework",
    "red_team_platform",
    "blue_team_validation_platform",
    "purple_team_framework",
    "ai_security_testing_platform",
    "chaos_security_engineering_platform",
    "performance_testing_framework",
    "compliance_validation_engine",
    "test_automation_architecture",
    "security_knowledge_graph_model",
    "digital_twin_validation_framework",
    "cqrs_architecture",
    "event_catalogue",
    "microservice_blueprint",
    "security_dashboards",
    "production_readiness_framework",
)

QUALITY_GATES_REJECT_IF: tuple[str, ...] = (
    "security_testing_is_manual_only",
    "no_adversarial_validation_exists",
    "ai_systems_are_not_tested",
    "compliance_cannot_be_verified",
    "production_readiness_is_undefined",
    "security_controls_cannot_be_measured",
    "test_evidence_cannot_be_audited",
    "sibling_qa_bc",
)


def architecture() -> dict[str, Any]:
    return {"pipeline": list(QA_PIPELINE), "layer_count": len(QA_PIPELINE)}


def test_domains() -> dict[str, Any]:
    return {"domains": list(TEST_DOMAINS), "domain_count": len(TEST_DOMAINS)}


def security_testing() -> dict[str, Any]:
    return {
        "methods": list(SECURITY_TESTING),
        "automated_required": True,
        "not_manual_only": True,
    }


def penetration_testing() -> dict[str, Any]:
    return {
        "methods": list(PENTEST),
        "via_workflow_approval": True,
    }


def red_team() -> dict[str, Any]:
    return {
        "simulations": list(RED_TEAM),
        "adversarial_validation_required": True,
        "not_absent": True,
        "via_workflow": True,
    }


def blue_team() -> dict[str, Any]:
    return {
        "validates": list(BLUE_TEAM),
        "via_siem_soar_xdr": True,
    }


def purple_team() -> dict[str, Any]:
    return {"activities": list(PURPLE_TEAM)}


def ai_security_testing() -> dict[str, Any]:
    return {
        "tests": list(AI_SECURITY_TESTS),
        "validates": list(AI_VALIDATE),
        "ai_systems_tested_required": True,
        "not_untested": True,
        "via_p210_m": True,
        "via_enterprise_ai": True,
    }


def automated_validation() -> dict[str, Any]:
    return {"capabilities": list(AUTO_VALIDATION), "continuous": True}


def chaos() -> dict[str, Any]:
    return {
        "simulations": list(CHAOS),
        "validates": list(CHAOS_VALIDATE),
    }


def performance() -> dict[str, Any]:
    return {
        "tests": list(PERFORMANCE),
        "metrics": list(PERF_METRICS),
    }


def compliance() -> dict[str, Any]:
    return {
        "frameworks": list(COMPLIANCE_FRAMEWORKS),
        "verifiable_required": True,
        "not_unverifiable": True,
        "via_compliance_framework": True,
        "evidence_collection": True,
        "control_mapping": True,
    }


def test_automation() -> dict[str, Any]:
    return {
        "capabilities": list(TEST_AUTOMATION),
        "via_p210_n": True,
    }


def knowledge_graph() -> dict[str, Any]:
    return {
        "chain": list(KG_CHAIN),
        "via_p210_k": True,
        "capabilities": [
            "test_coverage_mapping",
            "risk_correlation",
            "control_validation",
            "security_knowledge_discovery",
        ],
    }


def digital_twin() -> dict[str, Any]:
    return {
        "capabilities": list(DIGITAL_TWIN),
        "via_p210_k": True,
    }


def observability() -> dict[str, Any]:
    return {"monitors": list(OBSERVABILITY)}


def measurable_controls() -> dict[str, Any]:
    return {
        "measurable_required": True,
        "not_unmeasurable": True,
    }


def auditable_evidence() -> dict[str, Any]:
    return {
        "auditable_required": True,
        "not_unauditable": True,
        "via_audit_platform": True,
    }


def production_readiness_gate() -> dict[str, Any]:
    return {
        "defined_required": True,
        "not_undefined": True,
        "via_workflow": True,
    }


def ddd() -> dict[str, Any]:
    return {
        "sor": SOR,
        "logical_subdomains": [
            "security_testing",
            "penetration_testing",
            "red_blue_purple",
            "ai_security_testing",
            "chaos_resilience",
            "performance_scale",
            "compliance_validation",
            "production_readiness",
        ],
        "sibling_bc_forbidden": [
            "qa_platform",
            "security_testing",
            "red_team",
            "penetration_testing",
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
            "security_testing_automated": True,
            "adversarial_validation": True,
            "ai_systems_tested": True,
            "compliance_verifiable": True,
            "production_readiness_defined": True,
            "controls_measurable": True,
            "evidence_auditable": True,
            "foundation_tests": True,
            "qa_api_live": True,
            "p210_series_complete": True,
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
            "P210-I",
            "P210-J",
            "P210-K",
            "P210-L",
            "P210-M",
            "P210-N",
            "ADR-361",
            "ADR-362",
            "ADR-363",
            "ADR-364",
            "ADR-365",
            "ADR-366",
            "ADR-367",
            "ADR-368",
            "ADR-369",
            "ADR-370",
            "ADR-371",
            "ADR-372",
            "ADR-373",
            "ADR-374",
        ],
        "architecture": architecture(),
        "test_domains": test_domains(),
        "security_testing": security_testing(),
        "penetration_testing": penetration_testing(),
        "red_team": red_team(),
        "blue_team": blue_team(),
        "purple_team": purple_team(),
        "ai_security_testing": ai_security_testing(),
        "automated_validation": automated_validation(),
        "chaos": chaos(),
        "performance": performance(),
        "compliance": compliance(),
        "test_automation": test_automation(),
        "knowledge_graph": knowledge_graph(),
        "digital_twin": digital_twin(),
        "observability": observability(),
        "measurable_controls": measurable_controls(),
        "auditable_evidence": auditable_evidence(),
        "production_readiness_gate": production_readiness_gate(),
        "ddd": ddd(),
        "cqrs": cqrs(),
        "microservices": microservices(),
        "integrations": integrations(),
        "cursor_outputs": cursor_outputs(),
        "quality_gates": quality_gates(),
        "production_readiness": production_readiness(),
        "security_testing_automated_required": True,
        "adversarial_validation_required": True,
        "ai_systems_tested_required": True,
        "compliance_verifiable_required": True,
        "production_readiness_defined_required": True,
        "security_controls_measurable_required": True,
        "test_evidence_auditable_required": True,
        "sibling_qa_bc_forbidden": True,
        "api_prefix": f"{API_PREFIX}/qa",
        "forbidden_sibling_bc": [
            "qa_platform",
            "security_testing",
            "red_team",
            "penetration_testing",
        ],
        "distinct_from": [
            "compliance framework (evidence orchestration)",
            "P210-N /deploy* (pipeline plumbing)",
            "P210-M /gov* (AI governance policy)",
            "workflow approvals for destructive tests",
        ],
        "series_complete": True,
    }


def executive_summary() -> dict[str, Any]:
    return catalog()


def qa_surface() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "routes": [
            "GET /cyber-security/qa",
            "GET /cyber-security/qa/architecture",
            "GET /cyber-security/qa/domains",
            "GET /cyber-security/qa/security-testing",
            "GET /cyber-security/qa/penetration",
            "GET /cyber-security/qa/red-team",
            "GET /cyber-security/qa/blue-team",
            "GET /cyber-security/qa/purple-team",
            "GET /cyber-security/qa/ai-security",
            "GET /cyber-security/qa/validation",
            "GET /cyber-security/qa/chaos",
            "GET /cyber-security/qa/performance",
            "GET /cyber-security/qa/compliance",
            "GET /cyber-security/qa/automation",
            "GET /cyber-security/qa/knowledge-graph",
            "GET /cyber-security/qa/digital-twin",
            "GET /cyber-security/qa/observability",
            "GET /cyber-security/qa/cqrs",
            "GET /cyber-security/qa/events",
            "GET /cyber-security/qa/microservices",
            "GET /cyber-security/qa/integrations",
            "GET /cyber-security/qa/outputs",
            "GET /cyber-security/qa/production-readiness",
            "GET /cyber-security/qa/readiness",
        ],
    }
