"""P213-O Enterprise Deployment, DevSecOps, Kubernetes, Scalability & Observability — immutable catalog."""
from __future__ import annotations

from typing import Any

PROMPT_ID = "P213-O"
ADR = 419
SOR = "analytics"
API_PREFIX = "/api/v1/analytics"
PRODUCT = "Enterprise BI Deployment, DevSecOps & Observability Platform"
CAPABILITY = "CAP-PLT-BI-001"

PRINCIPLE = (
    "Every analytics capability SHALL be continuously deployed through "
    "secure GitOps, remain cloud-native and observable, and satisfy "
    "enterprise Definition of Done before production promotion."
)

FABRIC = "meos_enterprise_bi_operations_fabric"

CORE_DOMAIN = "enterprise_analytics_operational_excellence"

SUPPORTING_DOMAINS: tuple[dict[str, str], ...] = (
    {"id": "kubernetes_runtime", "purpose": "Enterprise Kubernetes runtime for BI services."},
    {"id": "gitops_delivery", "purpose": "Declarative GitOps promotion and reconciliation."},
    {"id": "cicd_pipelines", "purpose": "Build, release, and rollback pipelines."},
    {"id": "devsecops", "purpose": "Secure SDLC, scanning, and supply-chain gates."},
    {"id": "observability", "purpose": "Metrics, logs, traces, and business telemetry."},
    {"id": "site_reliability", "purpose": "SLIs, SLOs, error budgets, and incident ops."},
    {"id": "scalability", "purpose": "Elastic, geo, and workload-specific scaling."},
    {"id": "platform_engineering", "purpose": "Golden paths, templates, and developer portal."},
    {"id": "aiops", "purpose": "AI-assisted ops agents via Enterprise AI."},
)

LOGICAL_BOUNDED_CONTEXTS: tuple[dict[str, Any], ...] = (
    {
        "id": "deployment_platform",
        "bc": "BC-01",
        "name": "Deployment Platform Context",
        "purpose": "Environment topology, promotion, production deployment.",
    },
    {
        "id": "kubernetes_platform",
        "bc": "BC-02",
        "name": "Kubernetes Platform Context",
        "purpose": "Cluster runtime, workloads, autoscaling, security policies.",
    },
    {
        "id": "gitops_cicd",
        "bc": "BC-03",
        "name": "GitOps & CI/CD Context",
        "purpose": "Git as source of truth, pipelines, progressive delivery.",
    },
    {
        "id": "devsecops",
        "bc": "BC-04",
        "name": "DevSecOps Context",
        "purpose": "SAST/DAST/SCA, image signing, supply-chain security.",
    },
    {
        "id": "observability_sre",
        "bc": "BC-05",
        "name": "Observability & SRE Context",
        "purpose": "OTel, SLOs, incidents, reliability reviews.",
    },
    {
        "id": "scalability_dr",
        "bc": "BC-06",
        "name": "Scalability & DR Context",
        "purpose": "Elastic scale, HA, multi-region, disaster recovery.",
    },
)

AGGREGATE = {
    "name": "BiOperationsPlatformAggregate",
    "root": "BiOperationsPlatform",
    "entities": (
        "Environment",
        "DeploymentRelease",
        "KubernetesCluster",
        "GitOpsApplication",
        "PipelineRun",
        "SecurityGate",
        "ServiceLevelObjective",
        "Incident",
        "Runbook",
        "ObservabilityDashboard",
    ),
    "value_objects": (
        "EnvironmentId",
        "ReleaseVersion",
        "ClusterName",
        "ImageDigest",
        "SbomRef",
        "ErrorBudget",
        "PromotionRule",
        "RollbackPlan",
    ),
    "events": (
        "BiDeploymentCompletedEvent",
        "BiScalingExecutedEvent",
        "BiIncidentDetectedEvent",
        "BiRecoveryCompletedEvent",
        "BiSecurityGatePassedEvent",
        "BiGitOpsReconciledEvent",
    ),
}

