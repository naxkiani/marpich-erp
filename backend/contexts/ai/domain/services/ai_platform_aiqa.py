"""P214-O Enterprise AI Testing, Evaluation, Validation & Quality Assurance — immutable catalog."""
from __future__ import annotations

from typing import Any

PROMPT_ID = "P214-O"
ADR = 435
SOR = "ai"
API_PREFIX = "/api/v1/ai"
PRODUCT = (
    "Enterprise AI Testing, Evaluation, Validation & AI Quality Assurance Platform"
)
CAPABILITY = "CAP-PLT-AI-001"

PRINCIPLE = (
    "Enterprise AI Quality Platform SHALL transform AI quality from manual "
    "verification into continuous intelligent validation and autonomous improvement."
)

FABRIC = "meos_enterprise_ai_quality_intelligence_fabric"

CORE_DOMAIN = "enterprise_ai_quality_intelligence_management"

SUPPORTING_DOMAINS: tuple[dict[str, str], ...] = (
    {"id": "ai_testing", "purpose": "Test management, execution, automation, reporting."},
    {"id": "ai_evaluation", "purpose": "Model/output evaluation and quality measurement."},
    {"id": "ai_validation", "purpose": "Requirement, business, compliance validation."},
    {"id": "ai_benchmarking", "purpose": "Benchmarks, comparative analysis, ranking."},
    {"id": "ai_safety_testing", "purpose": "Safety, harm detection, RAI testing."},
    {"id": "ai_reliability_testing", "purpose": "Failure, resilience, availability."},
    {"id": "ai_regression_testing", "purpose": "Change detection and rollback signals."},
    {"id": "ai_certification", "purpose": "Approval, quality certification, evidence."},
    {"id": "ai_quality_intelligence", "purpose": "Quality scores and AI Quality Index."},
)

AGGREGATE = {
    "name": "EnterpriseAIQualityAssuranceAggregate",
    "root": "EnterpriseAIQualityAssurance",
    "entities": (
        "AITestSuite",
        "AITestCase",
        "AIEvaluationRun",
        "AIValidationReport",
        "AIQualityScore",
        "AIBenchmark",
        "AISafetyAssessment",
        "AIRegressionTest",
        "AICertification",
        "QualityPolicy",
    ),
    "value_objects": (
        "TestIdentifier",
        "EvaluationScore",
        "QualityScore",
        "ConfidenceScore",
        "RiskScore",
        "ValidationStatus",
        "CertificationStatus",
        "PerformanceMetric",
    ),
    "events": (
        "AITestCreatedEvent",
        "EvaluationStartedEvent",
        "ValidationCompletedEvent",
        "QualityScoreUpdatedEvent",
        "SafetyViolationDetectedEvent",
        "CertificationGrantedEvent",
        "RegressionDetectedEvent",
    ),
}

LOGICAL_BOUNDED_CONTEXTS: tuple[dict[str, Any], ...] = (
    {
        "id": "ai_testing",
        "bc": "BC-01",
        "name": "AI Testing Context",
        "purpose": "Test management, execution, automation, reporting.",
    },
    {
        "id": "ai_evaluation",
        "bc": "BC-02",
        "name": "AI Evaluation Context",
        "purpose": "Model evaluation, output evaluation, quality measurement.",
    },
    {
        "id": "ai_validation",
        "bc": "BC-03",
        "name": "AI Validation Context",
        "purpose": "Requirement, business, and compliance validation.",
    },
    {
        "id": "ai_benchmarking",
        "bc": "BC-04",
        "name": "AI Benchmarking Context",
        "purpose": "Benchmark management, comparative analysis, ranking.",
    },
    {
        "id": "ai_safety_testing",
        "bc": "BC-05",
        "name": "AI Safety Testing Context",
        "purpose": "Safety validation, harm detection, responsible AI testing.",
    },
    {
        "id": "ai_reliability_testing",
        "bc": "BC-06",
        "name": "AI Reliability Testing Context",
        "purpose": "Failure testing, resilience testing, availability validation.",
    },
    {
        "id": "ai_certification",
        "bc": "BC-07",
        "name": "AI Certification Context",
        "purpose": "AI approval, quality certification, governance evidence.",
    },
)

