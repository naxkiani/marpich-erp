"""Cyber Security P210-L Ops fabric foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/372-enterprise-cyber-security-cqrs-ops.md",
    "docs/architecture/ENTERPRISE_CYBER_SECURITY_CQRS_OPS.md",
    "docs/architecture/cyber_security/CYBER_OPS_CAPABILITIES.v1.yaml",
    "docs/architecture/cyber_security/CYBER_OPS_DDD_CQRS.v1.yaml",
    "docs/architecture/cyber_security/CYBER_OPS_SECURITY.v1.yaml",
    "docs/architecture/cyber_security/CYBER_OPS_VALIDATION.v1.yaml",
    "backend/contexts/cyber_security/domain/services/cs_platform_ops.py",
    "backend/contexts/cyber_security/domain/aggregates/cs_ops_aggregates.py",
    "backend/contexts/cyber_security/infrastructure/acl/cs_ops_acl.py",
    "backend/contexts/cyber_security/application/cs_ops_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/cyber_ops",
    "backend/contexts/security_mesh",
    "backend/contexts/cyber_event_bus",
    "backend/contexts/cyber_graph",
    "backend/contexts/ai_ops",
)


def validate_cs_ops_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.cyber_security.domain.aggregates.cs_ops_aggregates import (
        CsOpsAiIntegrableRoot,
        CsOpsCqrsSeparationRoot,
        CsOpsEventGovernanceRoot,
        CsOpsImmutableEventsRoot,
        CsOpsIndependentScaleRoot,
        CsOpsLooseCouplingRoot,
        CsOpsObservabilityRoot,
        CsOpsSecuredApisRoot,
    )
    from contexts.cyber_security.domain.services import cs_platform_ops as ops

    cat = ops.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P210-L"
        and cat.get("adr") == 372
        and cat.get("sor") == "cyber_security"
        and cat["services_loosely_coupled_required"] is True
        and cat["events_immutable_required"] is True
        and cat["apis_security_controls_required"] is True
        and cat["cqrs_separation_complete_required"] is True
        and cat["microservices_independently_scalable_required"] is True
        and cat["observability_required"] is True
        and cat["ai_integration_possible_required"] is True
        and cat["event_governance_required"] is True
        and cat["microservices"]["not_tightly_coupled"] is True
        and cat["event_sourcing"]["not_mutable"] is True
        and cat["api_platform"]["not_unsecured"] is True
        and cat["cqrs"]["not_incomplete"] is True
        and cat["microservices"]["not_non_independent_scale"] is True
        and cat["observability"]["not_missing"] is True
        and cat["ai_event_intelligence"]["not_impossible"] is True
        and cat["event_streaming"]["not_ungoverned"] is True
        and cat["cqrs_events"]["event_count"] >= 10
        and cat["cursor_outputs"]["count"] >= 20
        and "services_tightly_coupled" in cat["quality_gates"]["reject_if"]
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
            CsOpsLooseCouplingRoot.bind,
            tenant_id="t1",
            service_ref="s1",
            tightly_coupled=True,
        )
        and CsOpsLooseCouplingRoot.bind(
            tenant_id="t1", service_ref="s2"
        ).is_tightly_coupled()
        is False
    )
    checks.append(
        not _bad(
            CsOpsImmutableEventsRoot.append,
            tenant_id="t1",
            event_ref="e1",
            immutable=False,
        )
        and CsOpsImmutableEventsRoot.append(
            tenant_id="t1", event_ref="e2"
        ).is_mutable()
        is False
    )
    checks.append(
        not _bad(
            CsOpsSecuredApisRoot.protect,
            tenant_id="t1",
            api_ref="a1",
            secured=False,
        )
        and CsOpsSecuredApisRoot.protect(
            tenant_id="t1", api_ref="a2"
        ).lacks_security()
        is False
    )
    checks.append(
        not _bad(
            CsOpsCqrsSeparationRoot.enforce,
            tenant_id="t1",
            model_ref="m1",
            separated=False,
        )
        and CsOpsCqrsSeparationRoot.enforce(
            tenant_id="t1", model_ref="m2"
        ).is_incomplete()
        is False
    )
    checks.append(
        not _bad(
            CsOpsIndependentScaleRoot.enable,
            tenant_id="t1",
            service_ref="svc1",
            independent=False,
        )
        and CsOpsIndependentScaleRoot.enable(
            tenant_id="t1", service_ref="svc2"
        ).cannot_scale_independently()
        is False
    )
    checks.append(
        not _bad(
            CsOpsObservabilityRoot.enable,
            tenant_id="t1",
            plane_ref="p1",
            present=False,
        )
        and CsOpsObservabilityRoot.enable(
            tenant_id="t1", plane_ref="p2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            CsOpsAiIntegrableRoot.enable,
            tenant_id="t1",
            integration_ref="i1",
            possible=False,
        )
        and CsOpsAiIntegrableRoot.enable(
            tenant_id="t1", integration_ref="i2"
        ).is_impossible()
        is False
    )
    checks.append(
        not _bad(
            CsOpsEventGovernanceRoot.govern,
            tenant_id="t1",
            schema_ref="sch1",
            governed=False,
        )
        and CsOpsEventGovernanceRoot.govern(
            tenant_id="t1", schema_ref="sch2"
        ).is_absent()
        is False
    )
    aggregates_ok = all(checks)

    acl_path = root / "backend/contexts/cyber_security/infrastructure/acl/cs_ops_acl.py"
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_enterprise_event_bus" in acl_text
        and "events_immutable_required" in acl_text
        and "via_api_gateway" in acl_text
        and "ai_integration_possible_required" in acl_text
        and "observability_required" in acl_text
    )

    router = (
        root / "backend/contexts/cyber_security/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '/ops"' in router
        and "/ops/cqrs" in router
        and "/ops/microservices" in router
        and "/ops/event-sourcing" in router
        and "/ops/readiness" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_CYBER_SECURITY_CQRS_OPS.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never services are tightly coupled" in law
        and "Never events are mutable" in law
        and "Never APIs lack security controls" in law
        and "Never CQRS separation is incomplete" in law
        and "Never microservices cannot scale independently" in law
        and "Never observability is missing" in law
        and "Never AI integration is impossible" in law
        and "Never event governance is absent" in law
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
        "prompt": "P210-L",
        "adr": 372,
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
