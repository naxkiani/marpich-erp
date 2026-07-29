"""AI P214-H Governance / Responsible AI / Risk foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/428-enterprise-ai-governance.md",
    "docs/architecture/ENTERPRISE_AI_GOVERNANCE.md",
    "docs/architecture/enterprise_ai/AI_GOVERNANCE_CAPABILITIES.v1.yaml",
    "docs/architecture/enterprise_ai/AI_GOVERNANCE_DDD_CQRS.v1.yaml",
    "docs/architecture/enterprise_ai/AI_GOVERNANCE_SECURITY.v1.yaml",
    "docs/architecture/enterprise_ai/AI_GOVERNANCE_VALIDATION.v1.yaml",
    "backend/contexts/ai/domain/services/ai_platform_governance.py",
    "backend/contexts/ai/domain/aggregates/ai_governance_aggregates.py",
    "backend/contexts/ai/infrastructure/acl/ai_governance_acl.py",
    "backend/contexts/ai/application/ai_governance_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/ml_platform",
    "backend/contexts/generative_ai",
    "backend/contexts/llm_platform",
    "backend/contexts/ai_core",
    "backend/contexts/vector_intelligence",
    "backend/contexts/ai_governance",
    "backend/contexts/responsible_ai",
    "backend/contexts/ai_risk",
    "backend/contexts/ai_ethics",
    "backend/contexts/ai_trust",
    "backend/contexts/ai_explainability",
)


def validate_ai_governance_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.ai.domain.aggregates.ai_governance_aggregates import (
        AiPolicyRoot,
        AiRiskRoot,
        AiTrustRoot,
        GovernancePlatformRoot,
        GovernanceTwinRoot,
        ResponsibleAiRoot,
    )
    from contexts.ai.domain.services import ai_platform_governance as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P214-H"
        and cat.get("adr") == 428
        and cat.get("sor") == "ai"
        and cat.get("capability") == "CAP-PLT-AI-001"
        and cat.get("principle") == catmod.PRINCIPLE
        and cat.get("fabric") == catmod.FABRIC
        and "trust framework" in cat["principle"]
        and cat["domain_model"]["core_domain"] == catmod.CORE_DOMAIN
        and cat["domain_model"]["supporting_count"] >= 9
        and cat["bounded_contexts"]["context_count"] >= 7
        and cat["policies"]["lifecycle_stage_count"] >= 7
        and cat["enterprise_ai_governance_platform_present_required"] is True
        and cat["responsible_ai_platform_present_required"] is True
        and cat["ai_risk_management_platform_present_required"] is True
        and cat["ai_policy_engine_present_required"] is True
        and cat["ai_compliance_platform_present_required"] is True
        and cat["ai_explainability_platform_present_required"] is True
        and cat["ai_audit_platform_present_required"] is True
        and cat["ai_trust_management_present_required"] is True
        and cat["governance_digital_twin_present_required"] is True
        and cat["cqrs_architecture_present_required"] is True
        and cat["event_architecture_present_required"] is True
        and cat["microservices_architecture_present_required"] is True
        and cat["api_first_architecture_present_required"] is True
        and cat["zero_trust_security_present_required"] is True
        and cat["cloud_native_deployment_present_required"] is True
        and cat["sibling_ai_bc_forbidden"] is True
        and cat["policies"]["via_policy_engine"] is True
        and cat["explainability"]["via_p214_d"] is True
        and cat["explainability"]["via_p214_e"] is True
        and cat["explainability"]["via_p214_f"] is True
        and cat["audit"]["via_audit"] is True
        and cat["compliance"]["via_compliance"] is True
        and cat["deployment"]["via_p213_o"] is True
        and cat["cqrs"]["command_count"] >= 6
        and cat["events"]["core_event_count"] >= 8
        and cat["microservices"]["service_count"] >= 9
        and cat["cursor_outputs"]["count"] >= 20
        and "enterprise_ai_governance_platform_is_missing"
        in cat["quality_gates"]["reject_if"]
        and "P214-G" in cat["builds_on"]
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
            GovernancePlatformRoot.enable,
            tenant_id="t1",
            platform_ref="p1",
            present=False,
        )
        and GovernancePlatformRoot.enable(
            tenant_id="t1", platform_ref="p2"
        ).is_missing()
        is False,
        not _bad(
            AiPolicyRoot.enable,
            tenant_id="t1",
            policy_ref="pol1",
            present=False,
        )
        and AiPolicyRoot.enable(
            tenant_id="t1", policy_ref="pol2"
        ).is_missing()
        is False,
        not _bad(
            AiRiskRoot.enable,
            tenant_id="t1",
            risk_ref="r1",
            present=False,
        )
        and AiRiskRoot.enable(tenant_id="t1", risk_ref="r2").is_missing()
        is False,
        not _bad(
            ResponsibleAiRoot.enable,
            tenant_id="t1",
            ethics_ref="e1",
            present=False,
        )
        and ResponsibleAiRoot.enable(
            tenant_id="t1", ethics_ref="e2"
        ).is_missing()
        is False,
        not _bad(
            AiTrustRoot.enable,
            tenant_id="t1",
            trust_ref="t1",
            present=False,
        )
        and AiTrustRoot.enable(tenant_id="t1", trust_ref="t2").is_missing()
        is False,
        not _bad(
            GovernanceTwinRoot.enable,
            tenant_id="t1",
            twin_ref="tw1",
            present=False,
        )
        and GovernanceTwinRoot.enable(
            tenant_id="t1", twin_ref="tw2"
        ).is_missing()
        is False,
    ]
    aggregates_ok = all(checks)

    acl_path = (
        root / "backend/contexts/ai/infrastructure/acl/ai_governance_acl.py"
    )
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_p207" in acl_text
        and "via_p208" in acl_text
        and "via_p209" in acl_text
        and "via_p210" in acl_text
        and "via_p211" in acl_text
        and "via_p212" in acl_text
        and "via_policy_engine" in acl_text
        and "via_workflow_engine" in acl_text
        and "via_audit" in acl_text
        and "via_compliance" in acl_text
        and "via_p214_d" in acl_text
        and "via_p214_e" in acl_text
        and "via_p214_f" in acl_text
        and "via_p214_g" in acl_text
        and "module_local_governance_forbidden" in acl_text
    )

    router = (
        root / "backend/contexts/ai/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@router.get("/governance")' in router
        and "/governance/readiness" in router
        and "/governance/policies" in router
        and "/governance/risk" in router
        and "/governance/trust" in router
        and "/governance/responsible-ai" in router
        and "/governance/digital-twin" in router
    )

    law = (root / "docs/architecture/ENTERPRISE_AI_GOVERNANCE.md").read_text(
        encoding="utf-8"
    )
    doc_ok = (
        "Never Enterprise AI Governance platform is missing" in law
        and "Never Responsible AI platform is missing" in law
        and "Never AI Risk Management platform is missing" in law
        and "Never AI Policy Engine is missing" in law
        and "Never AI Compliance platform is missing" in law
        and "Never AI Explainability platform is missing" in law
        and "Never AI Audit platform is missing" in law
        and "Never AI Trust management is missing" in law
        and "Never Governance Digital Twin is missing" in law
        and "Never CQRS architecture is missing" in law
        and "Never Event architecture is missing" in law
        and "Never Microservices architecture is missing" in law
        and "Never API first architecture is missing" in law
        and "Never Zero trust security is missing" in law
        and "Never Cloud native deployment is missing" in law
        and "Never Sibling AI BC" in law
        and "MEOS Trusted AI Governance Fabric" in law
        and "trust framework" in law
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
        "prompt": "P214-H",
        "adr": 428,
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
