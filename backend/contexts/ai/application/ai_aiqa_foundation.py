"""AI P214-O Testing / Evaluation / Validation / QA foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/435-enterprise-ai-aiqa.md",
    "docs/architecture/ENTERPRISE_AI_AIQA.md",
    "docs/architecture/enterprise_ai/AI_AIQA_CAPABILITIES.v1.yaml",
    "docs/architecture/enterprise_ai/AI_AIQA_DDD_CQRS.v1.yaml",
    "docs/architecture/enterprise_ai/AI_AIQA_SECURITY.v1.yaml",
    "docs/architecture/enterprise_ai/AI_AIQA_VALIDATION.v1.yaml",
    "backend/contexts/ai/domain/services/ai_platform_aiqa.py",
    "backend/contexts/ai/domain/aggregates/ai_aiqa_aggregates.py",
    "backend/contexts/ai/infrastructure/acl/ai_aiqa_acl.py",
    "backend/contexts/ai/application/ai_aiqa_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/ml_platform",
    "backend/contexts/generative_ai",
    "backend/contexts/llm_platform",
    "backend/contexts/ai_core",
    "backend/contexts/vector_intelligence",
    "backend/contexts/ai_testing",
    "backend/contexts/ai_qa",
    "backend/contexts/ai_evaluation",
    "backend/contexts/ai_quality",
    "backend/contexts/ai_validation",
    "backend/contexts/ai_benchmarking",
)


def validate_ai_aiqa_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.ai.domain.aggregates.ai_aiqa_aggregates import (
        AiqaPlatformRoot,
        CertificationRoot,
        EvaluationRoot,
        QualityDigitalTwinRoot,
        QualityIntelligenceRoot,
        RegressionRoot,
        SafetyTestingRoot,
        ValidationRoot,
    )
    from contexts.ai.domain.services import ai_platform_aiqa as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P214-O"
        and cat.get("adr") == 435
        and cat.get("sor") == "ai"
        and cat.get("capability") == "CAP-PLT-AI-001"
        and cat.get("principle") == catmod.PRINCIPLE
        and cat.get("fabric") == catmod.FABRIC
        and "continuous intelligent validation" in cat["principle"]
        and "autonomous improvement" in cat["principle"]
        and cat["domain_model"]["core_domain"] == catmod.CORE_DOMAIN
        and cat["domain_model"]["supporting_count"] >= 9
        and cat["bounded_contexts"]["context_count"] >= 7
        and cat["enterprise_ai_testing_platform_present_required"] is True
        and cat["ai_evaluation_platform_present_required"] is True
        and cat["ai_validation_platform_present_required"] is True
        and cat["ai_quality_assurance_platform_present_required"] is True
        and cat["ai_benchmarking_platform_present_required"] is True
        and cat["ai_safety_testing_present_required"] is True
        and cat["ai_reliability_testing_present_required"] is True
        and cat["ai_regression_testing_present_required"] is True
        and cat["ai_certification_platform_present_required"] is True
        and cat["quality_intelligence_platform_present_required"] is True
        and cat["knowledge_graph_integration_present_required"] is True
        and cat["digital_twin_integration_present_required"] is True
        and cat["cqrs_architecture_present_required"] is True
        and cat["event_architecture_present_required"] is True
        and cat["microservices_architecture_present_required"] is True
        and cat["api_first_architecture_present_required"] is True
        and cat["zero_trust_security_present_required"] is True
        and cat["cloud_native_deployment_present_required"] is True
        and cat["sibling_ai_bc_forbidden"] is True
        and cat["genai_quality"]["via_p214_e"] is True
        and cat["agent_testing"]["via_p214_f"] is True
        and cat["safety"]["via_p214_h"] is True
        and cat["safety"]["via_p214_i"] is True
        and cat["knowledge_graph"]["via_p214_g"] is True
        and cat["deployment"]["via_p214_n"] is True
        and cat["cqrs"]["command_count"] >= 6
        and cat["events"]["core_event_count"] >= 8
        and cat["microservices"]["service_count"] >= 10
        and cat["cursor_outputs"]["count"] >= 20
        and "enterprise_ai_testing_platform_is_missing"
        in cat["quality_gates"]["reject_if"]
        and "P214-N" in cat["builds_on"]
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
            AiqaPlatformRoot.enable,
            tenant_id="t1",
            platform_ref="p1",
            present=False,
        )
        and AiqaPlatformRoot.enable(
            tenant_id="t1", platform_ref="p2"
        ).is_missing()
        is False,
        not _bad(
            EvaluationRoot.enable,
            tenant_id="t1",
            evaluation_ref="e1",
            present=False,
        )
        and EvaluationRoot.enable(
            tenant_id="t1", evaluation_ref="e2"
        ).is_missing()
        is False,
        not _bad(
            ValidationRoot.enable,
            tenant_id="t1",
            validation_ref="v1",
            present=False,
        )
        and ValidationRoot.enable(
            tenant_id="t1", validation_ref="v2"
        ).is_missing()
        is False,
        not _bad(
            SafetyTestingRoot.enable,
            tenant_id="t1",
            safety_ref="s1",
            present=False,
        )
        and SafetyTestingRoot.enable(
            tenant_id="t1", safety_ref="s2"
        ).is_missing()
        is False,
        not _bad(
            RegressionRoot.enable,
            tenant_id="t1",
            regression_ref="r1",
            present=False,
        )
        and RegressionRoot.enable(
            tenant_id="t1", regression_ref="r2"
        ).is_missing()
        is False,
        not _bad(
            CertificationRoot.enable,
            tenant_id="t1",
            certification_ref="c1",
            present=False,
        )
        and CertificationRoot.enable(
            tenant_id="t1", certification_ref="c2"
        ).is_missing()
        is False,
        not _bad(
            QualityIntelligenceRoot.enable,
            tenant_id="t1",
            quality_ref="q1",
            present=False,
        )
        and QualityIntelligenceRoot.enable(
            tenant_id="t1", quality_ref="q2"
        ).is_missing()
        is False,
        not _bad(
            QualityDigitalTwinRoot.enable,
            tenant_id="t1",
            twin_ref="tw1",
            present=False,
        )
        and QualityDigitalTwinRoot.enable(
            tenant_id="t1", twin_ref="tw2"
        ).is_missing()
        is False,
    ]
    aggregates_ok = all(checks)

    acl_path = root / "backend/contexts/ai/infrastructure/acl/ai_aiqa_acl.py"
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_p207" in acl_text
        and "via_p208" in acl_text
        and "via_p209" in acl_text
        and "via_p210" in acl_text
        and "via_workflow_engine" in acl_text
        and "via_p214_d" in acl_text
        and "via_p214_e" in acl_text
        and "via_p214_f" in acl_text
        and "via_p214_g" in acl_text
        and "via_p214_h" in acl_text
        and "via_p214_i" in acl_text
        and "via_p214_j" in acl_text
        and "via_p214_k" in acl_text
        and "via_p214_l" in acl_text
        and "via_p214_m" in acl_text
        and "via_p214_n" in acl_text
        and "module_local_ai_qa_forbidden" in acl_text
    )

    router = (
        root / "backend/contexts/ai/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@router.get("/aiqa")' in router
        and "/aiqa/readiness" in router
        and "/aiqa/evaluation" in router
        and "/aiqa/safety" in router
        and "/aiqa/regression" in router
        and "/aiqa/quality-score" in router
        and "/aiqa/digital-twin" in router
    )

    law = (root / "docs/architecture/ENTERPRISE_AI_AIQA.md").read_text(
        encoding="utf-8"
    )
    doc_ok = (
        "Never Enterprise AI Testing Platform is missing" in law
        and "Never AI Evaluation Platform is missing" in law
        and "Never AI Validation Platform is missing" in law
        and "Never AI Quality Assurance Platform is missing" in law
        and "Never AI Benchmarking Platform is missing" in law
        and "Never AI Safety Testing is missing" in law
        and "Never AI Reliability Testing is missing" in law
        and "Never AI Regression Testing is missing" in law
        and "Never AI Certification Platform is missing" in law
        and "Never Quality Intelligence Platform is missing" in law
        and "Never Knowledge Graph Integration is missing" in law
        and "Never Digital Twin Integration is missing" in law
        and "Never CQRS architecture is missing" in law
        and "Never Event architecture is missing" in law
        and "Never Microservices architecture is missing" in law
        and "Never API first architecture is missing" in law
        and "Never Zero trust security is missing" in law
        and "Never Cloud native deployment is missing" in law
        and "Never Sibling AI BC" in law
        and "MEOS Enterprise AI Quality Intelligence Fabric" in law
        and "continuous intelligent validation" in law
        and "autonomous improvement" in law
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
        "prompt": "P214-O",
        "adr": 435,
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
