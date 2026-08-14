"""Cyber Security P210-H Threat Intelligence foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/368-enterprise-cyber-security-threat-intelligence.md",
    "docs/architecture/ENTERPRISE_CYBER_SECURITY_THREAT_INTELLIGENCE.md",
    "docs/architecture/cyber_security/CYBER_INTEL_CAPABILITIES.v1.yaml",
    "docs/architecture/cyber_security/CYBER_INTEL_DDD_CQRS.v1.yaml",
    "docs/architecture/cyber_security/CYBER_INTEL_SECURITY.v1.yaml",
    "docs/architecture/cyber_security/CYBER_INTEL_VALIDATION.v1.yaml",
    "backend/contexts/cyber_security/domain/services/cs_platform_intel.py",
    "backend/contexts/cyber_security/domain/aggregates/cs_intel_aggregates.py",
    "backend/contexts/cyber_security/infrastructure/acl/cs_intel_acl.py",
    "backend/contexts/cyber_security/application/cs_intel_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/threat_intel",
    "backend/contexts/threat_hunting",
    "backend/contexts/cti_platform",
    "backend/contexts/siem_platform",
    "backend/contexts/soar_platform",
    "backend/contexts/soc_platform",
    "backend/contexts/xdr",
)


def validate_cs_intel_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.cyber_security.domain.aggregates.cs_intel_aggregates import (
        CsIntelAttributionRoot,
        CsIntelCampaignDetectedRoot,
        CsIntelConnectedDetectionRoot,
        CsIntelExplainableAiRoot,
        CsIntelKnowledgeGraphRoot,
        CsIntelProactiveHuntRoot,
        CsIntelStandardsSharingRoot,
        CsIntelValidatedRoot,
    )
    from contexts.cyber_security.domain.services import cs_platform_intel as intel

    cat = intel.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P210-H"
        and cat.get("adr") == 368
        and cat.get("sor") == "cyber_security"
        and cat["threat_intelligence_validated_required"] is True
        and cat["threat_hunting_proactive_required"] is True
        and cat["knowledge_graph_integration_required"] is True
        and cat["ai_recommendations_explainable_required"] is True
        and cat["detection_engineering_connected_required"] is True
        and cat["intelligence_sharing_standards_required"] is True
        and cat["threat_actor_attribution_supported_required"] is True
        and cat["validation"]["not_unvalidated"] is True
        and cat["threat_hunting"]["not_reactive_only"] is True
        and cat["knowledge_graph"]["not_absent"] is True
        and cat["ai"]["not_unexplainable"] is True
        and cat["detection_engineering"]["not_disconnected"] is True
        and cat["intelligence_sharing"]["not_lacking_standards"] is True
        and cat["threat_entities"]["not_unsupported_attribution"] is True
        and cat["architecture"]["layer_count"] >= 10
        and cat["sources"]["source_count"] >= 15
        and cat["cqrs"]["event_count"] >= 8
        and cat["cursor_outputs"]["count"] >= 20
        and "threat_intelligence_cannot_be_validated"
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
            CsIntelValidatedRoot.validate,
            tenant_id="t1",
            intel_ref="i1",
            validated=False,
        )
        and CsIntelValidatedRoot.validate(
            tenant_id="t1", intel_ref="i2"
        ).is_unvalidated()
        is False
    )
    checks.append(
        not _bad(
            CsIntelProactiveHuntRoot.launch,
            tenant_id="t1",
            hunt_ref="h1",
            proactive=False,
        )
        and CsIntelProactiveHuntRoot.launch(
            tenant_id="t1", hunt_ref="h2"
        ).is_reactive_only()
        is False
    )
    checks.append(
        not _bad(
            CsIntelKnowledgeGraphRoot.bind,
            tenant_id="t1",
            graph_ref="g1",
            integrated=False,
        )
        and CsIntelKnowledgeGraphRoot.bind(
            tenant_id="t1", graph_ref="g2"
        ).is_absent()
        is False
    )
    checks.append(
        not _bad(
            CsIntelExplainableAiRoot.advise,
            tenant_id="t1",
            advisory_ref="a1",
            explainable=False,
        )
        and CsIntelExplainableAiRoot.advise(
            tenant_id="t1", advisory_ref="a2"
        ).is_unexplainable()
        is False
    )
    checks.append(
        not _bad(
            CsIntelConnectedDetectionRoot.publish,
            tenant_id="t1",
            pack_ref="p1",
            connected=False,
        )
        and CsIntelConnectedDetectionRoot.publish(
            tenant_id="t1", pack_ref="p2"
        ).is_disconnected()
        is False
    )
    checks.append(
        not _bad(
            CsIntelStandardsSharingRoot.publish,
            tenant_id="t1",
            channel_ref="c1",
            standards_based=False,
        )
        and CsIntelStandardsSharingRoot.publish(
            tenant_id="t1", channel_ref="c2"
        ).lacks_standards()
        is False
    )
    checks.append(
        not _bad(
            CsIntelAttributionRoot.register,
            tenant_id="t1",
            actor_ref="act1",
            attribution_supported=False,
        )
        and CsIntelAttributionRoot.register(
            tenant_id="t1", actor_ref="act2"
        ).is_unsupported()
        is False
    )
    camp = CsIntelCampaignDetectedRoot.detect(
        tenant_id="t1", campaign_ref="camp1", actor_ref="act3"
    )
    checks.append("CampaignDetected" in camp.pending_events)
    aggregates_ok = all(checks)

    acl_path = (
        root / "backend/contexts/cyber_security/infrastructure/acl/cs_intel_acl.py"
    )
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_p210_e_siem" in acl_text
        and "via_p210_g_xdr" in acl_text
        and "explainable_required" in acl_text
        and "stix_taxii" in acl_text
        and "via_knowledge_graph" in acl_text
    )

    router = (
        root / "backend/contexts/cyber_security/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '/intel"' in router
        and "/intel/hunting" in router
        and "/intel/sharing" in router
        and "/intel/detection-engineering" in router
        and "/intel/readiness" in router
    )

    law = (
        root
        / "docs/architecture/ENTERPRISE_CYBER_SECURITY_THREAT_INTELLIGENCE.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never threat intelligence cannot be validated" in law
        and "Never threat hunting is reactive only" in law
        and "Never knowledge graph integration is absent" in law
        and "Never AI cannot explain recommendations" in law
        and "Never detection engineering is disconnected" in law
        and "Never intelligence sharing lacks standards" in law
        and "Never threat actor attribution is unsupported" in law
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
        "prompt": "P210-H",
        "adr": 368,
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
