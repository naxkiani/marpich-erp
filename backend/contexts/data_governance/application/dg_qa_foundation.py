"""Data Governance P212-O QA foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/407-enterprise-data-governance-qa.md",
    "docs/architecture/ENTERPRISE_DATA_GOVERNANCE_QA.md",
    "docs/architecture/data_governance/DATA_GOVERNANCE_QA_CAPABILITIES.v1.yaml",
    "docs/architecture/data_governance/DATA_GOVERNANCE_QA_DDD_CQRS.v1.yaml",
    "docs/architecture/data_governance/DATA_GOVERNANCE_QA_SECURITY.v1.yaml",
    "docs/architecture/data_governance/DATA_GOVERNANCE_QA_VALIDATION.v1.yaml",
    "backend/contexts/data_governance/domain/services/dg_platform_qa.py",
    "backend/contexts/data_governance/domain/aggregates/dg_qa_aggregates.py",
    "backend/contexts/data_governance/infrastructure/acl/dg_qa_acl.py",
    "backend/contexts/data_governance/application/dg_qa_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/data_governance_qa",
    "backend/contexts/dg_assurance_platform",
    "backend/contexts/governance_certification_platform",
    "backend/contexts/data_mesh",
    "backend/contexts/data_marketplace",
    "backend/contexts/metadata_governance_platform",
)


def validate_dg_qa_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.data_governance.domain.aggregates.dg_qa_aggregates import (
        DgQaAiQualityRoot,
        DgQaApiFirstRoot,
        DgQaComplianceRoot,
        DgQaContinuousRoot,
        DgQaCqrsRoot,
        DgQaDodRoot,
        DgQaEventSourcingRoot,
        DgQaGovernanceRoot,
        DgQaGraphRoot,
        DgQaMicroservicesRoot,
        DgQaSecurityRoot,
        DgQaTestingRoot,
        DgQaTwinRoot,
    )
    from contexts.data_governance.domain.services import dg_platform_qa as qa

    cat = qa.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P212-O"
        and cat.get("adr") == 407
        and cat.get("sor") == "data_governance"
        and cat.get("capability") == "CAP-PLT-DG-001"
        and cat["complete_enterprise_testing_architecture_present_required"] is True
        and cat["governance_validation_platform_present_required"] is True
        and cat["compliance_automation_present_required"] is True
        and cat["security_assurance_present_required"] is True
        and cat["definition_of_done_engine_present_required"] is True
        and cat["ai_quality_intelligence_present_required"] is True
        and cat["knowledge_graph_integration_present_required"] is True
        and cat["digital_twin_integration_present_required"] is True
        and cat["cqrs_architecture_present_required"] is True
        and cat["event_sourcing_architecture_present_required"] is True
        and cat["microservices_architecture_present_required"] is True
        and cat["api_first_architecture_present_required"] is True
        and cat["continuous_governance_present_required"] is True
        and cat["testing_architecture"]["not_missing"] is True
        and cat["governance_validation"]["not_missing"] is True
        and cat["compliance_automation"]["not_missing"] is True
        and cat["security_assurance"]["not_missing"] is True
        and cat["definition_of_done"]["not_missing"] is True
        and cat["ai_quality_intelligence"]["not_missing"] is True
        and cat["knowledge_graph_integration"]["not_missing"] is True
        and cat["digital_twin_integration"]["not_missing"] is True
        and cat["cqrs_architecture"]["not_missing"] is True
        and cat["event_sourcing"]["not_missing"] is True
        and cat["microservices"]["not_missing"] is True
        and cat["api_first"]["not_missing"] is True
        and cat["continuous_governance"]["not_missing"] is True
        and cat["testing_architecture"]["layer_count"] >= 6
        and cat["governance_validation"]["bc_count"] >= 5
        and cat["ai_quality_intelligence"]["agent_count"] >= 5
        and cat["event_sourcing"]["event_count"] >= 6
        and cat["microservices"]["service_count"] >= 7
        and cat["cursor_outputs"]["count"] >= 19
        and cat["compliance_automation"]["via_compliance_framework"] is True
        and cat["knowledge_graph_integration"]["via_p212_j"] is True
        and cat["digital_twin_integration"]["via_p212_l"] is True
        and cat["deployment_validation"]["via_p212_n"] is True
        and cat["api_first"]["via_api_gateway"] is True
        and (
            "complete_enterprise_testing_architecture_is_missing"
            in cat["quality_gates"]["reject_if"]
        )
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
        and cat["production_readiness"]["checklist"]["p212_series_complete"] is True
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
            DgQaTestingRoot.publish,
            tenant_id="t1",
            testing_ref="r0",
            present=False,
        )
        and DgQaTestingRoot.publish(
            tenant_id="t1", testing_ref="ok0"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgQaGovernanceRoot.enable,
            tenant_id="t1",
            gov_ref="r1",
            present=False,
        )
        and DgQaGovernanceRoot.enable(
            tenant_id="t1", gov_ref="ok1"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgQaComplianceRoot.enable,
            tenant_id="t1",
            compliance_ref="r2",
            present=False,
        )
        and DgQaComplianceRoot.enable(
            tenant_id="t1", compliance_ref="ok2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgQaSecurityRoot.enable,
            tenant_id="t1",
            security_ref="r3",
            present=False,
        )
        and DgQaSecurityRoot.enable(
            tenant_id="t1", security_ref="ok3"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgQaDodRoot.enable,
            tenant_id="t1",
            dod_ref="r4",
            present=False,
        )
        and DgQaDodRoot.enable(
            tenant_id="t1", dod_ref="ok4"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgQaAiQualityRoot.enable,
            tenant_id="t1",
            ai_ref="r5",
            present=False,
        )
        and DgQaAiQualityRoot.enable(
            tenant_id="t1", ai_ref="ok5"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgQaGraphRoot.integrate,
            tenant_id="t1",
            graph_ref="r6",
            present=False,
        )
        and DgQaGraphRoot.integrate(
            tenant_id="t1", graph_ref="ok6"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgQaTwinRoot.integrate,
            tenant_id="t1",
            twin_ref="r7",
            present=False,
        )
        and DgQaTwinRoot.integrate(
            tenant_id="t1", twin_ref="ok7"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgQaCqrsRoot.confirm,
            tenant_id="t1",
            cqrs_ref="r8",
            present=False,
        )
        and DgQaCqrsRoot.confirm(
            tenant_id="t1", cqrs_ref="ok8"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgQaEventSourcingRoot.enable,
            tenant_id="t1",
            es_ref="r9",
            present=False,
        )
        and DgQaEventSourcingRoot.enable(
            tenant_id="t1", es_ref="ok9"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgQaMicroservicesRoot.declare,
            tenant_id="t1",
            ms_ref="r10",
            present=False,
        )
        and DgQaMicroservicesRoot.declare(
            tenant_id="t1", ms_ref="ok10"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgQaApiFirstRoot.confirm,
            tenant_id="t1",
            api_ref="r11",
            present=False,
        )
        and DgQaApiFirstRoot.confirm(
            tenant_id="t1", api_ref="ok11"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgQaContinuousRoot.enable,
            tenant_id="t1",
            continuous_ref="r12",
            present=False,
        )
        and DgQaContinuousRoot.enable(
            tenant_id="t1", continuous_ref="ok12"
        ).is_missing()
        is False
    )
    aggregates_ok = all(checks)

    acl_path = (
        root
        / "backend/contexts/data_governance/infrastructure/acl/dg_qa_acl.py"
    )
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_compliance_framework" in acl_text
        and "via_audit_platform" in acl_text
        and "via_p212_j" in acl_text
        and "via_p212_l" in acl_text
        and "via_p212_n" in acl_text
        and "via_p208" in acl_text
        and "via_enterprise_ai" in acl_text
        and "via_api_gateway" in acl_text
        and "module_local_compliance_tables_forbidden" in acl_text
        and "digital_twin_integration_present_required" in acl_text
    )

    router = (
        root / "backend/contexts/data_governance/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@data_governance_router.get("/qa")' in router
        and "/qa/testing" in router
        and "/qa/compliance" in router
        and "/qa/dod" in router
        and "/qa/readiness" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_DATA_GOVERNANCE_QA.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never Complete enterprise testing architecture is missing" in law
        and "Never Governance validation platform is missing" in law
        and "Never Compliance automation is missing" in law
        and "Never Security assurance is missing" in law
        and "Never Definition of done engine is missing" in law
        and "Never AI quality intelligence is missing" in law
        and "Never Knowledge graph integration is missing" in law
        and "Never Digital twin integration is missing" in law
        and "Never CQRS architecture is missing" in law
        and "Never Event sourcing architecture is missing" in law
        and "Never Microservices architecture is missing" in law
        and "Never API first architecture is missing" in law
        and "Never Continuous governance is missing" in law
        and "Never Sibling data governance qa BC" in law
        and (
            "Enterprise systems SHALL prove their correctness"
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
        "prompt": "P212-O",
        "adr": 407,
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
        "series": "P212",
        "series_complete": passed,
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
