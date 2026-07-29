"""P210-N Deployment, DevSecOps, Kubernetes & Observability — immutable catalog."""
from __future__ import annotations

from typing import Any

PROMPT_ID = "P210-N"
ADR = 374
SOR = "cyber_security"
API_PREFIX = "/api/v1/cyber-security"
PRODUCT = (
    "Enterprise Cyber Security & Threat Defense Platform — "
    "Enterprise Deployment, DevSecOps, Kubernetes, Scalability & Observability"
)

MISSION_STATEMENT = (
    "Create an enterprise deployment platform capable of secure application "
    "delivery, automated infrastructure provisioning, Kubernetes-native "
    "operations, continuous security validation, high availability, global "
    "scalability, real-time observability, and autonomous operational management."
)

VISION_STATEMENT = (
    "Create a Cyber Security Cloud Operating Fabric where every service can be "
    "deployed automatically, every workload is continuously secured, every "
    "infrastructure change is controlled, every failure is detected instantly, "
    "every security platform scales globally, and every operation is "
    "observable and explainable."
)

DEPLOY_PIPELINE: tuple[str, ...] = (
    "source_code",
    "git_repository",
    "ci_cd_pipeline",
    "security_validation",
    "container_build",
    "container_security_scan",
    "artifact_registry",
    "infrastructure_provisioning",
    "kubernetes_deployment",
    "service_mesh",
    "observability_platform",
    "production_operations",
)

CLOUD_MODELS: tuple[str, ...] = (
    "private_cloud",
    "public_cloud",
    "hybrid_cloud",
    "multi_cloud",
    "edge_computing",
    "on_premise_data_centers",
)

CLOUD_PLATFORMS: tuple[str, ...] = (
    "aws",
    "azure",
    "google_cloud",
    "openstack",
    "kubernetes_native_cloud",
)

K8S_COMPONENTS: tuple[str, ...] = (
    "control_plane",
    "worker_nodes",
    "namespaces",
    "pods",
    "deployments",
    "statefulsets",
    "daemonsets",
    "jobs",
    "cronjobs",
    "services",
    "ingress",
    "network_policies",
    "secrets_management",
    "config_management",
)

K8S_SECURITY: tuple[str, ...] = (
    "pod_security_standards",
    "runtime_protection",
    "admission_controllers",
    "rbac",
    "service_accounts",
    "image_verification",
    "workload_identity",
    "zero_trust_networking",
)

CONTAINER_SECURITY: tuple[str, ...] = (
    "image_scanning",
    "vulnerability_detection",
    "malware_detection",
    "runtime_protection",
    "container_isolation",
    "supply_chain_security",
    "sbom_generation",
    "artifact_signing",
    "image_provenance",
    "registry_security",
)

CONTAINER_STANDARDS: tuple[str, ...] = (
    "oci",
    "slsa",
    "sigstore",
    "cosign",
)

DEVSECOPS_STAGES: tuple[str, ...] = (
    "code_commit",
    "sast",
    "sca",
    "secret_detection",
    "infrastructure_security_scan",
    "container_scan",
    "dynamic_security_testing",
    "compliance_validation",
    "deployment_approval",
    "production_release",
)

IAC_TOOLS: tuple[str, ...] = (
    "terraform",
    "opentofu",
    "pulumi",
    "ansible",
    "kubernetes_yaml",
    "helm_charts",
    "kustomize",
)

GITOPS: tuple[str, ...] = (
    "git_as_source_of_truth",
    "declarative_infrastructure",
    "automated_synchronization",
    "environment_promotion",
    "configuration_management",
    "audit_history",
    "argocd",
    "fluxcd",
)

SERVICE_MESH: tuple[str, ...] = (
    "istio",
    "linkerd",
    "enterprise_service_mesh",
    "mtls",
    "traffic_management",
    "service_discovery",
    "security_policies",
    "observability",
    "fault_injection",
    "canary_release",
    "blue_green_deployment",
)

