"""Cyber Security P210-F SOAR foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/365-enterprise-cyber-security-soar.md",
    "docs/architecture/ENTERPRISE_CYBER_SECURITY_SOAR.md",
    "docs/architecture/cyber_security/CYBER_SOAR_CAPABILITIES.v1.yaml",
    "docs/architecture/cyber_security/CYBER_SOAR_DDD_CQRS.v1.yaml",
    "docs/architecture/cyber_security/CYBER_SOAR_SECURITY.v1.yaml",
    "docs/architecture/cyber_security/CYBER_SOAR_VALIDATION.v1.yaml",
    "backend/contexts/cyber_security/domain/services/cs_platform_soar.py",
    "backend/contexts/cyber_security/domain/aggregates/cs_soar_aggregates.py",
    "backend/contexts/cyber_security/infrastructure/acl/cs_soar_acl.py",
    "backend/contexts/cyber_security/application/cs_soar_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/soar_platform",
    "backend/contexts/soc_platform",
    "backend/contexts/siem_platform",
    "backend/contexts/xdr",
    "backend/contexts/security_ops",
    "backend/contexts/cyber_defense",
)


def validate_cs_soar_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.cyber_security.domain.aggregates.cs_soar_aggregates import (
        CsSoarAutomationAuditableRoot,
        CsSoarEvidencePreservedRoot,
        CsSoarExplainableAiRoot,
        CsSoarHumanApprovalRoot,
        CsSoarLooseConnectorsRoot,
        CsSoarPlaybookExecutionRoot,
        CsSoarPlaybookVersionedRoot,
        CsSoarRollbackRoot,
    )
    from contexts.cyber_security.domain.services import cs_platform_soar as soar

    cat = soar.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P210-F"
        and cat.get("adr") == 365
        and cat.get("sor") == "cyber_security"
        and cat["playbooks_versioned_required"] is True
        and cat["automation_auditable_required"] is True
        and cat["human_approval_required"] is True
        and cat["ai_recommendations_explainable_required"] is True
        and cat["rollback_capability_required"] is True
        and cat["connectors_tightly_coupled_forbidden"] is True
        and cat["incident_evidence_preservation_required"] is True
        and cat["playbook_engine"]["not_unversioned"] is True
        and cat["automation_engine"]["not_unauditable"] is True
        and cat["human_in_the_loop"]["not_unavailable"] is True
        and cat["ai"]["not_unexplainable"] is True
        and cat["automation_engine"]["not_absent_rollback"] is True
        and cat["connectors"]["not_tightly_coupled"] is True
        and cat["evidence"]["not_unpreservable"] is True
        and cat["architecture"]["layer_count"] >= 10
        and cat["playbook_engine"]["category_count"] >= 10
        and cat["cqrs"]["event_count"] >= 12
        and cat["cursor_outputs"]["count"] >= 20
        and "playbooks_cannot_be_versioned" in cat["quality_gates"]["reject_if"]
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
            CsSoarPlaybookVersionedRoot.publish,
            tenant_id="t1",
            playbook_ref="pb1",
            versioned=False,
        )
        and CsSoarPlaybookVersionedRoot.publish(
            tenant_id="t1", playbook_ref="pb2"
        ).is_unversioned()
        is False
    )
    checks.append(
        not _bad(
            CsSoarAutomationAuditableRoot.execute,
            tenant_id="t1",
            run_ref="r1",
            audited=False,
        )
        and CsSoarAutomationAuditableRoot.execute(
            tenant_id="t1", run_ref="r2"
        ).is_unauditable()
        is False
    )
    checks.append(
        not _bad(
            CsSoarHumanApprovalRoot.require,
            tenant_id="t1",
            gate_ref="g1",
            available=False,
        )
        and CsSoarHumanApprovalRoot.require(
            tenant_id="t1", gate_ref="g2"
        ).is_unavailable()
        is False
    )
    checks.append(
        not _bad(
            CsSoarExplainableAiRoot.advise,
            tenant_id="t1",
            advisory_ref="a1",
            explainable=False,
        )
        and CsSoarExplainableAiRoot.advise(
            tenant_id="t1", advisory_ref="a2"
        ).is_unexplainable()
        is False
    )
    checks.append(
        not _bad(
            CsSoarRollbackRoot.enable,
            tenant_id="t1",
            plan_ref="p1",
            rollback_available=False,
        )
        and CsSoarRollbackRoot.enable(tenant_id="t1", plan_ref="p2").is_absent()
        is False
    )
    checks.append(
        not _bad(
            CsSoarLooseConnectorsRoot.bind,
            tenant_id="t1",
            connector_ref="c1",
            tightly_coupled=True,
        )
        and CsSoarLooseConnectorsRoot.bind(
            tenant_id="t1", connector_ref="c2"
        ).is_tightly_coupled()
        is False
    )
    checks.append(
        not _bad(
            CsSoarEvidencePreservedRoot.preserve,
            tenant_id="t1",
            evidence_ref="e1",
            preserved=False,
        )
        and CsSoarEvidencePreservedRoot.preserve(
            tenant_id="t1", evidence_ref="e2"
        ).is_unpreservable()
        is False
    )
    exec_root = CsSoarPlaybookExecutionRoot.execute(
        tenant_id="t1", execution_ref="x1", playbook_ref="pb3"
    )
    checks.append("PlaybookExecuted" in exec_root.pending_events)
    aggregates_ok = all(checks)

    acl_path = root / "backend/contexts/cyber_security/infrastructure/acl/cs_soar_acl.py"
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_workflow" in acl_text
        and "tightly_coupled_forbidden" in acl_text
        and "explainable_required" in acl_text
        and "automation_auditable_required" in acl_text
        and "preservation_required" in acl_text
    )

    router = (
        root / "backend/contexts/cyber_security/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '/soar"' in router
        and "/soar/playbooks" in router
        and "/soar/approvals" in router
        and "/soar/connectors" in router
        and "/soar/readiness" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_CYBER_SECURITY_SOAR.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never playbooks cannot be versioned" in law
        and "Never automation is not auditable" in law
        and "Never human approval is unavailable" in law
        and "Never AI recommendations are not explainable" in law
        and "Never rollback capability is absent" in law
        and "Never connectors are tightly coupled" in law
        and "Never incident evidence cannot be preserved" in law
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
        "prompt": "P210-F",
        "adr": 365,
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
