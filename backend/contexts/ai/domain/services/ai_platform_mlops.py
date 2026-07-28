"""P214-D Enterprise MLOps Platform — immutable catalog."""
from __future__ import annotations

from typing import Any

PROMPT_ID = "P214-D"
ADR = 424
SOR = "ai"
API_PREFIX = "/api/v1/ai"
PRODUCT = "Enterprise Machine Learning Operations (MLOps) Platform"
CAPABILITY = "CAP-PLT-AI-001"

PRINCIPLE = (
    "Enterprise MLOps SHALL transform machine learning from isolated "
    "experiments into governed, scalable, secure and continuously "
    "improving enterprise capabilities."
)

FABRIC = "meos_enterprise_machine_learning_intelligence_fabric"

CORE_DOMAIN = "enterprise_machine_learning_lifecycle_management"

LIFECYCLE_FLOW: tuple[str, ...] = (
    "data",
    "experiment",
    "train",
    "validate",
    "register",
    "deploy",
    "monitor",
    "improve",
    "retrain",
)

SUPPORTING_DOMAINS: tuple[dict[str, str], ...] = (
    {"id": "ml_experiment_management", "purpose": "Track and compare experiments."},
    {"id": "feature_management", "purpose": "Govern feature engineering and reuse."},
    {"id": "training_management", "purpose": "Orchestrate training jobs and resources."},
    {"id": "model_registry", "purpose": "Version, approve, and store model artifacts."},
    {"id": "model_deployment", "purpose": "Serve models for inference."},
    {"id": "model_monitoring", "purpose": "Detect drift and quality regressions."},
    {"id": "model_governance", "purpose": "Compliance, approval, and risk controls."},
    {"id": "ml_infrastructure_management", "purpose": "GPU, pipelines, and runtimes."},
    {"id": "ml_security", "purpose": "Protect artifacts, datasets, and serving."},
)

AGGREGATE = {
    "name": "MLLifecycleAggregate",
    "root": "MLLifecycle",
    "entities": (
        "MLModel",
        "ModelVersion",
        "Experiment",
        "TrainingRun",
        "DatasetVersion",
        "FeatureSet",
        "FeaturePipeline",
        "EvaluationResult",
        "DeploymentInstance",
        "MonitoringProfile",
        "RetrainingPolicy",
    ),
    "value_objects": (
        "ModelIdentifier",
        "ExperimentIdentifier",
        "DatasetIdentifier",
        "FeatureIdentifier",
        "AccuracyScore",
        "PrecisionScore",
        "RecallScore",
        "LatencyScore",
        "TrainingConfiguration",
        "DeploymentConfiguration",
    ),
    "events": (
        "ExperimentCreatedEvent",
        "TrainingStartedEvent",
        "TrainingCompletedEvent",
        "ModelValidatedEvent",
        "ModelRegisteredEvent",
        "ModelDeployedEvent",
        "ModelPerformanceChangedEvent",
        "RetrainingTriggeredEvent",
    ),
}

LOGICAL_BOUNDED_CONTEXTS: tuple[dict[str, Any], ...] = (
    {
        "id": "ml_experiment",
        "bc": "BC-01",
        "name": "ML Experiment Context",
        "purpose": "Experiment lifecycle, research workflows, HPO, comparison.",
    },
    {
        "id": "feature_engineering",
        "bc": "BC-02",
        "name": "Feature Engineering Context",
        "purpose": "Feature creation, storage, reuse, and governance.",
    },
    {
        "id": "training_pipeline",
        "bc": "BC-03",
        "name": "Training Pipeline Context",
        "purpose": "Training orchestration, distributed training, resources.",
    },
    {
        "id": "model_registry",
        "bc": "BC-04",
        "name": "Model Registry Context",
        "purpose": "Versioning, approval, metadata, and lifecycle.",
    },
    {
        "id": "model_deployment",
        "bc": "BC-05",
        "name": "Model Deployment Context",
        "purpose": "Serving, inference deployment, scaling, runtime.",
    },
    {
        "id": "model_monitoring",
        "bc": "BC-06",
        "name": "Model Monitoring Context",
        "purpose": "Performance, drift, quality monitoring, alerting.",
    },
    {
        "id": "ml_governance",
        "bc": "BC-07",
        "name": "ML Governance Context",
        "purpose": "Compliance, approval, audit, risk management.",
    },
)

