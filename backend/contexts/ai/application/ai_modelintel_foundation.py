"""AI P214-L Model Intelligence / Lifecycle / Governance foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/432-enterprise-ai-modelintel.md",
    "docs/architecture/ENTERPRISE_AI_MODELINTEL.md",
    "docs/architecture/enterprise_ai/AI_MODELINTEL_CAPABILITIES.v1.yaml",
    "docs/architecture/enterprise_ai/AI_MODELINTEL_DDD_CQRS.v1.yaml",
    "docs/architecture/enterprise_ai/AI_MODELINTEL_SECURITY.v1.yaml",
    "docs/architecture/enterprise_ai/AI_MODELINTEL_VALIDATION.v1.yaml",
    "backend/contexts/ai/domain/services/ai_platform_modelintel.py",
    "backend/contexts/ai/domain/aggregates/ai_modelintel_aggregates.py",
    "backend/contexts/ai/infrastructure/acl/ai_modelintel_acl.py",
    "backend/contexts/ai/application/ai_modelintel_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/ml_platform",
    "backend/contexts/generative_ai",
    "backend/contexts/llm_platform",
    "backend/contexts/ai_core",
    "backend/contexts/vector_intelligence",
    "backend/contexts/model_lifecycle_platform",
    "backend/contexts/model_registry",
    "backend/contexts/model_governance_platform",
    "backend/contexts/ai_model_platform",
)


def validate_ai_modelintel_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.ai.domain.aggregates.ai_modelintel_aggregates import (
        ModelDigitalTwinRoot,
        ModelDriftRoot,
        ModelEvaluationRoot,
        ModelLifecycleRoot,
        ModelMonitoringRoot,
        ModelRegistryRoot,
        ModelRiskRoot,
        ModelintelPlatformRoot,
    )
    from contexts.ai.domain.services import ai_platform_modelintel as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P214-L"
        and cat.get("adr") == 432
        and cat.get("sor") == "ai"
        and cat.get("capability") == "CAP-PLT-AI-001"
        and cat.get("principle") == catmod.PRINCIPLE
        and cat.get("fabric") == catmod.FABRIC
        and "lifecycle visibility" in cat["principle"]
        and "governance and intelligence" in cat["principle"]
        and cat["domain_model"]["core_domain"] == catmod.CORE_DOMAIN
        and cat["domain_model"]["supporting_count"] >= 9
        and cat["bounded_contexts"]["context_count"] >= 7
        and cat["enterprise_ai_model_platform_present_required"] is True
        and cat["model_registry_present_required"] is True
        and cat["model_lifecycle_management_present_required"] is True
        and cat["model_version_management_present_required"] is True
        and cat["model_evaluation_intelligence_present_required"] is True
        and cat["model_approval_governance_present_required"] is True
        and cat["model_governance_present_required"] is True
        and cat["model_monitoring_present_required"] is True
        and cat["drift_detection_present_required"] is True
        and cat["model_risk_management_present_required"] is True
        and cat["model_knowledge_graph_present_required"] is True
        and cat["model_digital_twin_present_required"] is True
        and cat["cqrs_architecture_present_required"] is True
        and cat["event_architecture_present_required"] is True
        and cat["microservices_architecture_present_required"] is True
        and cat["api_first_architecture_present_required"] is True
        and cat["zero_trust_security_present_required"] is True
        and cat["cloud_native_deployment_present_required"] is True
        and cat["sibling_ai_bc_forbidden"] is True
        and cat["approval"]["via_p214_h"] is True
        and cat["approval"]["via_workflow_engine"] is True
        and cat["knowledge_graph"]["via_p214_g"] is True
        and cat["deployment"]["via_p213_o"] is True
        and cat["cqrs"]["command_count"] >= 7
        and cat["events"]["core_event_count"] >= 8
        and cat["microservices"]["service_count"] >= 10
        and cat["cursor_outputs"]["count"] >= 20
        and "enterprise_ai_model_platform_is_missing"
        in cat["quality_gates"]["reject_if"]
        and "P214-K" in cat["builds_on"]
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
            ModelintelPlatformRoot.enable,
            tenant_id="t1",
            platform_ref="p1",
            present=False,
        )
        and ModelintelPlatformRoot.enable(
            tenant_id="t1", platform_ref="p2"
        ).is_missing()
        is False,
        not _bad(
            ModelRegistryRoot.enable,
            tenant_id="t1",
            registry_ref="r1",
            present=False,
        )
        and ModelRegistryRoot.enable(
            tenant_id="t1", registry_ref="r2"
        ).is_missing()
        is False,
        not _bad(
            ModelLifecycleRoot.enable,
            tenant_id="t1",
            lifecycle_ref="lc1",
            present=False,
        )
        and ModelLifecycleRoot.enable(
            tenant_id="t1", lifecycle_ref="lc2"
        ).is_missing()
        is False,
        not _bad(
            ModelEvaluationRoot.enable,
            tenant_id="t1",
            evaluation_ref="e1",
            present=False,
        )
        and ModelEvaluationRoot.enable(
            tenant_id="t1", evaluation_ref="e2"
        ).is_missing()
        is False,
        not _bad(
            ModelMonitoringRoot.enable,
            tenant_id="t1",
            monitoring_ref="m1",
            present=False,
        )
        and ModelMonitoringRoot.enable(
            tenant_id="t1", monitoring_ref="m2"
        ).is_missing()
        is False,
        not _bad(
            ModelDriftRoot.enable,
            tenant_id="t1",
            drift_ref="d1",
            present=False,
        )
        and ModelDriftRoot.enable(
            tenant_id="t1", drift_ref="d2"
        ).is_missing()
        is False,
        not _bad(
            ModelRiskRoot.enable,
            tenant_id="t1",
            risk_ref="rk1",
            present=False,
        )
        and ModelRiskRoot.enable(
            tenant_id="t1", risk_ref="rk2"
        ).is_missing()
        is False,
        not _bad(
            ModelDigitalTwinRoot.enable,
            tenant_id="t1",
            twin_ref="tw1",
            present=False,
        )
        and ModelDigitalTwinRoot.enable(
            tenant_id="t1", twin_ref="tw2"
        ).is_missing()
        is False,
    ]
    aggregates_ok = all(checks)

    acl_path = root / "backend/contexts/ai/infrastructure/acl/ai_modelintel_acl.py"
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_p207" in acl_text
        and "via_p208" in acl_text
        and "via_p209" in acl_text
        and "via_p210" in acl_text
        and "via_p211" in acl_text
        and "via_p212" in acl_text
        and "via_p213" in acl_text
        and "via_p213_o" in acl_text
        and "via_p214_d" in acl_text
        and "via_p214_e" in acl_text
        and "via_p214_f" in acl_text
        and "via_p214_g" in acl_text
        and "via_p214_h" in acl_text
        and "via_workflow_engine" in acl_text
        and "via_p214_i" in acl_text
        and "via_p214_j" in acl_text
        and "via_p214_k" in acl_text
        and "module_local_model_registry_forbidden" in acl_text
    )

    router = (
        root / "backend/contexts/ai/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@router.get("/modelintel")' in router
        and "/modelintel/readiness" in router
        and "/modelintel/registry" in router
        and "/modelintel/lifecycle" in router
        and "/modelintel/drift" in router
        and "/modelintel/knowledge-graph" in router
        and "/modelintel/digital-twin" in router
    )

    law = (root / "docs/architecture/ENTERPRISE_AI_MODELINTEL.md").read_text(
        encoding="utf-8"
    )
    doc_ok = (
        "Never Enterprise AI Model Platform is missing" in law
        and "Never Model Registry is missing" in law
        and "Never Model Lifecycle Management is missing" in law
        and "Never Model Evaluation Intelligence is missing" in law
        and "Never Model Governance is missing" in law
        and "Never Model Monitoring is missing" in law
        and "Never Drift Detection is missing" in law
        and "Never Model Risk Management is missing" in law
        and "Never Model Knowledge Graph is missing" in law
        and "Never Model Digital Twin is missing" in law
        and "Never CQRS architecture is missing" in law
        and "Never Event architecture is missing" in law
        and "Never Microservices architecture is missing" in law
        and "Never API first architecture is missing" in law
        and "Never Zero trust security is missing" in law
        and "Never Cloud native deployment is missing" in law
        and "Never Sibling AI BC" in law
        and "MEOS Enterprise AI Model Intelligence Fabric" in law
        and "lifecycle visibility" in law
        and "governance and intelligence" in law
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
        "prompt": "P214-L",
        "adr": 432,
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
