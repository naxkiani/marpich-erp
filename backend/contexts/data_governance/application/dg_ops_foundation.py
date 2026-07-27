"""Data Governance P212-M Ops foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/405-enterprise-data-governance-ops.md",
    "docs/architecture/ENTERPRISE_DATA_GOVERNANCE_OPS.md",
    "docs/architecture/data_governance/DATA_GOVERNANCE_OPS_CAPABILITIES.v1.yaml",
    "docs/architecture/data_governance/DATA_GOVERNANCE_OPS_DDD_CQRS.v1.yaml",
    "docs/architecture/data_governance/DATA_GOVERNANCE_OPS_SECURITY.v1.yaml",
    "docs/architecture/data_governance/DATA_GOVERNANCE_OPS_VALIDATION.v1.yaml",
    "backend/contexts/data_governance/domain/services/dg_platform_ops.py",
    "backend/contexts/data_governance/domain/aggregates/dg_ops_aggregates.py",
    "backend/contexts/data_governance/infrastructure/acl/dg_ops_acl.py",
    "backend/contexts/data_governance/application/dg_ops_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/data_governance_ops",
    "backend/contexts/dg_event_bus",
    "backend/contexts/governance_api_platform",
    "backend/contexts/data_mesh",
    "backend/contexts/data_marketplace",
    "backend/contexts/metadata_governance_platform",
)


def validate_dg_ops_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.data_governance.domain.aggregates.dg_ops_aggregates import (
        DgOpsCqrsRoot,
        DgOpsCommandSideRoot,
        DgOpsQuerySideRoot,
        DgOpsEventSourcingRoot,
        DgOpsEventBusRoot,
        DgOpsEventContractsRoot,
        DgOpsMicroservicesRoot,
        DgOpsApiFirstRoot,
        DgOpsHexagonalRoot,
        DgOpsDgIntegrationRoot,
        DgOpsAiIntegrationRoot,
        DgOpsTwinIntegrationRoot,
        DgOpsMultiTenantRoot,
        DgOpsObservabilityRoot,
        DgOpsScalabilityRoot,
    )
    from contexts.data_governance.domain.services import dg_platform_ops as ops

    cat = ops.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P212-M"
        and cat.get("adr") == 405
        and cat.get("sor") == "data_governance"
        and cat.get("capability") == "CAP-PLT-DG-001"
        and cat["cqrs_architecture_complete_required"] is True
        and cat["command_side_design_present_required"] is True
        and cat["query_side_design_present_required"] is True
        and cat["event_sourcing_architecture_present_required"] is True
        and cat["event_bus_architecture_present_required"] is True
        and cat["event_contract_governance_present_required"] is True
        and cat["microservice_architecture_present_required"] is True
        and cat["api_first_architecture_present_required"] is True
        and cat["hexagonal_architecture_present_required"] is True
        and cat["data_governance_integration_present_required"] is True
        and cat["ai_governance_integration_present_required"] is True
        and cat["digital_twin_integration_present_required"] is True
        and cat["multi_tenant_architecture_present_required"] is True
        and cat["observability_architecture_present_required"] is True
        and cat["enterprise_scalability_present_required"] is True
        and cat["cqrs_architecture"]["not_incomplete"] is True
        and cat["command_side"]["not_missing"] is True
        and cat["query_side"]["not_missing"] is True
        and cat["event_sourcing"]["not_missing"] is True
        and cat["event_bus"]["not_missing"] is True
        and cat["event_contracts"]["not_missing"] is True
        and cat["microservices"]["not_missing"] is True
        and cat["api_first"]["not_missing"] is True
        and cat["hexagonal"]["not_missing"] is True
        and cat["data_governance_integration"]["not_missing"] is True
        and cat["ai_governance_integration"]["not_missing"] is True
        and cat["digital_twin_integration"]["not_missing"] is True
        and cat["multi_tenant"]["not_missing"] is True
        and cat["observability"]["not_missing"] is True
        and cat["scalability"]["not_missing"] is True
        and cat["command_side"]["category_count"] >= 5
        and cat["query_side"]["read_model_count"] >= 7
        and cat["microservices"]["service_count"] >= 11
        and cat["event_sourcing"]["event_count"] >= 4
        and cat["hexagonal"]["layer_count"] >= 5
        and cat["cursor_outputs"]["count"] >= 18
        and cat["event_bus"]["via_enterprise_event_bus"] is True
        and cat["api_first"]["via_api_gateway"] is True
        and (
            "cqrs_architecture_is_incomplete"
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
            DgOpsCqrsRoot.publish,
            tenant_id="t1",
            cqrs_ref="r0",
            complete=False,
        )
        and DgOpsCqrsRoot.publish(
            tenant_id="t1", cqrs_ref="ok0"
        ).is_incomplete()
        is False
    )
    checks.append(
        not _bad(
            DgOpsCommandSideRoot.define,
            tenant_id="t1",
            command_ref="r1",
            present=False,
        )
        and DgOpsCommandSideRoot.define(
            tenant_id="t1", command_ref="ok1"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgOpsQuerySideRoot.define,
            tenant_id="t1",
            query_ref="r2",
            present=False,
        )
        and DgOpsQuerySideRoot.define(
            tenant_id="t1", query_ref="ok2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgOpsEventSourcingRoot.enable,
            tenant_id="t1",
            es_ref="r3",
            present=False,
        )
        and DgOpsEventSourcingRoot.enable(
            tenant_id="t1", es_ref="ok3"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgOpsEventBusRoot.enable,
            tenant_id="t1",
            bus_ref="r4",
            present=False,
        )
        and DgOpsEventBusRoot.enable(
            tenant_id="t1", bus_ref="ok4"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgOpsEventContractsRoot.enable,
            tenant_id="t1",
            contract_ref="r5",
            present=False,
        )
        and DgOpsEventContractsRoot.enable(
            tenant_id="t1", contract_ref="ok5"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgOpsMicroservicesRoot.declare,
            tenant_id="t1",
            ms_ref="r6",
            present=False,
        )
        and DgOpsMicroservicesRoot.declare(
            tenant_id="t1", ms_ref="ok6"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgOpsApiFirstRoot.confirm,
            tenant_id="t1",
            api_ref="r7",
            present=False,
        )
        and DgOpsApiFirstRoot.confirm(
            tenant_id="t1", api_ref="ok7"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgOpsHexagonalRoot.align,
            tenant_id="t1",
            hex_ref="r8",
            present=False,
        )
        and DgOpsHexagonalRoot.align(
            tenant_id="t1", hex_ref="ok8"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgOpsDgIntegrationRoot.integrate,
            tenant_id="t1",
            integ_ref="r9",
            present=False,
        )
        and DgOpsDgIntegrationRoot.integrate(
            tenant_id="t1", integ_ref="ok9"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgOpsAiIntegrationRoot.integrate,
            tenant_id="t1",
            ai_ref="r10",
            present=False,
        )
        and DgOpsAiIntegrationRoot.integrate(
            tenant_id="t1", ai_ref="ok10"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgOpsTwinIntegrationRoot.integrate,
            tenant_id="t1",
            twin_ref="r11",
            present=False,
        )
        and DgOpsTwinIntegrationRoot.integrate(
            tenant_id="t1", twin_ref="ok11"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgOpsMultiTenantRoot.confirm,
            tenant_id="t1",
            tenant_ref="r12",
            present=False,
        )
        and DgOpsMultiTenantRoot.confirm(
            tenant_id="t1", tenant_ref="ok12"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgOpsObservabilityRoot.enable,
            tenant_id="t1",
            obs_ref="r13",
            present=False,
        )
        and DgOpsObservabilityRoot.enable(
            tenant_id="t1", obs_ref="ok13"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgOpsScalabilityRoot.confirm,
            tenant_id="t1",
            scale_ref="r14",
            present=False,
        )
        and DgOpsScalabilityRoot.confirm(
            tenant_id="t1", scale_ref="ok14"
        ).is_missing()
        is False
    )
    aggregates_ok = all(checks)

    acl_path = (
        root
        / "backend/contexts/data_governance/infrastructure/acl/dg_ops_acl.py"
    )
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_enterprise_event_bus" in acl_text
        and "via_api_gateway" in acl_text
        and "via_p212_j" in acl_text
        and "via_p212_k" in acl_text
        and "via_p212_l" in acl_text
        and "via_p208" in acl_text
        and "module_local_broker_forbidden" in acl_text
        and "digital_twin_integration_present_required" in acl_text
    )

    router = (
        root / "backend/contexts/data_governance/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@data_governance_router.get("/ops")' in router
        and "/ops/commands" in router
        and "/ops/events" in router
        and "/ops/microservices" in router
        and "/ops/readiness" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_DATA_GOVERNANCE_OPS.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never CQRS architecture is incomplete" in law
        and "Never Command side design is missing" in law
        and "Never Query side design is missing" in law
        and "Never Event sourcing architecture is missing" in law
        and "Never Event bus architecture is missing" in law
        and "Never Event contract governance is missing" in law
        and "Never Microservice architecture is missing" in law
        and "Never API first architecture is missing" in law
        and "Never Hexagonal architecture is missing" in law
        and "Never Data governance integration is missing" in law
        and "Never AI governance integration is missing" in law
        and "Never Digital twin integration is missing" in law
        and "Never Multi tenant architecture is missing" in law
        and "Never Observability architecture is missing" in law
        and "Never Enterprise scalability is missing" in law
        and "Never Sibling data governance ops BC" in law
        and (
            "Enterprise governance decisions SHALL be separated"
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
        "prompt": "P212-M",
        "adr": 405,
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
