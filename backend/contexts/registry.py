"""
Marpich ERP — Bounded Context Registry

44+ independent domains. Communication ONLY via Integration Events.
NO direct imports between business context domain layers.
"""

from __future__ import annotations

from shared.domain.events.integration_event import BoundedContext, BoundedContextType

# ── Platform & Supporting ────────────────────────────────────────────────

CORE_PLATFORM = BoundedContext(
    id="core_platform",
    display_name="Core Platform",
    context_type=BoundedContextType.PLATFORM,
    schema_name="platform",
    description="Tenant lifecycle, module activation, platform configuration kernel",
    publishes=(
        "platform.tenant.provisioned",
        "platform.module.activated",
        "platform.module.deactivated",
    ),
    subscribes=(),
)

IDENTITY = BoundedContext(
    id="identity",
    display_name="Identity & Access",
    context_type=BoundedContextType.PLATFORM,
    schema_name="identity",
    description="Users, roles, permissions, JWT, MFA, ABAC, sessions",
    publishes=(
        "identity.user.created",
        "identity.user.deactivated",
        "identity.role.assigned",
        "identity.login.succeeded",
        "identity.login.failed",
        "identity.mfa.enabled",
    ),
    subscribes=("platform.tenant.provisioned",),
)

WORKFLOW = BoundedContext(
    id="workflow",
    display_name="Workflow Engine",
    context_type=BoundedContextType.PLATFORM,
    schema_name="workflow",
    description="BPMN processes, approvals, task routing",
    publishes=(
        "workflow.process.started",
        "workflow.task.assigned",
        "workflow.task.completed",
        "workflow.process.completed",
    ),
    subscribes=("platform.module.activated",),
)

INTEGRATION = BoundedContext(
    id="integration",
    display_name="Integration",
    context_type=BoundedContextType.PLATFORM,
    schema_name="integration",
    description="Webhooks, connectors, and external system sync",
    publishes=(
        "integration.webhook.delivered",
        "integration.webhook.failed",
        "integration.sync.completed",
        "integration.connector.registered",
    ),
    subscribes=("*", "platform.tenant.provisioned"),
)

DOCUMENTS = BoundedContext(
    id="documents",
    display_name="Document Management",
    context_type=BoundedContextType.PLATFORM,
    schema_name="documents",
    description="DMS, versioning, e-signature, retention",
    publishes=(
        "documents.document.uploaded",
        "documents.document.signed",
        "documents.document.archived",
        "documents.version.created",
    ),
    subscribes=("platform.tenant.provisioned",),
)

NOTIFICATIONS = BoundedContext(
    id="notifications",
    display_name="Notifications",
    context_type=BoundedContextType.SUPPORTING,
    schema_name="notifications",
    description="Email, SMS, push, in-app notification delivery",
    publishes=("notifications.message.delivered", "notifications.message.failed"),
    subscribes=(
        "identity.login.succeeded",
        "workflow.task.completed",
        "finance.payment.received",
    ),
)

ANALYTICS = BoundedContext(
    id="analytics",
    display_name="Analytics",
    context_type=BoundedContextType.SUPPORTING,
    schema_name="analytics",
    description="OLAP, dashboards, KPIs, data warehouse projections",
    publishes=("analytics.report.generated", "analytics.alert.triggered"),
    subscribes=("*", "platform.tenant.provisioned"),
)

AI = BoundedContext(
    id="ai",
    display_name="AI",
    context_type=BoundedContextType.SUPPORTING,
    schema_name="ai",
    description="LLM orchestration, embeddings, domain AI agents",
    publishes=(
        "ai.insight.generated",
        "ai.fraud.alert.raised",
        "ai.document.parsed",
    ),
    subscribes=(
        "documents.document.uploaded",
        "banking.transaction.posted",
        "hospital.encounter.completed",
    ),
)