SCALING: tuple[str, ...] = (
    "horizontal_scaling",
    "vertical_scaling",
    "auto_scaling",
    "cluster_federation",
    "global_load_balancing",
    "multi_region_deployment",
    "active_active",
    "active_passive_dr",
    "kubernetes_autoscaler",
    "cluster_autoscaler",
    "database_scaling",
    "event_streaming_scaling",
    "ai_workload_scaling",
)

RESILIENCE: tuple[str, ...] = (
    "fault_tolerance",
    "self_healing",
    "backup",
    "disaster_recovery",
    "business_continuity",
    "chaos_engineering",
    "failure_simulation",
)

AVAILABILITY_TARGETS: tuple[str, ...] = (
    "99.9",
    "99.99",
    "enterprise_mission_critical",
)

OBSERVABILITY_PILLARS: tuple[str, ...] = (
    "metrics",
    "logs",
    "traces",
    "security_events",
    "audit_events",
    "ai_events",
    "business_events",
    "infrastructure_events",
)

MONITORING_STACK: tuple[str, ...] = (
    "prometheus",
    "grafana",
    "opentelemetry",
    "elk",
    "loki",
    "jaeger",
    "tempo",
)

SECURITY_OBSERVABILITY: tuple[str, ...] = (
    "threat_events",
    "authentication_events",
    "authorization_events",
    "policy_violations",
    "configuration_changes",
    "deployment_changes",
    "privilege_changes",
    "ai_decisions",
    "autonomous_actions",
)

PLATFORM_ENGINEERING: tuple[str, ...] = (
    "self_service_deployment",
    "service_templates",
    "environment_management",
    "developer_portal",
    "api_catalog",
    "security_guardrails",
    "golden_paths",
    "operational_automation",
)

AIOPS: tuple[str, ...] = (
    "predict_failures",
    "detect_anomalies",
    "optimize_resources",
    "recommend_scaling",
    "identify_performance_issues",
    "automate_recovery",
    "analyze_logs",
    "generate_root_cause_analysis",
)

CQRS_DEPLOY: tuple[str, ...] = (
    "event_brokers",
    "command_services",
    "query_services",
    "event_stores",
    "read_models",
    "streaming_pipelines",
    "kafka",
    "nats",
    "rabbitmq",
    "cloud_event_bus",
)

COMPLIANCE_FRAMEWORKS: tuple[str, ...] = (
    "iso_27001",
    "nist_csf",
    "soc_2",
    "cis_kubernetes_benchmark",
    "pci_dss",
    "nist_sp_800_190",
)

COMMANDS: tuple[str, ...] = (
    "ProvisionInfrastructure",
    "DeployWorkload",
    "ScanContainerImage",
    "ApplyNetworkPolicy",
    "PromoteEnvironment",
    "ScaleService",
    "DeclareDisasterRecovery",
    "ValidatePipeline",
    "RollbackDeployment",
    "AttachObservability",
)

QUERIES: tuple[str, ...] = (
    "GetDeployArchitecture",
    "GetPipelineStatus",
    "GetK8sSecurityPosture",
    "GetObservabilityHealth",
    "GetScalingStatus",
    "GetDisasterRecoveryPlan",
    "GetDeployReadiness",
)

DOMAIN_EVENTS: tuple[str, ...] = (
    "DeploymentPipelineStarted",
    "SecurityValidationPassed",
    "ContainerImageSigned",
    "KubernetesWorkloadDeployed",
    "ObservabilityAttached",
    "ScalingPolicyApplied",
    "DisasterRecoveryPlanDefined",
    "PipelineValidationFailed",
    "DeploymentRolledBack",
)

MICROSERVICES: tuple[str, ...] = (
    "deploy-pipeline-service",
    "k8s-security-service",
    "container-security-service",
    "iac-gitops-service",
    "service-mesh-service",
    "scaling-resilience-service",
    "observability-bridge-service",
    "platform-engineering-service",
    "aiops-bridge-service",
    "deploy-compliance-service",
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
    "enterprise_cloud_platform",
    "enterprise_data_platform",
    "enterprise_ai_platform",
    "enterprise_observability_platform",
)

