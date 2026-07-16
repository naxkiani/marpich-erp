"""Lazy startup registry — routers and services loaded on demand."""
from __future__ import annotations

import importlib
from typing import TYPE_CHECKING

from core.presentation.api.app_profiles import filter_specs_by_profile

if TYPE_CHECKING:
    from fastapi import FastAPI

API_PREFIX = "/api/v1"

# Eager-loaded at startup in lazy mode (auth, policy, platform shell).
CORE_SERVICE_SPECS: list[tuple[str, str]] = [
    ("contexts.identity.container", "get_identity_service"),
    ("contexts.authorization.container", "get_authorization_service"),
    ("contexts.permission_registry.container", "get_permission_registry_service"),
    ("contexts.authentication.container", "get_authentication_service"),
    ("contexts.data_isolation.container", "get_data_isolation_service"),
    ("contexts.directory.container", "get_directory_service"),
    ("contexts.mfa.container", "get_mfa_service"),
    ("contexts.adaptive_authentication.container", "get_adaptive_auth_service"),
    ("contexts.identity_federation.container", "get_identity_federation_service"),
    ("contexts.identity_digital_twin.container", "get_identity_digital_twin_service"),
    ("contexts.consent.container", "get_consent_service"),
    ("contexts.identity_federation.container", "get_fabric_security_service"),
    ("contexts.identity_federation.container", "get_fabric_intelligence_service"),
    ("contexts.identity_federation.container", "get_identity_federation_ai_service"),
    ("contexts.identity_federation.container", "get_federation_trust_facts"),
    ("contexts.identity_risk.container", "get_identity_risk_service"),
    ("contexts.identity_resilience.container", "get_identity_resilience_service"),
    ("contexts.identity_lifecycle.container", "get_identity_lifecycle_service"),
    ("contexts.identity_lifecycle.container", "get_registration_onboarding_service"),
    ("contexts.policy.container", "get_policy_service"),
    ("contexts.core_platform.container", "get_platform_service"),
]