ENVIRONMENTS: tuple[dict[str, Any], ...] = (
    {"id": "development", "purpose": "Feature development", "isolation": "namespace"},
    {"id": "local_development", "purpose": "Developer workstation", "isolation": "local"},
    {"id": "integration", "purpose": "Service integration", "isolation": "namespace"},
    {"id": "continuous_integration", "purpose": "Automated CI validation", "isolation": "ephemeral"},
    {"id": "quality_assurance", "purpose": "Functional QA", "isolation": "cluster"},
    {"id": "performance_testing", "purpose": "Load and stress", "isolation": "cluster"},
    {"id": "security_testing", "purpose": "Security verification", "isolation": "cluster"},
    {"id": "user_acceptance_testing", "purpose": "Business UAT", "isolation": "cluster"},
    {"id": "pre_production", "purpose": "Prod-like validation", "isolation": "cluster"},
    {"id": "production", "purpose": "Live workloads", "isolation": "multi_zone"},
    {"id": "disaster_recovery", "purpose": "DR failover", "isolation": "multi_region"},
)

KUBERNETES: dict[str, Any] = {
    "control_plane": True,
    "worker_nodes": True,
    "gpu_nodes": True,
    "autoscaling_node_pools": True,
    "namespaces": True,
    "network_policies": True,
    "pod_security_standards": True,
    "admission_controllers": True,
    "workload_kinds": (
        "StatefulSets",
        "Deployments",
        "DaemonSets",
        "Jobs",
        "CronJobs",
    ),
    "autoscalers": (
        "horizontal_pod_autoscaler",
        "vertical_pod_autoscaler",
        "cluster_autoscaler",
    ),
}

GITOPS: dict[str, Any] = {
    "git_as_source_of_truth": True,
    "declarative_infrastructure": True,
    "tools": ("argo_cd", "flux_cd"),
    "progressive_delivery": True,
    "drift_detection": True,
    "automatic_reconciliation": True,
    "rollback": True,
    "multi_cluster": True,
    "repository_strategy": "environment_overlays",
    "branch_strategy": "trunk_with_release_tags",
    "promotion_workflow": True,
    "approval_workflow": True,
    "release_governance": True,
}

CICD_PIPELINE: tuple[str, ...] = (
    "source_control",
    "static_code_analysis",
    "dependency_validation",
    "secret_detection",
    "container_build",
    "sbom_generation",
    "unit_tests",
    "integration_tests",
    "contract_tests",
    "security_tests",
    "image_signing",
    "container_registry",
    "gitops_deployment",
    "verification",
    "production_promotion",
)

DEVSECOPS: dict[str, Any] = {
    "secure_sdlc": True,
    "sast": True,
    "dast": True,
    "sca": True,
    "iac_security": True,
    "container_scanning": True,
    "kubernetes_security": True,
    "runtime_protection": True,
    "image_signing": True,
    "supply_chain_security": True,
    "vulnerability_management": True,
    "security_gates": True,
    "via_p209": True,
    "via_p210": True,
}

OBSERVABILITY: dict[str, Any] = {
    "signals": (
        "metrics",
        "logs",
        "distributed_traces",
        "events",
        "business_kpis",
        "ai_telemetry",
        "graph_metrics",
        "forecast_metrics",
        "decision_metrics",
    ),
    "stack": (
        "opentelemetry",
        "prometheus",
        "grafana",
        "loki",
        "tempo",
        "alert_manager",
    ),
    "dashboards": ("service_dashboards", "executive_dashboards"),
    "via_enterprise_observability": True,
}

SRE: dict[str, Any] = {
    "slis": True,
    "slos": True,
    "slas": True,
    "error_budgets": True,
    "incident_management": True,
    "problem_management": True,
    "capacity_planning": True,
    "reliability_reviews": True,
    "operational_readiness_reviews": True,
    "chaos_engineering": True,
}