LIFECYCLE_STAGES: tuple[dict[str, Any], ...] = (
    {
        "id": "problem_definition",
        "process": "Frame business ML problem",
        "owner": "ai_product_owner",
        "technology": "intake_catalog",
        "governance": "use_case_approval",
        "metrics": ("problem_clarity_score",),
    },
    {
        "id": "data_discovery",
        "process": "Locate governed datasets",
        "owner": "data_steward",
        "technology": "data_catalog",
        "governance": "p212_access",
        "metrics": ("dataset_coverage",),
    },
    {
        "id": "data_preparation",
        "process": "Clean and version training data",
        "owner": "ml_engineer",
        "technology": "data_pipelines",
        "governance": "privacy_controls",
        "metrics": ("data_quality_score",),
    },
    {
        "id": "feature_engineering",
        "process": "Build and publish features",
        "owner": "feature_owner",
        "technology": "feature_store",
        "governance": "feature_lineage",
        "metrics": ("feature_reuse_rate",),
    },
    {
        "id": "experimentation",
        "process": "Run tracked experiments",
        "owner": "data_scientist",
        "technology": "experiment_tracker",
        "governance": "reproducibility",
        "metrics": ("experiment_throughput",),
    },
    {
        "id": "training",
        "process": "Train candidate models",
        "owner": "ml_engineer",
        "technology": "gpu_training",
        "governance": "training_security",
        "metrics": ("training_cost", "accuracy"),
    },
    {
        "id": "validation",
        "process": "Validate quality and risk",
        "owner": "ml_governance",
        "technology": "validation_suite",
        "governance": "approval_gates",
        "metrics": ("bias_score", "robustness"),
    },
    {
        "id": "registration",
        "process": "Register model versions",
        "owner": "model_owner",
        "technology": "model_registry",
        "governance": "metadata_complete",
        "metrics": ("registry_completeness",),
    },
    {
        "id": "approval",
        "process": "Approve for production",
        "owner": "ai_risk_owner",
        "technology": "workflow",
        "governance": "responsible_ai",
        "metrics": ("approval_cycle_time",),
    },
    {
        "id": "deployment",
        "process": "Serve model endpoints",
        "owner": "ml_platform",
        "technology": "model_serving",
        "governance": "canary_policy",
        "metrics": ("latency_p95", "availability"),
    },
    {
        "id": "monitoring",
        "process": "Observe production quality",
        "owner": "sre_ai_ops",
        "technology": "monitoring_stack",
        "governance": "alert_slas",
        "metrics": ("drift_score", "business_impact"),
    },
    {
        "id": "optimization",
        "process": "Tune cost and performance",
        "owner": "ml_engineer",
        "technology": "autoscaling",
        "governance": "finops",
        "metrics": ("cost_per_prediction",),
    },
    {
        "id": "retraining",
        "process": "Trigger continuous learning",
        "owner": "ml_platform",
        "technology": "retraining_pipeline",
        "governance": "retrain_approval",
        "metrics": ("retrain_success_rate",),
    },
)

EXPERIMENT_PLATFORM: dict[str, Any] = {
    "capabilities": (
        "experiment_tracking",
        "parameter_management",
        "metric_tracking",
        "artifact_storage",
        "reproducibility",
        "collaboration",
        "experiment_comparison",
    ),
    "repository": True,
    "metadata": True,
    "versioning": True,
    "approval_workflow": True,
    "present_required": True,
}

FEATURE_STORE: dict[str, Any] = {
    "via_p212": True,
    "capabilities": (
        "offline_feature_store",
        "online_feature_store",
        "feature_discovery",
        "feature_versioning",
        "feature_lineage",
        "feature_governance",
        "feature_reuse",
    ),
    "present_required": True,
}

TRAINING_PLATFORM: dict[str, Any] = {
    "capabilities": (
        "training_pipelines",
        "distributed_training",
        "gpu_training",
        "hyperparameter_optimization",
        "automated_training",
        "neural_network_training",
        "deep_learning_training",
        "classical_ml_training",
    ),
    "infrastructure": True,
    "workflow": True,
    "security": True,
    "monitoring": True,
    "present_required": True,
}

