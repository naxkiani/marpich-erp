"""AI P214-J AIOps / Autonomous AI Management foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/430-enterprise-ai-aiops.md",
    "docs/architecture/ENTERPRISE_AI_AIOPS.md",
    "docs/architecture/enterprise_ai/AI_AIOPS_CAPABILITIES.v1.yaml",
    "docs/architecture/enterprise_ai/AI_AIOPS_DDD_CQRS.v1.yaml",
    "docs/architecture/enterprise_ai/AI_AIOPS_SECURITY.v1.yaml",
    "docs/architecture/enterprise_ai/AI_AIOPS_VALIDATION.v1.yaml",
    "backend/contexts/ai/domain/services/ai_platform_aiops.py",
    "backend/contexts/ai/domain/aggregates/ai_aiops_aggregates.py",
    "backend/contexts/ai/infrastructure/acl/ai_aiops_acl.py",
    "backend/contexts/ai/application/ai_aiops_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/ml_platform",
    "backend/contexts/generative_ai",
    "backend/contexts/llm_platform",
    "backend/contexts/ai_core",
    "backend/contexts/vector_intelligence",
    "backend/contexts/aiops",
    "backend/contexts/ai_operations",
    "backend/contexts/ai_observability",
    "backend/contexts/ai_remediation",
    "backend/contexts/ai_finops",
)


def validate_ai_aiops_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.ai.domain.aggregates.ai_aiops_aggregates import (
        AiopsPlatformRoot,
        AutonomousRemediationRoot,
        IncidentIntelligenceRoot,
        ObservabilityRoot,
        OpsDigitalTwinRoot,
        PerformanceIntelligenceRoot,
    )
    from contexts.ai.domain.services import ai_platform_aiops as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P214-J"
        and cat.get("adr") == 430
        and cat.get("sor") == "ai"
        and cat.get("capability") == "CAP-PLT-AI-001"
        and cat.get("principle") == catmod.PRINCIPLE
        and cat.get("fabric") == catmod.FABRIC
        and "self-optimizing" in cat["principle"]
        and cat["domain_model"]["core_domain"] == catmod.CORE_DOMAIN
        and cat["domain_model"]["supporting_count"] >= 9
        and cat["bounded_contexts"]["context_count"] >= 7
        and cat["enterprise_aiops_platform_present_required"] is True
        and cat["ai_operations_center_present_required"] is True
        and cat["ai_observability_present_required"] is True
        and cat["ai_monitoring_present_required"] is True
        and cat["incident_intelligence_present_required"] is True
        and cat["root_cause_analysis_present_required"] is True
        and cat["autonomous_remediation_present_required"] is True
        and cat["ai_reliability_engineering_present_required"] is True
        and cat["performance_intelligence_present_required"] is True
        and cat["capacity_intelligence_present_required"] is True
        and cat["cost_optimization_present_required"] is True
        and cat["operational_digital_twin_present_required"] is True
        and cat["cqrs_architecture_present_required"] is True
        and cat["event_architecture_present_required"] is True
        and cat["microservices_architecture_present_required"] is True
        and cat["api_first_architecture_present_required"] is True
        and cat["zero_trust_security_present_required"] is True
        and cat["cloud_native_deployment_present_required"] is True
        and cat["sibling_ai_bc_forbidden"] is True
        and cat["observability"]["via_observability"] is True
        and cat["rca"]["via_p210"] is True
        and cat["rca"]["via_p213_o"] is True
        and cat["remediation"]["via_workflow_engine"] is True
        and cat["deployment"]["via_p213_o"] is True
        and cat["cqrs"]["command_count"] >= 6
        and cat["events"]["core_event_count"] >= 8
        and cat["microservices"]["service_count"] >= 10
        and cat["cursor_outputs"]["count"] >= 20
        and "enterprise_aiops_platform_is_missing"
        in cat["quality_gates"]["reject_if"]
        and "P214-I" in cat["builds_on"]
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
            AiopsPlatformRoot.enable,
            tenant_id="t1",
            platform_ref="p1",
            present=False,
        )
        and AiopsPlatformRoot.enable(
            tenant_id="t1", platform_ref="p2"
        ).is_missing()
        is False,
        not _bad(
            ObservabilityRoot.enable,
            tenant_id="t1",
            observability_ref="o1",
            present=False,
        )
        and ObservabilityRoot.enable(
            tenant_id="t1", observability_ref="o2"
        ).is_missing()
        is False,
        not _bad(
            IncidentIntelligenceRoot.enable,
            tenant_id="t1",
            incident_ref="i1",
            present=False,
        )
        and IncidentIntelligenceRoot.enable(
            tenant_id="t1", incident_ref="i2"
        ).is_missing()
        is False,
        not _bad(
            AutonomousRemediationRoot.enable,
            tenant_id="t1",
            remediation_ref="r1",
            present=False,
        )
        and AutonomousRemediationRoot.enable(
            tenant_id="t1", remediation_ref="r2"
        ).is_missing()
        is False,
        not _bad(
            PerformanceIntelligenceRoot.enable,
            tenant_id="t1",
            performance_ref="pf1",
            present=False,
        )
        and PerformanceIntelligenceRoot.enable(
            tenant_id="t1", performance_ref="pf2"
        ).is_missing()
        is False,
        not _bad(
            OpsDigitalTwinRoot.enable,
            tenant_id="t1",
            twin_ref="tw1",
            present=False,
        )
        and OpsDigitalTwinRoot.enable(
            tenant_id="t1", twin_ref="tw2"
        ).is_missing()
        is False,
    ]
    aggregates_ok = all(checks)

    acl_path = root / "backend/contexts/ai/infrastructure/acl/ai_aiops_acl.py"
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_p207" in acl_text
        and "via_p208" in acl_text
        and "via_p209" in acl_text
        and "via_p210" in acl_text
        and "via_p211" in acl_text
        and "via_p213_o" in acl_text
        and "via_observability" in acl_text
        and "via_workflow_engine" in acl_text
        and "via_p214_d" in acl_text
        and "via_p214_e" in acl_text
        and "via_p214_f" in acl_text
        and "via_p214_g" in acl_text
        and "via_p214_h" in acl_text
        and "via_p214_i" in acl_text
        and "module_local_aiops_forbidden" in acl_text
    )

    router = (
        root / "backend/contexts/ai/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@router.get("/aiops")' in router
        and "/aiops/readiness" in router
        and "/aiops/observability" in router
        and "/aiops/incidents" in router
        and "/aiops/remediation" in router
        and "/aiops/rca" in router
        and "/aiops/digital-twin" in router
    )

    law = (root / "docs/architecture/ENTERPRISE_AI_AIOPS.md").read_text(
        encoding="utf-8"
    )
    doc_ok = (
        "Never Enterprise AIOps platform is missing" in law
        and "Never AI Operations Center is missing" in law
        and "Never AI Observability is missing" in law
        and "Never AI Monitoring is missing" in law
        and "Never Incident Intelligence is missing" in law
        and "Never Root Cause Analysis is missing" in law
        and "Never Autonomous Remediation is missing" in law
        and "Never AI Reliability Engineering is missing" in law
        and "Never Performance Intelligence is missing" in law
        and "Never Capacity Intelligence is missing" in law
        and "Never Cost Optimization is missing" in law
        and "Never Operational Digital Twin is missing" in law
        and "Never CQRS architecture is missing" in law
        and "Never Event architecture is missing" in law
        and "Never Microservices architecture is missing" in law
        and "Never API first architecture is missing" in law
        and "Never Zero trust security is missing" in law
        and "Never Cloud native deployment is missing" in law
        and "Never Sibling AI BC" in law
        and "MEOS Autonomous AI Operations Fabric" in law
        and "self-optimizing" in law
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
        "prompt": "P214-J",
        "adr": 430,
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
