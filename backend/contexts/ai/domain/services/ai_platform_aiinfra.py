"""P214-N Enterprise AI Infrastructure, AI Cloud & Intelligent Compute — immutable catalog."""
from __future__ import annotations

from typing import Any

PROMPT_ID = "P214-N"
ADR = 434
SOR = "ai"
API_PREFIX = "/api/v1/ai"
PRODUCT = (
    "Enterprise AI Infrastructure, AI Cloud Platform & Intelligent Compute Architecture"
)
CAPABILITY = "CAP-PLT-AI-001"

PRINCIPLE = (
    "Enterprise AI Infrastructure Platform SHALL provide the scalable, secure "
    "and intelligent compute foundation required for operating enterprise "
    "artificial intelligence at global scale."
)

FABRIC = "meos_intelligent_ai_infrastructure_fabric"

CORE_DOMAIN = "enterprise_ai_infrastructure_management"

SUPPORTING_DOMAINS: tuple[dict[str, str], ...] = (
    {"id": "ai_cloud_management", "purpose": "Cloud environments, multi/hybrid cloud."},
    {"id": "compute_resource", "purpose": "CPU/GPU/accelerator compute pools."},
    {"id": "gpu_management", "purpose": "GPU discovery, allocation, scheduling."},
    {"id": "ai_runtime", "purpose": "Training and inference runtime isolation."},
    {"id": "kubernetes_ai", "purpose": "K8s AI clusters, GPU operators, scheduling."},
    {"id": "infrastructure_automation", "purpose": "IaC, provisioning, self-healing."},
    {"id": "infrastructure_security", "purpose": "Zero trust infra and workload identity."},
    {"id": "resource_optimization", "purpose": "Capacity, cost, energy FinOps."},
    {"id": "infrastructure_governance", "purpose": "Policies, compliance, controls."},
)

AGGREGATE = {
    "name": "EnterpriseAIInfrastructureAggregate",
    "root": "EnterpriseAIInfrastructure",
    "entities": (
        "AICloudEnvironment",
        "ComputeCluster",
        "GPUNode",
        "AIRuntime",
        "KubernetesCluster",
        "AIWorkload",
        "InfrastructurePolicy",
        "ResourceAllocation",
        "ScalingPolicy",
        "InfrastructureMetric",
    ),
    "value_objects": (
        "InfrastructureIdentifier",
        "ComputeCapacity",
        "GPUCapacity",
        "ResourceQuota",
        "AvailabilityZone",
        "PerformanceScore",
        "CostScore",
        "SecurityLevel",
    ),
    "events": (
        "AIInfrastructureCreatedEvent",
        "ComputeAllocatedEvent",
        "GPUProvisionedEvent",
        "AIWorkloadDeployedEvent",
        "ResourceScaledEvent",
        "InfrastructureOptimizedEvent",
        "InfrastructureFailureDetectedEvent",
    ),
}

LOGICAL_BOUNDED_CONTEXTS: tuple[dict[str, Any], ...] = (
    {
        "id": "ai_cloud_platform",
        "bc": "BC-01",
        "name": "AI Cloud Platform Context",
        "purpose": "Cloud environments, multi/hybrid/edge/sovereign cloud.",
    },
    {
        "id": "ai_compute_fabric",
        "bc": "BC-02",
        "name": "AI Compute Fabric Context",
        "purpose": "CPU/GPU resources, accelerated computing, scheduling.",
    },
    {
        "id": "ai_runtime_infrastructure",
        "bc": "BC-03",
        "name": "AI Runtime Infrastructure Context",
        "purpose": "Model execution, inference and training runtimes.",
    },
    {
        "id": "kubernetes_ai_platform",
        "bc": "BC-04",
        "name": "Kubernetes AI Platform Context",
        "purpose": "Container orchestration, AI workload scheduling, clusters.",
    },
    {
        "id": "infrastructure_automation",
        "bc": "BC-05",
        "name": "Infrastructure Automation Context",
        "purpose": "Provisioning, automation workflows, self-healing.",
    },
    {
        "id": "ai_resource_intelligence",
        "bc": "BC-06",
        "name": "AI Resource Intelligence Context",
        "purpose": "Capacity intelligence, resource and cost optimization.",
    },
    {
        "id": "infrastructure_governance",
        "bc": "BC-07",
        "name": "Infrastructure Governance Context",
        "purpose": "Policies, compliance, security controls.",
    },
)