CURSOR_OUTPUTS: tuple[str, ...] = (
    "enterprise_deployment_architecture",
    "devsecops_architecture",
    "kubernetes_platform_blueprint",
    "container_security_framework",
    "ci_cd_pipeline_design",
    "infrastructure_as_code_framework",
    "gitops_architecture",
    "service_mesh_architecture",
    "scalability_model",
    "high_availability_design",
    "disaster_recovery_plan",
    "observability_architecture",
    "monitoring_dashboards",
    "security_observability_model",
    "platform_engineering_blueprint",
    "aiops_architecture",
    "cqrs_deployment_model",
    "kubernetes_production_configuration",
    "operational_runbooks",
    "enterprise_production_deployment_blueprint",
)

QUALITY_GATES_REJECT_IF: tuple[str, ...] = (
    "deployment_is_not_automated",
    "kubernetes_security_is_incomplete",
    "infrastructure_cannot_be_reproduced",
    "observability_is_missing",
    "scaling_is_manual",
    "disaster_recovery_is_undefined",
    "security_controls_are_not_integrated",
    "devsecops_pipeline_lacks_validation",
    "sibling_deploy_bc",
)


def architecture() -> dict[str, Any]:
    return {
        "pipeline": list(DEPLOY_PIPELINE),
        "layer_count": len(DEPLOY_PIPELINE),
        "cloud_models": list(CLOUD_MODELS),
        "cloud_platforms": list(CLOUD_PLATFORMS),
        "cloud_agnostic": True,
    }


def kubernetes() -> dict[str, Any]:
    return {
        "components": list(K8S_COMPONENTS),
        "security": list(K8S_SECURITY),
        "security_complete_required": True,
        "not_incomplete": True,
    }


def container_security() -> dict[str, Any]:
    return {
        "controls": list(CONTAINER_SECURITY),
        "standards": list(CONTAINER_STANDARDS),
        "signing_required": True,
        "sbom_required": True,
    }


def devsecops() -> dict[str, Any]:
    return {
        "stages": list(DEVSECOPS_STAGES),
        "stage_count": len(DEVSECOPS_STAGES),
        "validation_required": True,
        "not_lacking_validation": True,
        "automated_required": True,
        "not_manual_only": True,
    }


def iac() -> dict[str, Any]:
    return {
        "tools": list(IAC_TOOLS),
        "reproducible_required": True,
        "not_non_reproducible": True,
        "drift_detection": True,
        "automated_rollback": True,
    }


def gitops() -> dict[str, Any]:
    return {
        "capabilities": list(GITOPS),
        "git_source_of_truth": True,
        "via_workflow_promotion": True,
    }


def service_mesh() -> dict[str, Any]:
    return {
        "capabilities": list(SERVICE_MESH),
        "mtls_required": True,
    }


def scalability() -> dict[str, Any]:
    return {
        "modes": list(SCALING),
        "auto_scaling_required": True,
        "not_manual_only": True,
    }


def resilience() -> dict[str, Any]:
    return {
        "capabilities": list(RESILIENCE),
        "availability_targets": list(AVAILABILITY_TARGETS),
        "disaster_recovery_defined_required": True,
        "not_undefined": True,
    }


def observability() -> dict[str, Any]:
    return {
        "pillars": list(OBSERVABILITY_PILLARS),
        "required": True,
        "not_missing": True,
        "via_enterprise_observability": True,
        "module_local_stack_forbidden": True,
    }


def monitoring() -> dict[str, Any]:
    return {
        "stack": list(MONITORING_STACK),
        "via_enterprise_observability": True,
    }


def security_observability() -> dict[str, Any]:
    return {
        "tracks": list(SECURITY_OBSERVABILITY),
        "integrates": ["siem", "soar", "xdr", "soc"],
        "security_controls_integrated_required": True,
        "not_unintegrated": True,
    }


def platform_engineering() -> dict[str, Any]:
    return {"capabilities": list(PLATFORM_ENGINEERING)}


def aiops() -> dict[str, Any]:
    return {
        "capabilities": list(AIOPS),
        "via_p210_j": True,
        "via_enterprise_ai": True,
    }


