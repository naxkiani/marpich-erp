# Bounded Contexts Reference

**44 independent bounded contexts** — see [BOUNDED_CONTEXTS_REGISTRY.md](BOUNDED_CONTEXTS_REGISTRY.md) for master catalog.

**Never merge unrelated domains. Every context evolves independently.**

## Core Platform (`core_platform`)

**Type:** platform · **Schema:** `platform_*` · **Path:** `backend/contexts/core_platform/`

Tenant lifecycle, module activation, platform configuration

### Aggregates

- `Tenant`
- `Subscription`
- `ModuleActivation`
- `IndustryPack`

### Publishes

- `platform.tenant.provisioned`
- `platform.module.activated`
- `platform.tenant.suspended`

### Subscribes


---

## Identity (`identity`)

**Type:** platform · **Schema:** `identity_*` · **Path:** `backend/contexts/identity/`

Authentication, authorization, RBAC, ABAC, MFA, sessions

### Aggregates

- `User`
- `Role`
- `Permission`
- `Session`
- `AbacPolicy`

### Publishes

- `identity.user.created`
- `identity.user.logged_in`
- `identity.role.assigned`
- `identity.mfa.enabled`

### Subscribes

- `platform.tenant.provisioned`

---

## Finance (`finance`)

**Type:** generic · **Schema:** `finance_*` · **Path:** `backend/contexts/finance/`

General ledger orchestration, financial periods, chart of accounts coordination

### Aggregates

- `FiscalPeriod`
- `ChartOfAccounts`
- `FinancialReport`

### Publishes

- `finance.period.closed`
- `finance.report.generated`

### Subscribes

- `accounting.journal.posted`
- `banking.transaction.posted`
- `sales.invoice.issued`

---

## Accounting (`accounting`)

**Type:** generic · **Schema:** `accounting_*` · **Path:** `backend/contexts/accounting/`

Journal entries, AP/AR, general ledger postings

### Aggregates

- `JournalEntry`
- `Account`
- `Invoice`
- `Payment`
- `VendorBill`

### Publishes

- `accounting.journal.posted`
- `accounting.invoice.issued`
- `accounting.payment.received`

### Subscribes

- `sales.order.fulfilled`
- `procurement.po.received`
- `payroll.run.completed`
- `hospital.encounter.completed`

---

## Banking (`banking`)

**Type:** specialized · **Schema:** `banking_*` · **Path:** `backend/contexts/banking/`

Core banking — accounts, loans, cards, transfers

### Aggregates

- `BankAccount`
- `Loan`
- `Card`
- `Transfer`
- `CustomerKYC`

### Publishes

- `banking.account.opened`
- `banking.transaction.posted`
- `banking.loan.disbursed`

### Subscribes

- `identity.user.created`
- `islamic_banking.murabaha.executed`

---

## Islamic Banking (`islamic_banking`)

**Type:** specialized · **Schema:** `islamic_banking_*` · **Path:** `backend/contexts/islamic_banking/`

Sharia-compliant products — Murabaha, Ijara, Sukuk, Musharaka

### Aggregates

- `MurabahaContract`
- `IjaraContract`
- `SukukIssue`
- `ShariaComplianceReview`

### Publishes

- `islamic_banking.murabaha.approved`
- `islamic_banking.murabaha.executed`
- `islamic_banking.ijara.started`

### Subscribes

- `banking.account.opened`
- `identity.user.created`

---

## Treasury (`treasury`)

**Type:** generic · **Schema:** `treasury_*` · **Path:** `backend/contexts/treasury/`

Cash management, liquidity, investments, FX hedging

### Aggregates

- `CashPosition`
- `Investment`
- `Hedge`
- `LiquidityForecast`

### Publishes

- `treasury.liquidity.updated`
- `treasury.transfer.executed`

### Subscribes

- `banking.transaction.posted`
- `currency_exchange.deal.settled`
- `finance.period.closed`

---

## Currency Exchange (`currency_exchange`)

**Type:** specialized · **Schema:** `currency_exchange_*` · **Path:** `backend/contexts/currency_exchange/`

FX rates, deals, vault, compliance

### Aggregates

- `ExchangeRate`
- `FxDeal`
- `Vault`
- `ComplianceCheck`

### Publishes

- `currency_exchange.rate.updated`
- `currency_exchange.deal.settled`

### Subscribes

- `identity.user.created`
- `banking.transaction.posted`

---

## Tax (`tax`)

**Type:** generic · **Schema:** `tax_*` · **Path:** `backend/contexts/tax/`

Tax rules, filings, VAT/GST, withholding

### Aggregates