ALL_SERVICE_SPECS: list[tuple[str, str]] = [
    ("contexts.accounting.container", "get_accounting_service"),
    ("contexts.finance.container", "get_finance_service"),
    ("contexts.notifications.container", "get_notification_service"),
    ("contexts.settings.container", "get_settings_service"),
    ("contexts.organization.container", "get_organization_service"),
    ("contexts.audit.container", "get_audit_service"),
    ("contexts.audit.container", "get_enterprise_audit_service"),
    ("contexts.documents.container", "get_documents_service"),
    ("contexts.workflow.container", "get_workflow_service"),
    ("contexts.workflow.container", "get_workflow_designer_service"),
    ("contexts.workflow.container", "get_approval_matrix_service"),
    ("contexts.workflow.container", "get_exception_management_service"),
    ("contexts.workflow.container", "get_event_driven_workflow_service"),
    ("contexts.workflow.container", "get_workflow_security_service"),
    ("contexts.workflow.container", "get_workflow_analytics_service"),
    ("contexts.workflow.container", "get_process_library_service"),
    ("contexts.integration.container", "get_integration_service"),
    ("contexts.media.container", "get_media_service"),
    ("contexts.analytics.container", "get_analytics_service"),
    ("contexts.analytics.container", "get_executive_dashboard_service"),
    ("contexts.analytics.container", "get_kpi_platform_service"),
    ("contexts.search.container", "get_search_service"),
    ("contexts.messenger.container", "get_messenger_service"),
    ("contexts.ai.container", "get_ai_service"),
    ("contexts.clinic.container", "get_clinic_service"),
    ("contexts.university.container", "get_university_service"),
    ("contexts.municipality.container", "get_municipality_service"),
    ("contexts.pos.container", "get_pos_service"),
    ("contexts.inventory.container", "get_inventory_service"),
    ("contexts.localization.container", "get_localization_service"),
    ("contexts.policy.container", "get_policy_service"),
    ("contexts.policy.container", "get_enterprise_policy_service"),
    ("contexts.compliance.container", "get_compliance_service"),
    ("contexts.compliance.container", "get_enterprise_compliance_service"),
    ("contexts.fraud_detection.container", "get_fraud_detection_service"),
    ("contexts.data_protection.container", "get_data_protection_service"),
    ("contexts.risk.container", "get_risk_service"),
    ("contexts.security_incident.container", "get_security_incident_service"),
    ("contexts.business_continuity.container", "get_business_continuity_service"),
    ("contexts.regulatory_reporting.container", "get_enterprise_regulatory_reporting_service"),
    ("contexts.identity_governance.container", "get_identity_governance_service"),
    ("contexts.enterprise_executive_dashboard.container", "get_enterprise_executive_dashboard_service"),
    ("contexts.enterprise_decision_support.container", "get_enterprise_decision_support_service"),
    ("contexts.financial_data_science.container", "get_financial_data_science_service"),
    ("contexts.natural_language_analytics.container", "get_natural_language_analytics_service"),
    ("contexts.ai_governance.container", "get_ai_governance_service"),
    ("contexts.enterprise_api_gateway.container", "get_enterprise_api_gateway_service"),
    ("contexts.enterprise_event_bus.container", "get_enterprise_event_bus_service"),
    ("contexts.enterprise_message_orchestration.container", "get_enterprise_message_orchestration_service"),
    ("contexts.enterprise_webhook_platform.container", "get_enterprise_webhook_platform_service"),
    ("contexts.enterprise_connector_framework.container", "get_enterprise_connector_framework_service"),
    ("contexts.enterprise_saga_orchestration.container", "get_enterprise_saga_orchestration_service"),
    ("contexts.enterprise_reliability_platform.container", "get_enterprise_reliability_platform_service"),
    ("contexts.enterprise_observability.container", "get_enterprise_observability_service"),
    ("contexts.enterprise_scheduler.container", "get_enterprise_scheduler_service"),
    ("contexts.enterprise_integration_studio.container", "get_enterprise_integration_studio_service"),
    ("contexts.enterprise_automation_platform.container", "get_enterprise_automation_platform_service"),
    ("contexts.enterprise_integration_security.container", "get_enterprise_integration_security_service"),
    ("contexts.financial_anomaly_detection.container", "get_financial_anomaly_detection_service"),
    ("contexts.enterprise_forecasting.container", "get_enterprise_forecasting_service"),
    ("contexts.ai_cfo_assistant.container", "get_ai_cfo_service"),
    ("contexts.ai_security.container", "get_ai_security_service"),
    ("contexts.financial_ai_analytics.container", "get_financial_ai_analytics_service"),
    ("contexts.financial_kpi.container", "get_financial_kpi_service"),
    ("contexts.grc.container", "get_grc_service"),
    ("contexts.security.container", "get_security_service"),
    ("contexts.feature_flags.container", "get_feature_flag_service"),
    ("contexts.plugins.container", "get_plugin_service"),
    ("contexts.treasury.container", "get_treasury_service"),
    ("contexts.banking.container", "get_banking_customer_account_service"),
    ("contexts.banking.container", "get_banking_kyc_platform_service"),
    ("contexts.banking.container", "get_banking_deposit_management_service"),
    ("contexts.banking.container", "get_banking_loan_management_service"),
    ("contexts.banking.container", "get_banking_interest_calculation_service"),
    ("contexts.banking.container", "get_banking_payment_platform_service"),
    ("contexts.banking.container", "get_banking_settlement_engine_service"),
    ("contexts.banking.container", "get_banking_branch_platform_service"),
    ("contexts.banking.container", "get_banking_security_platform_service"),
    ("contexts.banking.container", "get_banking_analytics_platform_service"),
    ("contexts.currency_exchange.container", "get_fx_rate_engine_service"),
    ("contexts.currency_exchange.container", "get_fx_transaction_platform_service"),
    ("contexts.currency_exchange.container", "get_commission_platform_service"),
    ("contexts.currency_exchange.container", "get_currency_inventory_service"),
    ("contexts.currency_exchange.container", "get_remittance_platform_service"),
    ("contexts.currency_exchange.container", "get_fx_position_platform_service"),
    ("contexts.currency_exchange.container", "get_fx_risk_platform_service"),
    ("contexts.currency_exchange.container", "get_aml_integration_platform_service"),
    ("contexts.currency_exchange.container", "get_fx_workflow_engine_service"),
    ("contexts.currency_exchange.container", "get_fx_security_platform_service"),
    ("contexts.currency_exchange.container", "get_fx_analytics_platform_service"),
    ("contexts.digital_exchange.container", "get_digital_exchange_layer_service"),
    ("contexts.tax.container", "get_tax_engine_service"),
    ("contexts.tax.container", "get_tax_rule_engine_service"),
    ("contexts.tax.container", "get_tax_calculation_service"),
    ("contexts.tax.container", "get_withholding_platform_service"),
    ("contexts.tax.container", "get_payroll_tax_service"),
    ("contexts.tax.container", "get_einvoice_platform_service"),
    ("contexts.tax.container", "get_gov_tax_integration_service"),
    ("contexts.tax.container", "get_tax_reporting_service"),
    ("contexts.tax.container", "get_tax_audit_platform_service"),
    ("contexts.tax.container", "get_tax_workflow_platform_service"),
    ("contexts.tax.container", "get_tax_security_platform_service"),
    ("contexts.tax.container", "get_tax_ai_assistant_platform_service"),
    ("contexts.tax.container", "get_tax_compliance_platform_service"),
    ("contexts.reporting.container", "get_reporting_platform_service"),
    ("contexts.reporting.container", "get_regulatory_reporting_service"),
    ("contexts.reporting.container", "get_scheduled_reporting_service"),
    ("contexts.reporting.container", "get_report_security_service"),
    ("contexts.reporting.container", "get_enterprise_export_service"),
    ("contexts.reporting.container", "get_reporting_apis_service"),
    ("contexts.reporting.container", "get_ai_reporting_service"),
    ("contexts.reporting.container", "get_report_lifecycle_service"),
    ("contexts.financial_kernel.container", "get_financial_kernel_service"),
    ("contexts.financial_kernel.container", "get_financial_statements_platform_service"),
    ("contexts.financial_kernel.container", "get_financial_consolidation_service"),
    ("contexts.financial_kernel.container", "get_payment_workflow_service"),
    ("contexts.financial_kernel.container", "get_procurement_workflow_service"),
    ("contexts.financial_kernel.container", "get_budget_workflow_service"),
    ("contexts.financial_kernel.container", "get_treasury_workflow_service"),
    ("contexts.financial_kernel.container", "get_tax_workflow_service"),
    ("contexts.financial_kernel.container", "get_payment_service"),
    ("contexts.financial_kernel.container", "get_financial_document_service"),
    ("contexts.financial_kernel.container", "get_cost_center_service"),
    ("contexts.financial_kernel.container", "get_financial_workflow_service"),
    ("contexts.financial_kernel.container", "get_financial_security_service"),
    ("contexts.financial_kernel.container", "get_financial_ai_service"),
]

