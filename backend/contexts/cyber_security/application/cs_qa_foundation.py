"""Cyber Security P210-O QA / Validation foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/375-enterprise-cyber-security-qa-validation.md",
    "docs/architecture/ENTERPRISE_CYBER_SECURITY_QA.md",
    "docs/architecture/cyber_security/CYBER_QA_CAPABILITIES.v1.yaml",
    "docs/architecture/cyber_security/CYBER_QA_DDD_CQRS.v1.yaml",
    "docs/architecture/cyber_security/CYBER_QA_SECURITY.v1.yaml",
    "docs/architecture/cyber_security/CYBER_QA_VALIDATION.v1.yaml",
    "backend/contexts/cyber_security/domain/services/cs_platform_qa.py",
    "backend/contexts/cyber_security/domain/aggregates/cs_qa_aggregates.py",
    "backend/contexts/cyber_security/infrastructure/acl/cs_qa_acl.py",
    "backend/contexts/cyber_security/application/cs_qa_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/qa_platform",
    "backend/contexts/security_testing",
    "backend/contexts/red_team",
    "backend/contexts/penetration_testing",
    "backend/contexts/cyber_ops",
)


def validate_cs_qa_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.cyber_security.domain.aggregates.cs_qa_aggregates import (
        CsQaAdversarialValidationRoot,
        CsQaAiSystemsTestedRoot,
        CsQaAuditableEvidenceRoot,
        CsQaAutomatedTestingRoot,
        CsQaComplianceVerificationRoot,
        CsQaMeasurableControlsRoot,
        CsQaProductionReadinessRoot,
        CsQaReleaseApprovalRoot,
    )
    from contexts.cyber_security.domain.services import cs_platform_qa as qa

    cat = qa.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P210-O"
        and cat.get("adr") == 375
        and cat.get("sor") == "cyber_security"
        and cat["security_testing_automated_required"] is True
        and cat["adversarial_validation_required"] is True
        and cat["ai_systems_tested_required"] is True
        and cat["compliance_verifiable_required"] is True
        and cat["production_readiness_defined_required"] is True
        and cat["security_controls_measurable_required"] is True
        and cat["test_evidence_auditable_required"] is True
        and cat["security_testing"]["not_manual_only"] is True
        and cat["red_team"]["not_absent"] is True
        and cat["ai_security_testing"]["not_untested"] is True
        and cat["compliance"]["not_unverifiable"] is True
        and cat["production_readiness_gate"]["not_undefined"] is True
        and cat["measurable_controls"]["not_unmeasurable"] is True
        and cat["auditable_evidence"]["not_unauditable"] is True
        and cat["architecture"]["layer_count"] >= 8
        and cat["test_domains"]["domain_count"] >= 10
        and cat["cqrs"]["event_count"] >= 7
        and cat["cursor_outputs"]["count"] >= 20
        and cat["series_complete"] is True
        and "security_testing_is_manual_only" in cat["quality_gates"]["reject_if"]
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
            CsQaAutomatedTestingRoot.create_plan,
            tenant_id="t1",
            plan_ref="p1",
            automated=False,
        )
        and CsQaAutomatedTestingRoot.create_plan(
            tenant_id="t1", plan_ref="p2"
        ).is_manual_only()
        is False
    )
    checks.append(
        not _bad(
            CsQaAdversarialValidationRoot.launch,
            tenant_id="t1",
            exercise_ref="e1",
            adversarial=False,
        )
        and CsQaAdversarialValidationRoot.launch(
            tenant_id="t1", exercise_ref="e2"
        ).is_absent()
        is False
    )
    checks.append(
        not _bad(
            CsQaAiSystemsTestedRoot.test,
            tenant_id="t1",
            model_ref="m1",
            tested=False,
        )
        and CsQaAiSystemsTestedRoot.test(
            tenant_id="t1", model_ref="m2"
        ).is_untested()
        is False
    )
    checks.append(
        not _bad(
            CsQaComplianceVerificationRoot.verify,
            tenant_id="t1",
            evidence_ref="ev1",
            verifiable=False,
        )
        and CsQaComplianceVerificationRoot.verify(
            tenant_id="t1", evidence_ref="ev2"
        ).is_unverifiable()
        is False
    )
    checks.append(
        not _bad(
            CsQaProductionReadinessRoot.define,
            tenant_id="t1",
            gate_ref="g1",
            defined=False,
        )
        and CsQaProductionReadinessRoot.define(
            tenant_id="t1", gate_ref="g2"
        ).is_undefined()
        is False
    )
    checks.append(
        not _bad(
            CsQaMeasurableControlsRoot.measure,
            tenant_id="t1",
            control_ref="c1",
            measurable=False,
        )
        and CsQaMeasurableControlsRoot.measure(
            tenant_id="t1", control_ref="c2"
        ).is_unmeasurable()
        is False
    )
    checks.append(
        not _bad(
            CsQaAuditableEvidenceRoot.collect,
            tenant_id="t1",
            evidence_ref="a1",
            auditable=False,
        )
        and CsQaAuditableEvidenceRoot.collect(
            tenant_id="t1", evidence_ref="a2"
        ).is_unauditable()
        is False
    )
    approved = CsQaReleaseApprovalRoot.approve(
        tenant_id="t1", release_ref="r1"
    )
    checks.append("ReleaseApproved" in approved.pending_events)
    aggregates_ok = all(checks)

    acl_path = root / "backend/contexts/cyber_security/infrastructure/acl/cs_qa_acl.py"
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_workflow" in acl_text
        and "via_compliance_framework" in acl_text
        and "via_audit_platform" in acl_text
        and "ai_systems_tested_required" in acl_text
        and "test_evidence_auditable_required" in acl_text
    )

    router = (
        root / "backend/contexts/cyber_security/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@cyber_security_router.get("/qa")' in router
        and "/qa/security-testing" in router
        and "/qa/red-team" in router
        and "/qa/compliance" in router
        and "/qa/readiness" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_CYBER_SECURITY_QA.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never Security testing is manual only" in law
        and "Never No adversarial validation exists" in law
        and "Never AI systems are not tested" in law
        and "Never Compliance cannot be verified" in law
        and "Never Production readiness is undefined" in law
        and "Never Security controls cannot be measured" in law
        and "Never Test evidence cannot be audited" in law
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
        "prompt": "P210-O",
        "adr": 375,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "catalog": catalog_ok,
        "aggregates": aggregates_ok,
        "acl": acl_ok,
        "router": router_ok,
        "documentation": doc_ok,
        "sor": "cyber_security",
        "series_complete": True,
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
