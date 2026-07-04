# Domain Events Catalog
Published language for cross-context communication.

| Event | Version | Publisher | Subscribers |
|-------|---------|-----------|-------------|
| `accounting.invoice.issued` | 1 | `accounting` | — |
| `accounting.journal.posted` | 1 | `accounting` | tax |
| `accounting.payment.received` | 1 | `accounting` | real_estate |
| `ai.fraud.detected` | 1 | `ai` | — |
| `ai.insight.generated` | 1 | `ai` | — |
| `ai.prediction.completed` | 1 | `ai` | — |
| `analytics.alert.triggered` | 1 | `analytics` | — |
| `analytics.report.generated` | 1 | `analytics` | — |
| `banking.account.opened` | 1 | `banking` | islamic_banking |
| `banking.loan.disbursed` | 1 | `banking` | — |
| `banking.transaction.posted` | 1 | `banking` | treasury, currency_exchange, ai |
| `construction.boq.approved` | 1 | `construction` | — |
| `construction.milestone.completed` | 1 | `construction` | — |
| `construction.site.opened` | 1 | `construction` | — |
| `crm.contact.updated` | 1 | `crm` | ngo |
| `crm.lead.converted` | 1 | `crm` | real_estate |
| `crm.opportunity.won` | 1 | `crm` | sales, projects |
| `currency_exchange.deal.settled` | 1 | `currency_exchange` | — |
| `currency_exchange.rate.updated` | 1 | `currency_exchange` | — |
| `documents.document.archived` | 1 | `documents` | — |
| `documents.document.signed` | 1 | `documents` | — |
| `documents.document.uploaded` | 1 | `documents` | ai, media |
| `finance.period.closed` | 1 | `finance` | treasury, university, hotel, ngo |
| `finance.report.generated` | 1 | `finance` | — |
| `government.permit.issued` | 1 | `government` | — |
| `government.service.submitted` | 1 | `government` | — |
| `government.tender.awarded` | 1 | `government` | — |
| `hospital.admission.registered` | 1 | `hospital` | — |
| `hospital.encounter.completed` | 1 | `hospital` | — |
| `hospital.encounter.started` | 1 | `hospital` | laboratory, pharmacy |
| `hotel.checkin.completed` | 1 | `hotel` | restaurant |
| `hotel.checkout.completed` | 1 | `hotel` | — |
| `hotel.reservation.confirmed` | 1 | `hotel` | — |
| `human_resources.attendance.closed` | 1 | `human_resources` | — |
| `human_resources.employee.hired` | 1 | `human_resources` | construction, projects, university |
| `human_resources.employee.terminated` | 1 | `human_resources` | — |
| `identity.mfa.enabled` | 1 | `identity` | — |
| `identity.role.assigned` | 1 | `identity` | — |
| `identity.user.created` | 1 | `identity` | banking, islamic_banking, currency_exchange, human_resources, crm, university, school, hospital, hotel, government |
| `identity.user.logged_in` | 1 | `identity` | — |
| `inventory.reorder.triggered` | 1 | `inventory` | — |
| `inventory.stock.adjusted` | 1 | `inventory` | manufacturing, pharmacy, restaurant |
| `inventory.stock.reserved` | 1 | `inventory` | warehouse |
| `islamic_banking.ijara.started` | 1 | `islamic_banking` | — |
| `islamic_banking.murabaha.approved` | 1 | `islamic_banking` | — |
| `islamic_banking.murabaha.executed` | 1 | `islamic_banking` | — |
| `laboratory.qc.failed` | 1 | `laboratory` | — |
| `laboratory.result.available` | 1 | `laboratory` | — |
| `laboratory.sample.received` | 1 | `laboratory` | — |
| `manufacturing.order.completed` | 1 | `manufacturing` | — |
| `manufacturing.order.started` | 1 | `manufacturing` | — |
| `manufacturing.quality.failed` | 1 | `manufacturing` | — |
| `media.asset.uploaded` | 1 | `media` | — |
| `media.transcode.completed` | 1 | `media` | — |
| `ngo.donation.received` | 1 | `ngo` | — |
| `ngo.grant.awarded` | 1 | `ngo` | — |
| `ngo.program.completed` | 1 | `ngo` | — |
| `notifications.message.failed` | 1 | `notifications` | — |
| `notifications.message.sent` | 1 | `notifications` | — |
| `payroll.payslip.issued` | 1 | `payroll` | — |
| `payroll.run.completed` | 1 | `payroll` | — |
| `pharmacy.dispense.completed` | 1 | `pharmacy` | — |
| `pharmacy.prescription.received` | 1 | `pharmacy` | — |
| `platform.module.activated` | 1 | `core_platform` | settings |
| `platform.tenant.provisioned` | 1 | `core_platform` | identity, documents, settings |
| `platform.tenant.suspended` | 1 | `core_platform` | — |
| `procurement.goods.received` | 1 | `procurement` | inventory, manufacturing |
| `procurement.po.approved` | 1 | `procurement` | warehouse, construction |
| `projects.milestone.reached` | 1 | `projects` | ngo |
| `projects.project.created` | 1 | `projects` | — |
| `projects.task.completed` | 1 | `projects` | — |
| `real_estate.lease.signed` | 1 | `real_estate` | — |
| `real_estate.listing.published` | 1 | `real_estate` | — |
| `real_estate.sale.closed` | 1 | `real_estate` | — |
| `restaurant.order.completed` | 1 | `restaurant` | — |
| `restaurant.order.placed` | 1 | `restaurant` | — |
| `sales.order.fulfilled` | 1 | `sales` | — |
| `sales.order.placed` | 1 | `sales` | inventory, warehouse, manufacturing, projects |
| `sales.quote.accepted` | 1 | `sales` | — |
| `school.attendance.recorded` | 1 | `school` | — |
| `school.grade.published` | 1 | `school` | — |
| `school.student.enrolled` | 1 | `school` | — |
| `search.index.updated` | 1 | `search` | — |
| `settings.config.updated` | 1 | `settings` | — |
| `settings.feature.toggled` | 1 | `settings` | — |
| `tax.liability.calculated` | 1 | `tax` | — |
| `tax.return.filed` | 1 | `tax` | — |
| `treasury.liquidity.updated` | 1 | `treasury` | — |
| `treasury.transfer.executed` | 1 | `treasury` | — |
| `university.course.completed` | 1 | `university` | — |
| `university.grade.published` | 1 | `university` | — |
| `university.student.enrolled` | 1 | `university` | — |
| `warehouse.picklist.created` | 1 | `warehouse` | — |
| `warehouse.receipt.confirmed` | 1 | `warehouse` | — |
| `warehouse.shipment.dispatched` | 1 | `warehouse` | — |
| `workflow.process.approved` | 1 | `workflow` | — |
| `workflow.process.started` | 1 | `workflow` | — |
| `workflow.task.completed` | 1 | `workflow` | — |