AI_TESTING = {
    "present_required": True,
    "framework": "meos_ai_testing_framework",
    "supports": (
        "model_testing",
        "llm_testing",
        "agent_testing",
        "rag_testing",
        "ai_application_testing",
        "ai_infrastructure_testing",
    ),
    "types": (
        "functional_testing",
        "integration_testing",
        "performance_testing",
        "security_testing",
        "safety_testing",
        "regression_testing",
    ),
}

MODEL_EVALUATION = {
    "present_required": True,
    "engine": "enterprise_ai_evaluation_intelligence_engine",
    "evaluates": (
        "accuracy",
        "precision",
        "recall",
        "robustness",
        "fairness",
        "explainability",
        "reliability",
        "consistency",
        "cost_efficiency",
    ),
    "supports": (
        "automated_evaluation",
        "human_evaluation",
        "benchmark_evaluation",
    ),
}

GENAI_QUALITY = {
    "present_required": True,
    "via_p214_e": True,
    "framework": "enterprise_llm_evaluation_framework",
    "evaluates": (
        "response_quality",
        "hallucination_rate",
        "context_accuracy",
        "reasoning_quality",
        "instruction_following",
        "safety_alignment",
        "token_efficiency",
    ),
    "supports": (
        "prompt_testing",
        "response_testing",
        "rag_evaluation",
        "agent_evaluation",
    ),
}

AGENT_TESTING = {
    "present_required": True,
    "via_p214_f": True,
    "framework": "autonomous_agent_validation_framework",
    "tests": (
        "agent_planning",
        "tool_usage",
        "decision_making",
        "memory_usage",
        "collaboration",
        "goal_achievement",
    ),
    "supports": (
        "multi_agent_simulation",
        "agent_failure_testing",
        "agent_safety_testing",
    ),
}

SAFETY_VALIDATION = {
    "present_required": True,
    "via_p214_h": True,
    "via_p214_i": True,
    "engine": "responsible_ai_testing_engine",
    "validates": (
        "bias",
        "fairness",
        "privacy",
        "security",
        "safety",
        "transparency",
        "explainability",
    ),
}

PERFORMANCE_TESTING = {
    "present_required": True,
    "measures": (
        "latency",
        "throughput",
        "scalability",
        "resource_usage",
        "inference_speed",
        "cost_efficiency",
    ),
    "supports": (
        "load_testing",
        "stress_testing",
        "capacity_testing",
        "performance_benchmarking",
    ),
}

REGRESSION_TESTING = {
    "present_required": True,
    "intelligence": "continuous_ai_regression_intelligence",
    "monitors": (
        "model_changes",
        "prompt_changes",
        "data_changes",
        "infrastructure_changes",
        "behavior_changes",
    ),
    "supports": (
        "automated_regression_detection",
        "quality_comparison",
        "rollback_recommendation",
    ),
}

QUALITY_SCORE = {
    "present_required": True,
    "platform": "enterprise_ai_quality_intelligence_score",
    "calculates": (
        "accuracy_score",
        "safety_score",
        "reliability_score",
        "performance_score",
        "compliance_score",
        "trust_score",
    ),
    "index": "ai_quality_index",
}

QUALITY_KNOWLEDGE_GRAPH = {
    "present_required": True,
    "via_p214_g": True,
    "represents": (
        "models",
        "datasets",
        "tests",
        "results",
        "failures",
        "risks",
        "policies",
        "certifications",
    ),
    "enables": (
        "impact_analysis",
        "failure_prediction",
        "quality_optimization",
    ),
}

QUALITY_DIGITAL_TWIN = {
    "present_required": True,
    "represents": (
        "ai_system_state",
        "quality_state",
        "risk_state",
        "test_state",
        "compliance_state",
    ),
    "enables": (
        "simulation",
        "prediction",
        "optimization",
        "certification_planning",
    ),
}

COMMANDS: tuple[str, ...] = (
    "CreateAITestCommand",
    "ExecuteEvaluationCommand",
    "ValidateAIComponentCommand",
    "RunBenchmarkCommand",
    "GenerateQualityReportCommand",
    "ApproveCertificationCommand",
)

