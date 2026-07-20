"""Identity Intelligence P207-O QA foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]

REQUIRED_ARTIFACTS = [
    "docs/adr/330-enterprise-identity-intelligence-qa-governance-dod.md",
    "docs/architecture/ENTERPRISE_IDENTITY_INTELLIGENCE_QA_GOVERNANCE.md",
    "docs/architecture/identity/intelligence/II_QA_CAPABILITIES.v1.yaml",
    "docs/architecture/identity/intelligence/II_QA_DDD_CQRS.v1.yaml",
    "docs/architecture/identity/intelligence/II_QA_SECURITY.v1.yaml",
    "docs/architecture/identity/intelligence/II_QA_VALIDATION.v1.yaml",
    "backend/contexts/identity_intelligence/domain/services/ii_platform_qa.py",
    "backend/contexts/identity_intelligence/domain/aggregates/ii_qa_aggregates.py",
    "backend/contexts/identity_intelligence/infrastructure/acl/ii_qa_acl.py",
    "backend/contexts/identity_intelligence/domain/services/ii_qa_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/identity_qa_platform",
    "backend/contexts/identity_assurance_bc",
    "backend/contexts/identity_dod",
)


def validate_ii_qa_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.identity_intelligence.domain.aggregates.ii_qa_aggregates import (
        AIValidationRecordRoot,
        ComplianceEvidencePackRoot,
        ContinuousAssuranceBaselineRoot,
        DefinitionOfDoneCertificationRoot,
        IdentityTestSuitePlanRoot,
        ReleaseGovernanceApprovalRoot,
        SecurityValidationCaseRoot,
    )
    from contexts.identity_intelligence.domain.services import ii_platform_qa as qa
    from contexts.identity_intelligence.infrastructure.acl import ii_qa_acl as acls

    cat = qa.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P207-O"
        and cat.get("adr") == 330
        and cat.get("sor") == "identity_intelligence"
        and cat["certification_complete"] is True
        and cat["p207_series_complete"] is True
        and cat["capabilities"]["not_manual_only"] is True
        and cat["capabilities"]["not_incomplete_security"] is True
        and cat["capabilities"]["not_undefined_governance"] is True
        and cat["capabilities"]["not_missing_evidence"] is True
        and cat["capabilities"]["not_absent_ai_validation"] is True
        and cat["capabilities"]["not_incomplete_dod"] is True
        and cat["test_strategy"]["not_manual_only"] is True
        and cat["security_validation"]["not_incomplete"] is True
        and cat["ai_testing"]["not_absent"] is True
        and cat["definition_of_done"]["not_incomplete"] is True
        and cat["definition_of_done"]["p207_completion_gate"] is True
        and cat["ddd"]["aggregate_count"] >= 7
        and cat["integrations"]["qa_integration_complete"] is True
        and "testing_manual_only" in cat["quality_gates"]["reject_if"]
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
        and cat["production_readiness"]["checklist"]["p207_series_complete"] is True
    )

    try:
        IdentityTestSuitePlanRoot.register(
            tenant_id="t1", suite_ref="s1", automated=False
        )
        manual = True
    except ValueError:
        manual = False

    suite = IdentityTestSuitePlanRoot.register(tenant_id="t1", suite_ref="s2")
    suite_ok = (
        not manual
        and suite.is_manual_only() is False
        and "TestCompleted" in suite.pending_events
    )

    try:
        SecurityValidationCaseRoot.assess(
            tenant_id="t1", case_ref="c1", zero_trust=False
        )
        inc_sec = True
    except ValueError:
        inc_sec = False

    sec = SecurityValidationCaseRoot.assess(tenant_id="t1", case_ref="c2")
    sec_ok = (
        not inc_sec
        and sec.is_incomplete() is False
        and "SecurityValidated" in sec.pending_events
    )

    try:
        AIValidationRecordRoot.validate(
            tenant_id="t1", record_ref="a1", explainable=False
        )
        no_ai = True
    except ValueError:
        no_ai = False

    ai = AIValidationRecordRoot.validate(tenant_id="t1", record_ref="a2")
    ai_ok = not no_ai and ai.is_absent() is False

    try:
        ReleaseGovernanceApprovalRoot.approve(
            tenant_id="t1",
            approval_ref="g1",
            domain="unknown",
            owner_ref="owner",
        )
        undef_gov = True
    except ValueError:
        undef_gov = False

    gov = ReleaseGovernanceApprovalRoot.approve(
        tenant_id="t1",
        approval_ref="g2",
        domain="architecture",
        owner_ref="chief-architect",
    )
    gov_ok = (
        not undef_gov
        and gov.is_undefined() is False
        and "GovernanceApproved" in gov.pending_events
    )

    try:
        ComplianceEvidencePackRoot.collect(
            tenant_id="t1", pack_ref="p1", evidence_refs=()
        )
        no_ev = True
    except ValueError:
        no_ev = False

    comp = ComplianceEvidencePackRoot.collect(tenant_id="t1", pack_ref="p2")
    comp_ok = not no_ev and comp.is_missing() is False

    baseline = ContinuousAssuranceBaselineRoot.establish(
        tenant_id="t1", baseline_ref="b1"
    )
    baseline_ok = baseline.regression_detection is True

    try:
        DefinitionOfDoneCertificationRoot.certify(
            tenant_id="t1",
            cert_ref="d1",
            criteria_met=("secure", "scalable"),
        )
        inc_dod = True
    except ValueError:
        inc_dod = False

    dod = DefinitionOfDoneCertificationRoot.certify(tenant_id="t1", cert_ref="d2")
    dod_ok = (
        not inc_dod
        and dod.is_certified() is True
        and dod.p207_series_complete is True
        and "DefinitionOfDoneCertified" in dod.pending_events
    )

    aggregates_ok = (
        suite_ok
        and sec_ok
        and ai_ok
        and gov_ok
        and comp_ok
        and baseline_ok
        and dod_ok
    )

    acl_ok = (
        acls.to_compliance(
            tenant_id="t1", pack_ref="p1", frameworks=["iso_27001"]
        )["local_compliance_store_forbidden"]
        is True
        and acls.to_audit(tenant_id="t1", action="qa.certify", resource_ref="d2")[
            "traceability_required"
        ]
        is True
        and acls.to_policy_evaluate(
            tenant_id="t1", policy_key="ii.qa.release", context={}
        )["policy_validation"]
        is True
        and acls.to_ai_infer(tenant_id="t1", surface="bias", context={})[
            "ai_validation"
        ]
        is True
        and acls.to_observability(
            tenant_id="t1", metric_name="quality", value=1.0
        )["continuous_assurance_metrics"]
        is True
        and acls.to_ops_readiness(tenant_id="t1", review_ref="r1")["via_p207n"]
        is True
    )

    router = (
        root / "backend/contexts/identity_intelligence/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@identity_intelligence_router.get("/qa"' in router
        and "/qa/test-strategy" in router
        and "/qa/security" in router
        and "/qa/definition-of-done" in router
        and "/qa/readiness" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_IDENTITY_INTELLIGENCE_QA_GOVERNANCE.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never testing manual only" in law
        and "Never security validation incomplete" in law
        and "Never governance undefined" in law
        and "Never compliance evidence missing" in law
        and "Never AI validation absent" in law
        and "Never Definition of Done incomplete" in law
        and "P207 Completion Gate" in law
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
        "prompt": "P207-O",
        "adr": 330,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "catalog": catalog_ok,
        "aggregates": aggregates_ok,
        "acl": acl_ok,
        "router": router_ok,
        "documentation": doc_ok,
        "sor": "identity_intelligence",
        "certification_complete": passed,
        "p207_series_complete": passed,
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