MEDIA = BoundedContext(
    id="media",
    display_name="Media",
    context_type=BoundedContextType.SUPPORTING,
    schema_name="media",
    description="Image/video processing, CDN, asset pipeline",
    publishes=(
        "media.asset.uploaded",
        "media.transcode.completed",
        "media.asset.deleted",
    ),
    subscribes=("documents.document.uploaded",),
)

SEARCH = BoundedContext(
    id="search",
    display_name="Search",
    context_type=BoundedContextType.SUPPORTING,
    schema_name="search",
    description="Full-text and faceted search index (Elasticsearch/OpenSearch)",
    publishes=("search.index.updated",),
    subscribes=("*",),
)

SETTINGS = BoundedContext(
    id="settings",
    display_name="Settings",
    context_type=BoundedContextType.PLATFORM,
    schema_name="settings",
    description="Tenant preferences, feature flags, module configuration",
    publishes=("settings.configuration.changed",),
    subscribes=("platform.tenant.provisioned",),
)

LOCALIZATION = BoundedContext(
    id="localization",
    display_name="Localization",
    context_type=BoundedContextType.PLATFORM,
    schema_name="localization",
    description="i18n/l10n — locales, translation keys, RTL/LTR formats",
    publishes=(
        "localization.locale.changed",
        "localization.translation.updated",
        "localization.key.missing",
    ),
    subscribes=("platform.tenant.provisioned", "settings.configuration.changed"),
)

ORGANIZATION = BoundedContext(
    id="organization",
    display_name="Organization",
    context_type=BoundedContextType.PLATFORM,
    schema_name="organization",
    description="Multi-org hierarchy — companies, branches, departments, memberships",
    publishes=(
        "organization.org.created",
        "organization.unit.created",
        "organization.member.added",
        "organization.member.removed",
    ),
    subscribes=("platform.tenant.provisioned", "identity.user.created"),
)

AUDIT = BoundedContext(
    id="audit",
    display_name="Audit",
    context_type=BoundedContextType.PLATFORM,
    schema_name="audit",
    description="Immutable append-only audit trail for compliance",
    publishes=("audit.export.completed", "audit.retention.applied"),
    subscribes=("*", "platform.tenant.provisioned"),
)

POLICY = BoundedContext(
    id="policy",
    display_name="Policy Engine",
    context_type=BoundedContextType.PLATFORM,
    schema_name="policy",
    description="Configurable business rules — versioning, evaluation, simulation",
    publishes=(
        "policy.version.submitted",
        "policy.version.activated",
        "policy.version.rolled_back",
        "policy.evaluation.denied",
        "policy.simulation.executed",
    ),
    subscribes=("platform.tenant.provisioned", "workflow.process.completed"),
)

IDENTITY_LIFECYCLE = BoundedContext(
    id="identity_lifecycle",
    display_name="Enterprise Identity Lifecycle Management Platform (EILMP)",
    context_type=BoundedContextType.PLATFORM,
    schema_name="identity_lifecycle",
    description="Registration, onboarding, verification, JML, archive/deletion — SoR for P201 EILMP",
    publishes=(
        "identity_lifecycle.case.opened",
        "identity_lifecycle.state.changed",
        "identity_lifecycle.verification.completed",
        "identity_lifecycle.consent.recorded",
        "identity_lifecycle.identity.deleted",
        "identity_lifecycle.registration.requested",
        "identity_lifecycle.registration.validated",
        "identity_lifecycle.registration.duplicate_detected",
        "identity_lifecycle.registration.approved",
        "identity_lifecycle.registration.rejected",
        "identity_lifecycle.identity.created",
        "identity_lifecycle.profile.initialized",
        "identity_lifecycle.onboarding.started",
        "identity_lifecycle.provisioning.requested",
        "identity_lifecycle.welcome.generated",
        "identity_lifecycle.activation.requested",
    ),
    subscribes=("platform.tenant.provisioned",),
)

