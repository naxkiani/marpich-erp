"""Data Governance P212-H Data Policies foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/401-enterprise-data-governance-data-policies.md",
    "docs/architecture/ENTERPRISE_DATA_GOVERNANCE_DATA_POLICIES.md",
    "docs/architecture/data_governance/DATA_GOVERNANCE_POLICIES_CAPABILITIES.v1.yaml",
    "docs/architecture/data_governance/DATA_GOVERNANCE_POLICIES_DDD_CQRS.v1.yaml",
    "docs/architecture/data_governance/DATA_GOVERNANCE_POLICIES_SECURITY.v1.yaml",
    "docs/architecture/data_governance/DATA_GOVERNANCE_POLICIES_VALIDATION.v1.yaml",
    "backend/contexts/data_governance/domain/services/dg_platform_policies.py",
    "backend/contexts/data_governance/domain/aggregates/dg_policy_aggregates.py",
    "backend/contexts/data_governance/infrastructure/acl/dg_policy_acl.py",
    "backend/contexts/data_governance/application/dg_policy_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/data_policy_platform",
    "backend/contexts/governance_automation_platform",
    "backend/contexts/data_mesh",
    "backend/contexts/data_product_platform",
    "backend/contexts/data_marketplace",
    "backend/contexts/metadata_governance_platform",
)


def validate_dg_policy_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.data_governance.domain.aggregates.dg_policy_aggregates import (
        DgPolicyArchitectureRoot,
        DgPolicyLifecycleRoot,
        DgPolicyRuleEngineRoot,
        DgGovernanceAutomationRoot,
        DgPolicyIntelligenceRoot,
        DgAiGovernanceRoot,
        DgPolicyKnowledgeGraphRoot,
        DgPolicyDigitalTwinRoot,
        DgPolicyCqrsRoot,
        DgPolicyEventSourcingRoot,
        DgPolicyMicroservicesRoot,
        DgPolicyZeroTrustRoot,
        DgPolicyScalabilityRoot,
    )
    from contexts.data_governance.domain.services import (
        dg_platform_policies as pol,
    )

    cat = pol.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P212-H"
        and cat.get("adr") == 401
        and cat.get("sor") == "data_governance"
        and cat.get("capability") == "CAP-PLT-DG-001"
        and cat["data_policy_architecture_complete_required"] is True
        and cat["policy_lifecycle_management_present_required"] is True
        and cat["policy_rule_engine_present_required"] is True
        and cat["governance_automation_present_required"] is True
        and cat["policy_intelligence_present_required"] is True
        and cat["ai_governance_integration_present_required"] is True
        and cat["knowledge_graph_integration_present_required"] is True
        and cat["digital_twin_integration_present_required"] is True
        and cat["cqrs_architecture_present_required"] is True
        and cat["event_sourcing_architecture_present_required"] is True
        and cat["microservices_architecture_present_required"] is True
        and cat["zero_trust_alignment_present_required"] is True
        and cat["enterprise_scalability_present_required"] is True
        and cat["policy_architecture"]["not_incomplete"] is True
        and cat["policy_lifecycle"]["not_missing"] is True
        and cat["policy_rule_engine"]["not_missing"] is True
        and cat["governance_automation"]["not_missing"] is True
        and cat["policy_intelligence"]["not_missing"] is True
        and cat["ai_governance"]["not_missing"] is True
        and cat["knowledge_graph"]["not_missing"] is True
        and cat["digital_twin"]["not_missing"] is True
        and cat["cqrs"]["not_missing"] is True
        and cat["event_sourcing"]["not_missing"] is True
        and cat["microservices"]["not_missing"] is True
        and cat["zero_trust"]["not_missing"] is True
        and cat["scalability"]["not_missing"] is True
        and cat["policy_architecture"]["bc_count"] >= 5
        and cat["policy_lifecycle"]["stage_count"] >= 8
        and cat["policy_framework"]["category_count"] >= 6
        and cat["policy_rule_engine"]["via_policy_engine"] is True
        and cat["governance_automation"]["step_count"] >= 5
        and cat["microservices"]["service_count"] >= 6
        and cat["cqrs"]["event_count"] >= 7
        and cat["cursor_outputs"]["count"] >= 18
        and (
            "data_policy_architecture_is_incomplete"
            in cat["quality_gates"]["reject_if"]
        )
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
            DgPolicyArchitectureRoot.publish,
            tenant_id="t1",
            architecture_ref="r0",
            complete=False,
        )
        and DgPolicyArchitectureRoot.publish(
            tenant_id="t1", architecture_ref="ok0"
        ).is_incomplete()
        is False
    )
    checks.append(
        not _bad(
            DgPolicyLifecycleRoot.enable,
            tenant_id="t1",
            lifecycle_ref="r1",
            present=False,
        )
        and DgPolicyLifecycleRoot.enable(
            tenant_id="t1", lifecycle_ref="ok1"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgPolicyRuleEngineRoot.enable,
            tenant_id="t1",
            engine_ref="r2",
            present=False,
        )
        and DgPolicyRuleEngineRoot.enable(
            tenant_id="t1", engine_ref="ok2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgGovernanceAutomationRoot.enable,
            tenant_id="t1",
            automation_ref="r3",
            present=False,
        )
        and DgGovernanceAutomationRoot.enable(
            tenant_id="t1", automation_ref="ok3"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgPolicyIntelligenceRoot.enable,
            tenant_id="t1",
            intel_ref="r4",
            present=False,
        )
        and DgPolicyIntelligenceRoot.enable(
            tenant_id="t1", intel_ref="ok4"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgAiGovernanceRoot.enable,
            tenant_id="t1",
            ai_ref="r5",
            present=False,
        )
        and DgAiGovernanceRoot.enable(
            tenant_id="t1", ai_ref="ok5"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgPolicyKnowledgeGraphRoot.integrate,
            tenant_id="t1",
            graph_ref="r6",
            present=False,
        )
        and DgPolicyKnowledgeGraphRoot.integrate(
            tenant_id="t1", graph_ref="ok6"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgPolicyDigitalTwinRoot.integrate,
            tenant_id="t1",
            twin_ref="r7",
            present=False,
        )
        and DgPolicyDigitalTwinRoot.integrate(
            tenant_id="t1", twin_ref="ok7"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgPolicyCqrsRoot.align,
            tenant_id="t1",
            cqrs_ref="r8",
            present=False,
        )
        and DgPolicyCqrsRoot.align(
            tenant_id="t1", cqrs_ref="ok8"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgPolicyEventSourcingRoot.enable,
            tenant_id="t1",
            es_ref="r9",
            present=False,
        )
        and DgPolicyEventSourcingRoot.enable(
            tenant_id="t1", es_ref="ok9"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgPolicyMicroservicesRoot.declare,
            tenant_id="t1",
            ms_ref="r10",
            present=False,
        )
        and DgPolicyMicroservicesRoot.declare(
            tenant_id="t1", ms_ref="ok10"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgPolicyZeroTrustRoot.confirm,
            tenant_id="t1",
            zt_ref="r11",
            present=False,
        )
        and DgPolicyZeroTrustRoot.confirm(
            tenant_id="t1", zt_ref="ok11"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgPolicyScalabilityRoot.confirm,
            tenant_id="t1",
            scale_ref="r12",
            present=False,
        )
        and DgPolicyScalabilityRoot.confirm(
            tenant_id="t1", scale_ref="ok12"
        ).is_missing()
        is False
    )
    aggregates_ok = all(checks)

    acl_path = (
        root
        / "backend/contexts/data_governance/infrastructure/acl/dg_policy_acl.py"
    )
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_p212_d" in acl_text
        and "via_p212_e" in acl_text
        and "via_p212_f" in acl_text
        and "via_p212_g" in acl_text
        and "via_policy_engine" in acl_text
        and "via_p208" in acl_text
        and "ai_governance_integration_present_required" in acl_text
        and "via_workflow" in acl_text
        and "module_local_pdp_forbidden" in acl_text
    )

    router = (
        root / "backend/contexts/data_governance/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@data_governance_router.get("/policies")' in router
        and "/policies/lifecycle" in router
        and "/policies/rules" in router
        and "/policies/automation" in router
        and "/policies/readiness" in router
    )

    law = (
        root
        / "docs/architecture/ENTERPRISE_DATA_GOVERNANCE_DATA_POLICIES.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never Data policy architecture is incomplete" in law
        and "Never Policy lifecycle management is missing" in law
        and "Never Policy rule engine is missing" in law
        and "Never Governance automation is missing" in law
        and "Never Policy intelligence is missing" in law
        and "Never AI governance integration is missing" in law
        and "Never Knowledge graph integration is missing" in law
        and "Never Digital twin integration is missing" in law
        and "Never CQRS architecture is missing" in law
        and "Never Event sourcing architecture is missing" in law
        and "Never Microservices architecture is missing" in law
        and "Never Zero trust alignment is missing" in law
        and "Never Enterprise scalability is missing" in law
        and "Never Sibling data policy BC" in law
        and (
            "Enterprise data governance SHALL become policy driven,"
            in law
        )
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
        "prompt": "P212-H",
        "adr": 401,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "catalog": catalog_ok,
        "aggregates": aggregates_ok,
        "acl": acl_ok,
        "router": router_ok,
        "documentation": doc_ok,
        "sor": "data_governance",
        "capability": "CAP-PLT-DG-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
