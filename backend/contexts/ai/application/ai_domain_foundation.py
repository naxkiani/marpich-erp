"""AI P214-C domain architecture foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/423-enterprise-ai-domain-architecture.md",
    "docs/architecture/ENTERPRISE_AI_DOMAIN_ARCHITECTURE.md",
    "docs/architecture/enterprise_ai/AI_DOMAIN_CAPABILITIES.v1.yaml",
    "docs/architecture/enterprise_ai/AI_DOMAIN_DDD_CQRS.v1.yaml",
    "docs/architecture/enterprise_ai/AI_DOMAIN_SECURITY.v1.yaml",
    "docs/architecture/enterprise_ai/AI_DOMAIN_VALIDATION.v1.yaml",
    "backend/contexts/ai/domain/services/ai_platform_domain.py",
    "backend/contexts/ai/domain/aggregates/ai_domain_aggregates.py",
    "backend/contexts/ai/infrastructure/acl/ai_domain_acl.py",
    "backend/contexts/ai/application/ai_domain_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/ml_platform",
    "backend/contexts/generative_ai",
    "backend/contexts/llm_platform",
    "backend/contexts/ai_core",
    "backend/contexts/vector_intelligence",
    "backend/contexts/model_lifecycle_platform",
)


def validate_ai_domain_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.ai.domain.aggregates.ai_domain_aggregates import (
        AiAggregatesDefinedRoot,
        AiBoundedContextsRoot,
        AiDomainMapRoot,
        AiEventsPresentRoot,
        AiIntegrationBoundariesRoot,
        AiMicroserviceBoundariesRoot,
    )
    from contexts.ai.domain.services import ai_platform_domain as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P214-C"
        and cat.get("adr") == 423
        and cat.get("sor") == "ai"
        and cat.get("capability") == "CAP-PLT-AI-001"
        and cat.get("principle") == catmod.PRINCIPLE
        and cat.get("fabric") == catmod.FABRIC
        and "governed enterprise domains" in cat["principle"]
        and cat["domain_map"]["core_domain"] == catmod.CORE_DOMAIN
        and cat["domain_map"]["supporting_count"] >= 11
        and cat["domain_map"]["strategic_count"] >= 3
        and cat["bounded_contexts"]["context_count"] >= 8
        and cat["complete_ai_domain_model_present_required"] is True
        and cat["strategic_ddd_design_present_required"] is True
        and cat["core_domain_defined_required"] is True
        and cat["supporting_domains_defined_required"] is True
        and cat["bounded_contexts_present_required"] is True
        and cat["aggregates_defined_required"] is True
        and cat["entities_defined_required"] is True
        and cat["value_objects_defined_required"] is True
        and cat["domain_events_present_required"] is True
        and cat["microservice_mapping_present_required"] is True
        and cat["integration_boundaries_clear_required"] is True
        and cat["governance_model_present_required"] is True
        and cat["sibling_ai_bc_forbidden"] is True
        and cat["tactical_ddd"]["aggregate_count"] >= 6
        and cat["tactical_ddd"]["entity_count"] >= 20
        and cat["events"]["core_event_count"] >= 9
        and cat["microservice_mapping"]["service_count"] >= 9
        and cat["knowledge_domain"]["via_p213_l"] is True
        and cat["data_domain"]["via_p212"] is True
        and cat["security_domain"]["via_p210"] is True
        and cat["integration"]["via_p214_a"] is True
        and cat["integration"]["via_p214_b"] is True
        and cat["cqrs"]["command_count"] >= 10
        and cat["cursor_outputs"]["count"] >= 16
        and "complete_ai_domain_model_is_missing"
        in cat["quality_gates"]["reject_if"]
        and "P214-B" in cat["builds_on"]
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )

    def _bad(fn, **kwargs):
        try:
            fn(**kwargs)
            return True
        except ValueError:
            return False

    checks = [
        not _bad(
            AiDomainMapRoot.publish,
            tenant_id="t1",
            map_ref="m1",
            complete=False,
        )
        and AiDomainMapRoot.publish(
            tenant_id="t1", map_ref="m2"
        ).is_incomplete()
        is False,
        not _bad(
            AiBoundedContextsRoot.enable,
            tenant_id="t1",
            context_ref="c1",
            present=False,
        )
        and AiBoundedContextsRoot.enable(
            tenant_id="t1", context_ref="c2"
        ).is_missing()
        is False,
        not _bad(
            AiAggregatesDefinedRoot.publish,
            tenant_id="t1",
            aggregate_ref="a1",
            defined=False,
        )
        and AiAggregatesDefinedRoot.publish(
            tenant_id="t1", aggregate_ref="a2"
        ).is_undefined()
        is False,
        not _bad(
            AiEventsPresentRoot.enable,
            tenant_id="t1",
            events_ref="e1",
            present=False,
        )
        and AiEventsPresentRoot.enable(
            tenant_id="t1", events_ref="e2"
        ).is_missing()
        is False,
        not _bad(
            AiMicroserviceBoundariesRoot.publish,
            tenant_id="t1",
            boundary_ref="b1",
            clear=False,
        )
        and AiMicroserviceBoundariesRoot.publish(
            tenant_id="t1", boundary_ref="b2"
        ).is_unclear()
        is False,
        not _bad(
            AiIntegrationBoundariesRoot.publish,
            tenant_id="t1",
            integration_ref="i1",
            clear=False,
        )
        and AiIntegrationBoundariesRoot.publish(
            tenant_id="t1", integration_ref="i2"
        ).is_unclear()
        is False,
    ]
    aggregates_ok = all(checks)

    acl_path = root / "backend/contexts/ai/infrastructure/acl/ai_domain_acl.py"
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_p207" in acl_text
        and "via_p208" in acl_text
        and "via_p209" in acl_text
        and "via_p210" in acl_text
        and "via_p211" in acl_text
        and "via_p212" in acl_text
        and "via_p213_l" in acl_text
        and "via_p214_a" in acl_text
        and "via_p214_b" in acl_text
        and "module_local_llm_sdk_forbidden" in acl_text
    )

    router = (
        root / "backend/contexts/ai/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@router.get("/domain")' in router
        and "/domain/readiness" in router
        and "/domain/map" in router
        and "/domain/bounded-contexts" in router
        and "/domain/microservices" in router
        and "/domain/events" in router
        and "/domain/governance" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_AI_DOMAIN_ARCHITECTURE.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never Complete AI domain model is missing" in law
        and "Never Strategic DDD design is missing" in law
        and "Never Core domain is undefined" in law
        and "Never Supporting domains are missing" in law
        and "Never Bounded contexts are missing" in law
        and "Never Aggregates are undefined" in law
        and "Never Entities are undefined" in law
        and "Never Value objects are undefined" in law
        and "Never Domain events are missing" in law
        and "Never Microservice mapping is missing" in law
        and "Never Integration boundaries are unclear" in law
        and "Never Governance model is missing" in law
        and "Never Sibling AI BC" in law
        and "MEOS Enterprise AI Domain Model" in law
        and "governed enterprise domains" in law
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
        "prompt": "P214-C",
        "adr": 423,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "catalog": catalog_ok,
        "aggregates": aggregates_ok,
        "acl": acl_ok,
        "router": router_ok,
        "documentation": doc_ok,
        "sor": "ai",
        "capability": "CAP-PLT-AI-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