COMPLIANCE = BoundedContext(
    id="compliance",
    display_name="Compliance Framework",
    context_type=BoundedContextType.PLATFORM,
    schema_name="compliance",
    description="Compliance monitoring, violations, reports, alerts",
    publishes=(
        "compliance.violation.detected",
        "compliance.alert.triggered",
        "compliance.report.generated",
    ),
    subscribes=(
        "platform.tenant.provisioned",
        "policy.evaluation.denied",
        "authorization.access.denied",
        "audit.retention.applied",
    ),
)

FEATURE_FLAGS = BoundedContext(
    id="feature_flags",
    display_name="Feature Flag System",
    context_type=BoundedContextType.PLATFORM,
    schema_name="feature_flags",
    description="Multi-scope flags, rollout, A/B, emergency disable",
    publishes=(
        "feature_flag.created",
        "feature_flag.updated",
        "feature_flag.rollout.updated",
        "feature_flag.emergency_disabled",
        "feature_flag.rollback.applied",
    ),
    subscribes=("platform.tenant.provisioned",),
)

PLUGINS = BoundedContext(
    id="plugins",
    display_name="Plugin Platform",
    context_type=BoundedContextType.PLATFORM,
    schema_name="plugins",
    description="Third-party plugins, marketplace, sandbox runtime",
    publishes=(
        "plugin.registered",
        "plugin.published",
        "plugin.installed",
        "plugin.upgraded",
        "plugin.uninstalled",
        "plugin.sandbox.violation",
    ),
    subscribes=(),
)

FINANCIAL_KERNEL = BoundedContext(
    id="financial_kernel",
    display_name="Enterprise Financial Kernel",
    context_type=BoundedContextType.PLATFORM,
    schema_name="financial_kernel",
    description="Platform financial foundation — GL, COA, journals, engines",
    publishes=(
        "financial_kernel.coa.seeded",
        "financial_kernel.journal.posted",
        "financial_kernel.voucher.approved",
        "financial_kernel.period.closed",
        "financial_kernel.payment.settled",
    ),
    subscribes=("platform.tenant.provisioned",),
)

# ── Finance cluster (independent contexts — NOT a monolith) ──────────────

FINANCE = BoundedContext(
    id="finance",
    display_name="Finance (General)",
    context_type=BoundedContextType.FINANCE,
    schema_name="finance",
    description="Financial planning, budgets, cost centers — orchestrates finance sub-domains via events",
    publishes=("finance.budget.approved", "finance.period.closed"),
    subscribes=("accounting.journal.posted",),
)

ACCOUNTING = BoundedContext(
    id="accounting",
    display_name="Accounting",
    context_type=BoundedContextType.FINANCE,
    schema_name="accounting",
    description="GL, chart of accounts, journal entries, AP/AR",
    publishes=(
        "accounting.journal.posted",
        "accounting.invoice.issued",
        "accounting.payment.recorded",
    ),
    subscribes=(
        "sales.order.invoiced",
        "procurement.invoice.received",
        "payroll.run.completed",
    ),
)

BANKING = BoundedContext(
    id="banking",
    display_name="Banking",
    context_type=BoundedContextType.FINANCE,
    schema_name="banking",
    description="Core banking, accounts, loans, cards",
    publishes=(
        "banking.account.opened",
        "banking.transaction.posted",
        "banking.loan.disbursed",
    ),
    subscribes=("identity.user.created",),
)

ISLAMIC_BANKING = BoundedContext(
    id="islamic_banking",
    display_name="Islamic Banking",
    context_type=BoundedContextType.FINANCE,
    schema_name="islamic_banking",
    description="Sharia products: Murabaha, Ijara, Sukuk, profit distribution",
    publishes=(
        "islamic_banking.contract.executed",
        "islamic_banking.profit.distributed",
    ),
    subscribes=("banking.account.opened",),
)

TREASURY = BoundedContext(
    id="treasury",
    display_name="Treasury",
    context_type=BoundedContextType.FINANCE,
    schema_name="treasury",
    description="Cash management, liquidity, investments",
    publishes=("treasury.transfer.executed", "treasury.position.updated"),
    subscribes=("banking.transaction.posted", "currency_exchange.deal.settled"),
)