SCALABILITY: tuple[str, ...] = (
    "horizontal_scaling",
    "vertical_scaling",
    "elastic_scaling",
    "geo_scaling",
    "read_scaling",
    "write_scaling",
    "streaming_scaling",
    "ai_workload_scaling",
    "knowledge_graph_scaling",
    "digital_twin_scaling",
    "decision_engine_scaling",
    "forecast_engine_scaling",
)

HA_DR: dict[str, Any] = {
    "multi_zone": True,
    "multi_region": True,
    "active_active": True,
    "active_passive": True,
    "backup_strategy": True,
    "point_in_time_recovery": True,
    "automated_failover": True,
    "cross_region_replication": True,
    "disaster_recovery_automation": True,
    "business_continuity": True,
}

PLATFORM_ENGINEERING: tuple[str, ...] = (
    "developer_portal",
    "service_catalog",
    "golden_paths",
    "platform_templates",
    "infrastructure_templates",
    "deployment_templates",
    "api_templates",
    "monitoring_templates",
    "security_templates",
    "runbooks",
    "operational_playbooks",
)

SERVICE_MESH: dict[str, Any] = {
    "implementations": ("istio", "linkerd"),
    "mtls": True,
    "traffic_splitting": True,
    "canary_routing": True,
    "blue_green_routing": True,
    "circuit_breaking": True,
    "retries": True,
    "timeouts": True,
    "fault_injection": True,
    "policy_enforcement": True,
}

SECRETS: dict[str, Any] = {
    "via_p209": True,
    "external_secrets": True,
    "vault_integration": True,
    "kms_integration": True,
    "encrypted_configuration": True,
    "dynamic_secrets": True,
    "secret_rotation": True,
    "certificate_rotation": True,
}

COST_OPTIMIZATION: tuple[str, ...] = (
    "resource_quotas",
    "namespace_quotas",
    "cost_allocation",
    "chargeback",
    "showback",
    "idle_resource_detection",
    "autoscaling_optimization",
    "gpu_optimisation",
    "storage_optimisation",
    "forecast_based_capacity_planning",
)

AIOPS_AGENTS: tuple[str, ...] = (
    "deployment_agent",
    "release_agent",
    "incident_agent",
    "observability_agent",
    "capacity_agent",
    "performance_agent",
    "reliability_agent",
    "cost_optimisation_agent",
    "security_operations_agent",
)

AIOPS_CAPABILITIES: tuple[str, ...] = (
    "predictive_scaling",
    "intelligent_alert_correlation",
    "root_cause_analysis",
    "self_healing",
    "auto_remediation",
    "operational_recommendations",
)

DEPLOYMENT_QUALITY_GATES: tuple[str, ...] = (
    "build_successful",
    "security_gates_passed",
    "sbom_generated",
    "container_signed",
    "vulnerabilities_within_policy",
    "unit_tests_passed",
    "integration_tests_passed",
    "contract_tests_passed",
    "performance_targets_met",
    "observability_enabled",
    "runbooks_published",
    "slo_compliance_verified",
    "rollback_verified",
    "documentation_updated",
)

DEFINITION_OF_DONE: tuple[str, ...] = (
    "all_bi_services_production_deployed",
    "all_analytics_services_cloud_native",
    "cqrs_architecture_operational",
    "event_streaming_operational",
    "knowledge_graph_operational",
    "ai_decision_intelligence_operational",
    "predictive_analytics_operational",
    "prescriptive_analytics_operational",
    "enterprise_reporting_operational",
    "self_service_bi_operational",
    "semantic_layer_operational",
    "api_platform_operational",
    "kubernetes_deployment_operational",
    "gitops_pipeline_operational",
    "devsecops_pipeline_operational",
    "observability_platform_operational",
    "sre_processes_operational",
    "disaster_recovery_validated",
    "scalability_objectives_validated",
    "security_controls_verified",
    "compliance_controls_verified",
    "operational_documentation_complete",
    "platform_governance_complete",
)

