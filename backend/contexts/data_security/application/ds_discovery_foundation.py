"""Data Security P211-D Discovery / inventory foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/379-enterprise-data-security-discovery-inventory.md",
    "docs/architecture/ENTERPRISE_DATA_SECURITY_DISCOVERY.md",
    "docs/architecture/data_security/DATA_SECURITY_DISCOVERY_CAPABILITIES.v1.yaml",
    "docs/architecture/data_security/DATA_SECURITY_DISCOVERY_DDD_CQRS.v1.yaml",
    "docs/architecture/data_security/DATA_SECURITY_DISCOVERY_SECURITY.v1.yaml",
    "docs/architecture/data_security/DATA_SECURITY_DISCOVERY_VALIDATION.v1.yaml",
    "backend/contexts/data_security/domain/services/ds_platform_discovery.py",
    "backend/contexts/data_security/domain/aggregates/ds_discovery_aggregates.py",
    "backend/contexts/data_security/infrastructure/acl/ds_discovery_acl.py",
    "backend/contexts/data_security/application/ds_discovery_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/data_discovery",
    "backend/contexts/data_inventory",
    "backend/contexts/metadata_platform",
    "backend/contexts/shadow_data",
    "backend/contexts/dspm",
)


def validate_ds_discovery_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.data_security.domain.aggregates.ds_discovery_aggregates import (
        DsAiDiscoveryRoot,
        DsAnalyzableRelationshipsRoot,
        DsAvailableMetadataRoot,
        DsCompleteInventoryRoot,
        DsDeterminableOwnershipRoot,
        DsDiscoverableAssetsRoot,
        DsDiscoveryJobRoot,
        DsVisibleShadowDataRoot,
    )
    from contexts.data_security.domain.services import (
        ds_platform_discovery as disc,
    )

    cat = disc.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P211-D"
        and cat.get("adr") == 379
        and cat.get("sor") == "data_security"
        and cat["data_assets_discoverable_required"] is True
        and cat["inventory_complete_required"] is True
        and cat["metadata_available_required"] is True
        and cat["ownership_determinable_required"] is True
        and cat["shadow_data_visible_required"] is True
        and cat["ai_discovery_required"] is True
        and cat["relationships_analyzable_required"] is True
        and cat["inventory"]["not_undiscoverable"] is True
        and cat["inventory"]["not_incomplete"] is True
        and cat["metadata"]["not_unavailable"] is True
        and cat["ownership"]["not_undeterminable"] is True
        and cat["shadow_data"]["not_invisible"] is True
        and cat["ai_discovery"]["not_missing"] is True
        and cat["knowledge_graph"]["not_unanalyzable"] is True
        and cat["architecture"]["layer_count"] >= 8
        and cat["connectors"]["connector_count"] >= 20
        and cat["cqrs"]["event_count"] >= 10
        and cat["cursor_outputs"]["count"] >= 18
        and "data_assets_cannot_be_discovered" in cat["quality_gates"]["reject_if"]
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
            DsDiscoverableAssetsRoot.register,
            tenant_id="t1",
            asset_ref="a1",
            discoverable=False,
        )
        and DsDiscoverableAssetsRoot.register(
            tenant_id="t1", asset_ref="a2"
        ).is_undiscoverable()
        is False
    )
    checks.append(
        not _bad(
            DsCompleteInventoryRoot.update,
            tenant_id="t1",
            inventory_ref="i1",
            complete=False,
        )
        and DsCompleteInventoryRoot.update(
            tenant_id="t1", inventory_ref="i2"
        ).is_incomplete()
        is False
    )
    checks.append(
        not _bad(
            DsAvailableMetadataRoot.collect,
            tenant_id="t1",
            metadata_ref="m1",
            available=False,
        )
        and DsAvailableMetadataRoot.collect(
            tenant_id="t1", metadata_ref="m2"
        ).is_unavailable()
        is False
    )
    checks.append(
        not _bad(
            DsDeterminableOwnershipRoot.determine,
            tenant_id="t1",
            asset_ref="a3",
            determinable=False,
        )
        and DsDeterminableOwnershipRoot.determine(
            tenant_id="t1", asset_ref="a4"
        ).is_undeterminable()
        is False
    )
    checks.append(
        not _bad(
            DsVisibleShadowDataRoot.detect,
            tenant_id="t1",
            shadow_ref="s1",
            visible=False,
        )
        and DsVisibleShadowDataRoot.detect(
            tenant_id="t1", shadow_ref="s2"
        ).is_invisible()
        is False
    )
    checks.append(
        not _bad(
            DsAiDiscoveryRoot.enable,
            tenant_id="t1",
            capability_ref="c1",
            present=False,
        )
        and DsAiDiscoveryRoot.enable(
            tenant_id="t1", capability_ref="c2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DsAnalyzableRelationshipsRoot.analyze,
            tenant_id="t1",
            graph_ref="g1",
            analyzable=False,
        )
        and DsAnalyzableRelationshipsRoot.analyze(
            tenant_id="t1", graph_ref="g2"
        ).is_unanalyzable()
        is False
    )
    job = DsDiscoveryJobRoot.start(tenant_id="t1", job_ref="j1")
    checks.append("DiscoveryStarted" in job.pending_events)
    aggregates_ok = all(checks)

    acl_path = (
        root
        / "backend/contexts/data_security/infrastructure/acl/ds_discovery_acl.py"
    )
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_integration_platform" in acl_text
        and "ai_discovery_required" in acl_text
        and "shadow_data_visible_required" in acl_text
        and "via_p209" in acl_text
        and "vendor_sdk_embed_forbidden" in acl_text
    )

    router = (
        root / "backend/contexts/data_security/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@data_security_router.get("/discovery")' in router
        and "/discovery/inventory" in router
        and "/discovery/shadow-data" in router
        and "/discovery/ai" in router
        and "/discovery/readiness" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_DATA_SECURITY_DISCOVERY.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never Data assets cannot be discovered" in law
        and "Never Inventory is incomplete" in law
        and "Never Metadata is unavailable" in law
        and "Never Ownership cannot be determined" in law
        and "Never Shadow data remains invisible" in law
        and "Never AI discovery capability is missing" in law
        and "Never Data relationships cannot be analyzed" in law
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
        "prompt": "P211-D",
        "adr": 379,
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