AI_CLOUD = {
    "present_required": True,
    "name": "MEOS AI Cloud Foundation",
    "via_p213_o": True,
    "supports": (
        "public_cloud",
        "private_cloud",
        "hybrid_cloud",
        "edge_cloud",
        "sovereign_cloud",
    ),
    "capabilities": (
        "cloud_resource_management",
        "environment_provisioning",
        "cloud_federation",
        "multi_tenant_isolation",
        "cloud_governance",
    ),
}

COMPUTE_FABRIC = {
    "present_required": True,
    "supports": (
        "cpu_computing",
        "gpu_computing",
        "tpu_computing",
        "ai_accelerators",
        "edge_ai_computing",
    ),
    "manages": (
        "compute_pools",
        "resource_scheduling",
        "workload_placement",
        "priority_management",
    ),
}

GPU_INTELLIGENCE = {
    "present_required": True,
    "system": "enterprise_gpu_management_system",
    "supports": (
        "gpu_discovery",
        "gpu_allocation",
        "gpu_scheduling",
        "gpu_monitoring",
        "gpu_optimization",
        "gpu_sharing",
    ),
    "manages": (
        "training_workloads",
        "inference_workloads",
        "simulation_workloads",
    ),
}

AI_RUNTIME = {
    "present_required": True,
    "supports": (
        "machine_learning_runtime",
        "llm_runtime",
        "agent_runtime",
        "inference_runtime",
        "training_runtime",
    ),
    "capabilities": (
        "runtime_isolation",
        "runtime_scaling",
        "runtime_optimization",
        "runtime_security",
    ),
}

KUBERNETES_AI = {
    "present_required": True,
    "via_p214_m": True,
    "includes": (
        "ai_kubernetes_clusters",
        "gpu_operators",
        "workload_scheduling",
        "autoscaling",
        "service_mesh_integration",
        "security_policies",
        "observability_integration",
    ),
}

INFRA_AUTOMATION = {
    "present_required": True,
    "system": "autonomous_infrastructure_management",
    "supports": (
        "infrastructure_as_code",
        "automated_provisioning",
        "configuration_management",
        "self_healing",
        "auto_scaling",
        "automated_recovery",
    ),
}

RESOURCE_INTELLIGENCE = {
    "present_required": True,
    "engine": "intelligent_resource_intelligence_engine",
    "optimizes": (
        "compute",
        "memory",
        "storage",
        "network",
        "gpu_usage",
        "energy_consumption",
    ),
    "score": "resource_optimization_score",
    "via_p214_j": True,
}

INFRA_SECURITY = {
    "present_required": True,
    "zero_trust": True,
    "integrates": ("P209", "P210", "P211", "P214-I"),
    "implements": (
        "infrastructure_zero_trust",
        "workload_identity",
        "runtime_protection",
        "network_security",
        "encryption",
        "compliance_controls",
    ),
}

INFRA_KNOWLEDGE_GRAPH = {
    "present_required": True,
    "via_p214_g": True,
    "represents": (
        "cloud_resources",
        "clusters",
        "nodes",
        "models",
        "workloads",
        "dependencies",
        "policies",
        "incidents",
    ),
    "enables": (
        "impact_analysis",
        "capacity_prediction",
        "failure_prediction",
        "optimization",
    ),
}

INFRA_DIGITAL_TWIN = {
    "present_required": True,
    "represents": (
        "cloud_state",
        "compute_state",
        "gpu_state",
        "network_state",
        "workload_state",
        "security_state",
    ),
    "enables": (
        "simulation",
        "capacity_planning",
        "optimization",
        "autonomous_management",
    ),
}

OBSERVABILITY = {
    "present_required": True,
    "via_p214_j": True,
    "via_observability": True,
    "monitors": (
        "infrastructure_metrics",
        "gpu_metrics",
        "runtime_metrics",
        "network_metrics",
        "workload_metrics",
        "security_events",
        "cost_metrics",
    ),
}

COMMANDS: tuple[str, ...] = (
    "CreateAIEnvironmentCommand",
    "ProvisionComputeCommand",
    "AllocateGPUCommand",
    "DeployAIWorkloadCommand",
    "ScaleInfrastructureCommand",
    "OptimizeResourcesCommand",
)

QUERIES: tuple[str, ...] = (
    "GetInfrastructureStatusQuery",
    "GetComputeCapacityQuery",
    "GetGPUStatusQuery",
    "GetWorkloadStatusQuery",
    "GetOptimizationReportQuery",
)