MODEL_REGISTRY: dict[str, Any] = {
    "manages": (
        "model_metadata",
        "model_versions",
        "model_artifacts",
        "model_ownership",
        "model_status",
        "model_approval",
        "model_dependencies",
        "model_lineage",
    ),
    "lifecycle": (
        "development",
        "testing",
        "validation",
        "approval",
        "production",
        "retirement",
    ),
    "present_required": True,
}

VALIDATION_PLATFORM: dict[str, Any] = {
    "tests": (
        "accuracy_testing",
        "bias_testing",
        "robustness_testing",
        "explainability_testing",
        "security_testing",
        "performance_testing",
        "data_drift_testing",
        "concept_drift_testing",
    ),
    "framework": True,
    "policies": True,
    "approval_gates": True,
    "present_required": True,
}

DEPLOYMENT_PLATFORM: dict[str, Any] = {
    "modes": (
        "online_inference",
        "batch_inference",
        "real_time_prediction",
        "edge_deployment",
        "cloud_deployment",
        "hybrid_deployment",
    ),
    "includes": (
        "model_serving",
        "api_gateway",
        "runtime_scaling",
        "version_routing",
        "canary_deployment",
    ),
    "present_required": True,
}

MONITORING_PLATFORM: dict[str, Any] = {
    "signals": (
        "model_accuracy",
        "data_drift",
        "concept_drift",
        "latency",
        "throughput",
        "resource_usage",
        "prediction_quality",
        "business_impact",
    ),
    "supports": (
        "automated_alerts",
        "root_cause_analysis",
        "retraining_trigger",
        "performance_dashboard",
    ),
    "present_required": True,
}

CONTINUOUS_TRAINING: dict[str, Any] = {
    "capabilities": (
        "automated_retraining",
        "feedback_collection",
        "new_data_integration",
        "model_improvement",
        "model_replacement",
        "approval_workflow",
    ),
    "present_required": True,
}

MLOPS_PIPELINES: tuple[str, ...] = (
    "data_pipeline",
    "feature_pipeline",
    "training_pipeline",
    "validation_pipeline",
    "deployment_pipeline",
    "monitoring_pipeline",
    "retraining_pipeline",
)

COMMANDS: tuple[str, ...] = (
    "CreateExperimentCommand",
    "StartTrainingCommand",
    "RegisterModelCommand",
    "ApproveModelCommand",
    "DeployModelCommand",
    "TriggerRetrainingCommand",
)

QUERIES: tuple[str, ...] = (
    "GetModelQuery",
    "GetExperimentQuery",
    "GetTrainingStatusQuery",
    "GetModelPerformanceQuery",
    "GetDeploymentStatusQuery",
)

CORE_EVENTS: tuple[dict[str, Any], ...] = (
    {
        "name": "ExperimentCreatedEvent",
        "owner": "BC-01",
        "consumers": ("training", "governance"),
        "schema": ("tenant_id", "experiment_id"),
        "version": "v1",
    },
    {
        "name": "TrainingStartedEvent",
        "owner": "BC-03",
        "consumers": ("monitoring", "observability"),
        "schema": ("tenant_id", "training_run_id", "model_id"),
        "version": "v1",
    },
    {
        "name": "TrainingCompletedEvent",
        "owner": "BC-03",
        "consumers": ("validation", "registry"),
        "schema": ("tenant_id", "training_run_id", "metrics"),
        "version": "v1",
    },
    {
        "name": "ModelRegisteredEvent",
        "owner": "BC-04",
        "consumers": ("governance", "deployment"),
        "schema": ("tenant_id", "model_id", "version"),
        "version": "v1",
    },
    {
        "name": "ModelApprovedEvent",
        "owner": "BC-07",
        "consumers": ("deployment", "audit"),
        "schema": ("tenant_id", "model_id", "approval_ref"),
        "version": "v1",
    },
    {
        "name": "ModelDeployedEvent",
        "owner": "BC-05",
        "consumers": ("monitoring", "security", "observability"),
        "schema": ("tenant_id", "model_id", "endpoint_id"),
        "version": "v1",
    },
    {
        "name": "ModelDriftDetectedEvent",
        "owner": "BC-06",
        "consumers": ("retraining", "governance"),
        "schema": ("tenant_id", "model_id", "drift_score"),
        "version": "v1",
    },
    {
        "name": "RetrainingStartedEvent",
        "owner": "BC-03",
        "consumers": ("monitoring", "governance"),
        "schema": ("tenant_id", "model_id", "policy_id"),
        "version": "v1",
    },
)