CURRENCY_EXCHANGE = BoundedContext(
    id="currency_exchange",
    display_name="Currency Exchange",
    context_type=BoundedContextType.FINANCE,
    schema_name="currency_exchange",
    description="FX rates, deals, vault, compliance",
    publishes=(
        "currency_exchange.rate.updated",
        "currency_exchange.deal.settled",
    ),
    subscribes=("identity.user.created",),
)

TAX = BoundedContext(
    id="tax",
    display_name="Tax",
    context_type=BoundedContextType.FINANCE,
    schema_name="tax",
    description="Tax codes, filings, VAT/GST, withholding",
    publishes=("tax.return.filed", "tax.liability.calculated"),
    subscribes=("accounting.journal.posted", "payroll.run.completed"),
)

# ── HR & Commercial ──────────────────────────────────────────────────────

PAYROLL = BoundedContext(
    id="payroll",
    display_name="Payroll",
    context_type=BoundedContextType.OPERATIONS,
    schema_name="payroll",
    description="Salary runs, deductions, payslips",
    publishes=("payroll.run.completed", "payroll.payslip.generated"),
    subscribes=("human_resources.attendance.closed", "human_resources.employee.hired"),
)

HUMAN_RESOURCES = BoundedContext(
    id="human_resources",
    display_name="Human Resources",
    context_type=BoundedContextType.OPERATIONS,
    schema_name="human_resources",
    description="Employees, org structure, leave, performance",
    publishes=(
        "human_resources.employee.hired",
        "human_resources.employee.terminated",
        "human_resources.leave.requested",
        "human_resources.attendance.closed",
    ),
    subscribes=("identity.user.created",),
)

CRM = BoundedContext(
    id="crm",
    display_name="CRM",
    context_type=BoundedContextType.OPERATIONS,
    schema_name="crm",
    description="Contacts, accounts, opportunities, activities",
    publishes=(
        "crm.contact.created",
        "crm.opportunity.won",
        "crm.opportunity.lost",
    ),
    subscribes=("sales.quotation.sent",),
)

SALES = BoundedContext(
    id="sales",
    display_name="Sales",
    context_type=BoundedContextType.OPERATIONS,
    schema_name="sales",
    description="Quotations, orders, pricing, commissions",
    publishes=(
        "sales.quotation.sent",
        "sales.order.confirmed",
        "sales.order.invoiced",
    ),
    subscribes=("inventory.stock.reserved", "crm.opportunity.won"),
)

PROCUREMENT = BoundedContext(
    id="procurement",
    display_name="Procurement",
    context_type=BoundedContextType.OPERATIONS,
    schema_name="procurement",
    description="Requisitions, RFQ, purchase orders, vendor management",
    publishes=(
        "procurement.purchase_order.submitted",
        "procurement.goods.received",
        "procurement.invoice.received",
    ),
    subscribes=("inventory.reorder.triggered",),
)

INVENTORY = BoundedContext(
    id="inventory",
    display_name="Inventory",
    context_type=BoundedContextType.OPERATIONS,
    schema_name="inventory",
    description="Stock levels, SKUs, valuation, reorder rules",
    publishes=(
        "inventory.stock.adjusted",
        "inventory.stock.reserved",
        "inventory.reorder.triggered",
    ),
    subscribes=(
        "procurement.goods.received",
        "sales.order.confirmed",
        "manufacturing.production.completed",
    ),
)

WAREHOUSE = BoundedContext(
    id="warehouse",
    display_name="Warehouse",
    context_type=BoundedContextType.OPERATIONS,
    schema_name="warehouse",
    description="WMS — bins, picking, putaway, shipping",
    publishes=(
        "warehouse.shipment.dispatched",
        "warehouse.receipt.confirmed",
    ),
    subscribes=("procurement.purchase_order.submitted", "sales.order.confirmed"),
)

