# ADR-160: Enterprise Regulatory Reporting Platform

## Status

Accepted

## Context

A manifest-driven regulatory reporting engine exists in `contexts/reporting/` (ADR-129) at `/api/v1/reports/regulatory`, but there is no enterprise orchestration layer covering all regulator types, report categories (AML, KYC, risk, compliance), configurable country adapters, and digital submission workflows.

Requirements:
- Support Central Bank, Tax Authority, FIU, Audit Authority, Government, NGO reporting
- Compliance, Risk, AML, and KYC report categories with delegation
- Digital submission to regulator portals
- XML, JSON, PDF export (manifest-driven, no hardcoded formats)
- Configurable country adapters per jurisdiction

## Decision

Implement **Enterprise Regulatory Reporting Platform** at `/api/v1/regulatory-reporting`.

### New bounded context

`backend/contexts/regulatory_reporting/` — orchestration layer over the reporting regulatory engine.

### Capabilities (16)

| Capability | Feature |
|------------|---------|
| Central Bank | Central bank regulatory reports |
| Tax Authority | Tax filings (delegates to tax) |
| Financial Intelligence Unit | FIU / AML intelligence (delegates to AML) |
| Audit Authority | Audit reports (delegates to audit) |
| Government | Government filings |
| NGO Reporting | NGO and grant reporting |
| Compliance Reports | Compliance category (delegates to compliance) |
| Risk Reports | Risk category (delegates to risk) |
| AML Reports | AML category (delegates to currency_exchange) |
| KYC Reports | KYC category (delegates to banking) |
| Digital Submission | Portal submission workflow |
| XML Export | Manifest-driven XML rendering |
| JSON Export | Manifest-driven JSON rendering |
| PDF Export | Manifest-driven PDF rendering |
| Country Adapters | Per-jurisdiction configuration |
| Regulatory Dashboard | Unified reporting overview |

### Aggregates

- `RegulatoryTenantProfile` — default format, country, digital submission settings
- `CountryAdapter` — per-country regulator types, formats, package mapping, portal URL
- `DigitalSubmission` — submission lifecycle (draft → rendered → submitted → acknowledged)

### Policy Keys

- `regulatory_reporting.default_format`
- `regulatory_reporting.package.required`
- `regulatory_reporting.submission.audit`
- `regulatory_reporting.digital_submission.enabled`
- `regulatory_reporting.country.default`

### Events

- `regulatory.adapter.configured`
- `regulatory.submission.created`
- `regulatory.submission.submitted`

### Delegation

- **Format rendering** → `contexts/reporting` regulatory engine (manifest-driven)
- **Tax** → tax engine datasets
- **AML** → currency_exchange AML platform
- **KYC** → banking KYC platform
- **Compliance/Risk** → compliance and risk platforms

### API Surface

- `GET /catalog`, `GET /dependency-map`, `POST /seed`
- `GET /dashboard`
- `GET/POST /adapters`
- `POST /reports/generate`
- `GET /submissions`, `GET /submissions/{ref}`
- `POST /submissions/{ref}/submit`

Legacy manifest-driven API remains at `/api/v1/reports/regulatory` (ADR-129).

## Consequences

- Seed configures 4 country adapters (EXAMPLE, IR, US, GLOBAL) and reporting packages
- All XML/JSON/PDF rendering delegated to reporting engine — `hardcoded_regulatory_formats: false`
- Country adapters map jurisdictions to installed regulatory packages
- Digital submission generates portal references without autonomous filing

## Alternatives considered

- Extend reporting context only — rejected (no country adapter or digital submission orchestration)
- Hardcode country XML schemas — rejected (manifest-driven per ADR-129)
- Replace ADR-129 API — rejected (backward compatibility)
