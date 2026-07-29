"""Data Security P211-L AI autonomous protection foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/387-enterprise-data-security-ai.md",
    "docs/architecture/ENTERPRISE_DATA_SECURITY_AI.md",
    "docs/architecture/data_security/DATA_SECURITY_AI_CAPABILITIES.v1.yaml",
    "docs/architecture/data_security/DATA_SECURITY_AI_DDD_CQRS.v1.yaml",
    "docs/architecture/data_security/DATA_SECURITY_AI_SECURITY.v1.yaml",
    "docs/architecture/data_security/DATA_SECURITY_AI_VALIDATION.v1.yaml",
    "backend/contexts/data_security/domain/services/ds_platform_ai.py",
    "backend/contexts/data_security/domain/aggregates/ds_ai_aggregates.py",
    "backend/contexts/data_security/infrastructure/acl/ds_ai_acl.py",
    "backend/contexts/data_security/application/ds_ai_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/ai_data_security",
    "backend/contexts/autonomous_data_protection",
    "backend/contexts/data_security_ai",
)


def validate_ds_ai_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.data_security.domain.aggregates.ds_ai_aggregates import (
        DsAiGovernanceRoot,
        DsControlledAutonomyRoot,
        DsExplainableAiDecisionRoot,
        DsHumanOversightRoot,
        DsLearningLoopRoot,
        DsPolicyOptimizedRoot,
        DsPredictableRiskRoot,
        DsThreatDetectedRoot,
    )
    from contexts.data_security.domain.services import ds_platform_ai as ai

    cat = ai.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P211-L"
        and cat.get("adr") == 387
        and cat.get("sor") == "data_security"
        and cat["ai_decisions_explainable_required"] is True
        and cat["autonomous_actions_controlled_required"] is True
        and cat["data_risks_predictable_required"] is True
        and cat["learning_loop_present_required"] is True
        and cat["ai_security_governance_present_required"] is True
        and cat["human_oversight_possible_required"] is True
        and cat["explainability"]["not_unexplainable"] is True
        and cat["autonomy_control"]["not_uncontrolled"] is True
        and cat["risk_prediction"]["not_unpredictable"] is True
        and cat["learning_loop"]["not_missing"] is True
        and cat["ai_governance"]["not_absent"] is True
        and cat["human_oversight"]["not_impossible"] is True
        and cat["architecture"]["layer_count"] >= 8
        and cat["domain"]["context_count"] >= 7
        and cat["agents"]["agent_count"] >= 6
        and cat["cqrs"]["event_count"] >= 7
        and cat["cursor_outputs"]["count"] >= 16
        and "ai_decisions_are_not_explainable"
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
            DsExplainableAiDecisionRoot.decide,
            tenant_id="t1",
            decision_ref="d1",
            explainable=False,
        )
        and DsExplainableAiDecisionRoot.decide(
            tenant_id="t1", decision_ref="d2"
        ).is_unexplainable()
        is False
    )
    checks.append(
        not _bad(
            DsControlledAutonomyRoot.execute,
            tenant_id="t1",
            action_ref="a1",
            controlled=False,
        )
        and DsControlledAutonomyRoot.execute(
            tenant_id="t1", action_ref="a2"
        ).is_uncontrolled()
        is False
    )
    checks.append(
        not _bad(
            DsPredictableRiskRoot.predict,
            tenant_id="t1",
            prediction_ref="p1",
            predictable=False,
        )
        and DsPredictableRiskRoot.predict(
            tenant_id="t1", prediction_ref="p2"
        ).is_unpredictable()
        is False
    )
    checks.append(
        not _bad(
            DsLearningLoopRoot.complete,
            tenant_id="t1",
            loop_ref="l1",
            present=False,
        )
        and DsLearningLoopRoot.complete(
            tenant_id="t1", loop_ref="l2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DsAiGovernanceRoot.establish,
            tenant_id="t1",
            governance_ref="g1",
            present=False,
        )
        and DsAiGovernanceRoot.establish(
            tenant_id="t1", governance_ref="g2"
        ).is_absent()
        is False
    )
    checks.append(
        not _bad(
            DsHumanOversightRoot.approve,
            tenant_id="t1",
            oversight_ref="o1",
            possible=False,
        )
        and DsHumanOversightRoot.approve(
            tenant_id="t1", oversight_ref="o2"
        ).is_impossible()
        is False
    )
    threat = DsThreatDetectedRoot.detect(tenant_id="t1", threat_ref="th1")
    pol = DsPolicyOptimizedRoot.optimize(tenant_id="t1", policy_ref="pol1")
    checks.append("ThreatDetected" in threat.pending_events)
    checks.append("PolicyOptimized" in pol.pending_events)
    aggregates_ok = all(checks)

    acl_path = (
        root / "backend/contexts/data_security/infrastructure/acl/ds_ai_acl.py"
    )
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_enterprise_ai" in acl_text
        and "ai_decisions_explainable_required" in acl_text
        and "human_oversight_possible_required" in acl_text
        and "autonomous_actions_controlled_required" in acl_text
        and "via_p211_k_intelligence" in acl_text
        and "module_local_llm_sdk_forbidden" in acl_text
    )

    router = (
        root / "backend/contexts/data_security/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@data_security_router.get("/ai-data")' in router
        and "/ai-data/explainability" in router
        and "/ai-data/autonomy" in router
        and "/ai-data/oversight" in router
        and "/ai-data/readiness" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_DATA_SECURITY_AI.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never AI decisions are not explainable" in law
        and "Never Autonomous actions are uncontrolled" in law
        and "Never Data risks cannot be predicted" in law
        and "Never Learning loop is missing" in law
        and "Never AI security governance is absent" in law
        and "Never Human oversight is impossible" in law
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
        "prompt": "P211-L",
        "adr": 387,
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
