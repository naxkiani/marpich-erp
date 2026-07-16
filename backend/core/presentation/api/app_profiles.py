"""Application profiles — subset routers/services for faster startup."""
from __future__ import annotations

CORE_CONTEXTS = frozenset({
    "identity",
    "authorization",
    "permission_registry",
    "authentication",
    "data_isolation",
    "directory",
    "identity_risk",
    "mfa",
    "adaptive_authentication",
    "identity_federation",
    "identity_digital_twin",
    "consent",
    "identity_resilience",
    "identity_lifecycle",
    "core_platform",
    "policy",
    "settings",
    "organization",
    "notifications",
    "audit",
    "documents",
    "integration",
    "media",
    "search",
    "feature_flags",
    "plugins",
    "workflow",
    "localization",
    "ai",
    "messenger",
})

ENTERPRISE_PLATFORM_CONTEXTS = frozenset({
    "ai_governance",
    "enterprise_api_gateway",
    "enterprise_event_bus",
    "enterprise_message_orchestration",
    "enterprise_webhook_platform",
    "enterprise_connector_framework",
    "enterprise_saga_orchestration",
    "enterprise_reliability_platform",
    "enterprise_observability",
    "enterprise_scheduler",
    "enterprise_integration_studio",
    "enterprise_automation_platform",
    "enterprise_integration_security",
    "ai_security",
    "ai_cfo_assistant",
    "natural_language_analytics",
    "financial_data_science",
    "financial_anomaly_detection",
    "enterprise_forecasting",
    "enterprise_decision_support",
    "enterprise_executive_dashboard",
    "financial_ai_analytics",
    "financial_kpi",
    "grc",
    "security",
    "compliance",
    "fraud_detection",
    "data_protection",
    "risk",
    "security_incident",
    "business_continuity",
    "regulatory_reporting",
    "identity_governance",
})

FINANCIAL_CONTEXTS = frozenset({
    "accounting",
    "finance",
    "financial_kernel",
    "treasury",
    "tax",
    "reporting",
})

BANKING_CONTEXTS = frozenset({
    "banking",
    "currency_exchange",
    "digital_exchange",
    "treasury",
})

INDUSTRY_CONTEXTS = frozenset({
    "hospital",
    "clinic",
    "pharmacy",
    "laboratory",
    "municipality",
    "pos",
    "inventory",
    "financial_kernel",
    "accounting",
    "analytics",
    "university",
    "enterprise_connector_framework",
})

# Minimal slice for integration smoke tests.
TEST_CONTEXTS = frozenset({
    "identity",
    "authorization",
    "permission_registry",
    "authentication",
    "data_isolation",
    "directory",
    "identity_risk",
    "mfa",
    "adaptive_authentication",
    "identity_federation",
    "identity_resilience",
    "identity_lifecycle",
    "identity_digital_twin",
    "consent",
    "organization",
    "core_platform",
    "policy",
    "enterprise_api_gateway",
    "enterprise_event_bus",
    "enterprise_message_orchestration",
    "enterprise_webhook_platform",
    "enterprise_connector_framework",
    "enterprise_saga_orchestration",
    "enterprise_reliability_platform",
    "enterprise_observability",
    "enterprise_scheduler",
    "enterprise_integration_studio",
    "enterprise_automation_platform",
    "enterprise_integration_security",
    "enterprise_forecasting",
    "enterprise_executive_dashboard",
    "enterprise_decision_support",
    "ai_governance",
})

PROFILE_LABELS: dict[str, str] = {
    "core": "Core platform shell",
    "enterprise": "Core + enterprise AI/governance platforms",
    "financial": "Core + financial kernel, treasury, tax, reporting",
    "banking": "Core + banking and FX",
    "industry": "Core + vertical industry modules",
    "test": "Minimal routers for platform smoke tests",
    "full": "All bounded contexts",
}


def contexts_for_profile(profile: str) -> frozenset[str] | None:
    """Return allowed context names, or None for full."""
    if profile == "full":
        return None
    if profile == "core":
        return CORE_CONTEXTS
    if profile == "enterprise":
        return CORE_CONTEXTS | ENTERPRISE_PLATFORM_CONTEXTS
    if profile == "financial":
        return CORE_CONTEXTS | FINANCIAL_CONTEXTS
    if profile == "banking":
        return CORE_CONTEXTS | BANKING_CONTEXTS
    if profile == "industry":
        return CORE_CONTEXTS | INDUSTRY_CONTEXTS
    if profile == "test":
        return TEST_CONTEXTS
    raise ValueError(f"Unknown app profile: {profile}")


def context_from_module(module_path: str) -> str:
    return module_path.split(".")[1]


def filter_specs_by_profile(
    specs: list[tuple[str, str]],
    profile: str,
) -> list[tuple[str, str]]:
    allowed = contexts_for_profile(profile)
    if allowed is None:
        return specs
    return [spec for spec in specs if context_from_module(spec[0]) in allowed]


def list_profiles() -> list[dict]:
    return [
        {"profile": name, "label": label}
        for name, label in PROFILE_LABELS.items()
    ]