COMMANDS: tuple[str, ...] = (
    "CreateDeploymentReleaseCommand",
    "PromoteEnvironmentCommand",
    "ReconcileGitOpsCommand",
    "ExecuteRollbackCommand",
    "RegisterSloCommand",
    "DeclareIncidentCommand",
)

QUERIES: tuple[str, ...] = (
    "GetDeploymentStatusQuery",
    "GetEnvironmentTopologyQuery",
    "GetSloComplianceQuery",
    "GetObservabilityHealthQuery",
    "GetSecurityGateStatusQuery",
    "GetDefinitionOfDoneQuery",
)

CORE_EVENTS: tuple[dict[str, Any], ...] = (
    {
        "name": "BiDeploymentCompletedEvent",
        "producer": "deployment_platform",
        "consumers": ("observability_sre", "audit"),
        "payload": ("tenant_id", "release_id", "environment"),
        "version": "v1",
    },
    {
        "name": "BiScalingExecutedEvent",
        "producer": "scalability_dr",
        "consumers": ("observability_sre", "cost"),
        "payload": ("tenant_id", "service_ref", "scale_delta"),
        "version": "v1",
    },
    {
        "name": "BiIncidentDetectedEvent",
        "producer": "observability_sre",
        "consumers": ("aiops", "notifications"),
        "payload": ("tenant_id", "incident_id", "severity"),
        "version": "v1",
    },
    {
        "name": "BiRecoveryCompletedEvent",
        "producer": "scalability_dr",
        "consumers": ("observability_sre", "audit"),
        "payload": ("tenant_id", "incident_id", "recovery_ref"),
        "version": "v1",
    },
    {
        "name": "BiSecurityGatePassedEvent",
        "producer": "devsecops",
        "consumers": ("gitops_cicd", "audit"),
        "payload": ("tenant_id", "pipeline_run_id", "gate_id"),
        "version": "v1",
    },
    {
        "name": "BiGitOpsReconciledEvent",
        "producer": "gitops_cicd",
        "consumers": ("deployment_platform", "observability_sre"),
        "payload": ("tenant_id", "application_ref", "revision"),
        "version": "v1",
    },
)

MICROSERVICES: tuple[dict[str, Any], ...] = (
    {
        "name": "bi-deployment-service",
        "responsibility": "Release and environment promotion orchestration.",
        "database_boundary": "analytics_ops_deploy",
        "api_boundary": "/api/v1/analytics/deploy",
        "events": ("BiDeploymentCompletedEvent",),
        "security_model": "analytics.deploy.*",
        "scaling_strategy": "horizontal_stateless",
    },
    {
        "name": "bi-gitops-service",
        "responsibility": "GitOps application reconciliation bindings.",
        "database_boundary": "analytics_ops_gitops",
        "api_boundary": "/api/v1/analytics/deploy/gitops",
        "events": ("BiGitOpsReconciledEvent",),
        "security_model": "analytics.gitops.*",
        "scaling_strategy": "horizontal_stateless",
    },
    {
        "name": "bi-devsecops-service",
        "responsibility": "Security gate evaluation and SBOM attestation.",
        "database_boundary": "analytics_ops_sec",
        "api_boundary": "/api/v1/analytics/deploy/devsecops",
        "events": ("BiSecurityGatePassedEvent",),
        "security_model": "analytics.devsecops.*",
        "scaling_strategy": "queue_backed_workers",
    },
    {
        "name": "bi-observability-service",
        "responsibility": "Telemetry bindings and health surfaces.",
        "database_boundary": "analytics_ops_otel",
        "api_boundary": "/api/v1/analytics/deploy/observability",
        "events": ("BiIncidentDetectedEvent",),
        "security_model": "analytics.observability.*",
        "scaling_strategy": "horizontal_stateless",
    },
    {
        "name": "bi-sre-service",
        "responsibility": "SLO, error budget, and incident lifecycle.",
        "database_boundary": "analytics_ops_sre",
        "api_boundary": "/api/v1/analytics/deploy/sre",
        "events": ("BiIncidentDetectedEvent", "BiRecoveryCompletedEvent"),
        "security_model": "analytics.sre.*",
        "scaling_strategy": "horizontal_stateless",
    },
    {
        "name": "bi-scalability-service",
        "responsibility": "Autoscaling policies and capacity planning.",
        "database_boundary": "analytics_ops_scale",
        "api_boundary": "/api/v1/analytics/deploy/scalability",
        "events": ("BiScalingExecutedEvent",),
        "security_model": "analytics.scalability.*",
        "scaling_strategy": "async_workers",
    },
    {
        "name": "bi-dr-service",
        "responsibility": "HA/DR orchestration and failover drills.",
        "database_boundary": "analytics_ops_dr",
        "api_boundary": "/api/v1/analytics/deploy/disaster-recovery",
        "events": ("BiRecoveryCompletedEvent",),
        "security_model": "analytics.dr.*",
        "scaling_strategy": "horizontal_stateless",
    },
    {
        "name": "bi-aiops-service",
        "responsibility": "AIOps agents via Enterprise AI only.",
        "database_boundary": "analytics_ops_aiops",
        "api_boundary": "/api/v1/analytics/deploy/aiops",
        "events": ("BiIncidentDetectedEvent",),
        "security_model": "analytics.aiops.*",
        "scaling_strategy": "async_via_enterprise_ai",
    },
)

