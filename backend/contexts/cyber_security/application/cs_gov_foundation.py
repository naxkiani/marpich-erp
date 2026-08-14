"""Cyber Security P210-M AI Governance foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/373-enterprise-cyber-security-ai-governance.md",
    "docs/architecture/ENTERPRISE_CYBER_SECURITY_AI_GOVERNANCE.md",
    "docs/architecture/cyber_security/CYBER_GOV_CAPABILITIES.v1.yaml",
    "docs/architecture/cyber_security/CYBER_GOV_DDD_CQRS.v1.yaml",
    "docs/architecture/cyber_security/CYBER_GOV_SECURITY.v1.yaml",
    "docs/architecture/cyber_security/CYBER_GOV_VALIDATION.v1.yaml",
    "backend/contexts/cyber_security/domain/services/cs_platform_gov.py",
    "backend/contexts/cyber_security/domain/aggregates/cs_gov_aggregates.py",
    "backend/contexts/cyber_security/infrastructure/acl/cs_gov_acl.py",
    "backend/contexts/cyber_security/application/cs_gov_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/ai_governance",
    "backend/contexts/ai_compliance",
    "backend/contexts/responsible_ai",
    "backend/contexts/ai_ops",
    "backend/contexts/cyber_ops",
)


def validate_cs_gov_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.cyber_security.domain.aggregates.cs_gov_aggregates import (
        CsGovAgentGovernanceRoot,
        CsGovAiInventoryRoot,
        CsGovAuditableDecisionRoot,
        CsGovComplianceEvidenceRoot,
        CsGovHumanOversightRoot,
        CsGovMeasurableRiskRoot,
        CsGovModelRegisteredRoot,
        CsGovPolicyEnforcementRoot,
    )
    from contexts.cyber_security.domain.services import cs_platform_gov as gov

    cat = gov.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P210-M"
        and cat.get("adr") == 373
        and cat.get("sor") == "cyber_security"
        and cat["ai_models_inventoried_required"] is True
        and cat["ai_decisions_auditable_required"] is True
        and cat["ai_risks_measurable_required"] is True
        and cat["ai_agents_governed_required"] is True
        and cat["policies_enforceable_required"] is True
        and cat["compliance_evidence_generatable_required"] is True
        and cat["human_oversight_required"] is True
        and cat["module_local_llm_sdk_forbidden"] is True
        and cat["inventory"]["not_uninventoried"] is True
        and cat["risk_management"]["not_unmeasurable"] is True
        and cat["agent_governance"]["not_ungoverned"] is True
        and cat["policy_engine"]["not_unenforceable"] is True
        and cat["compliance"]["not_ungeneratable"] is True
        and cat["human_oversight"]["not_unavailable"] is True
        and cat["architecture"]["layer_count"] >= 8
        and cat["inventory"]["asset_count"] >= 10
        and cat["cqrs"]["event_count"] >= 8
        and cat["cursor_outputs"]["count"] >= 20
        and "ai_models_cannot_be_inventoried" in cat["quality_gates"]["reject_if"]
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )

    def _bad(fn, **kwargs):
        try:
            fn(**kwargs)
            return True
        except ValueError:
            return False

    checks = []
    checks.append(
        not _bad(
            CsGovAiInventoryRoot.register,
            tenant_id="t1",
            model_ref="m1",
            inventoried=False,
        )
        and CsGovAiInventoryRoot.register(
            tenant_id="t1", model_ref="m2"
        ).is_uninventoried()
        is False
    )
    checks.append(
        not _bad(
            CsGovAuditableDecisionRoot.audit,
            tenant_id="t1",
            decision_ref="d1",
            auditable=False,
        )
        and CsGovAuditableDecisionRoot.audit(
            tenant_id="t1", decision_ref="d2"
        ).is_unauditable()
        is False
    )
    checks.append(
        not _bad(
            CsGovMeasurableRiskRoot.assess,
            tenant_id="t1",
            risk_ref="r1",
            measurable=False,
        )
        and CsGovMeasurableRiskRoot.assess(
            tenant_id="t1", risk_ref="r2"
        ).is_unmeasurable()
        is False
    )
    checks.append(
        not _bad(
            CsGovAgentGovernanceRoot.govern,
            tenant_id="t1",
            agent_ref="a1",
            governed=False,
        )
        and CsGovAgentGovernanceRoot.govern(
            tenant_id="t1", agent_ref="a2"
        ).is_ungoverned()
        is False
    )
    checks.append(
        not _bad(
            CsGovPolicyEnforcementRoot.enforce,
            tenant_id="t1",
            policy_ref="p1",
            enforceable=False,
        )
        and CsGovPolicyEnforcementRoot.enforce(
            tenant_id="t1", policy_ref="p2"
        ).is_unenforceable()
        is False
    )
    checks.append(
        not _bad(
            CsGovComplianceEvidenceRoot.generate,
            tenant_id="t1",
            evidence_ref="e1",
            generatable=False,
        )
        and CsGovComplianceEvidenceRoot.generate(
            tenant_id="t1", evidence_ref="e2"
        ).is_ungeneratable()
        is False
    )
    checks.append(
        not _bad(
            CsGovHumanOversightRoot.require,
            tenant_id="t1",
            gate_ref="g1",
            available=False,
        )
        and CsGovHumanOversightRoot.require(
            tenant_id="t1", gate_ref="g2"
        ).is_unavailable()
        is False
    )
    approved = CsGovModelRegisteredRoot.approve(
        tenant_id="t1", model_ref="m3"
    )
    checks.append("AIModelApproved" in approved.pending_events)
    aggregates_ok = all(checks)

    acl_path = root / "backend/contexts/cyber_security/infrastructure/acl/cs_gov_acl.py"
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_enterprise_ai_platform" in acl_text
        and "via_policy_engine" in acl_text
        and "human_oversight_required" in acl_text
        and "compliance_evidence_generatable_required" in acl_text
        and "ai_decisions_auditable_required" in acl_text
    )

    router = (
        root / "backend/contexts/cyber_security/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@cyber_security_router.get("/gov")' in router
        and "/gov/inventory" in router
        and "/gov/policies" in router
        and "/gov/compliance" in router
        and "/gov/readiness" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_CYBER_SECURITY_AI_GOVERNANCE.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never AI models cannot be inventoried" in law
        and "Never AI decisions cannot be audited" in law
        and "Never AI risks cannot be measured" in law
        and "Never AI agents operate without governance" in law
        and "Never policies cannot be enforced" in law
        and "Never compliance evidence cannot be generated" in law
        and "Never human oversight is unavailable" in law
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
        "prompt": "P210-M",
        "adr": 373,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "catalog": catalog_ok,
        "aggregates": aggregates_ok,
        "acl": acl_ok,
        "router": router_ok,
        "documentation": doc_ok,
        "sor": "cyber_security",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
