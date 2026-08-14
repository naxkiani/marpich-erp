"""AI P214-R Ecosystem Marketplace / Capability Exchange foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/438-enterprise-ai-aimarket.md",
    "docs/architecture/ENTERPRISE_AI_AIMARKET.md",
    "docs/architecture/enterprise_ai/AI_AIMARKET_CAPABILITIES.v1.yaml",
    "docs/architecture/enterprise_ai/AI_AIMARKET_DDD_CQRS.v1.yaml",
    "docs/architecture/enterprise_ai/AI_AIMARKET_SECURITY.v1.yaml",
    "docs/architecture/enterprise_ai/AI_AIMARKET_VALIDATION.v1.yaml",
    "backend/contexts/ai/domain/services/ai_platform_aimarket.py",
    "backend/contexts/ai/domain/aggregates/ai_aimarket_aggregates.py",
    "backend/contexts/ai/infrastructure/acl/ai_aimarket_acl.py",
    "backend/contexts/ai/application/ai_aimarket_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/ai_marketplace",
    "backend/contexts/capability_exchange",
    "backend/contexts/ai_economy_platform",
    "backend/contexts/ai_service_marketplace",
    "backend/contexts/ai_model_marketplace",
    "backend/contexts/ai_agent_marketplace",
    "backend/contexts/ai_plugin_marketplace",
)


def validate_ai_aimarket_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.ai.domain.aggregates.ai_aimarket_aggregates import (
        AgentExchangeRoot,
        CapabilityRegistryRoot,
        EconomyRoot,
        MarketplaceDigitalTwinRoot,
        MarketplaceRoot,
        ModelExchangeRoot,
        PluginMarketplaceRoot,
        ServiceCatalogRoot,
    )
    from contexts.ai.domain.services import ai_platform_aimarket as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P214-R"
        and cat.get("adr") == 438
        and cat.get("sor") == "ai"
        and cat.get("capability") == "CAP-PLT-AI-001"
        and cat.get("principle") == catmod.PRINCIPLE
        and cat.get("fabric") == catmod.FABRIC
        and "discoverable, governed and reusable enterprise intelligence assets" in cat["principle"]
        and cat["domain_model"]["core_domain"] == catmod.CORE_DOMAIN
        and cat["domain_model"]["supporting_count"] >= 9
        and cat["bounded_contexts"]["context_count"] >= 7
        and cat["enterprise_ai_marketplace_present_required"] is True
        and cat["ai_capability_registry_present_required"] is True
        and cat["ai_model_exchange_present_required"] is True
        and cat["ai_agent_marketplace_present_required"] is True
        and cat["ai_service_marketplace_present_required"] is True
        and cat["ai_plugin_marketplace_present_required"] is True
        and cat["ai_economy_platform_present_required"] is True
        and cat["ai_trust_ranking_present_required"] is True
        and cat["knowledge_graph_integration_present_required"] is True
        and cat["digital_twin_integration_present_required"] is True
        and cat["cqrs_architecture_present_required"] is True
        and cat["event_architecture_present_required"] is True
        and cat["microservices_architecture_present_required"] is True
        and cat["api_first_architecture_present_required"] is True
        and cat["zero_trust_security_present_required"] is True
        and cat["cloud_native_deployment_present_required"] is True
        and cat["sibling_ai_bc_forbidden"] is True
        and cat["plugin_marketplace_via_platform_required"] is True
        and cat["deepens_p214_q_economy_layer"] is True
        and cat["governed_by_p214_p"] is True
        and cat["models"]["via_p214_l"] is True
        and cat["agents"]["via_p214_f"] is True
        and cat["agents"]["via_p214_q"] is True
        and cat["services"]["via_p214_m"] is True
        and cat["plugins"]["via_plugin_platform"] is True
        and cat["trust_rating"]["via_p214_p"] is True
        and cat["trust_rating"]["via_p214_o"] is True
        and cat["knowledge_graph"]["via_p214_g"] is True
        and cat["cqrs"]["command_count"] >= 6
        and cat["events"]["core_event_count"] >= 8
        and cat["microservices"]["service_count"] >= 10
        and cat["cursor_outputs"]["count"] >= 20
        and "enterprise_ai_marketplace_is_missing" in cat["quality_gates"]["reject_if"]
        and "P214-Q" in cat["builds_on"]
        and "P214-P" in cat["builds_on"]
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )

    def _bad(fn, **kwargs):
        try:
            fn(**kwargs)
            return True
        except ValueError:
            return False

    checks = [
        not _bad(MarketplaceRoot.enable, tenant_id="t1", marketplace_ref="m1", present=False)
        and MarketplaceRoot.enable(tenant_id="t1", marketplace_ref="m2").is_missing() is False,
        not _bad(CapabilityRegistryRoot.enable, tenant_id="t1", capability_ref="c1", present=False)
        and CapabilityRegistryRoot.enable(tenant_id="t1", capability_ref="c2").is_missing() is False,
        not _bad(ModelExchangeRoot.enable, tenant_id="t1", model_ref="mo1", present=False)
        and ModelExchangeRoot.enable(tenant_id="t1", model_ref="mo2").is_missing() is False,
        not _bad(AgentExchangeRoot.enable, tenant_id="t1", agent_ref="a1", present=False)
        and AgentExchangeRoot.enable(tenant_id="t1", agent_ref="a2").is_missing() is False,
        not _bad(ServiceCatalogRoot.enable, tenant_id="t1", service_ref="s1", present=False)
        and ServiceCatalogRoot.enable(tenant_id="t1", service_ref="s2").is_missing() is False,
        not _bad(PluginMarketplaceRoot.enable, tenant_id="t1", plugin_ref="p1", present=False)
        and PluginMarketplaceRoot.enable(tenant_id="t1", plugin_ref="p2").is_missing() is False,
        not _bad(EconomyRoot.enable, tenant_id="t1", economy_ref="e1", present=False)
        and EconomyRoot.enable(tenant_id="t1", economy_ref="e2").is_missing() is False,
        not _bad(MarketplaceDigitalTwinRoot.enable, tenant_id="t1", twin_ref="tw1", present=False)
        and MarketplaceDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw2").is_missing() is False,
    ]
    aggregates_ok = all(checks)

    acl_path = root / "backend/contexts/ai/infrastructure/acl/ai_aimarket_acl.py"
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_p207" in acl_text
        and "via_p208" in acl_text
        and "via_p209" in acl_text
        and "via_p210" in acl_text
        and "via_p214_f" in acl_text
        and "via_p214_g" in acl_text
        and "via_p214_l" in acl_text
        and "via_p214_m" in acl_text
        and "via_p214_o" in acl_text
        and "via_p214_p" in acl_text
        and "via_p214_q" in acl_text
        and "via_plugin_platform" in acl_text
        and "via_audit_platform" in acl_text
        and "via_policy_engine" in acl_text
        and "module_local_ai_marketplace_forbidden" in acl_text
    )

    router = (root / "backend/contexts/ai/presentation/router.py").read_text(encoding="utf-8")
    router_ok = (
        '@router.get("/aimarket")' in router
        and "/aimarket/readiness" in router
        and "/aimarket/capabilities" in router
        and "/aimarket/models" in router
        and "/aimarket/agents" in router
        and "/aimarket/plugins" in router
        and "/aimarket/economy" in router
        and "/aimarket/digital-twin" in router
    )

    law = (root / "docs/architecture/ENTERPRISE_AI_AIMARKET.md").read_text(encoding="utf-8")
    doc_ok = (
        "Never Enterprise AI Marketplace is missing" in law
        and "Never AI Capability Registry is missing" in law
        and "Never AI Model Exchange is missing" in law
        and "Never AI Agent Marketplace is missing" in law
        and "Never AI Service Marketplace is missing" in law
        and "Never AI Plugin Marketplace is missing" in law
        and "Never AI Economy Platform is missing" in law
        and "Never AI Trust Ranking is missing" in law
        and "Never Knowledge Graph Integration is missing" in law
        and "Never Digital Twin Integration is missing" in law
        and "Never CQRS architecture is missing" in law
        and "Never Event architecture is missing" in law
        and "Never Microservices architecture is missing" in law
        and "Never API first architecture is missing" in law
        and "Never Zero trust security is missing" in law
        and "Never Cloud native deployment is missing" in law
        and "Never Sibling AI BC" in law
        and "MEOS Intelligent AI Economy Fabric" in law
        and "discoverable, governed and reusable enterprise intelligence assets" in law
        and "Plugin Platform" in law
        and "P214-P" in law
        and "P214-Q" in law
    )

    passed = not missing and not sibling and catalog_ok and aggregates_ok and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P214-R",
        "adr": 438,
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