MICROSERVICES: tuple[dict[str, Any], ...] = (
    {
        "name": "experiment-service",
        "responsibility": "Experiment tracking and comparison.",
        "api_boundary": "/api/v1/ai/mlops/experiments",
        "database_boundary": "ai_ml_experiments",
        "events": ("ExperimentCreatedEvent",),
        "security": "ai.mlops.experiments.*",
        "scaling_strategy": "horizontal_stateless",
    },
    {
        "name": "feature-store-service",
        "responsibility": "Online/offline feature serving.",
        "api_boundary": "/api/v1/ai/mlops/features",
        "database_boundary": "ai_ml_features",
        "events": ("TrainingStartedEvent",),
        "security": "ai.mlops.features.*",
        "scaling_strategy": "horizontal_stateless",
    },
    {
        "name": "training-service",
        "responsibility": "Distributed and GPU training jobs.",
        "api_boundary": "/api/v1/ai/mlops/training",
        "database_boundary": "ai_ml_training",
        "events": ("TrainingStartedEvent", "TrainingCompletedEvent"),
        "security": "ai.mlops.training.*",
        "scaling_strategy": "gpu_backed_workers",
    },
    {
        "name": "model-registry-service",
        "responsibility": "Model versions and artifacts.",
        "api_boundary": "/api/v1/ai/mlops/registry",
        "database_boundary": "ai_ml_registry",
        "events": ("ModelRegisteredEvent",),
        "security": "ai.mlops.registry.*",
        "scaling_strategy": "horizontal_stateless",
    },
    {
        "name": "validation-service",
        "responsibility": "Quality, bias, and drift validation.",
        "api_boundary": "/api/v1/ai/mlops/validation",
        "database_boundary": "ai_ml_validation",
        "events": ("ModelValidatedEvent", "ModelApprovedEvent"),
        "security": "ai.mlops.validation.*",
        "scaling_strategy": "queue_backed_workers",
    },
    {
        "name": "deployment-service",
        "responsibility": "Model serving rollout and routing.",
        "api_boundary": "/api/v1/ai/mlops/deployment",
        "database_boundary": "ai_ml_deployment",
        "events": ("ModelDeployedEvent",),
        "security": "ai.mlops.deployment.*",
        "scaling_strategy": "horizontal_stateless",
    },
    {
        "name": "inference-service",
        "responsibility": "Online and batch inference execution.",
        "api_boundary": "/api/v1/ai/inference",
        "database_boundary": "ai_ml_inference",
        "events": ("ModelPerformanceChangedEvent",),
        "security": "ai.inference.*",
        "scaling_strategy": "autoscaling_gpu_pools",
    },
    {
        "name": "monitoring-service",
        "responsibility": "Drift and performance telemetry.",
        "api_boundary": "/api/v1/ai/mlops/monitoring",
        "database_boundary": "ai_ml_monitoring",
        "events": ("ModelDriftDetectedEvent",),
        "security": "ai.mlops.monitoring.*",
        "scaling_strategy": "horizontal_stateless",
    },
    {
        "name": "retraining-service",
        "responsibility": "Continuous learning orchestration.",
        "api_boundary": "/api/v1/ai/mlops/retraining",
        "database_boundary": "ai_ml_retraining",
        "events": ("RetrainingStartedEvent", "RetrainingTriggeredEvent"),
        "security": "ai.mlops.retraining.*",
        "scaling_strategy": "async_workers",
    },
    {
        "name": "governance-service",
        "responsibility": "ML approval and risk controls.",
        "api_boundary": "/api/v1/ai/mlops/governance",
        "database_boundary": "ai_ml_governance",
        "events": ("ModelApprovedEvent",),
        "security": "ai.mlops.governance.*",
        "scaling_strategy": "horizontal_stateless",
    },
)