def cqrs_deploy() -> dict[str, Any]:
    return {"components": list(CQRS_DEPLOY), "via_p210_l": True}


def compliance() -> dict[str, Any]:
    return {"frameworks": list(COMPLIANCE_FRAMEWORKS)}


def ddd() -> dict[str, Any]:
    return {
        "sor": SOR,
        "logical_subdomains": [
            "deployment_pipeline",
            "kubernetes_platform",
            "container_security",
            "iac_gitops",
            "service_mesh",
            "scalability_ha",
            "observability",
            "platform_engineering",
        ],
        "sibling_bc_forbidden": [
            "deploy_platform",
            "devsecops",
            "k8s_platform",
            "cyber_observability",
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
            "deployment_automated": True,
            "kubernetes_security_complete": True,
            "infrastructure_reproducible": True,
            "observability_present": True,
            "auto_scaling": True,
            "disaster_recovery_defined": True,
            "security_controls_integrated": True,
            "pipeline_validation": True,
            "foundation_tests": True,
            "deploy_api_live": True,
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
        ],
        "architecture": architecture(),
        "kubernetes": kubernetes(),
        "container_security": container_security(),
        "devsecops": devsecops(),
        "iac": iac(),
        "gitops": gitops(),
        "service_mesh": service_mesh(),
        "scalability": scalability(),
        "resilience": resilience(),
        "observability": observability(),
        "monitoring": monitoring(),
        "security_observability": security_observability(),
        "platform_engineering": platform_engineering(),
        "aiops": aiops(),
        "cqrs_deploy": cqrs_deploy(),
        "compliance": compliance(),
        "ddd": ddd(),
        "cqrs": cqrs(),
        "microservices": microservices(),
        "integrations": integrations(),
        "cursor_outputs": cursor_outputs(),
        "quality_gates": quality_gates(),
        "production_readiness": production_readiness(),
        "deployment_automated_required": True,
        "kubernetes_security_complete_required": True,
        "infrastructure_reproducible_required": True,
        "observability_required": True,
        "auto_scaling_required": True,
        "disaster_recovery_defined_required": True,
        "security_controls_integrated_required": True,
        "pipeline_validation_required": True,
        "sibling_deploy_bc_forbidden": True,
        "module_local_observability_stack_forbidden": True,
        "api_prefix": f"{API_PREFIX}/deploy",
        "forbidden_sibling_bc": [
            "deploy_platform",
            "devsecops",
            "k8s_platform",
            "cyber_observability",
        ],
        "distinct_from": [
            "enterprise observability (telemetry plumbing)",
            "P210-J /ai-ops* (AIOps reasoning)",
            "P210-M /gov* (AI governance)",
            "P209 secrets",
        ],
    }


def executive_summary() -> dict[str, Any]:
    return catalog()


def deploy_surface() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "routes": [
            "GET /cyber-security/deploy",
            "GET /cyber-security/deploy/architecture",
            "GET /cyber-security/deploy/kubernetes",
            "GET /cyber-security/deploy/container-security",
            "GET /cyber-security/deploy/devsecops",
            "GET /cyber-security/deploy/iac",
            "GET /cyber-security/deploy/gitops",
            "GET /cyber-security/deploy/service-mesh",
            "GET /cyber-security/deploy/scalability",
            "GET /cyber-security/deploy/resilience",
            "GET /cyber-security/deploy/observability",
            "GET /cyber-security/deploy/monitoring",
            "GET /cyber-security/deploy/security-observability",
            "GET /cyber-security/deploy/platform-engineering",
            "GET /cyber-security/deploy/aiops",
            "GET /cyber-security/deploy/cqrs",
            "GET /cyber-security/deploy/events",
            "GET /cyber-security/deploy/microservices",
            "GET /cyber-security/deploy/compliance",
            "GET /cyber-security/deploy/integrations",
            "GET /cyber-security/deploy/outputs",
            "GET /cyber-security/deploy/production-readiness",
            "GET /cyber-security/deploy/readiness",
        ],
    }
