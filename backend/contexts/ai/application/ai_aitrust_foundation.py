"""AI P214-P Governance / Compliance / Audit / Continuous Trust foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/436-enterprise-ai-aitrust.md",
    "docs/architecture/ENTERPRISE_AI_AITRUST.md",
    "docs/architecture/enterprise_ai/AI_AITRUST_CAPABILITIES.v1.yaml",
    "docs/architecture/enterprise_ai/AI_AITRUST_DDD_CQRS.v1.yaml",
    "docs/architecture/enterprise_ai/AI_AITRUST_SECURITY.v1.yaml",
    "docs/architecture/enterprise_ai/AI_AITRUST_VALIDATION.v1.yaml",
    "backend/contexts/ai/domain/services/ai_platform_aitrust.py",
    "backend/contexts/ai/domain/aggregates/ai_aitrust_aggregates.py",
    "backend/contexts/ai/infrastructure/acl/ai_aitrust_acl.py",
    "backend/contexts/ai/application/ai_aitrust_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/ml_platform",
    "backend/contexts/generative_ai",
    "backend/contexts/llm_platform",
    "backend/contexts/ai_core",
    "backend/contexts/vector_intelligence",
    "backend/contexts/ai_trust",
    "backend/contexts/ai_compliance",
    "backend/contexts/continuous_ai_trust",
    "backend/contexts/ai_audit_platform",
    "backend/contexts/ai_regulatory",
)


def validate_ai_aitrust_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.ai.domain.aggregates.ai_aitrust_aggregates import (
        AitrustPlatformRoot,
        AuditRoot,
        CertificationRoot,
        ComplianceRoot,
        PolicyRoot,
        RiskRoot,
        TrustDigitalTwinRoot,
        TrustRoot,
    )
    from contexts.ai.domain.services import ai_platform_aitrust as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P214-P"
        and cat.get("adr") == 436
        and cat.get("sor") == "ai"
        and cat.get("capability") == "CAP-PLT-AI-001"
        and cat.get("principle") == catmod.PRINCIPLE
        and cat.get("fabric") == catmod.FABRIC
        and "continuous intelligent trust management" in cat["principle"]
        and cat["domain_model"]["core_domain"] == catmod.CORE_DOMAIN
        and cat["domain_model"]["supporting_count"] >= 9
        and cat["bounded_contexts"]["context_count"] >= 7
        and cat["enterprise_ai_governance_platform_present_required"] is True
        and cat["ai_compliance_platform_present_required"] is True
        and cat["ai_audit_platform_present_required"] is True
        and cat["ai_trust_platform_present_required"] is True
        and cat["ai_risk_management_present_required"] is True
        and cat["ai_policy_management_present_required"] is True
        and cat["ai_transparency_present_required"] is True
        and cat["ai_explainability_governance_present_required"] is True
        and cat["regulatory_intelligence_present_required"] is True
        and cat["certification_platform_present_required"] is True
        and cat["governance_knowledge_graph_present_required"] is True
        and cat["governance_digital_twin_present_required"] is True
        and cat["cqrs_architecture_present_required"] is True
        and cat["event_architecture_present_required"] is True
        and cat["microservices_architecture_present_required"] is True
        and cat["api_first_architecture_present_required"] is True
        and cat["zero_trust_security_present_required"] is True
        and cat["cloud_native_deployment_present_required"] is True
        and cat["sibling_ai_bc_forbidden"] is True
        and cat["deepens_p214_h_continuous_trust"] is True
        and cat["policies"]["via_p214_h"] is True
        and cat["policies"]["via_policy_engine"] is True
        and cat["compliance"]["via_p211"] is True
        and cat["audit"]["via_audit_platform"] is True
        and cat["trust"]["via_p214_o"] is True
        and cat["explainability"]["via_p214_l"] is True
        and cat["knowledge_graph"]["via_p214_g"] is True
        and cat["cqrs"]["command_count"] >= 6
        and cat["events"]["core_event_count"] >= 8
        and cat["microservices"]["service_count"] >= 10
        and cat["cursor_outputs"]["count"] >= 20
        and "enterprise_ai_governance_platform_is_missing"
        in cat["quality_gates"]["reject_if"]
        and "P214-O" in cat["builds_on"]
        and "P214-H" in cat["builds_on"]
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
            AitrustPlatformRoot.enable,
            tenant_id="t1",
            platform_ref="p1",
            present=False,
        )
        and AitrustPlatformRoot.enable(
            tenant_id="t1", platform_ref="p2"
        ).is_missing()
        is False,
        not _bad(
            ComplianceRoot.enable,
            tenant_id="t1",
            compliance_ref="c1",
            present=False,
        )
        and ComplianceRoot.enable(
            tenant_id="t1", compliance_ref="c2"
        ).is_missing()
        is False,
        not _bad(
            AuditRoot.enable,
            tenant_id="t1",
            audit_ref="a1",
            present=False,
        )
        and AuditRoot.enable(
            tenant_id="t1", audit_ref="a2"
        ).is_missing()
        is False,
        not _bad(
            TrustRoot.enable,
            tenant_id="t1",
            trust_ref="t1",
            present=False,
        )
        and TrustRoot.enable(
            tenant_id="t1", trust_ref="t2"
        ).is_missing()
        is False,
        not _bad(
            RiskRoot.enable,
            tenant_id="t1",
            risk_ref="r1",
            present=False,
        )
        and RiskRoot.enable(
            tenant_id="t1", risk_ref="r2"
        ).is_missing()
        is False,
        not _bad(
            PolicyRoot.enable,
            tenant_id="t1",
            policy_ref="pol1",
            present=False,
        )
        and PolicyRoot.enable(
            tenant_id="t1", policy_ref="pol2"
        ).is_missing()
        is False,
        not _bad(
            CertificationRoot.enable,
            tenant_id="t1",
            certification_ref="cert1",
            present=False,
        )
        and CertificationRoot.enable(
            tenant_id="t1", certification_ref="cert2"
        ).is_missing()
        is False,
        not _bad(
            TrustDigitalTwinRoot.enable,
            tenant_id="t1",
            twin_ref="tw1",
            present=False,
        )
        and TrustDigitalTwinRoot.enable(
            tenant_id="t1", twin_ref="tw2"
        ).is_missing()
        is False,
    ]
    aggregates_ok = all(checks)

    acl_path = root / "backend/contexts/ai/infrastructure/acl/ai_aitrust_acl.py"
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
        and "via_audit_platform" in acl_text
        and "via_policy_engine" in acl_text
        and "via_workflow_engine" in acl_text
        and "via_p214_d" in acl_text
        and "via_p214_e" in acl_text
        and "via_p214_f" in acl_text
        and "via_p214_g" in acl_text
        and "via_p214_h" in acl_text
        and "via_p214_i" in acl_text
        and "via_p214_j" in acl_text
        and "via_p214_l" in acl_text
        and "via_p214_o" in acl_text
        and "module_local_ai_governance_forbidden" in acl_text
    )

    router = (
        root / "backend/contexts/ai/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@router.get("/aitrust")' in router
        and "/aitrust/readiness" in router
        and "/aitrust/compliance" in router
        and "/aitrust/audit" in router
        and "/aitrust/trust" in router
        and "/aitrust/explainability" in router
        and "/aitrust/digital-twin" in router
    )

    law = (root / "docs/architecture/ENTERPRISE_AI_AITRUST.md").read_text(
        encoding="utf-8"
    )
    doc_ok = (
        "Never Enterprise AI Governance Platform is missing" in law
        and "Never AI Compliance Platform is missing" in law
        and "Never AI Audit Platform is missing" in law
        and "Never AI Trust Platform is missing" in law
        and "Never AI Risk Management is missing" in law
        and "Never AI Policy Management is missing" in law
        and "Never AI Transparency is missing" in law
        and "Never AI Explainability Governance is missing" in law
        and "Never Regulatory Intelligence is missing" in law
        and "Never Certification Platform is missing" in law
        and "Never Governance Knowledge Graph is missing" in law
        and "Never Governance Digital Twin is missing" in law
        and "Never CQRS architecture is missing" in law
        and "Never Event architecture is missing" in law
        and "Never Microservices architecture is missing" in law
        and "Never API first architecture is missing" in law
        and "Never Zero trust security is missing" in law
        and "Never Cloud native deployment is missing" in law
        and "Never Sibling AI BC" in law
        and "MEOS Continuous AI Trust Fabric" in law
        and "continuous intelligent trust management" in law
        and "P214-H" in law
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
        "prompt": "P214-P",
        "adr": 436,
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