SECURITY: dict[str, Any] = {
    "via_p207": True,
    "via_p208": True,
    "via_p209": True,
    "via_p210": True,
    "via_p211": True,
    "controls": (
        "model_access_control",
        "dataset_protection",
        "training_security",
        "artifact_security",
        "model_signing",
        "audit_logging",
        "ai_risk_controls",
    ),
    "zero_trust": True,
    "privacy_by_design": True,
}

DEPLOYMENT: dict[str, Any] = {
    "kubernetes": True,
    "gpu_clusters": True,
    "ml_runtime": True,
    "model_serving_infrastructure": True,
    "feature_store_cluster": True,
    "artifact_storage": True,
    "pipeline_orchestration": True,
    "monitoring_infrastructure": True,
    "auto_scaling": True,
    "cloud_native": True,
    "via_p213_o": True,
    "via_p214_a": True,
}

TESTING: tuple[str, ...] = (
    "ml_unit_testing",
    "data_validation_testing",
    "feature_testing",
    "model_testing",
    "pipeline_testing",
    "deployment_testing",
    "performance_testing",
    "security_testing",
    "drift_testing",
    "regression_testing",
)

CURSOR_OUTPUTS: tuple[str, ...] = (
    "enterprise_mlops_vision",
    "ddd_domain_model",
    "mlops_bounded_contexts",
    "ml_lifecycle_platform",
    "ml_experiment_platform",
    "feature_store_platform",
    "model_training_platform",
    "model_registry_platform",
    "model_validation_platform",
    "model_deployment_platform",
    "model_monitoring_platform",
    "continuous_training_platform",
    "mlops_pipeline_architecture",
    "cqrs_architecture",
    "event_sourcing_architecture",
    "microservice_architecture",
    "security_governance",
    "deployment_architecture",
    "testing_architecture",
    "production_readiness_checklist",
)

QUALITY_GATES_REJECT_IF: tuple[str, ...] = (
    "enterprise_mlops_platform_is_missing",
    "ml_lifecycle_management_is_missing",
    "experiment_platform_is_missing",
    "feature_store_is_missing",
    "training_platform_is_missing",
    "model_registry_is_missing",
    "validation_platform_is_missing",
    "deployment_platform_is_missing",
    "monitoring_platform_is_missing",
    "continuous_training_is_missing",
    "ml_governance_is_missing",
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
        "principle": PRINCIPLE,
        "fabric": FABRIC,
        "lifecycle_flow": list(LIFECYCLE_FLOW),
        "strategic_role": (
            "Industrialize ML with lifecycle governance, continuous "
            "improvement, and secure production operations."
        ),
        "why_mlops": (
            "operational_governance",
            "lifecycle_management",
            "continuous_improvement",
            "ml_differs_from_software_deploy",
            "industrialized_enterprise_ai",
        ),
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
        "contexts": list(LOGICAL_BOUNDED_CONTEXTS),
        "context_count": len(LOGICAL_BOUNDED_CONTEXTS),
        "logical_only": True,
        "sibling_bc_forbidden": True,
    }


def lifecycle() -> dict[str, Any]:
    return {
        "stages": [dict(s) for s in LIFECYCLE_STAGES],
        "stage_count": len(LIFECYCLE_STAGES),
        "present_required": True,
    }


def experiment_platform() -> dict[str, Any]:
    return dict(EXPERIMENT_PLATFORM)


def feature_store() -> dict[str, Any]:
    return dict(FEATURE_STORE)


def training_platform() -> dict[str, Any]:
    return dict(TRAINING_PLATFORM)


def model_registry() -> dict[str, Any]:
    return dict(MODEL_REGISTRY)


def validation_platform() -> dict[str, Any]:
    return dict(VALIDATION_PLATFORM)


def deployment_platform() -> dict[str, Any]:
    return dict(DEPLOYMENT_PLATFORM)


def monitoring_platform() -> dict[str, Any]:
    return dict(MONITORING_PLATFORM)


def continuous_training() -> dict[str, Any]:
    return dict(CONTINUOUS_TRAINING)


def pipelines() -> dict[str, Any]:
    return {
        "pipelines": list(MLOPS_PIPELINES),
        "pipeline_count": len(MLOPS_PIPELINES),
        "ci_cd_for_ml": True,
        "automation": True,
        "quality_gates": True,
        "security_gates": True,
        "present_required": True,
    }


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
    }