QUERIES: tuple[str, ...] = (
    "GetTestResultQuery",
    "GetEvaluationQuery",
    "GetQualityScoreQuery",
    "GetValidationReportQuery",
    "GetCertificationStatusQuery",
)

CORE_EVENTS: tuple[dict[str, str], ...] = (
    {"name": "TestCreatedEvent", "owner": "ai", "consumers": "audit,mlops"},
    {"name": "TestExecutedEvent", "owner": "ai", "consumers": "observability,aiops"},
    {"name": "EvaluationCompletedEvent", "owner": "ai", "consumers": "modelintel,governance"},
    {"name": "QualityScoreChangedEvent", "owner": "ai", "consumers": "analytics,notifications"},
    {"name": "FailureDetectedEvent", "owner": "ai", "consumers": "aiops,aisec,notifications"},
    {"name": "CertificationGrantedEvent", "owner": "ai", "consumers": "audit,governance,workflow"},
    {"name": "RegressionDetectedEvent", "owner": "ai", "consumers": "mlops,modelintel,notifications"},
    {"name": "SafetyViolationDetectedEvent", "owner": "ai", "consumers": "governance,aisec,audit"},
)

MICROSERVICES: tuple[dict[str, Any], ...] = (
    {
        "id": "ai_testing_service",
        "responsibility": "AI test suite management and execution",
        "api": "/ai/aiqa/tests",
        "db": "ai_*",
        "events": ("TestCreatedEvent", "TestExecutedEvent"),
        "security": ("ai.assist.infer",),
        "scaling": "compute_burst",
    },
    {
        "id": "evaluation_service",
        "responsibility": "model and output evaluation intelligence",
        "api": "/ai/aiqa/evaluation",
        "db": "ai_*",
        "events": ("EvaluationCompletedEvent",),
        "security": ("ai.assist.infer",),
        "scaling": "compute_burst",
    },
    {
        "id": "validation_service",
        "responsibility": "requirement business compliance validation",
        "api": "/ai/aiqa/validation",
        "db": "ai_*",
        "events": ("EvaluationCompletedEvent",),
        "security": ("ai.assist.read",),
        "scaling": "control_plane",
    },
    {
        "id": "benchmark_service",
        "responsibility": "benchmark runs and comparative ranking",
        "api": "/ai/aiqa/benchmarks",
        "db": "ai_*",
        "events": ("EvaluationCompletedEvent",),
        "security": ("ai.assist.infer",),
        "scaling": "batch_workers",
    },
    {
        "id": "safety_testing_service",
        "responsibility": "RAI safety and harm detection tests",
        "api": "/ai/aiqa/safety",
        "db": "ai_*",
        "events": ("SafetyViolationDetectedEvent",),
        "security": ("ai.assist.infer",),
        "scaling": "async_workers",
    },
    {
        "id": "performance_testing_service",
        "responsibility": "latency throughput stress capacity tests",
        "api": "/ai/aiqa/performance",
        "db": "ai_*",
        "events": ("TestExecutedEvent",),
        "security": ("ai.assist.infer",),
        "scaling": "load_generators",
    },
    {
        "id": "regression_service",
        "responsibility": "continuous regression detection and rollback signals",
        "api": "/ai/aiqa/regression",
        "db": "ai_*",
        "events": ("RegressionDetectedEvent",),
        "security": ("ai.assist.infer",),
        "scaling": "stream_consumers",
    },
    {
        "id": "quality_intelligence_service",
        "responsibility": "AI Quality Index and score aggregation",
        "api": "/ai/aiqa/quality",
        "db": "ai_*",
        "events": ("QualityScoreChangedEvent",),
        "security": ("ai.assist.read",),
        "scaling": "analytics_pipeline",
    },
    {
        "id": "certification_service",
        "responsibility": "quality certification and governance evidence",
        "api": "/ai/aiqa/certification",
        "db": "ai_*",
        "events": ("CertificationGrantedEvent",),
        "security": ("ai.assist.read",),
        "scaling": "control_plane",
    },
    {
        "id": "reporting_service",
        "responsibility": "quality reports and validation evidence packs",
        "api": "/ai/aiqa/reports",
        "db": "ai_*",
        "events": ("QualityScoreChangedEvent", "CertificationGrantedEvent"),
        "security": ("ai.assist.read",),
        "scaling": "catalog_ha",
    },
)