- `TaxRule`
- `TaxReturn`
- `TaxFiling`
- `WithholdingRecord`

### Publishes

- `tax.return.filed`
- `tax.liability.calculated`

### Subscribes

- `accounting.journal.posted`
- `payroll.run.completed`
- `sales.invoice.issued`

---

## Payroll (`payroll`)

**Type:** generic · **Schema:** `payroll_*` · **Path:** `backend/contexts/payroll/`

Salary processing, deductions, payslips

### Aggregates

- `PayrollRun`
- `Payslip`
- `SalaryStructure`
- `Deduction`

### Publishes

- `payroll.run.completed`
- `payroll.payslip.issued`

### Subscribes

- `human_resources.employee.hired`
- `human_resources.attendance.closed`
- `tax.rule.updated`

---

## Human Resources (`human_resources`)

**Type:** generic · **Schema:** `hr_*` · **Path:** `backend/contexts/human_resources/`

Employees, org structure, leave, recruitment

### Aggregates

- `Employee`
- `Department`
- `LeaveRequest`
- `JobOpening`
- `Candidate`

### Publishes

- `human_resources.employee.hired`
- `human_resources.employee.terminated`
- `human_resources.attendance.closed`

### Subscribes

- `identity.user.created`
- `workflow.process.approved`

---

## CRM (`crm`)

**Type:** generic · **Schema:** `crm_*` · **Path:** `backend/contexts/crm/`

Contacts, leads, opportunities, customer 360

### Aggregates

- `Contact`
- `Lead`
- `Opportunity`
- `Account`
- `Activity`

### Publishes

- `crm.lead.converted`
- `crm.opportunity.won`
- `crm.contact.updated`

### Subscribes

- `sales.order.placed`
- `identity.user.created`

---

## Sales (`sales`)

**Type:** generic · **Schema:** `sales_*` · **Path:** `backend/contexts/sales/`

Quotes, orders, pricing, commissions

### Aggregates

- `Quote`
- `SalesOrder`
- `PriceList`
- `Commission`

### Publishes

- `sales.order.placed`
- `sales.order.fulfilled`
- `sales.quote.accepted`

### Subscribes

- `crm.opportunity.won`
- `inventory.stock.reserved`
- `warehouse.shipment.dispatched`

---

## Procurement (`procurement`)

**Type:** generic · **Schema:** `procurement_*` · **Path:** `backend/contexts/procurement/`

Purchase requisitions, POs, vendor management

### Aggregates

- `PurchaseRequisition`
- `PurchaseOrder`
- `Vendor`
- `GoodsReceipt`

### Publishes

- `procurement.po.approved`
- `procurement.goods.received`

### Subscribes

- `inventory.reorder.triggered`
- `workflow.process.approved`

---

## Inventory (`inventory`)

**Type:** generic · **Schema:** `inventory_*` · **Path:** `backend/contexts/inventory/`

Stock levels, items, batches, valuation

### Aggregates

- `Item`
- `StockLevel`
- `Batch`
- `StockMovement`

### Publishes

- `inventory.stock.reserved`
- `inventory.stock.adjusted`
- `inventory.reorder.triggered`

### Subscribes

- `sales.order.placed`
- `procurement.goods.received`
- `manufacturing.order.completed`
- `pharmacy.dispense.completed`

---

## Warehouse (`warehouse`)

**Type:** generic · **Schema:** `warehouse_*` · **Path:** `backend/contexts/warehouse/`

WMS — picking, receiving, locations, shipments

### Aggregates

- `Warehouse`
- `Location`
- `PickList`
- `Shipment`
- `Receipt`

### Publishes

- `warehouse.picklist.created`
- `warehouse.shipment.dispatched`
- `warehouse.receipt.confirmed`

### Subscribes

- `sales.order.placed`
- `procurement.po.approved`
- `inventory.stock.reserved`

---

## Manufacturing (`manufacturing`)

**Type:** generic · **Schema:** `manufacturing_*` · **Path:** `backend/contexts/manufacturing/`

MRP, BOM, production orders, quality

### Aggregates

- `BillOfMaterials`
- `ProductionOrder`
- `WorkCenter`
- `QualityInspection`

### Publishes

- `manufacturing.order.started`
- `manufacturing.order.completed`
- `manufacturing.quality.failed`

### Subscribes

- `sales.order.placed`
- `inventory.stock.adjusted`
- `procurement.goods.received`

---

## Construction (`construction`)

**Type:** industry · **Schema:** `construction_*` · **Path:** `backend/contexts/construction/`

Construction sites, BOQ, subcontractors, equipment

### Aggregates