def microservices() -> dict[str, Any]:
    return {
        "services": [dict(s) for s in MICROSERVICES],
        "service_count": len(MICROSERVICES),
        "logical_decomposition": True,
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
            "enterprise_mlops_platform": True,
            "ml_lifecycle": True,
            "experiment_management": True,
            "feature_store": True,
            "training_platform": True,
            "model_registry": True,
            "model_validation": True,
            "model_deployment": True,
            "model_monitoring": True,
            "continuous_training": True,
            "ml_governance": True,
            "cqrs_architecture": True,
            "event_architecture": True,
            "microservice_architecture": True,
            "api_platform": True,
            "security_architecture": True,
            "deployment_architecture": True,
            "testing_architecture": True,
            "foundation_tests": True,
            "mlops_api_live": True,
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
            "ADR-421",
            "ADR-422",
            "ADR-423",
            "P212",
            "P213",
            "P213-J",
            "P213-O",
            "P207",
            "P208",
            "P209",
            "P210",
            "P211",
            "AI_PLATFORM_STANDARD",
        ],
        "vision": vision(),
        "domain_model": domain_model(),
        "bounded_contexts": bounded_contexts(),
        "lifecycle": lifecycle(),
        "experiment_platform": experiment_platform(),
        "feature_store": feature_store(),
        "training_platform": training_platform(),
        "model_registry": model_registry(),
        "validation_platform": validation_platform(),
        "deployment_platform": deployment_platform(),
        "monitoring_platform": monitoring_platform(),
        "continuous_training": continuous_training(),
        "pipelines": pipelines(),
        "cqrs": cqrs(),
        "events": events(),
        "microservices": microservices(),
        "security": security(),
        "deployment": deployment(),
        "testing": testing(),
        "cursor_outputs": cursor_outputs(),
        "quality_gates": quality_gates(),
        "production_readiness": production_readiness(),
        "enterprise_mlops_platform_present_required": True,
        "ml_lifecycle_management_present_required": True,
        "experiment_platform_present_required": True,
        "feature_store_present_required": True,
        "training_platform_present_required": True,
        "model_registry_present_required": True,
        "validation_platform_present_required": True,
        "deployment_platform_present_required": True,
        "monitoring_platform_present_required": True,
        "continuous_training_present_required": True,
        "ml_governance_present_required": True,
        "cqrs_architecture_present_required": True,
        "event_architecture_present_required": True,
        "microservices_architecture_present_required": True,
        "api_first_architecture_present_required": True,
        "zero_trust_security_present_required": True,
        "cloud_native_deployment_present_required": True,
        "sibling_ai_bc_forbidden": True,
        "module_local_llm_sdk_forbidden": True,
        "via_enterprise_ai": True,
        "via_api_gateway": True,
        "api_prefix": f"{API_PREFIX}/mlops",
        "forbidden_sibling_bc": [
            "ml_platform",
            "generative_ai",
            "llm_platform",
            "ai_core",
            "vector_intelligence",
            "model_lifecycle_platform",
        ],
    }


def mlops_surface() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "routes": [
            "GET /ai/mlops",
            "GET /ai/mlops/vision",
            "GET /ai/mlops/domain",
            "GET /ai/mlops/bounded-contexts",
            "GET /ai/mlops/lifecycle",
            "GET /ai/mlops/experiments",
            "GET /ai/mlops/features",
            "GET /ai/mlops/training",
            "GET /ai/mlops/registry",
            "GET /ai/mlops/validation",
            "GET /ai/mlops/deployment",
            "GET /ai/mlops/monitoring",
            "GET /ai/mlops/continuous-training",
            "GET /ai/mlops/pipelines",
            "GET /ai/mlops/cqrs",
            "GET /ai/mlops/events",
            "GET /ai/mlops/microservices",
            "GET /ai/mlops/security",
            "GET /ai/mlops/infrastructure",
            "GET /ai/mlops/testing",
            "GET /ai/mlops/outputs",
            "GET /ai/mlops/production-readiness",
            "GET /ai/mlops/readiness",
        ],
    }