API_SURFACES: tuple[str, ...] = (
    "/api/v1/ai/aiqa/tests",
    "/api/v1/ai/aiqa/evaluation",
    "/api/v1/ai/aiqa/validation",
    "/api/v1/ai/aiqa/benchmarks",
    "/api/v1/ai/aiqa/safety",
    "/api/v1/ai/aiqa/performance",
    "/api/v1/ai/aiqa/regression",
    "/api/v1/ai/aiqa/certification",
)

API_STYLES: tuple[str, ...] = ("REST", "GraphQL", "gRPC", "Streaming", "Event")

SECURITY = {
    "present_required": True,
    "zero_trust": True,
    "integrates": ("P207", "P208", "P209", "P210", "P214-H", "P214-I"),
    "controls": (
        "test_access_control",
        "evaluation_authorization",
        "certification_approval",
        "evidence_protection",
        "audit_security",
    ),
}

DEPLOYMENT = {
    "present_required": True,
    "cloud_native": True,
    "via_p213_o": True,
    "via_p214_n": True,
    "components": (
        "kubernetes",
        "testing_execution_cluster",
        "evaluation_engine",
        "benchmark_infrastructure",
        "quality_database",
        "reporting_platform",
        "observability_integration",
    ),
}

TESTING: tuple[str, ...] = (
    "ai_testing_testing",
    "model_validation_testing",
    "llm_evaluation_testing",
    "agent_testing",
    "security_testing",
    "safety_testing",
    "performance_testing",
    "regression_testing",
    "compliance_testing",
    "chaos_testing",
)

CURSOR_OUTPUTS: tuple[str, ...] = (
    "enterprise_ai_quality_vision",
    "ddd_domain_model",
    "bounded_context_map",
    "ai_testing_framework",
    "model_evaluation_engine",
    "genai_quality_testing",
    "agent_testing_platform",
    "safety_validation_platform",
    "performance_testing_platform",
    "regression_intelligence",
    "quality_score_platform",
    "quality_knowledge_graph",
    "quality_digital_twin",
    "cqrs_commands_queries",
    "event_sourcing_schema",
    "microservice_boundaries",
    "integration_architecture",
    "cloud_native_deployment",
    "testing_architecture",
    "quality_gates_dod",
    "adr_435",
    "enterprise_ai_aiqa_law",
)

QUALITY_GATES_REJECT_IF: tuple[str, ...] = (
    "enterprise_ai_testing_platform_is_missing",
    "ai_evaluation_platform_is_missing",
    "ai_validation_platform_is_missing",
    "ai_quality_assurance_platform_is_missing",
    "ai_benchmarking_platform_is_missing",
    "ai_safety_testing_is_missing",
    "ai_reliability_testing_is_missing",
    "ai_regression_testing_is_missing",
    "ai_certification_platform_is_missing",
    "quality_intelligence_platform_is_missing",
    "knowledge_graph_integration_is_missing",
    "digital_twin_integration_is_missing",
    "cqrs_architecture_is_missing",
    "event_architecture_is_missing",
    "microservices_architecture_is_missing",
    "api_first_architecture_is_missing",
    "zero_trust_security_is_missing",
    "cloud_native_deployment_is_missing",
    "sibling_ai_bc",
)


def vision() -> dict[str, Any]:
    return {
        "role": "MEOS Enterprise AI Quality Intelligence Fabric",
        "principle": PRINCIPLE,
        "equation": (
            "AI Data + AI Models + AI Agents + LLM Systems + AI Applications + "
            "AI Infrastructure → Tested → Evaluated → Validated → Certified → "
            "Monitored → Improved"
        ),
        "pillars": (
            "specialized_ai_testing_required",
            "traditional_software_testing_insufficient",
            "continuous_output_evaluation",
            "quality_changes_over_time",
            "measurable_validation_for_trust",
        ),
        "strategic_role": {
            "specialized_testing": (
                "AI systems need eval of accuracy, fairness, hallucination, and "
                "agent behavior — beyond unit/integration tests alone."
            ),
            "traditional_insufficient": (
                "Deterministic assertions miss stochastic model and GenAI outcomes."
            ),
            "continuous_evaluation": (
                "Outputs and drift require ongoing evaluation after deploy."
            ),
            "quality_over_time": (
                "Data, prompts, models, and infra changes alter quality continuously."
            ),
            "measurable_trust": (
                "Trust requires scored validation, certification evidence, and audit."
            ),
        },
    }


