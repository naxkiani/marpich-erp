"""AI P214-K AI Data Intelligence / Feature Engineering foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/431-enterprise-ai-aidata.md",
    "docs/architecture/ENTERPRISE_AI_AIDATA.md",
    "docs/architecture/enterprise_ai/AI_AIDATA_CAPABILITIES.v1.yaml",
    "docs/architecture/enterprise_ai/AI_AIDATA_DDD_CQRS.v1.yaml",
    "docs/architecture/enterprise_ai/AI_AIDATA_SECURITY.v1.yaml",
    "docs/architecture/enterprise_ai/AI_AIDATA_VALIDATION.v1.yaml",
    "backend/contexts/ai/domain/services/ai_platform_aidata.py",
    "backend/contexts/ai/domain/aggregates/ai_aidata_aggregates.py",
    "backend/contexts/ai/infrastructure/acl/ai_aidata_acl.py",
    "backend/contexts/ai/application/ai_aidata_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/ml_platform",
    "backend/contexts/generative_ai",
    "backend/contexts/llm_platform",
    "backend/contexts/ai_core",
    "backend/contexts/vector_intelligence",
    "backend/contexts/feature_store",
    "backend/contexts/ai_data",
    "backend/contexts/ai_data_platform",
    "backend/contexts/feature_engineering",
    "backend/contexts/training_data_platform",
    "backend/contexts/synthetic_data_platform",
)


def validate_ai_aidata_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.ai.domain.aggregates.ai_aidata_aggregates import (
        AidataPlatformRoot,
        DataLineageRoot,
        DataQualityRoot,
        DatasetManagementRoot,
        FeatureEngineeringRoot,
        FeatureStoreRoot,
        SyntheticDataRoot,
        TrainingDataRoot,
    )
    from contexts.ai.domain.services import ai_platform_aidata as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P214-K"
        and cat.get("adr") == 431
        and cat.get("sor") == "ai"
        and cat.get("capability") == "CAP-PLT-AI-001"
        and cat.get("principle") == catmod.PRINCIPLE
        and cat.get("fabric") == catmod.FABRIC
        and "governed" in cat["principle"]
        and "reusable AI assets" in cat["principle"]
        and cat["domain_model"]["core_domain"] == catmod.CORE_DOMAIN
        and cat["domain_model"]["supporting_count"] >= 9
        and cat["bounded_contexts"]["context_count"] >= 8
        and cat["enterprise_ai_data_platform_present_required"] is True
        and cat["ai_dataset_management_present_required"] is True
        and cat["feature_engineering_platform_present_required"] is True
        and cat["feature_store_platform_present_required"] is True
        and cat["training_data_platform_present_required"] is True
        and cat["ai_data_pipeline_present_required"] is True
        and cat["synthetic_data_platform_present_required"] is True
        and cat["data_quality_intelligence_present_required"] is True
        and cat["ai_data_lineage_present_required"] is True
        and cat["ai_data_marketplace_present_required"] is True
        and cat["ai_data_governance_present_required"] is True
        and cat["cqrs_architecture_present_required"] is True
        and cat["event_architecture_present_required"] is True
        and cat["microservices_architecture_present_required"] is True
        and cat["api_first_architecture_present_required"] is True
        and cat["zero_trust_security_present_required"] is True
        and cat["cloud_native_deployment_present_required"] is True
        and cat["sibling_ai_bc_forbidden"] is True
        and cat["feature_store"]["via_p214_d"] is True
        and cat["synthetic"]["via_p214_h"] is True
        and cat["lineage"]["via_p212_k"] is True
        and cat["deployment"]["via_p213_o"] is True
        and cat["cqrs"]["command_count"] >= 6
        and cat["events"]["core_event_count"] >= 8
        and cat["microservices"]["service_count"] >= 10
        and cat["cursor_outputs"]["count"] >= 20
        and "enterprise_ai_data_platform_is_missing"
        in cat["quality_gates"]["reject_if"]
        and "P214-J" in cat["builds_on"]
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
            AidataPlatformRoot.enable,
            tenant_id="t1",
            platform_ref="p1",
            present=False,
        )
        and AidataPlatformRoot.enable(
            tenant_id="t1", platform_ref="p2"
        ).is_missing()
        is False,
        not _bad(
            DatasetManagementRoot.enable,
            tenant_id="t1",
            dataset_ref="d1",
            present=False,
        )
        and DatasetManagementRoot.enable(
            tenant_id="t1", dataset_ref="d2"
        ).is_missing()
        is False,
        not _bad(
            FeatureEngineeringRoot.enable,
            tenant_id="t1",
            feature_ref="f1",
            present=False,
        )
        and FeatureEngineeringRoot.enable(
            tenant_id="t1", feature_ref="f2"
        ).is_missing()
        is False,
        not _bad(
            FeatureStoreRoot.enable,
            tenant_id="t1",
            store_ref="s1",
            present=False,
        )
        and FeatureStoreRoot.enable(
            tenant_id="t1", store_ref="s2"
        ).is_missing()
        is False,
        not _bad(
            TrainingDataRoot.enable,
            tenant_id="t1",
            training_ref="tr1",
            present=False,
        )
        and TrainingDataRoot.enable(
            tenant_id="t1", training_ref="tr2"
        ).is_missing()
        is False,
        not _bad(
            SyntheticDataRoot.enable,
            tenant_id="t1",
            synthetic_ref="sy1",
            present=False,
        )
        and SyntheticDataRoot.enable(
            tenant_id="t1", synthetic_ref="sy2"
        ).is_missing()
        is False,
        not _bad(
            DataQualityRoot.enable,
            tenant_id="t1",
            quality_ref="q1",
            present=False,
        )
        and DataQualityRoot.enable(
            tenant_id="t1", quality_ref="q2"
        ).is_missing()
        is False,
        not _bad(
            DataLineageRoot.enable,
            tenant_id="t1",
            lineage_ref="l1",
            present=False,
        )
        and DataLineageRoot.enable(
            tenant_id="t1", lineage_ref="l2"
        ).is_missing()
        is False,
    ]
    aggregates_ok = all(checks)

    acl_path = root / "backend/contexts/ai/infrastructure/acl/ai_aidata_acl.py"
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_p207" in acl_text
        and "via_p208" in acl_text
        and "via_p209" in acl_text
        and "via_p210" in acl_text
        and "via_p211" in acl_text
        and "via_p212" in acl_text
        and "via_p212_k" in acl_text
        and "via_p213" in acl_text
        and "via_p213_o" in acl_text
        and "via_p214_d" in acl_text
        and "via_p214_e" in acl_text
        and "via_p214_f" in acl_text
        and "via_p214_g" in acl_text
        and "via_p214_h" in acl_text
        and "via_p214_i" in acl_text
        and "via_p214_j" in acl_text
        and "module_local_feature_store_forbidden" in acl_text
    )

    router = (
        root / "backend/contexts/ai/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@router.get("/aidata")' in router
        and "/aidata/readiness" in router
        and "/aidata/fabric" in router
        and "/aidata/feature-store" in router
        and "/aidata/synthetic" in router
        and "/aidata/lineage" in router
        and "/aidata/marketplace" in router
    )

    law = (root / "docs/architecture/ENTERPRISE_AI_AIDATA.md").read_text(
        encoding="utf-8"
    )
    doc_ok = (
        "Never Enterprise AI Data Platform is missing" in law
        and "Never AI Dataset Management is missing" in law
        and "Never Feature Engineering Platform is missing" in law
        and "Never Feature Store Platform is missing" in law
        and "Never Training Data Platform is missing" in law
        and "Never Synthetic Data Platform is missing" in law
        and "Never Data Quality Intelligence is missing" in law
        and "Never AI Data Lineage is missing" in law
        and "Never AI Data Marketplace is missing" in law
        and "Never CQRS architecture is missing" in law
        and "Never Event architecture is missing" in law
        and "Never Microservices architecture is missing" in law
        and "Never API first architecture is missing" in law
        and "Never Zero trust security is missing" in law
        and "Never Cloud native deployment is missing" in law
        and "Never Sibling AI BC" in law
        and "MEOS Enterprise AI Data Intelligence Fabric" in law
        and "governed" in law
        and "reusable AI assets" in law
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
        "prompt": "P214-K",
        "adr": 431,
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
