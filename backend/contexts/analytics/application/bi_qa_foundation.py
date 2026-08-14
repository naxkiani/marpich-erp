"""Analytics P213-P foundation validator."""
from __future__ import annotations
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/420-enterprise-business-intelligence-qa.md",
    "docs/architecture/ENTERPRISE_BUSINESS_INTELLIGENCE_QA.md",
    "docs/architecture/business_intelligence/BI_QA_CAPABILITIES.v1.yaml",
    "docs/architecture/business_intelligence/BI_QA_DDD_CQRS.v1.yaml",
    "docs/architecture/business_intelligence/BI_QA_SECURITY.v1.yaml",
    "docs/architecture/business_intelligence/BI_QA_VALIDATION.v1.yaml",
    "backend/contexts/analytics/domain/services/bi_platform_qa.py",
    "backend/contexts/analytics/domain/aggregates/bi_qa_aggregates.py",
    "backend/contexts/analytics/infrastructure/acl/bi_qa_acl.py",
    "backend/contexts/analytics/application/bi_qa_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/business_intelligence",
    "backend/contexts/decision_intelligence",
    "backend/contexts/reporting_platform",
    "backend/contexts/metric_governance_platform",
    "backend/contexts/visualization_platform",
    "backend/contexts/bi_core",
)


def validate_bi_qa_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.analytics.domain.services import bi_platform_qa as catmod
    from contexts.analytics.domain.aggregates.bi_qa_aggregates import BiQaProfileRoot
    cat = catmod.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P213-P"
        and cat.get("adr") == 420
        and cat.get("sor") == "analytics"
        and cat.get("capability") == "CAP-PLT-BI-001"
        and cat["architecture"]["capability_count"] >= 5
        and cat["cqrs"]["event_count"] >= 4
        and cat["cursor_outputs"]["count"] >= 9
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    try:
        BiQaProfileRoot.publish(tenant_id="t1", profile_ref="r1", complete=False)
        aggregates_ok = False
    except ValueError:
        aggregates_ok = not BiQaProfileRoot.publish(
            tenant_id="t1", profile_ref="ok"
        ).is_incomplete()
    router = (root / "backend/contexts/analytics/presentation/router.py").read_text(
        encoding="utf-8"
    )
    router_ok = (
        '@router.get("/qa")' in router
        and "/qa/readiness" in router
    )
    law = (root / "docs/architecture/ENTERPRISE_BUSINESS_INTELLIGENCE_QA.md").read_text(encoding="utf-8")
    doc_ok = "Never BI assurance architecture is incomplete" in law and "Never Sibling business intelligence BC" in law
    passed = (
        not missing
        and not sibling
        and catalog_ok
        and aggregates_ok
        and router_ok
        and doc_ok
    )
    return {
        "prompt": "P213-P",
        "adr": 420,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "catalog": catalog_ok,
        "aggregates": aggregates_ok,
        "router": router_ok,
        "documentation": doc_ok,
        "sor": "analytics",
        "capability": "CAP-PLT-BI-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