def domain_model() -> dict[str, Any]:
    return {
        "core_domain": CORE_DOMAIN,
        "supporting_domains": [dict(d) for d in SUPPORTING_DOMAINS],
        "supporting_count": len(SUPPORTING_DOMAINS),
        "aggregate": dict(AGGREGATE),
    }


def bounded_contexts() -> dict[str, Any]:
    return {
        "contexts": [dict(c) for c in LOGICAL_BOUNDED_CONTEXTS],
        "context_count": len(LOGICAL_BOUNDED_CONTEXTS),
        "logical_partitions_same_sor": True,
    }


def testing_platform() -> dict[str, Any]:
    return dict(AI_TESTING)


def evaluation() -> dict[str, Any]:
    return dict(MODEL_EVALUATION)


def genai_quality() -> dict[str, Any]:
    return dict(GENAI_QUALITY)


def agent_testing() -> dict[str, Any]:
    return dict(AGENT_TESTING)


def safety() -> dict[str, Any]:
    return dict(SAFETY_VALIDATION)


def performance() -> dict[str, Any]:
    return dict(PERFORMANCE_TESTING)


def regression() -> dict[str, Any]:
    return dict(REGRESSION_TESTING)


def quality_score() -> dict[str, Any]:
    return dict(QUALITY_SCORE)


def knowledge_graph() -> dict[str, Any]:
    return dict(QUALITY_KNOWLEDGE_GRAPH)


def digital_twin() -> dict[str, Any]:
    return dict(QUALITY_DIGITAL_TWIN)


def cqrs() -> dict[str, Any]:
    return {
        "commands": list(COMMANDS),
        "command_count": len(COMMANDS),
        "queries": list(QUERIES),
        "query_count": len(QUERIES),
        "alignment_present_required": True,
    }


def events() -> dict[str, Any]:
    return {
        "core_events": [dict(e) for e in CORE_EVENTS],
        "core_event_count": len(CORE_EVENTS),
        "event_driven_required": True,
        "retention_policy": "tenant_scoped_immutable_append",
        "version_strategy": "event_version_field",
        "ownership": "ai",
    }


def microservices() -> dict[str, Any]:
    return {
        "services": [dict(s) for s in MICROSERVICES],
        "service_count": len(MICROSERVICES),
        "logical_decomposition": True,
    }


def api() -> dict[str, Any]:
    return {
        "surfaces": list(API_SURFACES),
        "styles": list(API_STYLES),
        "api_first_present_required": True,
    }


def integrations() -> dict[str, Any]:
    return {
        "peers": (
            "P214-D",
            "P214-E",
            "P214-F",
            "P214-G",
            "P214-H",
            "P214-I",
            "P214-J",
            "P214-K",
            "P214-L",
            "P214-M",
            "P214-N",
            "P207",
            "P208",
            "P209",
            "P210",
            "workflow",
        ),
        "via_events_and_acl": True,
    }


def security() -> dict[str, Any]:
    return dict(SECURITY)


def deployment() -> dict[str, Any]:
    return dict(DEPLOYMENT)


