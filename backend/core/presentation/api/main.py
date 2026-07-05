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
from contexts.analytics.container import get_analytics_service
from contexts.analytics.presentation.router import router as analytics_router
from contexts.audit.container import get_audit_service
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
from contexts.policy.container import get_policy_service
from contexts.policy.presentation.router import router as policy_router
from contexts.compliance.container import get_compliance_service
from contexts.compliance.presentation.router import router as compliance_router
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
from contexts.treasury.presentation.risk_router import risk_router
from contexts.treasury.presentation.cash_forecast_router import cash_forecast_router
from contexts.treasury.presentation.liquidity_router import liquidity_router
from contexts.treasury.presentation.treasury_transaction_router import treasury_transaction_router
from contexts.treasury.presentation.router import router as treasury_router
from contexts.banking.container import (
    get_banking_customer_account_service,
    get_banking_deposit_management_service,
    get_banking_kyc_platform_service,
    get_banking_loan_management_service,
)
from contexts.banking.presentation.banking_customer_account_router import banking_customer_account_router
from contexts.banking.presentation.banking_deposit_router import banking_deposit_router
from contexts.banking.presentation.banking_kyc_router import banking_kyc_router
from contexts.banking.presentation.banking_loan_router import banking_loan_router
from contexts.financial_kernel.container import (
    get_cost_center_service,
    get_financial_document_service,
    get_financial_kernel_service,
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
from contexts.financial_kernel.presentation.financial_dimensions_router import financial_dimensions_router
from contexts.financial_kernel.presentation.reconciliation_router import reconciliation_router
from contexts.financial_kernel.presentation.subledger_router import subledger_router
from contexts.financial_kernel.presentation.posting_rules_router import posting_rules_router
from contexts.financial_kernel.presentation.router import router as financial_kernel_router
from contexts.workflow.container import get_workflow_service
from contexts.workflow.presentation.router import router as workflow_router
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
    get_documents_service()
    get_workflow_service()
    get_integration_service()
    get_media_service()
    get_analytics_service()
    get_search_service()
    get_clinic_service()
    get_municipality_service()
    get_pos_service()
    get_localization_service()
    get_policy_service()
    get_compliance_service()
    get_feature_flag_service()
    get_plugin_service()
    get_treasury_service()
    get_banking_customer_account_service()
    get_banking_kyc_platform_service()
    get_banking_deposit_management_service()
    get_banking_loan_management_service()
    get_financial_kernel_service()
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
app.include_router(documents_router, prefix="/api/v1")
app.include_router(workflow_router, prefix="/api/v1")
app.include_router(integration_router, prefix="/api/v1")
app.include_router(media_router, prefix="/api/v1")
app.include_router(analytics_router, prefix="/api/v1")
app.include_router(search_router, prefix="/api/v1")
app.include_router(clinic_router, prefix="/api/v1")
app.include_router(municipality_router, prefix="/api/v1")
app.include_router(pos_router, prefix="/api/v1")
app.include_router(localization_router, prefix="/api/v1")
app.include_router(policy_router, prefix="/api/v1")
app.include_router(compliance_router, prefix="/api/v1")
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
app.include_router(risk_router, prefix="/api/v1")
app.include_router(multi_currency_router, prefix="/api/v1")
app.include_router(treasury_workflow_router, prefix="/api/v1")
app.include_router(treasury_security_router, prefix="/api/v1")
app.include_router(treasury_analytics_router, prefix="/api/v1")
app.include_router(banking_customer_account_router, prefix="/api/v1")
app.include_router(banking_kyc_router, prefix="/api/v1")
app.include_router(banking_deposit_router, prefix="/api/v1")
app.include_router(banking_loan_router, prefix="/api/v1")


@app.get("/api/v1/health", tags=["Monitoring"])
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "marpich-backend"}
