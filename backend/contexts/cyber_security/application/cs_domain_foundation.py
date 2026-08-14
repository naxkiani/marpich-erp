"""Cyber Security P210-C Domain Architecture foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/363-enterprise-cyber-security-domain.md",
    "docs/architecture/ENTERPRISE_CYBER_SECURITY_DOMAIN.md",
    "docs/architecture/cyber_security/CYBER_DOMAIN_CAPABILITIES.v1.yaml",
    "docs/architecture/cyber_security/CYBER_DOMAIN_DDD_CQRS.v1.yaml",
    "docs/architecture/cyber_security/CYBER_DOMAIN_SECURITY.v1.yaml",
    "docs/architecture/cyber_security/CYBER_DOMAIN_VALIDATION.v1.yaml",
    "backend/contexts/cyber_security/domain/services/cs_platform_domain.py",
    "backend/contexts/cyber_security/domain/aggregates/cs_domain_aggregates.py",
    "backend/contexts/cyber_security/infrastructure/acl/cs_domain_acl.py",
    "backend/contexts/cyber_security/application/cs_domain_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/cyber_defense",
    "backend/contexts/soc_platform",
    "backend/contexts/siem_platform",
    "backend/contexts/soar_platform",
    "backend/contexts/xdr",
    "backend/contexts/threat_detection",
    "backend/contexts/security_ops",
)


def validate_cs_domain_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.cyber_security.domain.aggregates.cs_domain_aggregates import (
        CsAclPresentRoot,
        CsAggregateBoundaryRoot,
        CsDigitalTwinLinkRoot,
        CsDomainDrivenEventsRoot,
        CsKnowledgeGraphRequiredRoot,
        CsNoRuleLeakRoot,
        CsNonOverlappingContextsRoot,
        CsOwnershipClearRoot,
    )
    from contexts.cyber_security.domain.services import cs_platform_domain as pdom

    cat = pdom.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P210-C"
        and cat.get("adr") == 363
        and cat.get("sor") == "cyber_security"
        and cat["bounded_contexts_overlap_forbidden"] is True
        and cat["aggregates_consistency_boundary_required"] is True
        and cat["domain_ownership_clear_required"] is True
        and cat["business_rules_leak_across_contexts_forbidden"] is True
        and cat["events_domain_driven_required"] is True
        and cat["knowledge_graph_integration_required"] is True
        and cat["anti_corruption_layers_required"] is True
        and cat["bounded_contexts"]["not_overlapping"] is True
        and cat["aggregates"]["not_violating_consistency"] is True
        and cat["context_map"]["not_unclear_ownership"] is True
        and cat["context_map"]["not_leaking_rules"] is True
        and cat["domain_events"]["not_non_domain_driven"] is True
        and cat["knowledge_graph"]["not_missing"] is True
        and cat["anti_corruption_layers"]["not_absent"] is True
        and cat["bounded_contexts"]["count"] >= 10
        and cat["aggregates"]["count"] >= 10
        and cat["cqrs"]["event_count"] >= 12
        and cat["cursor_outputs"]["count"] >= 20
        and "bounded_contexts_overlap" in cat["quality_gates"]["reject_if"]
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )

    def _bad(fn, **kwargs):
        try:
            fn(**kwargs)
            return True
        except ValueError:
            return False

    o_bad = _bad(
        CsNonOverlappingContextsRoot.register,
        tenant_id="t1",
        map_ref="m1",
        overlapping=True,
        context_count=3,
    )
    contexts = CsNonOverlappingContextsRoot.register(tenant_id="t1", map_ref="m2")
    o_ok = not o_bad and contexts.is_overlapping() is False

    a_bad = _bad(
        CsAggregateBoundaryRoot.define,
        tenant_id="t1",
        aggregate_ref="a1",
        consistency_ok=False,
    )
    agg = CsAggregateBoundaryRoot.define(tenant_id="t1", aggregate_ref="a2")
    a_ok = not a_bad and agg.violates_consistency() is False

    own_bad = _bad(
        CsOwnershipClearRoot.declare,
        tenant_id="t1",
        ownership_ref="o1",
        clear=False,
    )
    own = CsOwnershipClearRoot.declare(tenant_id="t1", ownership_ref="o2")
    own_ok = not own_bad and own.is_unclear() is False

    leak_bad = _bad(
        CsNoRuleLeakRoot.bind, tenant_id="t1", contract_ref="c1", leaking=True
    )
    leak = CsNoRuleLeakRoot.bind(tenant_id="t1", contract_ref="c2")
    leak_ok = not leak_bad and leak.is_leaking() is False

    evt_bad = _bad(
        CsDomainDrivenEventsRoot.publish,
        tenant_id="t1",
        catalog_ref="e1",
        domain_driven=False,
    )
    evt = CsDomainDrivenEventsRoot.publish(tenant_id="t1", catalog_ref="e2")
    evt_ok = not evt_bad and evt.is_non_domain_driven() is False

    kg_bad = _bad(
        CsKnowledgeGraphRequiredRoot.declare,
        tenant_id="t1",
        link_ref="k1",
        integrated=False,
    )
    kg = CsKnowledgeGraphRequiredRoot.declare(tenant_id="t1", link_ref="k2")
    kg_ok = not kg_bad and kg.is_missing() is False

    acl_bad = _bad(
        CsAclPresentRoot.register, tenant_id="t1", acl_ref="x1", present=False
    )
    acl = CsAclPresentRoot.register(tenant_id="t1", acl_ref="x2")
    acl_agg_ok = not acl_bad and acl.is_absent() is False

    twin = CsDigitalTwinLinkRoot.declare(tenant_id="t1", twin_ref="tw1")
    twin_ok = "DigitalTwinLinkDeclared" in twin.pending_events

    aggregates_ok = (
        o_ok and a_ok and own_ok and leak_ok and evt_ok and kg_ok and acl_agg_ok and twin_ok
    )

    acl_path = root / "backend/contexts/cyber_security/infrastructure/acl/cs_domain_acl.py"
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "ir_lifecycle_owned_by_security_incident" in acl_text
        and "via_knowledge_graph" in acl_text
        and "via_digital_twin" in acl_text
        and "via_p207" in acl_text
        and "via_p209" in acl_text
    )

    router = (
        root / "backend/contexts/cyber_security/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '/domain"' in router
        and "/domain/bounded-contexts" in router
        and "/domain/context-map" in router
        and "/domain/knowledge-graph" in router
        and "/domain/readiness" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_CYBER_SECURITY_DOMAIN.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never bounded contexts overlap" in law
        and "Never aggregates violate consistency boundaries" in law
        and "Never domain ownership is unclear" in law
        and "Never business rules leak across contexts" in law
        and "Never events are not domain-driven" in law
        and "Never knowledge graph integration is missing" in law
        and "Never anti-corruption layers are absent" in law
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
        "prompt": "P210-C",
        "adr": 363,
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