def testing() -> dict[str, Any]:
    return {"suites": list(TESTING), "suite_count": len(TESTING)}


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
            "enterprise_ai_testing_platform": True,
            "ai_evaluation_platform": True,
            "ai_validation_platform": True,
            "ai_quality_intelligence": True,
            "ai_benchmarking": True,
            "ai_safety_testing": True,
            "ai_reliability_testing": True,
            "ai_regression_testing": True,
            "ai_certification": True,
            "cqrs_architecture": True,
            "event_architecture": True,
            "microservice_architecture": True,
            "api_platform": True,
            "security_architecture": True,
            "knowledge_graph": True,
            "digital_twin": True,
            "deployment_architecture": True,
            "testing_architecture": True,
            "foundation_tests": True,
            "aiqa_api_live": True,
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
            "P214-A",
            "P214-B",
            "P214-C",
            "P214-D",
            "P214-E",
            "P214-F",
            "P214-G",
            "P214-H",
            "P214-I",
            "P214-J",
            "P214-K",
            "P214-L",
            "P214-M",
            "P214-N",
            "ADR-421",
            "ADR-422",
            "ADR-423",
            "ADR-424",
            "ADR-425",
            "ADR-426",
            "ADR-427",
            "ADR-428",
            "ADR-429",
            "ADR-430",
            "ADR-431",
            "ADR-432",
            "ADR-433",
            "ADR-434",
            "AI_PLATFORM_STANDARD",
        ],
        "vision": vision(),
        "domain_model": domain_model(),
        "bounded_contexts": bounded_contexts(),
        "testing_platform": testing_platform(),
        "evaluation": evaluation(),
        "genai_quality": genai_quality(),
        "agent_testing": agent_testing(),
        "safety": safety(),
        "performance": performance(),
        "regression": regression(),
        "quality_score": quality_score(),
        "knowledge_graph": knowledge_graph(),
        "digital_twin": digital_twin(),
        "cqrs": cqrs(),
        "events": events(),
        "microservices": microservices(),
        "api": api(),
        "integrations": integrations(),
        "security": security(),
        "deployment": deployment(),
        "testing": testing(),
        "cursor_outputs": cursor_outputs(),
        "quality_gates": quality_gates(),
        "production_readiness": production_readiness(),
        "enterprise_ai_testing_platform_present_required": True,
        "ai_evaluation_platform_present_required": True,
        "ai_validation_platform_present_required": True,
        "ai_quality_assurance_platform_present_required": True,
        "ai_benchmarking_platform_present_required": True,
        "ai_safety_testing_present_required": True,
        "ai_reliability_testing_present_required": True,
        "ai_regression_testing_present_required": True,
        "ai_certification_platform_present_required": True,
        "quality_intelligence_platform_present_required": True,
        "knowledge_graph_integration_present_required": True,
        "digital_twin_integration_present_required": True,
        "cqrs_architecture_present_required": True,
        "event_architecture_present_required": True,
        "microservices_architecture_present_required": True,
        "api_first_architecture_present_required": True,
        "zero_trust_security_present_required": True,
        "cloud_native_deployment_present_required": True,
        "sibling_ai_bc_forbidden": True,
        "module_local_ai_qa_forbidden": True,
        "via_enterprise_ai": True,
        "via_api_gateway": True,
        "api_prefix": f"{API_PREFIX}/aiqa",
        "forbidden_sibling_bc": [
            "ai_testing",
            "ai_qa",
            "ai_evaluation",
            "ai_quality",
            "ai_validation",
            "ai_benchmarking",
            "generative_ai",
            "llm_platform",
            "ai_core",
            "vector_intelligence",
            "ml_platform",
        ],
    }


def aiqa_surface() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "routes": [
            "GET /ai/aiqa",
            "GET /ai/aiqa/vision",
            "GET /ai/aiqa/domain",
            "GET /ai/aiqa/bounded-contexts",
            "GET /ai/aiqa/testing",
            "GET /ai/aiqa/evaluation",
            "GET /ai/aiqa/genai-quality",
            "GET /ai/aiqa/agent-testing",
            "GET /ai/aiqa/safety",
            "GET /ai/aiqa/performance",
            "GET /ai/aiqa/regression",
            "GET /ai/aiqa/quality-score",
            "GET /ai/aiqa/knowledge-graph",
            "GET /ai/aiqa/digital-twin",
            "GET /ai/aiqa/cqrs",
            "GET /ai/aiqa/events",
            "GET /ai/aiqa/microservices",
            "GET /ai/aiqa/integrations",
            "GET /ai/aiqa/api",
            "GET /ai/aiqa/security",
            "GET /ai/aiqa/deployment",
            "GET /ai/aiqa/testing-suites",
            "GET /ai/aiqa/outputs",
            "GET /ai/aiqa/production-readiness",
            "GET /ai/aiqa/readiness",
        ],
    }