ROUTER_SPECS: list[tuple[str, str]] = [
    ("contexts.identity.presentation.router", "router"),
    ("contexts.authorization.presentation.router", "authorization_router"),
    ("contexts.permission_registry.presentation.router", "permission_registry_router"),
    ("contexts.authentication.presentation.router", "authentication_router"),
    ("contexts.authentication.presentation.orchestration_router", "orchestration_router"),
    ("contexts.authentication.presentation.websocket_auth", "auth_ws_router"),
    ("contexts.authentication.presentation.password_router", "password_router"),
    ("contexts.authentication.presentation.passkey_router", "passkey_router"),
    ("contexts.authentication.presentation.passkey_router", "devices_router"),
    ("contexts.data_isolation.presentation.router", "data_isolation_router"),
    ("contexts.directory.presentation.router", "directory_router"),
    ("contexts.mfa.presentation.router", "mfa_router"),
    ("contexts.mfa.presentation.router", "trusted_devices_router"),
    ("contexts.adaptive_authentication.presentation.router", "adaptive_auth_router"),
    ("contexts.identity_federation.presentation.router", "identity_federation_router"),
    ("contexts.identity_digital_twin.presentation.router", "identity_digital_twin_router"),
    ("contexts.consent.presentation.router", "consent_router"),
    ("contexts.identity_federation.presentation.gateway_router", "federation_gateway_router"),
    ("contexts.identity_federation.presentation.gateway_router", "identity_gateway_router"),
    ("contexts.identity_federation.presentation.fabric_router", "fabric_security_router"),
    ("contexts.identity_federation.presentation.intelligence_router", "intelligence_router"),
    ("contexts.identity_federation.presentation.architecture_router", "architecture_router"),
    ("contexts.identity_federation.presentation.engine_router", "engine_router"),
    ("contexts.identity_federation.presentation.trust_fabric_router", "trust_fabric_router"),
    ("contexts.identity_federation.presentation.providers_router", "providers_router"),
    ("contexts.identity_federation.presentation.cross_tenant_router", "cross_tenant_router"),
    ("contexts.identity_federation.presentation.security_router", "security_router"),
    ("contexts.identity_federation.presentation.ohs_router", "ohs_router"),
    ("contexts.identity_federation.presentation.ops_router", "ops_router"),
    ("contexts.identity_federation.presentation.qa_router", "qa_router"),
    ("contexts.identity_risk.presentation.router", "identity_risk_router"),
    ("contexts.identity_resilience.presentation.router", "identity_resilience_router"),
    ("contexts.identity_lifecycle.presentation.router", "identity_lifecycle_router"),
    ("contexts.identity_lifecycle.presentation.registration_router", "registration_router"),
    ("contexts.core_platform.presentation.router", "router"),
    ("contexts.hospital.presentation.router", "router"),
    ("contexts.accounting.presentation.router", "router"),
    ("contexts.finance.presentation.router", "router"),
    ("contexts.notifications.presentation.router", "router"),
    ("contexts.settings.presentation.router", "router"),
    ("contexts.organization.presentation.router", "router"),
    ("contexts.audit.presentation.router", "router"),
    ("contexts.audit.presentation.enterprise_audit_router", "enterprise_audit_router"),
    ("contexts.documents.presentation.router", "router"),
    ("contexts.human_resources.presentation.router", "router"),
    ("contexts.workflow.presentation.router", "router"),
    ("contexts.workflow.presentation.workflow_designer_router", "workflow_designer_router"),
    ("contexts.workflow.presentation.exception_management_router", "exception_management_router"),
    ("contexts.workflow.presentation.event_driven_workflow_router", "event_driven_workflow_router"),
    ("contexts.workflow.presentation.workflow_security_router", "workflow_security_router"),
    ("contexts.workflow.presentation.workflow_analytics_router", "workflow_analytics_router"),
    ("contexts.workflow.presentation.process_library_router", "process_library_router"),
    ("contexts.workflow.presentation.approval_matrix_router", "approval_matrix_router"),
    ("contexts.integration.presentation.router", "router"),
    ("contexts.media.presentation.router", "router"),
    ("contexts.analytics.presentation.router", "router"),
    ("contexts.analytics.presentation.executive_dashboard_router", "executive_dashboard_router"),
    ("contexts.analytics.presentation.kpi_platform_router", "kpi_platform_router"),
    ("contexts.search.presentation.router", "router"),
    ("contexts.messenger.presentation.router", "router"),
    ("contexts.ai.presentation.router", "router"),
    ("contexts.clinic.presentation.router", "router"),
    ("contexts.university.presentation.router", "router"),
    ("contexts.municipality.presentation.router", "router"),
    ("contexts.pos.presentation.router", "router"),
    ("contexts.inventory.presentation.router", "router"),
    ("contexts.localization.presentation.router", "router"),
    ("contexts.policy.presentation.router", "router"),
    ("contexts.policy.presentation.enterprise_policy_router", "enterprise_policy_router"),
    ("contexts.compliance.presentation.router", "router"),
    ("contexts.compliance.presentation.enterprise_compliance_router", "enterprise_compliance_router"),
    ("contexts.fraud_detection.presentation.router", "fraud_detection_router"),
    ("contexts.data_protection.presentation.router", "data_protection_router"),
    ("contexts.risk.presentation.router", "risk_router"),
    ("contexts.security_incident.presentation.router", "security_incident_router"),
    ("contexts.business_continuity.presentation.router", "business_continuity_router"),
    ("contexts.regulatory_reporting.presentation.router", "enterprise_regulatory_reporting_router"),
    ("contexts.identity_governance.presentation.router", "identity_governance_router"),
    ("contexts.enterprise_executive_dashboard.presentation.router", "enterprise_executive_dashboard_router"),
    ("contexts.enterprise_decision_support.presentation.router", "enterprise_decision_support_router"),
    ("contexts.financial_data_science.presentation.router", "financial_data_science_router"),
    ("contexts.natural_language_analytics.presentation.router", "natural_language_analytics_router"),
    ("contexts.ai_governance.presentation.router", "ai_governance_router"),
    ("contexts.enterprise_api_gateway.presentation.router", "enterprise_api_gateway_router"),
    ("contexts.enterprise_event_bus.presentation.router", "enterprise_event_bus_router"),
    ("contexts.enterprise_message_orchestration.presentation.router", "enterprise_message_orchestration_router"),
    ("contexts.enterprise_webhook_platform.presentation.router", "enterprise_webhook_platform_router"),
    ("contexts.enterprise_connector_framework.presentation.router", "enterprise_connector_framework_router"),
    ("contexts.enterprise_saga_orchestration.presentation.router", "enterprise_saga_orchestration_router"),
    ("contexts.enterprise_reliability_platform.presentation.router", "enterprise_reliability_platform_router"),
    ("contexts.enterprise_observability.presentation.router", "enterprise_observability_router"),
    ("contexts.enterprise_scheduler.presentation.router", "enterprise_scheduler_router"),
    ("contexts.enterprise_integration_studio.presentation.router", "enterprise_integration_studio_router"),
    ("contexts.enterprise_automation_platform.presentation.router", "enterprise_automation_platform_router"),
    ("contexts.enterprise_integration_security.presentation.router", "enterprise_integration_security_router"),
    ("contexts.financial_anomaly_detection.presentation.router", "financial_anomaly_detection_router"),
    ("contexts.enterprise_forecasting.presentation.router", "enterprise_forecasting_router"),
    ("contexts.ai_cfo_assistant.presentation.router", "ai_cfo_router"),
    ("contexts.ai_security.presentation.router", "ai_security_router"),
    ("contexts.financial_ai_analytics.presentation.router", "financial_ai_analytics_router"),
    ("contexts.financial_kpi.presentation.router", "financial_kpi_router"),
    ("contexts.grc.presentation.router", "grc_router"),
    ("contexts.security.presentation.router", "security_router"),
    ("contexts.feature_flags.presentation.router", "router"),
    ("contexts.plugins.presentation.router", "router"),
    ("contexts.financial_kernel.presentation.router", "router"),
    ("contexts.financial_kernel.presentation.ledger_router", "ledger_router"),
    ("contexts.financial_kernel.presentation.journal_router", "journal_router"),
    ("contexts.financial_kernel.presentation.posting_rules_router", "posting_rules_router"),
    ("contexts.financial_kernel.presentation.fiscal_calendar_router", "fiscal_calendar_router"),
    ("contexts.financial_kernel.presentation.account_hierarchy_router", "account_hierarchy_router"),
    ("contexts.financial_kernel.presentation.subledger_router", "subledger_router"),
    ("contexts.financial_kernel.presentation.reconciliation_router", "reconciliation_router"),
    ("contexts.financial_kernel.presentation.financial_dimensions_router", "financial_dimensions_router"),
    ("contexts.financial_kernel.presentation.financial_validation_router", "financial_validation_router"),
    ("contexts.financial_kernel.presentation.financial_statements_router", "financial_statements_router"),
    ("contexts.financial_kernel.presentation.financial_consolidation_router", "financial_consolidation_router"),
    ("contexts.financial_kernel.presentation.payment_workflow_router", "payment_workflow_router"),
    ("contexts.financial_kernel.presentation.procurement_workflow_router", "procurement_workflow_router"),
    ("contexts.financial_kernel.presentation.budget_workflow_router", "budget_workflow_router"),
    ("contexts.financial_kernel.presentation.treasury_workflow_router", "treasury_workflow_router"),
    ("contexts.financial_kernel.presentation.tax_workflow_router", "tax_workflow_router"),
    ("contexts.financial_kernel.presentation.financial_audit_router", "financial_audit_router"),
    ("contexts.financial_kernel.presentation.coa_router", "coa_router"),
    ("contexts.financial_kernel.presentation.currency_router", "currency_router"),
    ("contexts.financial_kernel.presentation.payments_router", "payments_router"),
    ("contexts.financial_kernel.presentation.financial_documents_router", "financial_documents_router"),
    ("contexts.financial_kernel.presentation.cost_centers_router", "cost_centers_router"),
    ("contexts.financial_kernel.presentation.financial_workflows_router", "financial_workflows_router"),
    ("contexts.financial_kernel.presentation.financial_security_router", "financial_security_router"),
    ("contexts.financial_kernel.presentation.financial_ai_router", "financial_ai_router"),
    ("contexts.financial_kernel.presentation.gl_ai_router", "gl_ai_router"),
    ("contexts.treasury.presentation.router", "router"),
    ("contexts.treasury.presentation.banks_router", "banks_router"),
    ("contexts.treasury.presentation.bank_account_router", "bank_account_router"),
    ("contexts.treasury.presentation.cash_management_router", "cash_management_router"),
    ("contexts.treasury.presentation.treasury_transaction_router", "treasury_transaction_router"),
    ("contexts.treasury.presentation.liquidity_router", "liquidity_router"),
    ("contexts.treasury.presentation.cash_forecast_router", "cash_forecast_router"),
    ("contexts.treasury.presentation.bank_reconciliation_router", "bank_reconciliation_router"),
    ("contexts.treasury.presentation.cash_reconciliation_router", "cash_reconciliation_router"),
    ("contexts.treasury.presentation.investments_router", "investments_router"),
    ("contexts.treasury.presentation.risk_router", "risk_router"),
    ("contexts.treasury.presentation.treasury_workflow_router", "treasury_workflow_router"),
    ("contexts.treasury.presentation.treasury_security_router", "treasury_security_router"),
    ("contexts.treasury.presentation.treasury_analytics_router", "treasury_analytics_router"),
    ("contexts.banking.presentation.banking_customer_account_router", "banking_customer_account_router"),
    ("contexts.banking.presentation.banking_kyc_router", "banking_kyc_router"),
    ("contexts.banking.presentation.banking_deposit_router", "banking_deposit_router"),
    ("contexts.banking.presentation.banking_loan_router", "banking_loan_router"),
    ("contexts.banking.presentation.banking_interest_router", "banking_interest_router"),
    ("contexts.banking.presentation.banking_payment_router", "banking_payment_router"),
    ("contexts.banking.presentation.banking_settlement_router", "banking_settlement_router"),
    ("contexts.banking.presentation.banking_branch_router", "banking_branch_router"),
    ("contexts.banking.presentation.banking_security_router", "banking_security_router"),
    ("contexts.banking.presentation.banking_analytics_router", "banking_analytics_router"),
    ("contexts.currency_exchange.presentation.fx_rate_router", "fx_rate_router"),
    ("contexts.currency_exchange.presentation.fx_transaction_router", "fx_transaction_router"),
    ("contexts.currency_exchange.presentation.commission_router", "commission_router"),
    ("contexts.currency_exchange.presentation.currency_inventory_router", "inventory_router"),
    ("contexts.currency_exchange.presentation.remittance_router", "remittance_router"),
    ("contexts.currency_exchange.presentation.fx_position_router", "fx_position_router"),
    ("contexts.currency_exchange.presentation.fx_risk_router", "fx_risk_router"),
    ("contexts.currency_exchange.presentation.aml_router", "aml_router"),
    ("contexts.currency_exchange.presentation.fx_workflow_router", "fx_workflow_router"),
    ("contexts.currency_exchange.presentation.fx_security_router", "fx_security_router"),
    ("contexts.currency_exchange.presentation.fx_analytics_router", "fx_analytics_router"),
    ("contexts.digital_exchange.presentation.digital_exchange_router", "digital_exchange_router"),
    ("contexts.tax.presentation.tax_router", "tax_router"),
    ("contexts.tax.presentation.tax_rule_router", "tax_rule_router"),
    ("contexts.tax.presentation.tax_calculation_router", "tax_calculation_router"),
    ("contexts.tax.presentation.withholding_platform_router", "withholding_platform_router"),
    ("contexts.tax.presentation.payroll_tax_router", "payroll_tax_router"),
    ("contexts.tax.presentation.einvoice_platform_router", "einvoice_platform_router"),
    ("contexts.tax.presentation.gov_tax_integration_router", "gov_tax_integration_router"),
    ("contexts.tax.presentation.tax_reporting_router", "tax_reporting_router"),
    ("contexts.tax.presentation.tax_audit_router", "tax_audit_router"),
    ("contexts.tax.presentation.tax_workflow_router", "tax_workflow_router"),
    ("contexts.tax.presentation.tax_security_router", "tax_security_router"),
    ("contexts.tax.presentation.tax_ai_assistant_router", "tax_ai_assistant_router"),
    ("contexts.tax.presentation.tax_compliance_router", "tax_compliance_router"),
    ("contexts.reporting.presentation.reporting_router", "reporting_router"),
    ("contexts.reporting.presentation.report_builder_router", "report_builder_router"),
    ("contexts.reporting.presentation.regulatory_reporting_router", "regulatory_reporting_router"),
    ("contexts.reporting.presentation.scheduled_reporting_router", "scheduled_reporting_router"),
    ("contexts.reporting.presentation.report_security_router", "report_security_router"),
    ("contexts.reporting.presentation.enterprise_export_router", "enterprise_export_router"),
    ("contexts.reporting.presentation.reporting_apis_router", "reporting_apis_router"),
    ("contexts.reporting.presentation.ai_reporting_router", "ai_reporting_router"),
    ("contexts.reporting.presentation.report_lifecycle_router", "report_lifecycle_router"),
]

