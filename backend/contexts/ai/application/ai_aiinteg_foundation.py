"""AI P214-M Integration / API Gateway / Service Mesh foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/433-enterprise-ai-aiinteg.md",
    "docs/architecture/ENTERPRISE_AI_AIINTEG.md",
    "docs/architecture/enterprise_ai/AI_AIINTEG_CAPABILITIES.v1.yaml",
    "docs/architecture/enterprise_ai/AI_AIINTEG_DDD_CQRS.v1.yaml",
    "docs/architecture/enterprise_ai/AI_AIINTEG_SECURITY.v1.yaml",
    "docs/architecture/enterprise_ai/AI_AIINTEG_VALIDATION.v1.yaml",
    "backend/contexts/ai/domain/services/ai_platform_aiinteg.py",
    "backend/contexts/ai/domain/aggregates/ai_aiinteg_aggregates.py",
    "backend/contexts/ai/infrastructure/acl/ai_aiinteg_acl.py",
    "backend/contexts/ai/application/ai_aiinteg_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/ml_platform",
    "backend/contexts/generative_ai",
    "backend/contexts/llm_platform",
    "backend/contexts/ai_core",
    "backend/contexts/vector_intelligence",
    "backend/contexts/ai_integration",
    "backend/contexts/ai_api_gateway",
    "backend/contexts/ai_service_mesh",
    "backend/contexts/ai_communication",
    "backend/contexts/ai_connectivity",
    "backend/contexts/model_serving_gateway",
)


def validate_ai_aiinteg_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.ai.domain.aggregates.ai_aiinteg_aggregates import (
        AgentCommunicationRoot,
        AiintegPlatformRoot,
        EventIntegrationRoot,
        IntegrationDigitalTwinRoot,
        IntegrationGovernanceRoot,
        ModelServingRoot,
        ServiceMeshRoot,
        WorkflowIntegrationRoot,
    )
    from contexts.ai.domain.services import ai_platform_aiinteg as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P214-M"
        and cat.get("adr") == 433
        and cat.get("sor") == "ai"
        and cat.get("capability") == "CAP-PLT-AI-001"
        and cat.get("principle") == catmod.PRINCIPLE
        and cat.get("fabric") == catmod.FABRIC
        and "secure, intelligent" in cat["principle"]
        and "autonomous communication fabric" in cat["principle"]
        and cat["domain_model"]["core_domain"] == catmod.CORE_DOMAIN
        and cat["domain_model"]["supporting_count"] >= 9
        and cat["bounded_contexts"]["context_count"] >= 7
        and cat["enterprise_ai_api_gateway_present_required"] is True
        and cat["intelligent_service_mesh_present_required"] is True
        and cat["ai_communication_fabric_present_required"] is True
        and cat["model_serving_gateway_present_required"] is True
        and cat["agent_communication_platform_present_required"] is True
        and cat["event_integration_platform_present_required"] is True
        and cat["workflow_orchestration_present_required"] is True
        and cat["integration_governance_present_required"] is True
        and cat["security_architecture_present_required"] is True
        and cat["knowledge_graph_integration_present_required"] is True
        and cat["digital_twin_integration_present_required"] is True
        and cat["cqrs_architecture_present_required"] is True
        and cat["event_architecture_present_required"] is True
        and cat["microservices_architecture_present_required"] is True
        and cat["api_first_architecture_present_required"] is True
        and cat["zero_trust_security_present_required"] is True
        and cat["cloud_native_deployment_present_required"] is True
        and cat["sibling_ai_bc_forbidden"] is True
        and cat["platform_api_gateway_owns_edge"] is True
        and cat["platform_event_fabric_owns_bus"] is True
        and cat["gateway"]["via_api_gateway"] is True
        and cat["serving"]["via_p214_l"] is True
        and cat["agents"]["via_p214_f"] is True
        and cat["events_fabric"]["via_event_fabric"] is True
        and cat["workflows"]["via_workflow_engine"] is True
        and cat["routing"]["via_p214_j"] is True
        and cat["knowledge_graph"]["via_p214_g"] is True
        and cat["observability"]["via_p214_j"] is True
        and cat["deployment"]["via_p213_o"] is True
        and cat["cqrs"]["command_count"] >= 6
        and cat["events"]["core_event_count"] >= 7
        and cat["microservices"]["service_count"] >= 10
        and cat["cursor_outputs"]["count"] >= 20
        and "enterprise_ai_api_gateway_is_missing"
        in cat["quality_gates"]["reject_if"]
        and "P214-L" in cat["builds_on"]
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )

    def _bad(fn, **kwargs):
        try:
            fn(**kwargs)
            return True
        except ValueError:
            return False

    checks = [
        not _bad(
            AiintegPlatformRoot.enable,
            tenant_id="t1",
            platform_ref="p1",
            present=False,
        )
        and AiintegPlatformRoot.enable(
            tenant_id="t1", platform_ref="p2"
        ).is_missing()
        is False,
        not _bad(
            ServiceMeshRoot.enable,
            tenant_id="t1",
            mesh_ref="m1",
            present=False,
        )
        and ServiceMeshRoot.enable(
            tenant_id="t1", mesh_ref="m2"
        ).is_missing()
        is False,
        not _bad(
            ModelServingRoot.enable,
            tenant_id="t1",
            serving_ref="s1",
            present=False,
        )
        and ModelServingRoot.enable(
            tenant_id="t1", serving_ref="s2"
        ).is_missing()
        is False,
        not _bad(
            AgentCommunicationRoot.enable,
            tenant_id="t1",
            agent_comm_ref="a1",
            present=False,
        )
        and AgentCommunicationRoot.enable(
            tenant_id="t1", agent_comm_ref="a2"
        ).is_missing()
        is False,
        not _bad(
            EventIntegrationRoot.enable,
            tenant_id="t1",
            event_ref="e1",
            present=False,
        )
        and EventIntegrationRoot.enable(
            tenant_id="t1", event_ref="e2"
        ).is_missing()
        is False,
        not _bad(
            WorkflowIntegrationRoot.enable,
            tenant_id="t1",
            workflow_ref="w1",
            present=False,
        )
        and WorkflowIntegrationRoot.enable(
            tenant_id="t1", workflow_ref="w2"
        ).is_missing()
        is False,
        not _bad(
            IntegrationGovernanceRoot.enable,
            tenant_id="t1",
            governance_ref="g1",
            present=False,
        )
        and IntegrationGovernanceRoot.enable(
            tenant_id="t1", governance_ref="g2"
        ).is_missing()
        is False,
        not _bad(
            IntegrationDigitalTwinRoot.enable,
            tenant_id="t1",
            twin_ref="tw1",
            present=False,
        )
        and IntegrationDigitalTwinRoot.enable(
            tenant_id="t1", twin_ref="tw2"
        ).is_missing()
        is False,
    ]
    aggregates_ok = all(checks)

    acl_path = root / "backend/contexts/ai/infrastructure/acl/ai_aiinteg_acl.py"
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_p207" in acl_text
        and "via_p208" in acl_text
        and "via_p209" in acl_text
        and "via_p210" in acl_text
        and "via_p211" in acl_text
        and "via_p213_o" in acl_text
        and "via_api_gateway" in acl_text
        and "via_event_fabric" in acl_text
        and "via_workflow_engine" in acl_text
        and "via_observability" in acl_text
        and "via_p214_d" in acl_text
        and "via_p214_e" in acl_text
        and "via_p214_f" in acl_text
        and "via_p214_g" in acl_text
        and "via_p214_h" in acl_text
        and "via_p214_i" in acl_text
        and "via_p214_j" in acl_text
        and "via_p214_k" in acl_text
        and "via_p214_l" in acl_text
        and "module_local_ai_gateway_forbidden" in acl_text
    )

    router = (
        root / "backend/contexts/ai/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@router.get("/aiinteg")' in router
        and "/aiinteg/readiness" in router
        and "/aiinteg/gateway" in router
        and "/aiinteg/mesh" in router
        and "/aiinteg/serving" in router
        and "/aiinteg/agents" in router
        and "/aiinteg/digital-twin" in router
    )

    law = (root / "docs/architecture/ENTERPRISE_AI_AIINTEG.md").read_text(
        encoding="utf-8"
    )
    doc_ok = (
        "Never Enterprise AI API Gateway is missing" in law
        and "Never Intelligent Service Mesh is missing" in law
        and "Never AI Communication Fabric is missing" in law
        and "Never Model Serving Gateway is missing" in law
        and "Never Agent Communication Platform is missing" in law
        and "Never Event Integration Platform is missing" in law
        and "Never Workflow Orchestration is missing" in law
        and "Never Integration Governance is missing" in law
        and "Never Security Architecture is missing" in law
        and "Never Knowledge Graph Integration is missing" in law
        and "Never Digital Twin Integration is missing" in law
        and "Never CQRS architecture is missing" in law
        and "Never Event architecture is missing" in law
        and "Never Microservices architecture is missing" in law
        and "Never API first architecture is missing" in law
        and "Never Zero trust security is missing" in law
        and "Never Cloud native deployment is missing" in law
        and "Never Sibling AI BC" in law
        and "MEOS Intelligent AI Integration Fabric" in law
        and "secure, intelligent" in law
        and "autonomous communication fabric" in law
        and "Platform API Gateway owns edge" in law
    )

    passed = (
        not missing
        and not sibling
        and catalog_ok
        and aggregates_ok
        and acl_ok
        and router_ok
        and doc_ok
    )
    return {
        "prompt": "P214-M",
        "adr": 433,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "catalog": catalog_ok,
        "aggregates": aggregates_ok,
        "acl": acl_ok,
        "router": router_ok,
        "documentation": doc_ok,
        "sor": "ai",
        "capability": "CAP-PLT-AI-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