SECURITY: dict[str, Any] = {
    "via_p207": True,
    "via_p208": True,
    "via_p209": True,
    "via_p210": True,
    "via_p211": True,
    "via_p212": True,
    "zero_trust": True,
    "mtls": True,
    "pod_security_standards": True,
    "network_policies": True,
    "image_signing_required": True,
    "sbom_required": True,
    "audit_logging": True,
}

DEPLOYMENT: dict[str, Any] = {
    "kubernetes": True,
    "service_mesh": True,
    "ingress_controller": True,
    "api_gateway": True,
    "kafka_cluster": True,
    "redis_cluster": True,
    "object_storage": True,
    "container_registry": True,
    "gitops": True,
    "autoscaling": True,
    "multi_region": True,
    "blue_green": True,
    "canary_releases": True,
    "cloud_native": True,
}

TESTING: tuple[str, ...] = (
    "deployment_validation",
    "smoke_testing",
    "regression_testing",
    "performance_testing",
    "load_testing",
    "stress_testing",
    "chaos_testing",
    "failover_testing",
    "recovery_testing",
    "security_testing",
    "compliance_testing",
    "operational_acceptance_testing",
)

CURSOR_OUTPUTS: tuple[str, ...] = (
    "enterprise_deployment_vision",
    "production_environments",
    "kubernetes_platform",
    "gitops_platform",
    "cicd_pipeline",
    "devsecops_platform",
    "observability_platform",
    "site_reliability_engineering",
    "scalability_architecture",
    "high_availability_disaster_recovery",
    "platform_engineering",
    "service_mesh",
    "configuration_secrets_management",
    "cost_optimization",
    "ai_operations",
    "testing_validation",
    "quality_gates",
    "definition_of_done",
    "cqrs_event_architecture",
    "production_readiness_checklist",
)

QUALITY_GATES_REJECT_IF: tuple[str, ...] = (
    "enterprise_production_deployment_is_missing",
    "kubernetes_runtime_is_missing",
    "gitops_platform_is_missing",
    "devsecops_pipeline_is_missing",
    "observability_platform_is_missing",
    "sre_processes_are_missing",
    "scalability_architecture_is_missing",
    "disaster_recovery_is_missing",
    "definition_of_done_is_incomplete",
    "cloud_native_deployment_is_missing",
    "zero_trust_security_is_missing",
    "continuous_governance_is_missing",
    "bi_deploy_architecture_is_incomplete",
    "sibling_business_intelligence_bc",
)