- `ConstructionSite`
- `BillOfQuantities`
- `Subcontractor`
- `Equipment`

### Publishes

- `construction.site.opened`
- `construction.boq.approved`
- `construction.milestone.completed`

### Subscribes

- `projects.task.completed`
- `procurement.po.approved`
- `human_resources.employee.hired`

---

## Projects (`projects`)

**Type:** generic · **Schema:** `projects_*` · **Path:** `backend/contexts/projects/`

Project management, tasks, resources, timesheets

### Aggregates

- `Project`
- `Task`
- `Milestone`
- `Timesheet`
- `ResourceAllocation`

### Publishes

- `projects.project.created`
- `projects.task.completed`
- `projects.milestone.reached`

### Subscribes

- `crm.opportunity.won`
- `human_resources.employee.hired`
- `sales.order.placed`

---

## University (`university`)

**Type:** industry · **Schema:** `university_*` · **Path:** `backend/contexts/university/`

Higher education — admissions, academics, research

### Aggregates

- `Student`
- `Program`
- `Course`
- `Enrollment`
- `Grade`
- `ResearchProject`

### Publishes

- `university.student.enrolled`
- `university.grade.published`
- `university.course.completed`

### Subscribes

- `identity.user.created`
- `finance.period.closed`
- `human_resources.employee.hired`

---

## School (`school`)

**Type:** industry · **Schema:** `school_*` · **Path:** `backend/contexts/school/`

K-12 — classes, attendance, grading, parent portal

### Aggregates

- `Student`
- `Class`
- `AttendanceRecord`
- `GradeBook`
- `ParentGuardian`

### Publishes

- `school.student.enrolled`
- `school.attendance.recorded`
- `school.grade.published`

### Subscribes

- `identity.user.created`
- `notifications.template.send`

---

## Hospital (`hospital`)

**Type:** industry · **Schema:** `hospital_*` · **Path:** `backend/contexts/hospital/`

EMR, admissions, encounters, clinical workflows

### Aggregates

- `Patient`
- `Admission`
- `Encounter`
- `ClinicalOrder`
- `Bed`

### Publishes

- `hospital.admission.registered`
- `hospital.encounter.started`
- `hospital.encounter.completed`

### Subscribes

- `identity.user.created`
- `laboratory.result.available`
- `pharmacy.dispense.completed`

---

## Laboratory (`laboratory`)

**Type:** industry · **Schema:** `laboratory_*` · **Path:** `backend/contexts/laboratory/`

LIMS — samples, tests, results, QC

### Aggregates

- `Sample`
- `TestOrder`
- `TestResult`
- `QualityControl`

### Publishes

- `laboratory.sample.received`
- `laboratory.result.available`
- `laboratory.qc.failed`

### Subscribes

- `hospital.encounter.started`
- `hospital.clinical.order.placed`

---

## Pharmacy (`pharmacy`)

**Type:** industry · **Schema:** `pharmacy_*` · **Path:** `backend/contexts/pharmacy/`

Prescriptions, dispensing, drug inventory

### Aggregates

- `Prescription`
- `DispenseRecord`
- `DrugInteraction`
- `PharmacyStock`

### Publishes

- `pharmacy.prescription.received`
- `pharmacy.dispense.completed`

### Subscribes

- `hospital.encounter.started`
- `inventory.stock.adjusted`

---

## Hotel (`hotel`)

**Type:** industry · **Schema:** `hotel_*` · **Path:** `backend/contexts/hotel/`

Reservations, rooms, housekeeping, F&B integration

### Aggregates

- `Reservation`
- `Room`
- `Guest`
- `HousekeepingTask`
- `RatePlan`

### Publishes

- `hotel.reservation.confirmed`
- `hotel.checkin.completed`
- `hotel.checkout.completed`

### Subscribes

- `identity.user.created`
- `restaurant.order.placed`
- `finance.period.closed`

---

## Restaurant (`restaurant`)

**Type:** industry · **Schema:** `restaurant_*` · **Path:** `backend/contexts/restaurant/`

Tables, orders, kitchen, menu

### Aggregates

- `Table`
- `MenuItem`
- `RestaurantOrder`
- `KitchenTicket`

### Publishes

- `restaurant.order.placed`
- `restaurant.order.completed`

### Subscribes

- `inventory.stock.adjusted`
- `hotel.checkin.completed`

---

## Real Estate (`real_estate`)

**Type:** industry · **Schema:** `real_estate_*` · **Path:** `backend/contexts/real_estate/`

Listings, leases, sales, property management

### Aggregates

- `Property`
- `Listing`
- `Lease`
- `SaleTransaction`
- `MaintenanceRequest`