MANUFACTURING = BoundedContext(
    id="manufacturing",
    display_name="Manufacturing",
    context_type=BoundedContextType.OPERATIONS,
    schema_name="manufacturing",
    description="BOM, MRP, work orders, quality",
    publishes=(
        "manufacturing.work_order.released",
        "manufacturing.production.completed",
        "manufacturing.quality.failed",
    ),
    subscribes=("inventory.stock.reserved", "sales.order.confirmed"),
)

CONSTRUCTION = BoundedContext(
    id="construction",
    display_name="Construction",
    context_type=BoundedContextType.INDUSTRY,
    schema_name="construction",
    description="BOQ, subcontractors, site management",
    publishes=(
        "construction.boq.approved",
        "construction.milestone.completed",
    ),
    subscribes=("projects.phase.completed",),
)

PROJECTS = BoundedContext(
    id="projects",
    display_name="Projects",
    context_type=BoundedContextType.OPERATIONS,
    schema_name="projects",
    description="Project planning, tasks, resources, timesheets",
    publishes=(
        "projects.project.created",
        "projects.phase.completed",
        "projects.timesheet.approved",
    ),
    subscribes=("crm.opportunity.won",),
)

# ── Industry verticals ───────────────────────────────────────────────────

UNIVERSITY = BoundedContext(
    id="university",
    display_name="University",
    context_type=BoundedContextType.INDUSTRY,
    schema_name="university",
    description="Higher ed — admissions, academics, research",
    publishes=(
        "university.student.enrolled",
        "university.course.completed",
        "university.grade.posted",
    ),
    subscribes=("identity.user.created", "finance.budget.approved"),
)

SCHOOL = BoundedContext(
    id="school",
    display_name="School",
    context_type=BoundedContextType.INDUSTRY,
    schema_name="school",
    description="K-12 — enrollment, grading, parent portal",
    publishes=(
        "school.student.enrolled",
        "school.attendance.recorded",
        "school.grade.posted",
    ),
    subscribes=("identity.user.created",),
)

HOSPITAL = BoundedContext(
    id="hospital",
    display_name="Hospital",
    context_type=BoundedContextType.INDUSTRY,
    schema_name="hospital",
    description="EMR, encounters, clinical workflows",
    publishes=(
        "hospital.patient.admitted",
        "hospital.encounter.completed",
        "hospital.discharge.summary",
    ),
    subscribes=("identity.user.created", "laboratory.result.finalized"),
)

CLINIC = BoundedContext(
    id="clinic",
    display_name="Clinic",
    context_type=BoundedContextType.INDUSTRY,
    schema_name="clinic",
    description="Ambulatory care — appointments, outpatient encounters, referrals",
    publishes=(
        "clinic.appointment.scheduled",
        "clinic.encounter.completed",
        "clinic.referral.sent",
    ),
    subscribes=("identity.user.created", "laboratory.result.finalized"),
)

LABORATORY = BoundedContext(
    id="laboratory",
    display_name="Laboratory",
    context_type=BoundedContextType.INDUSTRY,
    schema_name="laboratory",
    description="LIMS, samples, results, QC",
    publishes=(
        "laboratory.sample.received",
        "laboratory.result.finalized",
    ),
    subscribes=("hospital.encounter.completed",),
)

PHARMACY = BoundedContext(
    id="pharmacy",
    display_name="Pharmacy",
    context_type=BoundedContextType.INDUSTRY,
    schema_name="pharmacy",
    description="Dispensing, prescriptions, drug inventory",
    publishes=(
        "pharmacy.prescription.dispensed",
        "pharmacy.stock.depleted",
    ),
    subscribes=("hospital.encounter.completed", "inventory.stock.adjusted"),
)

HOTEL = BoundedContext(
    id="hotel",
    display_name="Hotel",
    context_type=BoundedContextType.INDUSTRY,
    schema_name="hotel",
    description="Reservations, housekeeping, room management",
    publishes=(
        "hotel.reservation.confirmed",
        "hotel.checkout.completed",
    ),
    subscribes=("crm.contact.created", "accounting.invoice.issued"),
)

