"""Quantum P215-K Governance foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/403-enterprise-quantum-governance.md",
    "docs/architecture/ENTERPRISE_QUANTUM_GOVERNANCE.md",
    "docs/architecture/quantum/QUANTUM_GOVERNANCE_CAPABILITIES.v1.yaml",
    "docs/architecture/quantum/QUANTUM_GOVERNANCE_DDD_CQRS.v1.yaml",
    "docs/architecture/quantum/QUANTUM_GOVERNANCE_SECURITY.v1.yaml",
    "docs/architecture/quantum/QUANTUM_GOVERNANCE_VALIDATION.v1.yaml",
    "docs/architecture/quantum/P215_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/quantum/domain/services/qc_platform_governance.py",
    "backend/contexts/quantum/domain/aggregates/qc_governance_aggregates.py",
    "backend/contexts/quantum/infrastructure/acl/qc_governance_acl.py",
    "backend/contexts/quantum/application/qc_governance_foundation.py",
    "backend/contexts/quantum/context.yaml",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/quantum_governance",
    "backend/contexts/quantum_ethics_platform",
    "backend/contexts/quantum_regulation_platform",
    "backend/contexts/responsible_quantum_platform",
    "backend/contexts/quantum_compliance_platform",
    "backend/contexts/quantum_risk_platform",
    "backend/contexts/quantum_audit_platform",
)


def validate_qc_governance_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.quantum.domain.aggregates.qc_governance_aggregates import (
        QcGovernancePlatformRoot,
        QcRegulatoryIntelligenceRoot,
        QcResponsibleQuantumRoot,
        QcEthicsFrameworkRoot,
        QcRiskManagementRoot,
        QcComplianceAutomationRoot,
        QcAuditIntelligenceRoot,
        QcAccountabilityRoot,
        QcKnowledgeGraphRoot,
        QcDigitalTwinRoot,
        QcCqrsRoot,
        QcEventArchitectureRoot,
        QcMicroservicesRoot,
        QcApiFirstRoot,
        QcCloudNativeRoot,
    )
    from contexts.quantum.domain.services import qc_platform_governance as gov

    cat = gov.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P215-K"
        and cat.get("adr") == 403
        and cat.get("sor") == "quantum"
        and cat.get("capability") == "CAP-PLT-QC-001"
        and cat["quantum_governance_platform_complete_required"] is True
        and cat["quantum_regulatory_intelligence_present_required"] is True
        and cat["responsible_quantum_computing_present_required"] is True
        and cat["quantum_ethics_framework_present_required"] is True
        and cat["quantum_risk_management_present_required"] is True
        and cat["quantum_compliance_automation_present_required"] is True
        and cat["quantum_audit_intelligence_present_required"] is True
        and cat["accountability_framework_present_required"] is True
        and cat["knowledge_graph_integration_present_required"] is True
        and cat["digital_twin_integration_present_required"] is True
        and cat["cqrs_architecture_present_required"] is True
        and cat["event_architecture_present_required"] is True
        and cat["microservices_architecture_present_required"] is True
        and cat["api_first_architecture_present_required"] is True
        and cat["cloud_native_governance_present_required"] is True
        and cat["governance_platform"]["not_incomplete"] is True
        and cat["regulatory_intelligence"]["not_missing"] is True
        and cat["responsible_quantum"]["not_missing"] is True
        and cat["ethics_framework"]["not_missing"] is True
        and cat["risk_management"]["not_missing"] is True
        and cat["compliance_automation"]["not_missing"] is True
        and cat["audit_intelligence"]["not_missing"] is True
        and cat["accountability_framework"]["not_missing"] is True
        and cat["knowledge_graph"]["not_missing"] is True
        and cat["digital_twin"]["not_missing"] is True
        and cat["cqrs"]["not_missing"] is True
        and cat["event_architecture"]["not_missing"] is True
        and cat["microservices"]["not_missing"] is True
        and cat["apis"]["not_missing"] is True
        and cat["cloud_native"]["not_missing"] is True
        and cat["governance_platform"]["bc_count"] >= 7
        and cat["policy_management"]["category_count"] >= 6
        and cat["risk_management"]["risk_type_count"] >= 6
        and cat["microservices"]["service_count"] >= 11
        and cat["cqrs"]["event_count"] >= 6
        and cat["cursor_outputs"]["count"] >= 16
        and cat["policy_management"]["via_policy_engine"] is True
        and cat["audit_intelligence"]["module_local_audit_ledger_forbidden"] is True
        and (
            "quantum_governance_platform_is_incomplete"
            in cat["quality_gates"]["reject_if"]
        )
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
        and cat.get("fabric") == "meos_quantum_responsible_intelligence_fabric"
        and cat.get("builds_on_p215_a_through_j") is True
        and all(x in cat.get("builds_on", []) for x in (
            "P215-A", "P215-B", "P215-C", "P215-D", "P215-E", "P215-F",
            "P215-G", "P215-H", "P215-I", "P215-J", "P214-H", "P214-Y",
        ))
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
            QcGovernancePlatformRoot.publish,
            tenant_id="t1",
            platform_ref="r0",
            complete=False,
        )
        and QcGovernancePlatformRoot.publish(
            tenant_id="t1", platform_ref="ok0"
        ).is_incomplete()
        is False
    )
    checks.append(
        not _bad(
            QcRegulatoryIntelligenceRoot.enable,
            tenant_id="t1",
            regulation_ref="r1",
            present=False,
        )
        and QcRegulatoryIntelligenceRoot.enable(
            tenant_id="t1", regulation_ref="ok1"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            QcResponsibleQuantumRoot.enable,
            tenant_id="t1",
            responsible_ref="r2",
            present=False,
        )
        and QcResponsibleQuantumRoot.enable(
            tenant_id="t1", responsible_ref="ok2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            QcEthicsFrameworkRoot.enable,
            tenant_id="t1",
            ethics_ref="r3",
            present=False,
        )
        and QcEthicsFrameworkRoot.enable(
            tenant_id="t1", ethics_ref="ok3"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            QcRiskManagementRoot.enable,
            tenant_id="t1",
            risk_ref="r4",
            present=False,
        )
        and QcRiskManagementRoot.enable(
            tenant_id="t1", risk_ref="ok4"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            QcComplianceAutomationRoot.enable,
            tenant_id="t1",
            compliance_ref="r5",
            present=False,
        )
        and QcComplianceAutomationRoot.enable(
            tenant_id="t1", compliance_ref="ok5"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            QcAuditIntelligenceRoot.enable,
            tenant_id="t1",
            audit_ref="r6",
            present=False,
        )
        and QcAuditIntelligenceRoot.enable(
            tenant_id="t1", audit_ref="ok6"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            QcAccountabilityRoot.enable,
            tenant_id="t1",
            accountability_ref="r7",
            present=False,
        )
        and QcAccountabilityRoot.enable(
            tenant_id="t1", accountability_ref="ok7"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            QcKnowledgeGraphRoot.integrate,
            tenant_id="t1",
            graph_ref="r8",
            present=False,
        )
        and QcKnowledgeGraphRoot.integrate(
            tenant_id="t1", graph_ref="ok8"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            QcDigitalTwinRoot.integrate,
            tenant_id="t1",
            twin_ref="r9",
            present=False,
        )
        and QcDigitalTwinRoot.integrate(
            tenant_id="t1", twin_ref="ok9"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            QcCqrsRoot.align,
            tenant_id="t1",
            cqrs_ref="r10",
            present=False,
        )
        and QcCqrsRoot.align(
            tenant_id="t1", cqrs_ref="ok10"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            QcEventArchitectureRoot.enable,
            tenant_id="t1",
            es_ref="r11",
            present=False,
        )
        and QcEventArchitectureRoot.enable(
            tenant_id="t1", es_ref="ok11"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            QcMicroservicesRoot.declare,
            tenant_id="t1",
            ms_ref="r12",
            present=False,
        )
        and QcMicroservicesRoot.declare(
            tenant_id="t1", ms_ref="ok12"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            QcApiFirstRoot.confirm,
            tenant_id="t1",
            api_ref="r13",
            present=False,
        )
        and QcApiFirstRoot.confirm(
            tenant_id="t1", api_ref="ok13"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            QcCloudNativeRoot.confirm,
            tenant_id="t1",
            cloud_ref="r14",
            present=False,
        )
        and QcCloudNativeRoot.confirm(
            tenant_id="t1", cloud_ref="ok14"
        ).is_missing()
        is False
    )
    aggregates_ok = all(checks)

    acl_path = (
        root
        / "backend/contexts/quantum/infrastructure/acl/qc_governance_acl.py"
    )
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_p209" in acl_text
        and "via_p210" in acl_text
        and "via_p212" in acl_text
        and "via_policy_engine" in acl_text
        and "via_audit" in acl_text
        and "via_ai_governance" in acl_text
        and "pqc_remains_secrets" in acl_text
        and "module_local_pdp_forbidden" in acl_text
        and "human_oversight_required" in acl_text
        and "via_p214_h" in acl_text
        and "via_p214_y" in acl_text
        and "via_p215_a" in acl_text
        and "via_p215_j" in acl_text
        and "module_local_quantum_governance_forbidden" in acl_text
    )

    router = (
        root / "backend/contexts/quantum/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@quantum_router.get("/governance")' in router
        and "/governance/policies" in router
        and "/governance/ethics" in router
        and "/governance/compliance" in router
        and "/governance/readiness" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_QUANTUM_GOVERNANCE.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never Quantum governance platform is incomplete" in law
        and "Never Quantum regulatory intelligence is missing" in law
        and "Never Responsible quantum computing is missing" in law
        and "Never Quantum ethics framework is missing" in law
        and "Never Quantum risk management is missing" in law
        and "Never Quantum compliance automation is missing" in law
        and "Never Quantum audit intelligence is missing" in law
        and "Never Accountability framework is missing" in law
        and "Never Knowledge graph integration is missing" in law
        and "Never Digital twin integration is missing" in law
        and "Never CQRS architecture is missing" in law
        and "Never Event architecture is missing" in law
        and "Never Microservices architecture is missing" in law
        and "Never API first architecture is missing" in law
        and "Never Cloud native governance is missing" in law
        and "Never Sibling quantum governance BC" in law
        and "MEOS Quantum Governance Platform SHALL ensure that" in law
        and "P215-A" in law
        and "P215-J" in law
        and "MEOS Quantum Responsible Intelligence Fabric" in law
    )

    registry = (root / "backend/contexts/registry.py").read_text(encoding="utf-8")
    registry_ok = 'id="quantum"' in registry and "QUANTUM" in registry

    passed = (
        not missing
        and not sibling
        and catalog_ok
        and aggregates_ok
        and acl_ok
        and router_ok
        and doc_ok
        and registry_ok
    )
    return {
        "prompt": "P215-K",
        "adr": 403,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "catalog": catalog_ok,
        "aggregates": aggregates_ok,
        "acl": acl_ok,
        "router": router_ok,
        "documentation": doc_ok,
        "registry": registry_ok,
        "sor": "quantum",
        "capability": "CAP-PLT-QC-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