### Publishes

- `real_estate.listing.published`
- `real_estate.lease.signed`
- `real_estate.sale.closed`

### Subscribes

- `crm.lead.converted`
- `documents.document.signed`
- `accounting.payment.received`

---

## Government (`government`)

**Type:** industry · **Schema:** `government_*` · **Path:** `backend/contexts/government/`

Citizen services, permits, procurement, public finance

### Aggregates

- `Citizen`
- `ServiceRequest`
- `Permit`
- `PublicTender`
- `CaseFile`

### Publishes

- `government.service.submitted`
- `government.permit.issued`
- `government.tender.awarded`

### Subscribes

- `identity.user.created`
- `workflow.process.approved`
- `documents.document.signed`

---

## NGO (`ngo`)

**Type:** industry · **Schema:** `ngo_*` · **Path:** `backend/contexts/ngo/`

Donors, grants, programs, field operations

### Aggregates

- `Donor`
- `Grant`
- `Program`
- `Beneficiary`
- `FieldReport`

### Publishes

- `ngo.donation.received`
- `ngo.grant.awarded`
- `ngo.program.completed`

### Subscribes

- `crm.contact.updated`
- `finance.period.closed`
- `projects.milestone.reached`

---

## Workflow (`workflow`)

**Type:** platform · **Schema:** `workflow_*` · **Path:** `backend/contexts/workflow/`

BPM engine — process definitions, tasks, approvals

### Aggregates

- `ProcessDefinition`
- `ProcessInstance`
- `Task`
- `ApprovalChain`

### Publishes

- `workflow.process.started`
- `workflow.task.completed`
- `workflow.process.approved`

### Subscribes

- `*`

---

## Documents (`documents`)

**Type:** platform · **Schema:** `documents_*` · **Path:** `backend/contexts/documents/`

DMS — upload, version, sign, archive

### Aggregates

- `Document`
- `Folder`
- `DocumentVersion`
- `Signature`

### Publishes

- `documents.document.uploaded`
- `documents.document.signed`
- `documents.document.archived`

### Subscribes

- `platform.tenant.provisioned`

---

## Analytics (`analytics`)

**Type:** platform · **Schema:** `analytics_*` · **Path:** `backend/contexts/analytics/`

Data warehouse projections, dashboards, KPIs

### Aggregates

- `Dashboard`
- `Report`
- `Metric`
- `DataProjection`

### Publishes

- `analytics.report.generated`
- `analytics.alert.triggered`

### Subscribes

- `*`

---

## AI (`ai`)

**Type:** platform · **Schema:** `ai_*` · **Path:** `backend/contexts/ai/`

ML models, predictions, document intelligence, fraud

### Aggregates

- `ModelDeployment`
- `Prediction`
- `TrainingJob`
- `PromptTemplate`

### Publishes

- `ai.prediction.completed`
- `ai.fraud.detected`
- `ai.insight.generated`

### Subscribes

- `analytics.metric.updated`
- `documents.document.uploaded`
- `banking.transaction.posted`

---

## Notifications (`notifications`)

**Type:** platform · **Schema:** `notifications_*` · **Path:** `backend/contexts/notifications/`

Email, SMS, push, in-app notifications

### Aggregates

- `NotificationTemplate`
- `NotificationQueue`
- `DeliveryLog`

### Publishes

- `notifications.message.sent`
- `notifications.message.failed`

### Subscribes

- `*`

---

## Media (`media`)

**Type:** platform · **Schema:** `media_*` · **Path:** `backend/contexts/media/`

Asset storage, CDN, image processing, video

### Aggregates

- `MediaAsset`
- `MediaCollection`
- `TranscodingJob`

### Publishes

- `media.asset.uploaded`
- `media.transcode.completed`

### Subscribes

- `documents.document.uploaded`

---

## Search (`search`)

**Type:** platform · **Schema:** `search_*` · **Path:** `backend/contexts/search/`

Full-text search, indexing, facets

### Aggregates

- `SearchIndex`
- `IndexDocument`
- `SearchQuery`

### Publishes

- `search.index.updated`

### Subscribes

- `*`

---

## Settings (`settings`)

**Type:** platform · **Schema:** `settings_*` · **Path:** `backend/contexts/settings/`

Tenant config, feature flags, localization, industry pack

### Aggregates

- `TenantSettings`
- `FeatureFlag`
- `LocaleConfig`
- `IndustryPackConfig`

### Publishes

- `settings.config.updated`
- `settings.feature.toggled`

### Subscribes

- `platform.tenant.provisioned`
- `platform.module.activated`

---