def vision() -> dict[str, Any]:
    return {
        "statement": PRINCIPLE,
        "fabric": FABRIC,
        "operating_model": (
            "cloud_first_deployment",
            "immutable_infrastructure",
            "gitops_delivery",
            "infrastructure_as_code",
            "secure_software_supply_chain",
            "enterprise_operational_governance",
            "continuous_deployment_maturity",
        ),
        "operationalizes": (
            "P213-A",
            "P213-B",
            "P213-C",
            "P213-D",
            "P213-E",
            "P213-F",
            "P213-G",
            "P213-H",
            "P213-I",
            "P213-J",
            "P213-K",
            "P213-L",
            "P213-M",
            "P213-N",
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


def environments() -> dict[str, Any]:
    return {
        "environments": [dict(e) for e in ENVIRONMENTS],
        "environment_count": len(ENVIRONMENTS),
        "promotion_required": True,
    }


def kubernetes() -> dict[str, Any]:
    return dict(KUBERNETES)


def gitops() -> dict[str, Any]:
    return dict(GITOPS)


def cicd() -> dict[str, Any]:
    return {
        "pipeline_steps": list(CICD_PIPELINE),
        "step_count": len(CICD_PIPELINE),
        "pipeline_types": ("build", "release", "rollback"),
    }


def devsecops() -> dict[str, Any]:
    return dict(DEVSECOPS)


def observability() -> dict[str, Any]:
    return dict(OBSERVABILITY)


def sre() -> dict[str, Any]:
    return dict(SRE)


def scalability() -> dict[str, Any]:
    return {
        "modes": list(SCALABILITY),
        "mode_count": len(SCALABILITY),
    }


def ha_dr() -> dict[str, Any]:
    return dict(HA_DR)


def platform_engineering() -> dict[str, Any]:
    return {
        "capabilities": list(PLATFORM_ENGINEERING),
        "capability_count": len(PLATFORM_ENGINEERING),
    }


def service_mesh() -> dict[str, Any]:
    return dict(SERVICE_MESH)


def secrets() -> dict[str, Any]:
    return dict(SECRETS)


def cost_optimization() -> dict[str, Any]:
    return {
        "capabilities": list(COST_OPTIMIZATION),
        "capability_count": len(COST_OPTIMIZATION),
    }


def aiops() -> dict[str, Any]:
    return {
        "agents": list(AIOPS_AGENTS),
        "agent_count": len(AIOPS_AGENTS),
        "capabilities": list(AIOPS_CAPABILITIES),
        "via_enterprise_ai": True,
        "module_local_llm_sdk_forbidden": True,
    }


def deployment_quality_gates() -> dict[str, Any]:
    return {
        "gates": list(DEPLOYMENT_QUALITY_GATES),
        "gate_count": len(DEPLOYMENT_QUALITY_GATES),
    }


def definition_of_done() -> dict[str, Any]:
    return {
        "criteria": list(DEFINITION_OF_DONE),
        "criterion_count": len(DEFINITION_OF_DONE),
        "series_complete_required": True,
    }


def cqrs() -> dict[str, Any]:
    return {
        "commands": list(COMMANDS),
        "command_count": len(COMMANDS),
        "queries": list(QUERIES),
        "query_count": len(QUERIES),
        "alignment_present_required": True,
        "events": [e["name"] for e in CORE_EVENTS],
        "event_count": len(CORE_EVENTS),
    }


def events() -> dict[str, Any]:
    return {
        "core_events": [dict(e) for e in CORE_EVENTS],
        "core_event_count": len(CORE_EVENTS),
        "event_driven_required": True,
        "replay_strategy": "outbox_replay_by_event_id",
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
        "deployment_gates": list(DEPLOYMENT_QUALITY_GATES),
    }


def production_readiness() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "checklist": {
            "enterprise_production_deployment": True,
            "enterprise_platform_engineering": True,
            "enterprise_kubernetes_runtime": True,
            "enterprise_gitops_platform": True,
            "enterprise_cicd": True,
            "enterprise_sre": True,
            "enterprise_observability": True,
            "enterprise_reliability_engineering": True,
            "enterprise_scalability_platform": True,
            "enterprise_operational_governance": True,
            "definition_of_done": True,
            "foundation_tests": True,
            "deploy_api_live": True,
            "series_p213_a_through_n_operationalized": True,
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
            "P213-A",
            "P213-B",
            "P213-C",
            "P213-D",
            "P213-E",
            "P213-F",
            "P213-G",
            "P213-H",
            "P213-I",
            "P213-J",
            "P213-K",
            "P213-L",
            "P213-M",
            "P213-N",
            "ADR-394",
            "ADR-418",
            "P207",
            "P208",
            "P209",
            "P210",
            "P211",
            "P212",
        ],
        "architecture": {
            "present_required": True,
            "not_incomplete": True,
            "capabilities": [
                "enterprise_production_deployment",
                "enterprise_platform_engineering",
                "enterprise_kubernetes_runtime",
                "enterprise_gitops_platform",
                "enterprise_cicd",
                "enterprise_sre",
                "enterprise_observability",
                "enterprise_reliability_engineering",
                "enterprise_scalability_platform",
                "enterprise_operational_governance",
            ],
            "capability_count": 10,
        },
        "domain_model": domain_model(),
        "bounded_contexts": bounded_contexts(),
        "environments": environments(),
        "kubernetes": kubernetes(),
        "gitops": gitops(),
        "cicd": cicd(),
        "devsecops": devsecops(),
        "observability": observability(),
        "sre": sre(),
        "scalability": scalability(),
        "ha_dr": ha_dr(),
        "platform_engineering": platform_engineering(),
        "service_mesh": service_mesh(),
        "secrets": secrets(),
        "cost_optimization": cost_optimization(),
        "aiops": aiops(),
        "deployment_quality_gates": deployment_quality_gates(),
        "definition_of_done": definition_of_done(),
        "cqrs": cqrs(),
        "events": events(),
        "microservices": microservices(),
        "security": security(),
        "deployment": deployment(),
        "testing": testing(),
        "cursor_outputs": cursor_outputs(),
        "quality_gates": quality_gates(),
        "production_readiness": production_readiness(),
        "enterprise_production_deployment_present_required": True,
        "kubernetes_runtime_present_required": True,
        "gitops_platform_present_required": True,
        "devsecops_pipeline_present_required": True,
        "observability_platform_present_required": True,
        "sre_processes_present_required": True,
        "scalability_architecture_present_required": True,
        "disaster_recovery_present_required": True,
        "definition_of_done_present_required": True,
        "cloud_native_deployment_present_required": True,
        "zero_trust_security_present_required": True,
        "continuous_governance_present_required": True,
        "architecture_present_required": True,
        "sibling_business_intelligence_bc_forbidden": True,
        "api_prefix": f"{API_PREFIX}/deploy",
        "forbidden_sibling_bc": [
            "business_intelligence",
            "decision_intelligence",
            "reporting_platform",
            "metric_governance_platform",
            "visualization_platform",
            "bi_core",
        ],
    }


def deploy_surface() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "routes": [
            "GET /analytics/deploy",
            "GET /analytics/deploy/vision",
            "GET /analytics/deploy/domain",
            "GET /analytics/deploy/bounded-contexts",
            "GET /analytics/deploy/environments",
            "GET /analytics/deploy/kubernetes",
            "GET /analytics/deploy/gitops",
            "GET /analytics/deploy/cicd",
            "GET /analytics/deploy/devsecops",
            "GET /analytics/deploy/observability",
            "GET /analytics/deploy/sre",
            "GET /analytics/deploy/scalability",
            "GET /analytics/deploy/disaster-recovery",
            "GET /analytics/deploy/platform-engineering",
            "GET /analytics/deploy/aiops",
            "GET /analytics/deploy/definition-of-done",
            "GET /analytics/deploy/quality-gates",
            "GET /analytics/deploy/security",
            "GET /analytics/deploy/testing",
            "GET /analytics/deploy/outputs",
            "GET /analytics/deploy/production-readiness",
            "GET /analytics/deploy/readiness",
        ],
    }