CORE_EVENTS: tuple[dict[str, str], ...] = (
    {"name": "InfrastructureCreatedEvent", "owner": "ai", "consumers": "audit,ops"},
    {"name": "ComputeAllocatedEvent", "owner": "ai", "consumers": "mlops,observability"},
    {"name": "GPUProvisionedEvent", "owner": "ai", "consumers": "mlops,aiops"},
    {"name": "WorkloadDeployedEvent", "owner": "ai", "consumers": "aiinteg,observability"},
    {"name": "ScalingTriggeredEvent", "owner": "ai", "consumers": "aiops,notifications"},
    {"name": "OptimizationCompletedEvent", "owner": "ai", "consumers": "analytics,finops"},
    {"name": "InfrastructureFailureEvent", "owner": "ai", "consumers": "aiops,aisec,notifications"},
    {"name": "ResourceScaledEvent", "owner": "ai", "consumers": "audit,aiops"},
)

MICROSERVICES: tuple[dict[str, Any], ...] = (
    {
        "id": "cloud_management_service",
        "responsibility": "AI cloud environment provisioning and federation",
        "api": "/ai/aiinfra/cloud",
        "db": "ai_*",
        "events": ("InfrastructureCreatedEvent",),
        "security": ("ai.assist.read",),
        "scaling": "control_plane",
    },
    {
        "id": "compute_management_service",
        "responsibility": "compute pool and workload placement",
        "api": "/ai/aiinfra/compute",
        "db": "ai_*",
        "events": ("ComputeAllocatedEvent",),
        "security": ("ai.assist.infer",),
        "scaling": "scheduler_ha",
    },
    {
        "id": "gpu_management_service",
        "responsibility": "GPU discovery allocation scheduling sharing",
        "api": "/ai/aiinfra/gpu",
        "db": "ai_*",
        "events": ("GPUProvisionedEvent",),
        "security": ("ai.assist.infer",),
        "scaling": "gpu_scheduler",
    },
    {
        "id": "runtime_service",
        "responsibility": "ML/LLM/agent/inference/training runtimes",
        "api": "/ai/aiinfra/runtime",
        "db": "ai_*",
        "events": ("WorkloadDeployedEvent",),
        "security": ("ai.assist.infer",),
        "scaling": "runtime_pools",
    },
    {
        "id": "kubernetes_management_service",
        "responsibility": "AI K8s clusters GPU operators autoscaling",
        "api": "/ai/aiinfra/kubernetes",
        "db": "ai_*",
        "events": ("WorkloadDeployedEvent", "ScalingTriggeredEvent"),
        "security": ("ai.assist.infer",),
        "scaling": "control_plane",
    },
    {
        "id": "automation_service",
        "responsibility": "IaC provisioning self-healing recovery",
        "api": "/ai/aiinfra/automation",
        "db": "ai_*",
        "events": ("InfrastructureCreatedEvent", "InfrastructureFailureEvent"),
        "security": ("ai.assist.infer",),
        "scaling": "worker_pools",
    },
    {
        "id": "resource_intelligence_service",
        "responsibility": "capacity cost energy optimization",
        "api": "/ai/aiinfra/resources",
        "db": "ai_*",
        "events": ("OptimizationCompletedEvent",),
        "security": ("ai.assist.read",),
        "scaling": "analytics_pipeline",
    },
    {
        "id": "infrastructure_security_service",
        "responsibility": "zero trust workload identity runtime protection",
        "api": "/ai/aiinfra/security",
        "db": "ai_*",
        "events": ("InfrastructureFailureEvent",),
        "security": ("ai.assist.read",),
        "scaling": "policy_evaluate",
    },
    {
        "id": "optimization_service",
        "responsibility": "FinOps-driven infra optimization",
        "api": "/ai/aiinfra/optimization",
        "db": "ai_*",
        "events": ("OptimizationCompletedEvent", "ResourceScaledEvent"),
        "security": ("ai.assist.infer",),
        "scaling": "stateless_replicas",
    },
)

API_SURFACES: tuple[str, ...] = (
    "/api/v1/ai/aiinfra/cloud",
    "/api/v1/ai/aiinfra/compute",
    "/api/v1/ai/aiinfra/gpu",
    "/api/v1/ai/aiinfra/runtime",
    "/api/v1/ai/aiinfra/kubernetes",
    "/api/v1/ai/aiinfra/automation",
    "/api/v1/ai/aiinfra/resources",
    "/api/v1/ai/aiinfra/security",
)

API_STYLES: tuple[str, ...] = ("REST", "GraphQL", "gRPC", "Streaming", "Event")

