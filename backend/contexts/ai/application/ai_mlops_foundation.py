"""AI P214-D MLOps foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/424-enterprise-ai-mlops.md",
    "docs/architecture/ENTERPRISE_AI_MLOPS.md",
    "docs/architecture/enterprise_ai/AI_MLOPS_CAPABILITIES.v1.yaml",
    "docs/architecture/enterprise_ai/AI_MLOPS_DDD_CQRS.v1.yaml",
    "docs/architecture/enterprise_ai/AI_MLOPS_SECURITY.v1.yaml",
    "docs/architecture/enterprise_ai/AI_MLOPS_VALIDATION.v1.yaml",
    "backend/contexts/ai/domain/services/ai_platform_mlops.py",
    "backend/contexts/ai/domain/aggregates/ai_mlops_aggregates.py",
    "backend/contexts/ai/infrastructure/acl/ai_mlops_acl.py",
    "backend/contexts/ai/application/ai_mlops_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/ml_platform",
    "backend/contexts/generative_ai",
    "backend/contexts/llm_platform",
    "backend/contexts/ai_core",
    "backend/contexts/vector_intelligence",
    "backend/contexts/model_lifecycle_platform",
)


def validate_ai_mlops_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.ai.domain.aggregates.ai_mlops_aggregates import (
        ContinuousTrainingRoot,
        FeatureStoreRoot,
        MlLifecycleRoot,
        MlopsPlatformRoot,
        ModelMonitoringRoot,
        ModelRegistryRoot,
    )
    from contexts.ai.domain.services import ai_platform_mlops as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P214-D"
        and cat.get("adr") == 424
        and cat.get("sor") == "ai"
        and cat.get("capability") == "CAP-PLT-AI-001"
        and cat.get("principle") == catmod.PRINCIPLE
        and cat.get("fabric") == catmod.FABRIC
        and "isolated experiments" in cat["principle"]
        and cat["domain_model"]["core_domain"] == catmod.CORE_DOMAIN
        and cat["domain_model"]["supporting_count"] >= 9
        and cat["bounded_contexts"]["context_count"] >= 7
        and cat["lifecycle"]["stage_count"] >= 13
        and cat["enterprise_mlops_platform_present_required"] is True
        and cat["ml_lifecycle_management_present_required"] is True
        and cat["experiment_platform_present_required"] is True
        and cat["feature_store_present_required"] is True
        and cat["training_platform_present_required"] is True
        and cat["model_registry_present_required"] is True
        and cat["validation_platform_present_required"] is True
        and cat["deployment_platform_present_required"] is True
        and cat["monitoring_platform_present_required"] is True
        and cat["continuous_training_present_required"] is True
        and cat["ml_governance_present_required"] is True
        and cat["cqrs_architecture_present_required"] is True
        and cat["event_architecture_present_required"] is True
        and cat["microservices_architecture_present_required"] is True
        and cat["api_first_architecture_present_required"] is True
        and cat["zero_trust_security_present_required"] is True
        and cat["cloud_native_deployment_present_required"] is True
        and cat["sibling_ai_bc_forbidden"] is True
        and cat["feature_store"]["via_p212"] is True
        and cat["deployment"]["via_p213_o"] is True
        and cat["cqrs"]["command_count"] >= 6
        and cat["events"]["core_event_count"] >= 8
        and cat["microservices"]["service_count"] >= 10
        and cat["pipelines"]["pipeline_count"] >= 7
        and cat["cursor_outputs"]["count"] >= 20
        and "enterprise_mlops_platform_is_missing"
        in cat["quality_gates"]["reject_if"]
        and "P214-C" in cat["builds_on"]
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
            MlopsPlatformRoot.enable,
            tenant_id="t1",
            platform_ref="p1",
            present=False,
        )
        and MlopsPlatformRoot.enable(
            tenant_id="t1", platform_ref="p2"
        ).is_missing()
        is False,
        not _bad(
            MlLifecycleRoot.enable,
            tenant_id="t1",
            lifecycle_ref="l1",
            present=False,
        )
        and MlLifecycleRoot.enable(
            tenant_id="t1", lifecycle_ref="l2"
        ).is_missing()
        is False,
        not _bad(
            FeatureStoreRoot.enable,
            tenant_id="t1",
            store_ref="f1",
            present=False,
        )
        and FeatureStoreRoot.enable(
            tenant_id="t1", store_ref="f2"
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
            ContinuousTrainingRoot.enable,
            tenant_id="t1",
            retrain_ref="c1",
            present=False,
        )
        and ContinuousTrainingRoot.enable(
            tenant_id="t1", retrain_ref="c2"
        ).is_missing()
        is False,
    ]
    aggregates_ok = all(checks)

    acl_path = root / "backend/contexts/ai/infrastructure/acl/ai_mlops_acl.py"
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_p207" in acl_text
        and "via_p208" in acl_text
        and "via_p209" in acl_text
        and "via_p210" in acl_text
        and "via_p211" in acl_text
        and "via_p212" in acl_text
        and "via_p213_j" in acl_text
        and "via_p213_o" in acl_text
        and "via_p214_a" in acl_text
        and "via_p214_c" in acl_text
        and "model_signing" in acl_text
        and "module_local_llm_sdk_forbidden" in acl_text
    )

    router = (
        root / "backend/contexts/ai/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@router.get("/mlops")' in router
        and "/mlops/readiness" in router
        and "/mlops/lifecycle" in router
        and "/mlops/features" in router
        and "/mlops/registry" in router
        and "/mlops/monitoring" in router
        and "/mlops/continuous-training" in router
    )

    law = (root / "docs/architecture/ENTERPRISE_AI_MLOPS.md").read_text(
        encoding="utf-8"
    )
    doc_ok = (
        "Never Enterprise MLOps platform is missing" in law
        and "Never ML lifecycle management is missing" in law
        and "Never Experiment platform is missing" in law
        and "Never Feature store is missing" in law
        and "Never Training platform is missing" in law
        and "Never Model registry is missing" in law
        and "Never Validation platform is missing" in law
        and "Never Deployment platform is missing" in law
        and "Never Monitoring platform is missing" in law
        and "Never Continuous training is missing" in law
        and "Never ML governance is missing" in law
        and "Never CQRS architecture is missing" in law
        and "Never Event architecture is missing" in law
        and "Never Microservices architecture is missing" in law
        and "Never API first architecture is missing" in law
        and "Never Zero trust security is missing" in law
        and "Never Cloud native deployment is missing" in law
        and "Never Sibling AI BC" in law
        and "MEOS Enterprise Machine Learning Intelligence Fabric" in law
        and "isolated experiments" in law
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
        "prompt": "P214-D",
        "adr": 424,
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
