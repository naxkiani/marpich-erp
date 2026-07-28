"""Analytics P213-A BI strategy foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/394-enterprise-business-intelligence-strategy.md",
    "docs/architecture/ENTERPRISE_BUSINESS_INTELLIGENCE_STRATEGY.md",
    "docs/architecture/business_intelligence/BI_STRATEGY_CAPABILITIES.v1.yaml",
    "docs/architecture/business_intelligence/BI_STRATEGY_DDD_CQRS.v1.yaml",
    "docs/architecture/business_intelligence/BI_STRATEGY_SECURITY.v1.yaml",
    "docs/architecture/business_intelligence/BI_STRATEGY_VALIDATION.v1.yaml",
    "docs/architecture/business_intelligence/P213_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/analytics/domain/services/bi_platform_strategy.py",
    "backend/contexts/analytics/domain/aggregates/bi_strategy_aggregates.py",
    "backend/contexts/analytics/infrastructure/acl/bi_strategy_acl.py",
    "backend/contexts/analytics/application/bi_strategy_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/business_intelligence",
    "backend/contexts/decision_intelligence",
    "backend/contexts/reporting_platform",
    "backend/contexts/metric_governance_platform",
    "backend/contexts/visualization_platform",
    "backend/contexts/bi_core",
)


def validate_bi_strategy_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.analytics.domain.aggregates.bi_strategy_aggregates import (
        BiStrategyProfileRoot,
    )
    from contexts.analytics.domain.services import bi_platform_strategy as strat

    cat = strat.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P213-A"
        and cat.get("adr") == 394
        and cat.get("sor") == "analytics"
        and cat.get("capability") == "CAP-PLT-BI-001"
        and cat.get("principle")
        and "trusted data" in cat["principle"]
        and cat.get("core_domain") == "enterprise_decision_intelligence_management"
        and cat.get("aggregate") == "EnterpriseInsightAggregate"
        and cat["architecture"]["layer_count"] >= 6
        and cat["domains"]["supporting_count"] >= 8
        and cat["bounded_contexts"]["context_count"] >= 5
        and cat["microservices"]["service_count"] >= 6
        and cat["cqrs"]["event_count"] >= 8
        and cat["cqrs"]["command_count"] >= 4
        and cat["ai_native"]["agent_count"] >= 5
        and cat["knowledge_graph_integration"]["via_p212_j"] is True
        and cat["digital_twin_integration"]["via_p212_l"] is True
        and cat["api_first"]["via_api_gateway"] is True
        and cat["cursor_outputs"]["count"] >= 16
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
        and cat["bi_architecture_complete_required"] is True
        and cat["decision_intelligence_foundation_present_required"] is True
        and cat["knowledge_graph_integration_present_required"] is True
        and cat["digital_twin_integration_present_required"] is True
        and (
            "enterprise_bi_architecture_is_incomplete"
            in cat["quality_gates"]["reject_if"]
        )
    )

    try:
        BiStrategyProfileRoot.publish(
            tenant_id="t1", strategy_ref="s1", complete=False
        )
        aggregates_ok = False
    except ValueError:
        aggregates_ok = (
            not BiStrategyProfileRoot.publish(
                tenant_id="t1", strategy_ref="s2"
            ).is_incomplete()
        )

    acl_path = (
        root
        / "backend/contexts/analytics/infrastructure/acl/bi_strategy_acl.py"
    )
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_p212" in acl_text
        and "via_p212_j" in acl_text
        and "via_p212_l" in acl_text
        and "via_p207" in acl_text
        and "via_p208" in acl_text
        and "via_p211" in acl_text
        and "via_enterprise_ai" in acl_text
        and "module_local_llm_sdk_forbidden" in acl_text
    )

    router = (
        root / "backend/contexts/analytics/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@router.get("/strategy")' in router
        and "/strategy/readiness" in router
    )

    registry = (root / "backend/contexts/registry.py").read_text(encoding="utf-8")
    registry_ok = 'id="analytics"' in registry and "CAP-PLT-BI-001" in registry

    law = (
        root / "docs/architecture/ENTERPRISE_BUSINESS_INTELLIGENCE_STRATEGY.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never Enterprise BI architecture is incomplete" in law
        and "Never Analytics architecture is missing" in law
        and "Never Decision intelligence foundation is missing" in law
        and "Never DDD domain model is missing" in law
        and "Never CQRS architecture is missing" in law
        and "Never Microservices architecture is missing" in law
        and "Never API first design is missing" in law
        and "Never AI-native BI is missing" in law
        and "Never Knowledge graph integration is missing" in law
        and "Never Digital twin integration is missing" in law
        and "Never Governance alignment is missing" in law
        and "Never Sibling business intelligence BC" in law
        and (
            "Enterprise intelligence transforms trusted data"
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
        and registry_ok
        and doc_ok
    )
    return {
        "prompt": "P213-A",
        "adr": 394,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "catalog": catalog_ok,
        "aggregates": aggregates_ok,
        "acl": acl_ok,
        "router": router_ok,
        "registry": registry_ok,
        "documentation": doc_ok,
        "sor": "analytics",
        "capability": "CAP-PLT-BI-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