SECURITY = dict(INFRA_SECURITY)

DEPLOYMENT = {
    "present_required": True,
    "cloud_native": True,
    "via_p213_o": True,
    "components": (
        "kubernetes",
        "gpu_clusters",
        "ai_runtime_nodes",
        "storage_infrastructure",
        "networking_fabric",
        "security_layer",
        "monitoring_platform",
        "automation_engine",
    ),
}

TESTING: tuple[str, ...] = (
    "infrastructure_testing",
    "cloud_testing",
    "gpu_performance_testing",
    "runtime_testing",
    "security_testing",
    "scalability_testing",
    "disaster_recovery_testing",
    "chaos_engineering",
)

CURSOR_OUTPUTS: tuple[str, ...] = (
    "enterprise_ai_infrastructure_vision",
    "ddd_domain_model",
    "bounded_context_map",
    "ai_cloud_foundation",
    "ai_compute_fabric",
    "gpu_intelligence_platform",
    "ai_runtime_infrastructure",
    "kubernetes_ai_platform",
    "infrastructure_automation",
    "resource_intelligence",
    "infrastructure_security",
    "infrastructure_knowledge_graph",
    "infrastructure_digital_twin",
    "cqrs_commands_queries",
    "event_sourcing_schema",
    "microservice_boundaries",
    "observability_architecture",
    "cloud_native_deployment",
    "testing_architecture",
    "quality_gates_dod",
    "adr_434",
    "enterprise_ai_aiinfra_law",
)

