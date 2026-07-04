# ADR-045: Enterprise Compliance Framework

## Status

Accepted

## Context

Regulated tenants require continuous compliance across internal policies, financial (SOX), tax, educational (FERPA), healthcare (HIPAA), documents, security, audit trails, data privacy, and retention. Existing platform services provide pieces — Audit (evidence), Policy Engine (rules), Document Exchange (retention), Security Standard (controls) — but no unified violation detection, dashboard, reports, or alerts.

## Decision

Adopt **`docs/architecture/ENTERPRISE_COMPLIANCE_FRAMEWORK.md`** as canonical compliance law.

### Orchestration, not duplication

Compliance Framework monitors and reports; Audit/Policy/Documents enforce underlying controls.

### Capabilities

- Ten compliance domains with control registry
- Violation detection from integration events
- Compliance dashboard, reports, alerts
- Retention compliance monitoring view

### New bounded context

`backend/contexts/compliance/` — violations, reports, dashboard, alert events.

## Consequences

- Modules declare compliance domains in context.yaml
- Violations route alerts via Notification Platform
- Industry packs seed domain controls on tenant provision
- No local compliance stores in business modules

## Alternatives considered

- Compliance checks only in Audit — rejected (different concern: evidence vs pass/fail monitoring)
- Third-party GRC only — rejected (must integrate with Marpich events and tenant model)
- Per-module compliance — rejected (fragmentation)