_cache: dict[tuple[str, str], object] = {}
_registered_profiles: dict[int, str] = {}
_services_warmed_for: dict[int, str] = {}


def _resolve(module_path: str, attr: str):
    key = (module_path, attr)
    if key not in _cache:
        module = importlib.import_module(module_path)
        _cache[key] = getattr(module, attr)
    return _cache[key]


def resolve_service(module_path: str, getter: str):
    return _resolve(module_path, getter)()


def resolve_router(module_path: str, attr: str):
    return _resolve(module_path, attr)


def router_specs_for_profile(profile: str) -> list[tuple[str, str]]:
    return filter_specs_by_profile(ROUTER_SPECS, profile)


def service_specs_for_profile(profile: str, startup_mode: str) -> list[tuple[str, str]]:
    if startup_mode == "eager" and profile == "full":
        return ALL_SERVICE_SPECS
    allowed_specs = filter_specs_by_profile(ALL_SERVICE_SPECS, profile)
    seen: set[tuple[str, str]] = set()
    merged: list[tuple[str, str]] = []
    for spec in CORE_SERVICE_SPECS + allowed_specs:
        if spec not in seen:
            seen.add(spec)
            merged.append(spec)
    return merged


def register_routers(app: "FastAPI", *, profile: str = "full") -> int:
    app_id = id(app)
    if _registered_profiles.get(app_id) == profile:
        return len(router_specs_for_profile(profile))
    specs = router_specs_for_profile(profile)
    for module_path, attr in specs:
        app.include_router(resolve_router(module_path, attr), prefix=API_PREFIX)
    _registered_profiles[app_id] = profile
    return len(specs)


def warmup_services(app: "FastAPI", specs: list[tuple[str, str]]) -> int:
    app_id = id(app)
    for module_path, getter in specs:
        resolve_service(module_path, getter)
    _services_warmed_for[app_id] = "done"
    return len(specs)


def configure_application(
    app: "FastAPI",
    *,
    profile: str = "full",
    startup_mode: str = "lazy",
) -> dict:
    """Register profile routers and warm up services. Idempotent per app+profile."""
    from shared.infrastructure.settings import settings

    mode = startup_mode or settings.marpich_startup_mode
    prof = profile or settings.marpich_app_profile
    routes = register_routers(app, profile=prof)
    services = warmup_services(app, service_specs_for_profile(prof, mode))
    return {
        "profile": prof,
        "startup_mode": mode,
        "routes": routes,
        "services": services,
    }


def reset_startup_state() -> None:
    """Test helper — clear registration flags and import cache."""
    _registered_profiles.clear()
    _services_warmed_for.clear()
    _cache.clear()
