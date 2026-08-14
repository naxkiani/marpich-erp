"""Data Security P211-N CQRS/events/ops foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/389-enterprise-data-security-ops.md",
    "docs/architecture/ENTERPRISE_DATA_SECURITY_OPS.md",
    "docs/architecture/data_security/DATA_SECURITY_OPS_CAPABILITIES.v1.yaml",
    "docs/architecture/data_security/DATA_SECURITY_OPS_DDD_CQRS.v1.yaml",
    "docs/architecture/data_security/DATA_SECURITY_OPS_SECURITY.v1.yaml",
    "docs/architecture/data_security/DATA_SECURITY_OPS_VALIDATION.v1.yaml",
    "backend/contexts/data_security/domain/services/ds_platform_ops.py",
    "backend/contexts/data_security/domain/aggregates/ds_ops_aggregates.py",
    "backend/contexts/data_security/infrastructure/acl/ds_ops_acl.py",
    "backend/contexts/data_security/application/ds_ops_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/data_security_ops",
    "backend/contexts/ds_event_platform",
    "backend/contexts/data_security_microservices",
)


def validate_ds_ops_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.data_security.domain.aggregates.ds_ops_aggregates import (
        DsCompleteAuditHistoryRoot,
        DsEventPublishedRoot,
        DsImmutableEventsRoot,
        DsLooselyCoupledServicesRoot,
        DsManagedApisRoot,
        DsScalablePlatformRoot,
        DsSimulationExecutedRoot,
        DsTraceableSecurityDecisionsRoot,
    )
    from contexts.data_security.domain.services import ds_platform_ops as ops

    cat = ops.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P211-N"
        and cat.get("adr") == 389
        and cat.get("sor") == "data_security"
        and cat["services_loosely_coupled_required"] is True
        and cat["events_immutable_required"] is True
        and cat["apis_managed_required"] is True
        and cat["security_decisions_traceable_required"] is True
        and cat["scaling_possible_required"] is True
        and cat["audit_history_complete_required"] is True
        and cat["loose_coupling"]["not_tightly_coupled"] is True
        and cat["event_immutability"]["not_mutable"] is True
        and cat["api_governance"]["not_unmanaged"] is True
        and cat["decision_traceability"]["not_untraceable"] is True
        and cat["scalability"]["not_impossible"] is True
        and cat["audit_completeness"]["not_incomplete"] is True
        and cat["architecture"]["layer_count"] >= 8
        and cat["domain"]["context_count"] >= 7
        and cat["cqrs"]["command_count"] >= 20
        and cat["event_catalogue"]["event_count"] >= 25
        and cat["microservices"]["service_count"] >= 15
        and cat["cursor_outputs"]["count"] >= 16
        and "services_are_tightly_coupled"
        in cat["quality_gates"]["reject_if"]
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
            DsLooselyCoupledServicesRoot.establish,
            tenant_id="t1",
            fabric_ref="f1",
            loosely_coupled=False,
        )
        and DsLooselyCoupledServicesRoot.establish(
            tenant_id="t1", fabric_ref="f2"
        ).is_tightly_coupled()
        is False
    )
    checks.append(
        not _bad(
            DsImmutableEventsRoot.append,
            tenant_id="t1",
            event_ref="e1",
            immutable=False,
        )
        and DsImmutableEventsRoot.append(
            tenant_id="t1", event_ref="e2"
        ).is_mutable()
        is False
    )
    checks.append(
        not _bad(
            DsManagedApisRoot.register,
            tenant_id="t1",
            api_ref="a1",
            managed=False,
        )
        and DsManagedApisRoot.register(
            tenant_id="t1", api_ref="a2"
        ).is_unmanaged()
        is False
    )
    checks.append(
        not _bad(
            DsTraceableSecurityDecisionsRoot.record,
            tenant_id="t1",
            decision_ref="d1",
            traceable=False,
        )
        and DsTraceableSecurityDecisionsRoot.record(
            tenant_id="t1", decision_ref="d2"
        ).is_untraceable()
        is False
    )
    checks.append(
        not _bad(
            DsScalablePlatformRoot.enable,
            tenant_id="t1",
            platform_ref="p1",
            scalable=False,
        )
        and DsScalablePlatformRoot.enable(
            tenant_id="t1", platform_ref="p2"
        ).is_impossible()
        is False
    )
    checks.append(
        not _bad(
            DsCompleteAuditHistoryRoot.seal,
            tenant_id="t1",
            audit_ref="au1",
            complete=False,
        )
        and DsCompleteAuditHistoryRoot.seal(
            tenant_id="t1", audit_ref="au2"
        ).is_incomplete()
        is False
    )
    pub = DsEventPublishedRoot.publish(tenant_id="t1", stream_ref="s1")
    sim = DsSimulationExecutedRoot.execute(
        tenant_id="t1", simulation_ref="sim1"
    )
    checks.append("DataClassified" in pub.pending_events)
    checks.append("SimulationExecuted" in sim.pending_events)
    aggregates_ok = all(checks)

    acl_path = (
        root / "backend/contexts/data_security/infrastructure/acl/ds_ops_acl.py"
    )
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_enterprise_event_bus" in acl_text
        and "events_immutable_required" in acl_text
        and "apis_managed_required" in acl_text
        and "security_decisions_traceable_required" in acl_text
        and "via_api_gateway" in acl_text
        and "mtls_via_p209" in acl_text
        and "outbox_required" in acl_text
    )

    router = (
        root / "backend/contexts/data_security/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@data_security_router.get("/ops")' in router
        and "/ops/cqrs" in router
        and "/ops/events" in router
        and "/ops/service-mesh" in router
        and "/ops/readiness" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_DATA_SECURITY_OPS.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never Services are tightly coupled" in law
        and "Never Events are not immutable" in law
        and "Never APIs are unmanaged" in law
        and "Never Security decisions cannot be traced" in law
        and "Never Scaling is impossible" in law
        and "Never Audit history is incomplete" in law
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
        "prompt": "P211-N",
        "adr": 389,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "catalog": catalog_ok,
        "aggregates": aggregates_ok,
        "acl": acl_ok,
        "router": router_ok,
        "documentation": doc_ok,
        "sor": "data_security",
        "capability": "CAP-PLT-DS-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
