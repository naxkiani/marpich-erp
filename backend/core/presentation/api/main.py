"""
Marpich ERP — FastAPI composition root.

Mounts bounded context routers. Business domains never import each other.
Cross-context flow uses integration events only.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from contexts.clinic.container import get_clinic_service
from contexts.clinic.presentation.router import router as clinic_router
from contexts.localization.container import get_localization_service
from contexts.localization.presentation.router import router as localization_router
from contexts.municipality.container import get_municipality_service
from contexts.municipality.presentation.router import router as municipality_router
from contexts.pos.container import get_pos_service
from contexts.pos.presentation.router import router as pos_router
from contexts.accounting.container import get_accounting_service
from contexts.accounting.presentation.router import router as accounting_router
from contexts.core_platform.presentation.router import router as platform_router
from contexts.finance.container import get_finance_service
from contexts.finance.presentation.router import router as finance_router
from contexts.hospital.presentation.router import router as hospital_router
from contexts.identity.presentation.router import router as identity_router
from contexts.analytics.container import get_analytics_service, get_executive_dashboard_service, get_kpi_platform_service
from contexts.analytics.presentation.router import router as analytics_router
from contexts.analytics.presentation.executive_dashboard_router import executive_dashboard_router
from contexts.analytics.presentation.kpi_platform_router import kpi_platform_router
from contexts.audit.container import get_audit_service, get_enterprise_audit_service
from contexts.audit.presentation.enterprise_audit_router import enterprise_audit_router
from contexts.audit.presentation.router import router as audit_router
from contexts.documents.container import get_documents_service
from contexts.documents.presentation.router import router as documents_router
from contexts.integration.container import get_integration_service
from contexts.integration.presentation.router import router as integration_router
from contexts.media.container import get_media_service
from contexts.media.presentation.router import router as media_router
from contexts.notifications.container import get_notification_service
from contexts.notifications.presentation.router import router as notifications_router
from contexts.organization.container import get_organization_service
from contexts.organization.presentation.router import router as organization_router
from contexts.settings.container import get_settings_service
from contexts.settings.presentation.router import router as settings_router
from contexts.search.container import get_search_service
from contexts.search.presentation.router import router as search_router
from contexts.policy.container import get_enterprise_policy_service, get_policy_service
from contexts.policy.presentation.enterprise_policy_router import enterprise_policy_router
from contexts.policy.presentation.router import router as policy_router
from contexts.compliance.container import get_compliance_service, get_enterprise_compliance_service
from contexts.compliance.presentation.enterprise_compliance_router import enterprise_compliance_router
from contexts.compliance.presentation.router import router as compliance_router
from contexts.data_protection.container import get_data_protection_service
from contexts.data_protection.presentation.router import data_protection_router
from contexts.risk.container import get_risk_service
from contexts.risk.presentation.router import risk_router as enterprise_risk_router
from contexts.security_incident.container import get_security_incident_service
from contexts.security_incident.presentation.router import security_incident_router
from contexts.business_continuity.container import get_business_continuity_service
from contexts.business_continuity.presentation.router import business_continuity_router
from contexts.regulatory_reporting.container import get_enterprise_regulatory_reporting_service
from contexts.regulatory_reporting.presentation.router import enterprise_regulatory_reporting_router
from contexts.identity_governance.container import get_identity_governance_service
from contexts.identity_governance.presentation.router import identity_governance_router
from contexts.fraud_detection.container import get_fraud_detection_service
from contexts.fraud_detection.presentation.router import fraud_detection_router
from contexts.grc.container import get_grc_service
from contexts.grc.presentation.router import grc_router
from contexts.security.container import get_security_service
from contexts.security.presentation.router import security_router
from contexts.feature_flags.container import get_feature_flag_service
from contexts.feature_flags.presentation.router import router as feature_flags_router
from contexts.plugins.container import get_plugin_service
from contexts.plugins.presentation.router import router as plugins_router
from contexts.treasury.container import get_treasury_service
from contexts.treasury.presentation.bank_account_router import bank_account_router
from contexts.treasury.presentation.banks_router import banks_router
from contexts.treasury.presentation.cash_management_router import cash_management_router
from contexts.treasury.presentation.bank_reconciliation_router import bank_reconciliation_router
from contexts.treasury.presentation.cash_reconciliation_router import cash_reconciliation_router
from contexts.treasury.presentation.investments_router import investments_router
from contexts.treasury.presentation.treasury_workflow_router import treasury_workflow_router
from contexts.treasury.presentation.treasury_security_router import treasury_security_router
from contexts.treasury.presentation.treasury_analytics_router import treasury_analytics_router
from contexts.treasury.presentation.multi_currency_router import multi_currency_router
from contexts.treasury.presentation.risk_router import risk_router as treasury_risk_router
from contexts.treasury.presentation.cash_forecast_router import cash_forecast_router
from contexts.treasury.presentation.liquidity_router import liquidity_router
from contexts.treasury.presentation.treasury_transaction_router import treasury_transaction_router
from contexts.treasury.presentation.router import router as treasury_router
from contexts.banking.container import (
    get_banking_customer_account_service,
    get_banking_deposit_management_service,
    get_banking_kyc_platform_service,
    get_banking_loan_management_service,
    get_banking_interest_calculation_service,
    get_banking_payment_platform_service,
    get_banking_settlement_engine_service,
    get_banking_branch_platform_service,
    get_banking_security_platform_service,
    get_banking_analytics_platform_service,
)
from contexts.banking.presentation.banking_customer_account_router import banking_customer_account_router
from contexts.banking.presentation.banking_deposit_router import banking_deposit_router
from contexts.banking.presentation.banking_interest_router import banking_interest_router
from contexts.banking.presentation.banking_kyc_router import banking_kyc_router
from contexts.banking.presentation.banking_loan_router import banking_loan_router
from contexts.banking.presentation.banking_payment_router import banking_payment_router
from contexts.banking.presentation.banking_settlement_router import banking_settlement_router
from contexts.banking.presentation.banking_branch_router import banking_branch_router
from contexts.banking.presentation.banking_analytics_router import banking_analytics_router
from contexts.banking.presentation.banking_security_router import banking_security_router
from contexts.currency_exchange.container import (
    get_commission_platform_service,
    get_currency_inventory_service,
    get_fx_rate_engine_service,
    get_fx_transaction_platform_service,
    get_remittance_platform_service,
    get_fx_position_platform_service,
    get_fx_risk_platform_service,
    get_aml_integration_platform_service,
    get_fx_workflow_engine_service,
    get_fx_security_platform_service,
    get_fx_analytics_platform_service,
)
from contexts.currency_exchange.presentation.commission_router import commission_router
from contexts.currency_exchange.presentation.currency_inventory_router import inventory_router
from contexts.currency_exchange.presentation.fx_position_router import fx_position_router
from contexts.currency_exchange.presentation.fx_risk_router import fx_risk_router
from contexts.currency_exchange.presentation.aml_router import aml_router
from contexts.currency_exchange.presentation.fx_workflow_router import fx_workflow_router
from contexts.currency_exchange.presentation.fx_security_router import fx_security_router
from contexts.currency_exchange.presentation.fx_analytics_router import fx_analytics_router
from contexts.currency_exchange.presentation.fx_rate_router import fx_rate_router
from contexts.currency_exchange.presentation.fx_transaction_router import fx_transaction_router
from contexts.currency_exchange.presentation.remittance_router import remittance_router
from contexts.digital_exchange.container import get_digital_exchange_layer_service
from contexts.digital_exchange.presentation.digital_exchange_router import digital_exchange_router
from contexts.tax.container import get_tax_engine_service, get_tax_rule_engine_service, get_tax_calculation_service, get_withholding_platform_service, get_payroll_tax_service, get_einvoice_platform_service, get_gov_tax_integration_service, get_tax_reporting_service, get_tax_audit_platform_service, get_tax_workflow_platform_service, get_tax_security_platform_service, get_tax_ai_assistant_platform_service, get_tax_compliance_platform_service
from contexts.tax.presentation.tax_router import tax_router
from contexts.tax.presentation.tax_rule_router import tax_rule_router
from contexts.tax.presentation.tax_calculation_router import tax_calculation_router
from contexts.tax.presentation.withholding_platform_router import withholding_platform_router
from contexts.tax.presentation.payroll_tax_router import payroll_tax_router
from contexts.tax.presentation.einvoice_platform_router import einvoice_platform_router
from contexts.tax.presentation.gov_tax_integration_router import gov_tax_integration_router
from contexts.tax.presentation.tax_reporting_router import tax_reporting_router
from contexts.tax.presentation.tax_audit_router import tax_audit_router
from contexts.tax.presentation.tax_workflow_router import tax_workflow_router
from contexts.tax.presentation.tax_security_router import tax_security_router
from contexts.tax.presentation.tax_ai_assistant_router import tax_ai_assistant_router
from contexts.tax.presentation.tax_compliance_router import tax_compliance_router
from contexts.reporting.container import (
    get_enterprise_export_service,
    get_reporting_apis_service,
    get_ai_reporting_service,
    get_report_lifecycle_service,
    get_regulatory_reporting_service,
    get_report_security_service,
    get_reporting_platform_service,
    get_scheduled_reporting_service,
)
from contexts.reporting.presentation.reporting_router import reporting_router
from contexts.reporting.presentation.report_builder_router import report_builder_router
from contexts.reporting.presentation.regulatory_reporting_router import regulatory_reporting_router
from contexts.reporting.presentation.scheduled_reporting_router import scheduled_reporting_router
from contexts.reporting.presentation.report_security_router import report_security_router
from contexts.reporting.presentation.enterprise_export_router import enterprise_export_router
from contexts.reporting.presentation.reporting_apis_router import reporting_apis_router
from contexts.reporting.presentation.ai_reporting_router import ai_reporting_router
from contexts.reporting.presentation.report_lifecycle_router import report_lifecycle_router
from contexts.financial_kernel.container import (
    get_cost_center_service,
    get_financial_consolidation_service,
    get_payment_workflow_service,
    get_procurement_workflow_service,
    get_budget_workflow_service,
    get_treasury_workflow_service,
    get_tax_workflow_service,
    get_financial_document_service,
    get_financial_kernel_service,
    get_financial_statements_platform_service,
    get_financial_workflow_service,
    get_financial_security_service,
    get_financial_ai_service,
    get_payment_service,
)
from contexts.financial_kernel.presentation.financial_ai_router import financial_ai_router
from contexts.financial_kernel.presentation.gl_ai_router import gl_ai_router
from contexts.financial_kernel.presentation.financial_security_router import financial_security_router
from contexts.financial_kernel.presentation.coa_router import coa_router
from contexts.financial_kernel.presentation.cost_centers_router import cost_centers_router
from contexts.financial_kernel.presentation.financial_documents_router import financial_documents_router
from contexts.financial_kernel.presentation.financial_workflows_router import financial_workflows_router
from contexts.financial_kernel.presentation.payments_router import payments_router
from contexts.financial_kernel.presentation.currency_router import currency_router
from contexts.financial_kernel.presentation.ledger_router import ledger_router
from contexts.financial_kernel.presentation.journal_router import journal_router
from contexts.financial_kernel.presentation.fiscal_calendar_router import fiscal_calendar_router
from contexts.financial_kernel.presentation.account_hierarchy_router import account_hierarchy_router
from contexts.financial_kernel.presentation.financial_audit_router import financial_audit_router
from contexts.financial_kernel.presentation.financial_validation_router import financial_validation_router
from contexts.financial_kernel.presentation.payment_workflow_router import payment_workflow_router
from contexts.financial_kernel.presentation.procurement_workflow_router import procurement_workflow_router
from contexts.financial_kernel.presentation.budget_workflow_router import budget_workflow_router
from contexts.financial_kernel.presentation.treasury_workflow_router import (
    treasury_workflow_router as financial_kernel_treasury_workflow_router,
)
from contexts.financial_kernel.presentation.tax_workflow_router import (
    tax_workflow_router as financial_kernel_tax_workflow_router,
)
from contexts.financial_kernel.presentation.financial_consolidation_router import financial_consolidation_router
from contexts.financial_kernel.presentation.financial_statements_router import financial_statements_router
from contexts.financial_kernel.presentation.financial_dimensions_router import financial_dimensions_router
from contexts.financial_kernel.presentation.reconciliation_router import reconciliation_router
from contexts.financial_kernel.presentation.subledger_router import subledger_router
from contexts.financial_kernel.presentation.posting_rules_router import posting_rules_router
from contexts.financial_kernel.presentation.router import router as financial_kernel_router
from contexts.workflow.container import (
    get_approval_matrix_service,
    get_exception_management_service,
    get_event_driven_workflow_service,
    get_workflow_analytics_service,
    get_process_library_service,
    get_workflow_security_service,
    get_workflow_designer_service,
    get_workflow_service,
)
from contexts.workflow.presentation.exception_management_router import exception_management_router
from contexts.workflow.presentation.event_driven_workflow_router import event_driven_workflow_router
from contexts.workflow.presentation.process_library_router import process_library_router
from contexts.workflow.presentation.workflow_analytics_router import workflow_analytics_router
from contexts.workflow.presentation.workflow_security_router import workflow_security_router
from contexts.workflow.presentation.approval_matrix_router import approval_matrix_router
from contexts.workflow.presentation.router import router as workflow_router
from contexts.workflow.presentation.workflow_designer_router import workflow_designer_router
from core.presentation.middleware.platform_gateway import PlatformGatewayMiddleware
from shared.infrastructure.messaging.dispatcher import get_outbox_dispatcher
from shared.infrastructure.observability.telemetry import setup_observability, shutdown_observability


@asynccontextmanager
async def lifespan(_app: FastAPI):
    get_accounting_service()
    get_finance_service()
    get_notification_service()
    get_settings_service()
    get_organization_service()
    get_audit_service()
    get_enterprise_audit_service()
    get_documents_service()
    get_workflow_service()
    get_workflow_designer_service()
    get_approval_matrix_service()
    get_exception_management_service()
    get_event_driven_workflow_service()
    get_workflow_security_service()
    get_workflow_analytics_service()
    get_process_library_service()
    get_integration_service()
    get_media_service()
    get_analytics_service()
    get_executive_dashboard_service()
    get_kpi_platform_service()
    get_search_service()
    get_clinic_service()
    get_municipality_service()
    get_pos_service()
    get_localization_service()
    get_policy_service()
    get_enterprise_policy_service()
    get_compliance_service()
    get_enterprise_compliance_service()
    get_fraud_detection_service()
    get_data_protection_service()
    get_risk_service()
    get_security_incident_service()
    get_business_continuity_service()
    get_enterprise_regulatory_reporting_service()
    get_identity_governance_service()
    get_grc_service()
    get_security_service()
    get_feature_flag_service()
    get_plugin_service()
    get_treasury_service()
    get_banking_customer_account_service()
    get_banking_kyc_platform_service()
    get_banking_deposit_management_service()
    get_banking_loan_management_service()
    get_banking_interest_calculation_service()
    get_banking_payment_platform_service()
    get_banking_settlement_engine_service()
    get_banking_branch_platform_service()
    get_banking_security_platform_service()
    get_banking_analytics_platform_service()
    get_fx_rate_engine_service()
    get_fx_transaction_platform_service()
    get_commission_platform_service()
    get_currency_inventory_service()
    get_remittance_platform_service()
    get_fx_position_platform_service()
    get_fx_risk_platform_service()
    get_aml_integration_platform_service()
    get_fx_workflow_engine_service()
    get_fx_security_platform_service()
    get_fx_analytics_platform_service()
    get_digital_exchange_layer_service()
    get_tax_engine_service()
    get_tax_rule_engine_service()
    get_tax_calculation_service()
    get_withholding_platform_service()
    get_payroll_tax_service()
    get_einvoice_platform_service()
    get_gov_tax_integration_service()
    get_tax_reporting_service()
    get_tax_audit_platform_service()
    get_tax_workflow_platform_service()
    get_tax_security_platform_service()
    get_tax_ai_assistant_platform_service()
    get_tax_compliance_platform_service()
    get_reporting_platform_service()
    get_regulatory_reporting_service()
    get_scheduled_reporting_service()
    get_report_security_service()
    get_enterprise_export_service()
    get_reporting_apis_service()
    get_ai_reporting_service()
    get_report_lifecycle_service()
    get_financial_kernel_service()
    get_financial_statements_platform_service()
    get_financial_consolidation_service()
    get_payment_workflow_service()
    get_procurement_workflow_service()
    get_budget_workflow_service()
    get_treasury_workflow_service()
    get_tax_workflow_service()
    get_payment_service()
    get_financial_document_service()
    get_cost_center_service()
    get_financial_workflow_service()
    get_financial_security_service()
    get_financial_ai_service()
    dispatcher = get_outbox_dispatcher()
    await dispatcher.start()
    setup_observability(_app)
    yield
    await dispatcher.stop()
    shutdown_observability()


app = FastAPI(
    title="Marpich ERP",
    description="Enterprise Operating System — DDD + Clean Architecture",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(PlatformGatewayMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(identity_router, prefix="/api/v1")
app.include_router(platform_router, prefix="/api/v1")
app.include_router(hospital_router, prefix="/api/v1")
app.include_router(accounting_router, prefix="/api/v1")
app.include_router(finance_router, prefix="/api/v1")
app.include_router(notifications_router, prefix="/api/v1")
app.include_router(settings_router, prefix="/api/v1")
app.include_router(organization_router, prefix="/api/v1")
app.include_router(audit_router, prefix="/api/v1")
app.include_router(enterprise_audit_router, prefix="/api/v1")
app.include_router(documents_router, prefix="/api/v1")
app.include_router(workflow_router, prefix="/api/v1")
app.include_router(workflow_designer_router, prefix="/api/v1")
app.include_router(exception_management_router, prefix="/api/v1")
app.include_router(event_driven_workflow_router, prefix="/api/v1")
app.include_router(workflow_security_router, prefix="/api/v1")
app.include_router(workflow_analytics_router, prefix="/api/v1")
app.include_router(process_library_router, prefix="/api/v1")
app.include_router(approval_matrix_router, prefix="/api/v1")
app.include_router(integration_router, prefix="/api/v1")
app.include_router(media_router, prefix="/api/v1")
app.include_router(analytics_router, prefix="/api/v1")
app.include_router(executive_dashboard_router, prefix="/api/v1")
app.include_router(kpi_platform_router, prefix="/api/v1")
app.include_router(search_router, prefix="/api/v1")
app.include_router(clinic_router, prefix="/api/v1")
app.include_router(municipality_router, prefix="/api/v1")
app.include_router(pos_router, prefix="/api/v1")
app.include_router(localization_router, prefix="/api/v1")
app.include_router(policy_router, prefix="/api/v1")
app.include_router(enterprise_policy_router, prefix="/api/v1")
app.include_router(compliance_router, prefix="/api/v1")
app.include_router(enterprise_compliance_router, prefix="/api/v1")
app.include_router(fraud_detection_router, prefix="/api/v1")
app.include_router(data_protection_router, prefix="/api/v1")
app.include_router(enterprise_risk_router, prefix="/api/v1")
app.include_router(security_incident_router, prefix="/api/v1")
app.include_router(business_continuity_router, prefix="/api/v1")
app.include_router(enterprise_regulatory_reporting_router, prefix="/api/v1")
app.include_router(identity_governance_router, prefix="/api/v1")
app.include_router(grc_router, prefix="/api/v1")
app.include_router(security_router, prefix="/api/v1")
app.include_router(feature_flags_router, prefix="/api/v1")
app.include_router(plugins_router, prefix="/api/v1")
app.include_router(financial_kernel_router, prefix="/api/v1")
app.include_router(ledger_router, prefix="/api/v1")
app.include_router(journal_router, prefix="/api/v1")
app.include_router(posting_rules_router, prefix="/api/v1")
app.include_router(fiscal_calendar_router, prefix="/api/v1")
app.include_router(account_hierarchy_router, prefix="/api/v1")
app.include_router(subledger_router, prefix="/api/v1")
app.include_router(reconciliation_router, prefix="/api/v1")
app.include_router(financial_dimensions_router, prefix="/api/v1")
app.include_router(financial_validation_router, prefix="/api/v1")
app.include_router(financial_statements_router, prefix="/api/v1")
app.include_router(financial_consolidation_router, prefix="/api/v1")
app.include_router(payment_workflow_router, prefix="/api/v1")
app.include_router(procurement_workflow_router, prefix="/api/v1")
app.include_router(budget_workflow_router, prefix="/api/v1")
app.include_router(financial_kernel_treasury_workflow_router, prefix="/api/v1")
app.include_router(financial_kernel_tax_workflow_router, prefix="/api/v1")
app.include_router(financial_audit_router, prefix="/api/v1")
app.include_router(coa_router, prefix="/api/v1")
app.include_router(currency_router, prefix="/api/v1")
app.include_router(payments_router, prefix="/api/v1")
app.include_router(financial_documents_router, prefix="/api/v1")
app.include_router(cost_centers_router, prefix="/api/v1")
app.include_router(financial_workflows_router, prefix="/api/v1")
app.include_router(financial_security_router, prefix="/api/v1")
app.include_router(financial_ai_router, prefix="/api/v1")
app.include_router(gl_ai_router, prefix="/api/v1")
app.include_router(treasury_router, prefix="/api/v1")
app.include_router(banks_router, prefix="/api/v1")
app.include_router(bank_account_router, prefix="/api/v1")
app.include_router(cash_management_router, prefix="/api/v1")
app.include_router(treasury_transaction_router, prefix="/api/v1")
app.include_router(liquidity_router, prefix="/api/v1")
app.include_router(cash_forecast_router, prefix="/api/v1")
app.include_router(bank_reconciliation_router, prefix="/api/v1")
app.include_router(cash_reconciliation_router, prefix="/api/v1")
app.include_router(investments_router, prefix="/api/v1")
app.include_router(treasury_risk_router, prefix="/api/v1")
app.include_router(treasury_workflow_router, prefix="/api/v1")
app.include_router(treasury_security_router, prefix="/api/v1")
app.include_router(treasury_analytics_router, prefix="/api/v1")
app.include_router(banking_customer_account_router, prefix="/api/v1")
app.include_router(banking_kyc_router, prefix="/api/v1")
app.include_router(banking_deposit_router, prefix="/api/v1")
app.include_router(banking_loan_router, prefix="/api/v1")
app.include_router(banking_interest_router, prefix="/api/v1")
app.include_router(banking_payment_router, prefix="/api/v1")
app.include_router(banking_settlement_router, prefix="/api/v1")
app.include_router(banking_branch_router, prefix="/api/v1")
app.include_router(banking_security_router, prefix="/api/v1")
app.include_router(banking_analytics_router, prefix="/api/v1")
app.include_router(fx_rate_router, prefix="/api/v1")
app.include_router(fx_transaction_router, prefix="/api/v1")
app.include_router(commission_router, prefix="/api/v1")
app.include_router(inventory_router, prefix="/api/v1")
app.include_router(remittance_router, prefix="/api/v1")
app.include_router(fx_position_router, prefix="/api/v1")
app.include_router(fx_risk_router, prefix="/api/v1")
app.include_router(aml_router, prefix="/api/v1")
app.include_router(fx_workflow_router, prefix="/api/v1")
app.include_router(fx_security_router, prefix="/api/v1")
app.include_router(fx_analytics_router, prefix="/api/v1")
app.include_router(digital_exchange_router, prefix="/api/v1")
app.include_router(tax_router, prefix="/api/v1")
app.include_router(tax_rule_router, prefix="/api/v1")
app.include_router(tax_calculation_router, prefix="/api/v1")
app.include_router(withholding_platform_router, prefix="/api/v1")
app.include_router(payroll_tax_router, prefix="/api/v1")
app.include_router(einvoice_platform_router, prefix="/api/v1")
app.include_router(gov_tax_integration_router, prefix="/api/v1")
app.include_router(tax_reporting_router, prefix="/api/v1")
app.include_router(tax_audit_router, prefix="/api/v1")
app.include_router(tax_workflow_router, prefix="/api/v1")
app.include_router(tax_security_router, prefix="/api/v1")
app.include_router(tax_ai_assistant_router, prefix="/api/v1")
app.include_router(tax_compliance_router, prefix="/api/v1")
app.include_router(reporting_router, prefix="/api/v1")
app.include_router(report_builder_router, prefix="/api/v1")
app.include_router(regulatory_reporting_router, prefix="/api/v1")
app.include_router(scheduled_reporting_router, prefix="/api/v1")
app.include_router(report_security_router, prefix="/api/v1")
app.include_router(enterprise_export_router, prefix="/api/v1")
app.include_router(reporting_apis_router, prefix="/api/v1")
app.include_router(ai_reporting_router, prefix="/api/v1")
app.include_router(report_lifecycle_router, prefix="/api/v1")


@app.get("/api/v1/health", tags=["Monitoring"])
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "marpich-backend"}