RESTAURANT = BoundedContext(
    id="restaurant",
    display_name="Restaurant",
    context_type=BoundedContextType.INDUSTRY,
    schema_name="restaurant",
    description="Orders, kitchen, tables, menu",
    publishes=(
        "restaurant.order.placed",
        "restaurant.order.completed",
    ),
    subscribes=("inventory.stock.adjusted",),
)

POS = BoundedContext(
    id="pos",
    display_name="POS",
    context_type=BoundedContextType.INDUSTRY,
    schema_name="pos",
    description="Point of sale — terminals, shifts, receipts, in-store checkout",
    publishes=(
        "pos.sale.completed",
        "pos.shift.closed",
        "pos.receipt.issued",
    ),
    subscribes=(
        "inventory.stock.adjusted",
        "sales.order.confirmed",
        "identity.user.created",
    ),
)

REAL_ESTATE = BoundedContext(
    id="real_estate",
    display_name="Real Estate",
    context_type=BoundedContextType.INDUSTRY,
    schema_name="real_estate",
    description="Listings, leases, sales, property management",
    publishes=(
        "real_estate.listing.published",
        "real_estate.lease.signed",
        "real_estate.sale.closed",
    ),
    subscribes=("crm.contact.created",),
)

GOVERNMENT = BoundedContext(
    id="government",
    display_name="Government",
    context_type=BoundedContextType.INDUSTRY,
    schema_name="government",
    description="Citizen services, permits, public procurement",
    publishes=(
        "government.permit.issued",
        "government.case.resolved",
    ),
    subscribes=("procurement.purchase_order.submitted", "documents.document.signed"),
)

MUNICIPALITY = BoundedContext(
    id="municipality",
    display_name="Municipality",
    context_type=BoundedContextType.INDUSTRY,
    schema_name="municipality",
    description="Local government — permits, utilities, citizen services, local tax",
    publishes=(
        "municipality.permit.issued",
        "municipality.service.request.closed",
        "municipality.utility.bill.issued",
    ),
    subscribes=("government.permit.issued", "identity.user.created"),
)

NGO = BoundedContext(
    id="ngo",
    display_name="NGO",
    context_type=BoundedContextType.INDUSTRY,
    schema_name="ngo",
    description="Grants, programs, donor management, field ops",
    publishes=(
        "ngo.grant.awarded",
        "ngo.program.milestone.reached",
    ),
    subscribes=("crm.contact.created", "finance.budget.approved"),
)

ALL_CONTEXTS: tuple[BoundedContext, ...] = (
    CORE_PLATFORM,
    IDENTITY,
    WORKFLOW,
    INTEGRATION,
    DOCUMENTS,
    NOTIFICATIONS,
    ANALYTICS,
    AI,
    MEDIA,
    SEARCH,
    SETTINGS,
    LOCALIZATION,
    ORGANIZATION,
    AUDIT,
    POLICY,
    IDENTITY_LIFECYCLE,
    COMPLIANCE,
    FEATURE_FLAGS,
    PLUGINS,
    FINANCIAL_KERNEL,
    FINANCE,
    ACCOUNTING,
    BANKING,
    ISLAMIC_BANKING,
    TREASURY,
    CURRENCY_EXCHANGE,
    TAX,
    PAYROLL,
    HUMAN_RESOURCES,
    CRM,
    SALES,
    PROCUREMENT,
    INVENTORY,
    WAREHOUSE,
    MANUFACTURING,
    CONSTRUCTION,
    PROJECTS,
    UNIVERSITY,
    SCHOOL,
    HOSPITAL,
    CLINIC,
    LABORATORY,
    PHARMACY,
    HOTEL,
    RESTAURANT,
    POS,
    REAL_ESTATE,
    GOVERNMENT,
    MUNICIPALITY,
    NGO,
)

CONTEXT_BY_ID: dict[str, BoundedContext] = {c.id: c for c in ALL_CONTEXTS}


def get_context(context_id: str) -> BoundedContext | None:
    return CONTEXT_BY_ID.get(context_id)
