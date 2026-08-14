"""AI P214-N Infrastructure / Cloud / Compute foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/434-enterprise-ai-aiinfra.md",
    "docs/architecture/ENTERPRISE_AI_AIINFRA.md",
    "docs/architecture/enterprise_ai/AI_AIINFRA_CAPABILITIES.v1.yaml",
    "docs/architecture/enterprise_ai/AI_AIINFRA_DDD_CQRS.v1.yaml",
    "docs/architecture/enterprise_ai/AI_AIINFRA_SECURITY.v1.yaml",
    "docs/architecture/enterprise_ai/AI_AIINFRA_VALIDATION.v1.yaml",
    "backend/contexts/ai/domain/services/ai_platform_aiinfra.py",
    "backend/contexts/ai/domain/aggregates/ai_aiinfra_aggregates.py",
    "backend/contexts/ai/infrastructure/acl/ai_aiinfra_acl.py",
    "backend/contexts/ai/application/ai_aiinfra_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/ml_platform",
    "backend/contexts/generative_ai",
    "backend/contexts/llm_platform",
    "backend/contexts/ai_core",
    "backend/contexts/vector_intelligence",
    "backend/contexts/ai_infrastructure",
    "backend/contexts/ai_cloud",
    "backend/contexts/gpu_platform",
    "backend/contexts/ai_compute",
    "backend/contexts/ai_runtime_platform",
    "backend/contexts/kubernetes_ai",
)


def validate_ai_aiinfra_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.ai.domain.aggregates.ai_aiinfra_aggregates import (
        AIRuntimeRoot,
        AiinfraPlatformRoot,
        ComputeFabricRoot,
        GPUInfrastructureRoot,
        InfraAutomationRoot,
        InfraDigitalTwinRoot,
        KubernetesAIRoot,
        ResourceIntelligenceRoot,
    )
    from contexts.ai.domain.services import ai_platform_aiinfra as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P214-N"
        and cat.get("adr") == 434
        and cat.get("sor") == "ai"
        and cat.get("capability") == "CAP-PLT-AI-001"
        and cat.get("principle") == catmod.PRINCIPLE
        and cat.get("fabric") == catmod.FABRIC
        and "scalable, secure" in cat["principle"]
        and "intelligent compute foundation" in cat["principle"]
        and cat["domain_model"]["core_domain"] == catmod.CORE_DOMAIN
        and cat["domain_model"]["supporting_count"] >= 9
        and cat["bounded_contexts"]["context_count"] >= 7
        and cat["enterprise_ai_cloud_platform_present_required"] is True
        and cat["intelligent_compute_fabric_present_required"] is True
        and cat["gpu_infrastructure_platform_present_required"] is True
        and cat["ai_runtime_platform_present_required"] is True
        and cat["kubernetes_ai_platform_present_required"] is True
        and cat["infrastructure_automation_present_required"] is True
        and cat["resource_intelligence_present_required"] is True
        and cat["infrastructure_security_present_required"] is True
        and cat["infrastructure_knowledge_graph_present_required"] is True
        and cat["infrastructure_digital_twin_present_required"] is True
        and cat["cqrs_architecture_present_required"] is True
        and cat["event_architecture_present_required"] is True
        and cat["microservices_architecture_present_required"] is True
        and cat["api_first_architecture_present_required"] is True
        and cat["zero_trust_security_present_required"] is True
        and cat["cloud_native_deployment_present_required"] is True
        and cat["sibling_ai_bc_forbidden"] is True
        and cat["cloud"]["via_p213_o"] is True
        and cat["kubernetes"]["via_p214_m"] is True
        and cat["resources"]["via_p214_j"] is True
        and cat["knowledge_graph"]["via_p214_g"] is True
        and cat["observability"]["via_p214_j"] is True
        and cat["deployment"]["via_p213_o"] is True
        and cat["cqrs"]["command_count"] >= 6
        and cat["events"]["core_event_count"] >= 8
        and cat["microservices"]["service_count"] >= 9
        and cat["cursor_outputs"]["count"] >= 20
        and "enterprise_ai_cloud_platform_is_missing"
        in cat["quality_gates"]["reject_if"]
        and "P214-M" in cat["builds_on"]
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
            AiinfraPlatformRoot.enable,
            tenant_id="t1",
            platform_ref="p1",
            present=False,
        )
        and AiinfraPlatformRoot.enable(
            tenant_id="t1", platform_ref="p2"
        ).is_missing()
        is False,
        not _bad(
            ComputeFabricRoot.enable,
            tenant_id="t1",
            compute_ref="c1",
            present=False,
        )
        and ComputeFabricRoot.enable(
            tenant_id="t1", compute_ref="c2"
        ).is_missing()
        is False,
        not _bad(
            GPUInfrastructureRoot.enable,
            tenant_id="t1",
            gpu_ref="g1",
            present=False,
        )
        and GPUInfrastructureRoot.enable(
            tenant_id="t1", gpu_ref="g2"
        ).is_missing()
        is False,
        not _bad(
            AIRuntimeRoot.enable,
            tenant_id="t1",
            runtime_ref="r1",
            present=False,
        )
        and AIRuntimeRoot.enable(
            tenant_id="t1", runtime_ref="r2"
        ).is_missing()
        is False,
        not _bad(
            KubernetesAIRoot.enable,
            tenant_id="t1",
            k8s_ref="k1",
            present=False,
        )
        and KubernetesAIRoot.enable(
            tenant_id="t1", k8s_ref="k2"
        ).is_missing()
        is False,
        not _bad(
            InfraAutomationRoot.enable,
            tenant_id="t1",
            automation_ref="a1",
            present=False,
        )
        and InfraAutomationRoot.enable(
            tenant_id="t1", automation_ref="a2"
        ).is_missing()
        is False,
        not _bad(
            ResourceIntelligenceRoot.enable,
            tenant_id="t1",
            resource_ref="res1",
            present=False,
        )
        and ResourceIntelligenceRoot.enable(
            tenant_id="t1", resource_ref="res2"
        ).is_missing()
        is False,
        not _bad(
            InfraDigitalTwinRoot.enable,
            tenant_id="t1",
            twin_ref="tw1",
            present=False,
        )
        and InfraDigitalTwinRoot.enable(
            tenant_id="t1", twin_ref="tw2"
        ).is_missing()
        is False,
    ]
    aggregates_ok = all(checks)

    acl_path = root / "backend/contexts/ai/infrastructure/acl/ai_aiinfra_acl.py"
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_p209" in acl_text
        and "via_p210" in acl_text
        and "via_p211" in acl_text
        and "via_p213_o" in acl_text
        and "via_api_gateway" in acl_text
        and "via_event_fabric" in acl_text
        and "via_observability" in acl_text
        and "via_p214_d" in acl_text
        and "via_p214_e" in acl_text
        and "via_p214_f" in acl_text
        and "via_p214_g" in acl_text
        and "via_p214_i" in acl_text
        and "via_p214_j" in acl_text
        and "via_p214_m" in acl_text
        and "module_local_gpu_scheduler_forbidden" in acl_text
    )

    router = (
        root / "backend/contexts/ai/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@router.get("/aiinfra")' in router
        and "/aiinfra/readiness" in router
        and "/aiinfra/cloud" in router
        and "/aiinfra/gpu" in router
        and "/aiinfra/kubernetes" in router
        and "/aiinfra/runtime" in router
        and "/aiinfra/digital-twin" in router
    )

    law = (root / "docs/architecture/ENTERPRISE_AI_AIINFRA.md").read_text(
        encoding="utf-8"
    )
    doc_ok = (
        "Never Enterprise AI Cloud Platform is missing" in law
        and "Never Intelligent Compute Fabric is missing" in law
        and "Never GPU Infrastructure Platform is missing" in law
        and "Never AI Runtime Platform is missing" in law
        and "Never Kubernetes AI Platform is missing" in law
        and "Never Infrastructure Automation is missing" in law
        and "Never Resource Intelligence is missing" in law
        and "Never Infrastructure Security is missing" in law
        and "Never Infrastructure Knowledge Graph is missing" in law
        and "Never Infrastructure Digital Twin is missing" in law
        and "Never CQRS architecture is missing" in law
        and "Never Event architecture is missing" in law
        and "Never Microservices architecture is missing" in law
        and "Never API first architecture is missing" in law
        and "Never Zero trust security is missing" in law
        and "Never Cloud native deployment is missing" in law
        and "Never Sibling AI BC" in law
        and "MEOS Intelligent AI Infrastructure Fabric" in law
        and "scalable, secure" in law
        and "intelligent compute foundation" in law
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
        "prompt": "P214-N",
        "adr": 434,
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