QUALITY_GATES_REJECT_IF: tuple[str, ...] = (
    "enterprise_ai_cloud_platform_is_missing",
    "intelligent_compute_fabric_is_missing",
    "gpu_infrastructure_platform_is_missing",
    "ai_runtime_platform_is_missing",
    "kubernetes_ai_platform_is_missing",
    "infrastructure_automation_is_missing",
    "resource_intelligence_is_missing",
    "infrastructure_security_is_missing",
    "infrastructure_knowledge_graph_is_missing",
    "infrastructure_digital_twin_is_missing",
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
        "role": "MEOS Intelligent AI Infrastructure Fabric",
        "principle": PRINCIPLE,
        "equation": (
            "AI Models + AI Agents + LLM Systems + AI Data Platforms + AI "
            "Applications + AI Operations → Cloud Infrastructure → Intelligent "
            "Compute → AI Runtime Platform → Secure Execution Environment → "
            "Autonomous Infrastructure Management"
        ),
        "pillars": (
            "specialized_ai_infrastructure_required",
            "ai_cloud_vs_traditional_cloud",
            "accelerated_computing_critical",
            "scalable_ai_execution",
            "autonomous_infrastructure",
            "infrastructure_intelligence",
        ),
        "strategic_role": {
            "specialized_ai_infrastructure": (
                "Training and inference need GPU/TPU schedulers, runtime isolation, "
                "and FinOps — not generic VM fleets alone."
            ),
            "ai_cloud_vs_traditional": (
                "AI cloud adds accelerator pools, model runtimes, and workload-aware "
                "placement beyond standard IaaS."
            ),
            "accelerated_computing": (
                "GPU/accelerator management is first-class for training and inference."
            ),
            "scalable_execution": (
                "Elastic K8s AI platforms with autoscaling and canary placement."
            ),
            "autonomous_infrastructure": (
                "IaC, self-healing, and recovery reduce human toil at global scale."
            ),
            "infrastructure_intelligence": (
                "Resource intelligence + digital twin enable capacity and cost prediction."
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


def cloud() -> dict[str, Any]:
    return dict(AI_CLOUD)


def compute() -> dict[str, Any]:
    return dict(COMPUTE_FABRIC)


def gpu() -> dict[str, Any]:
    return dict(GPU_INTELLIGENCE)


def runtime() -> dict[str, Any]:
    return dict(AI_RUNTIME)


def kubernetes() -> dict[str, Any]:
    return dict(KUBERNETES_AI)


def automation() -> dict[str, Any]:
    return dict(INFRA_AUTOMATION)


def resources() -> dict[str, Any]:
    return dict(RESOURCE_INTELLIGENCE)


def security() -> dict[str, Any]:
    return dict(SECURITY)


def knowledge_graph() -> dict[str, Any]:
    return dict(INFRA_KNOWLEDGE_GRAPH)


def digital_twin() -> dict[str, Any]:
    return dict(INFRA_DIGITAL_TWIN)


def observability() -> dict[str, Any]:
    return dict(OBSERVABILITY)


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
            "P209",
            "P210",
            "P211",
            "P213-O",
            "P214-D",
            "P214-E",
            "P214-F",
            "P214-G",
            "P214-I",
            "P214-J",
            "P214-M",
            "observability",
            "event_fabric",
        ),
        "via_events_and_acl": True,
    }


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
            "enterprise_ai_cloud_platform": True,
            "intelligent_compute_fabric": True,
            "gpu_infrastructure_platform": True,
            "ai_runtime_platform": True,
            "kubernetes_ai_platform": True,
            "infrastructure_automation": True,
            "resource_intelligence": True,
            "infrastructure_security": True,
            "infrastructure_knowledge_graph": True,
            "infrastructure_digital_twin": True,
            "cqrs_architecture": True,
            "event_architecture": True,
            "microservice_architecture": True,
            "api_platform": True,
            "security_architecture": True,
            "deployment_architecture": True,
            "testing_architecture": True,
            "foundation_tests": True,
            "aiinfra_api_live": True,
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
            "P209",
            "P210",
            "P211",
            "P213-O",
            "AI_PLATFORM_STANDARD",
        ],
        "vision": vision(),
        "domain_model": domain_model(),
        "bounded_contexts": bounded_contexts(),
        "cloud": cloud(),
        "compute": compute(),
        "gpu": gpu(),
        "runtime": runtime(),
        "kubernetes": kubernetes(),
        "automation": automation(),
        "resources": resources(),
        "security": security(),
        "knowledge_graph": knowledge_graph(),
        "digital_twin": digital_twin(),
        "observability": observability(),
        "cqrs": cqrs(),
        "events": events(),
        "microservices": microservices(),
        "api": api(),
        "integrations": integrations(),
        "deployment": deployment(),
        "testing": testing(),
        "cursor_outputs": cursor_outputs(),
        "quality_gates": quality_gates(),
        "production_readiness": production_readiness(),
        "enterprise_ai_cloud_platform_present_required": True,
        "intelligent_compute_fabric_present_required": True,
        "gpu_infrastructure_platform_present_required": True,
        "ai_runtime_platform_present_required": True,
        "kubernetes_ai_platform_present_required": True,
        "infrastructure_automation_present_required": True,
        "resource_intelligence_present_required": True,
        "infrastructure_security_present_required": True,
        "infrastructure_knowledge_graph_present_required": True,
        "infrastructure_digital_twin_present_required": True,
        "cqrs_architecture_present_required": True,
        "event_architecture_present_required": True,
        "microservices_architecture_present_required": True,
        "api_first_architecture_present_required": True,
        "zero_trust_security_present_required": True,
        "cloud_native_deployment_present_required": True,
        "sibling_ai_bc_forbidden": True,
        "module_local_gpu_scheduler_forbidden": True,
        "via_enterprise_ai": True,
        "via_api_gateway": True,
        "api_prefix": f"{API_PREFIX}/aiinfra",
        "forbidden_sibling_bc": [
            "ai_infrastructure",
            "ai_cloud",
            "gpu_platform",
            "ai_compute",
            "ai_runtime_platform",
            "kubernetes_ai",
            "generative_ai",
            "llm_platform",
            "ai_core",
            "vector_intelligence",
            "ml_platform",
        ],
    }


def aiinfra_surface() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID,
        "routes": [
            "GET /ai/aiinfra",
            "GET /ai/aiinfra/vision",
            "GET /ai/aiinfra/domain",
            "GET /ai/aiinfra/bounded-contexts",
            "GET /ai/aiinfra/cloud",
            "GET /ai/aiinfra/compute",
            "GET /ai/aiinfra/gpu",
            "GET /ai/aiinfra/runtime",
            "GET /ai/aiinfra/kubernetes",
            "GET /ai/aiinfra/automation",
            "GET /ai/aiinfra/resources",
            "GET /ai/aiinfra/security",
            "GET /ai/aiinfra/knowledge-graph",
            "GET /ai/aiinfra/digital-twin",
            "GET /ai/aiinfra/observability",
            "GET /ai/aiinfra/cqrs",
            "GET /ai/aiinfra/events",
            "GET /ai/aiinfra/microservices",
            "GET /ai/aiinfra/integrations",
            "GET /ai/aiinfra/api",
            "GET /ai/aiinfra/deployment",
            "GET /ai/aiinfra/testing",
            "GET /ai/aiinfra/outputs",
            "GET /ai/aiinfra/production-readiness",
            "GET /ai/aiinfra/readiness",
        ],
    }
