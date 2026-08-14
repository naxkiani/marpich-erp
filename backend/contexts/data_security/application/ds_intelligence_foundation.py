"""Data Security P211-K Intelligence graph foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/386-enterprise-data-security-intelligence.md",
    "docs/architecture/ENTERPRISE_DATA_SECURITY_INTELLIGENCE.md",
    "docs/architecture/data_security/DATA_SECURITY_INTELLIGENCE_CAPABILITIES.v1.yaml",
    "docs/architecture/data_security/DATA_SECURITY_INTELLIGENCE_DDD_CQRS.v1.yaml",
    "docs/architecture/data_security/DATA_SECURITY_INTELLIGENCE_SECURITY.v1.yaml",
    "docs/architecture/data_security/DATA_SECURITY_INTELLIGENCE_VALIDATION.v1.yaml",
    "backend/contexts/data_security/domain/services/ds_platform_intelligence.py",
    "backend/contexts/data_security/domain/aggregates/ds_intelligence_aggregates.py",
    "backend/contexts/data_security/infrastructure/acl/ds_intelligence_acl.py",
    "backend/contexts/data_security/application/ds_intelligence_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/data_lineage_platform",
    "backend/contexts/metadata_platform",
    "backend/contexts/data_intelligence_graph",
)


def validate_ds_intelligence_foundation(
    *, repo_root: Path | None = None
) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.data_security.domain.aggregates.ds_intelligence_aggregates import (
        DsAiReasoningRoot,
        DsCompleteMetadataRoot,
        DsImpactAnalysisRoot,
        DsKnownOriginRoot,
        DsLineageBrokenRoot,
        DsQueryableRelationshipsRoot,
        DsSchemaChangedRoot,
        DsVisibleMovementRoot,
    )
    from contexts.data_security.domain.services import (
        ds_platform_intelligence as intel,
    )

    cat = intel.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P211-K"
        and cat.get("adr") == 386
        and cat.get("sor") == "data_security"
        and cat["data_origin_known_required"] is True
        and cat["data_movement_visible_required"] is True
        and cat["metadata_complete_required"] is True
        and cat["relationships_queryable_required"] is True
        and cat["impact_analysis_available_required"] is True
        and cat["ai_reasoning_over_context_required"] is True
        and cat["lineage"]["not_unknown_origin"] is True
        and cat["lineage"]["not_invisible_movement"] is True
        and cat["metadata"]["not_incomplete"] is True
        and cat["knowledge_graph"]["not_unqueryable"] is True
        and cat["impact_analysis"]["not_unavailable"] is True
        and cat["ai_reasoning"]["not_unable_to_reason"] is True
        and cat["architecture"]["layer_count"] >= 8
        and cat["domain"]["context_count"] >= 7
        and cat["cqrs"]["event_count"] >= 6
        and cat["cursor_outputs"]["count"] >= 15
        and "data_origin_is_unknown" in cat["quality_gates"]["reject_if"]
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
            DsKnownOriginRoot.register,
            tenant_id="t1",
            asset_ref="a1",
            known=False,
        )
        and DsKnownOriginRoot.register(
            tenant_id="t1", asset_ref="a2"
        ).is_unknown()
        is False
    )
    checks.append(
        not _bad(
            DsVisibleMovementRoot.track,
            tenant_id="t1",
            lineage_ref="l1",
            visible=False,
        )
        and DsVisibleMovementRoot.track(
            tenant_id="t1", lineage_ref="l2"
        ).is_invisible()
        is False
    )
    checks.append(
        not _bad(
            DsCompleteMetadataRoot.collect,
            tenant_id="t1",
            metadata_ref="m1",
            complete=False,
        )
        and DsCompleteMetadataRoot.collect(
            tenant_id="t1", metadata_ref="m2"
        ).is_incomplete()
        is False
    )
    checks.append(
        not _bad(
            DsQueryableRelationshipsRoot.update,
            tenant_id="t1",
            graph_ref="g1",
            queryable=False,
        )
        and DsQueryableRelationshipsRoot.update(
            tenant_id="t1", graph_ref="g2"
        ).is_unqueryable()
        is False
    )
    checks.append(
        not _bad(
            DsImpactAnalysisRoot.analyze,
            tenant_id="t1",
            analysis_ref="i1",
            available=False,
        )
        and DsImpactAnalysisRoot.analyze(
            tenant_id="t1", analysis_ref="i2"
        ).is_unavailable()
        is False
    )
    checks.append(
        not _bad(
            DsAiReasoningRoot.reason,
            tenant_id="t1",
            reasoning_ref="r1",
            capable=False,
        )
        and DsAiReasoningRoot.reason(
            tenant_id="t1", reasoning_ref="r2"
        ).is_unable()
        is False
    )
    broken = DsLineageBrokenRoot.detect(tenant_id="t1", break_ref="b1")
    schema = DsSchemaChangedRoot.record(tenant_id="t1", schema_ref="s1")
    checks.append("LineageBroken" in broken.pending_events)
    checks.append("SchemaChanged" in schema.pending_events)
    aggregates_ok = all(checks)

    acl_path = (
        root
        / "backend/contexts/data_security/infrastructure/acl/ds_intelligence_acl.py"
    )
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_p211_d_discovery" in acl_text
        and "via_enterprise_search" in acl_text
        and "module_local_search_forbidden" in acl_text
        and "ai_reasoning_over_context_required" in acl_text
        and "impact_analysis_available_required" in acl_text
        and "via_p211_j_protection" in acl_text
    )

    router = (
        root / "backend/contexts/data_security/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@data_security_router.get("/intelligence")' in router
        and "/intelligence/lineage" in router
        and "/intelligence/metadata" in router
        and "/intelligence/impact" in router
        and "/intelligence/readiness" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_DATA_SECURITY_INTELLIGENCE.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never Data origin is unknown" in law
        and "Never Data movement is invisible" in law
        and "Never Metadata is incomplete" in law
        and "Never Relationships cannot be queried" in law
        and "Never Impact analysis is unavailable" in law
        and "Never AI cannot reason over data context" in law
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
        "prompt": "P211-K",
        "adr": 386,
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
