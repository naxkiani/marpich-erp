# ADR-158: Enterprise Security Incident Platform

## Status

Accepted

## Context

Security attack monitoring exists in the Enterprise Security Platform, but there is no unified incident response orchestration covering detection through recovery. Incident response requires classification, investigation, containment, evidence collection, digital forensics, escalation, notification, SLA tracking, root cause analysis, and lessons learned.

Requirements:
- Full incident lifecycle management
- Evidence collection with chain of custody
- Digital forensics (explainable, no autonomous execution)
- SLA tracking for response and resolution
- Delegation to security, workflow, audit — no duplication

## Decision

Implement **Enterprise Security Incident Platform** at `/api/v1/security-incidents`.

### New bounded context

`backend/contexts/security_incident/` — orchestration layer over security and workflow engines.

### Capabilities (13)

| Capability | Feature |
|------------|---------|
| Incident Detection | Auto-detect from security.attack.detected events |
| Incident Classification | 9 classification types |
| Investigation | Assign and track investigation |
| Containment | Record containment actions |
| Recovery | Record recovery actions |
| Root Cause Analysis | Document root cause |
| Lessons Learned | Post-incident recommendations |
| Evidence Collection | Chain-of-custody evidence |
| Digital Forensics | Explainable forensic analysis |
| Escalation | Auto-escalate by severity threshold |
| Notification | Multi-channel incident alerts |
| SLA | Response and resolution SLA tracking |
| Incident Dashboard | Unified SOC dashboard |

### Aggregates

- `IncidentTenantProfile` — SLA settings, notification config
- `SecurityIncident` — canonical incident record
- `IncidentEvidence` — evidence with chain of custody
- `IncidentNotification` — sent notifications
- `IncidentLessonLearned` — post-incident lessons

### Policy Keys (domain: `tax`)

- `incident.detection.sensitivity_threshold`
- `incident.escalation.severity_threshold`
- `incident.sla.response_hours`
- `incident.sla.resolution_hours`
- `incident.notification.auto_notify`

### Events

- `incident.detected`
- `incident.classified`
- `incident.escalated`
- `incident.contained`
- `incident.resolved`
- `incident.evidence.collected`
- `incident.notification.sent`

Subscribes to `security.attack.detected` for automatic incident creation.

### API Surface

- `GET /catalog`, `GET /dependency-map`, `POST /seed`
- `GET /dashboard`
- `GET/POST /incidents`, `GET /incidents/{ref}`
- `POST /incidents/{ref}/classify`, `/investigate`, `/contain`, `/recover`
- `POST /incidents/{ref}/root-cause`, `/forensics`, `/escalate`, `/resolve`
- `POST/GET /incidents/{ref}/evidence`
- `POST /incidents/{ref}/lessons`, `GET /lessons`
- `POST /incidents/{ref}/notify`, `GET /notifications`
- `GET /sla`

### Permissions

- `incident.read`, `incident.write`, `incident.respond`

## Consequences

- Seed registers 6 incidents across classifications in various lifecycle states
- Critical/high severity incidents auto-escalate per policy threshold
- Security attack events automatically create incidents
- Digital forensics is explainable only — `autonomous_execution: false`
- Workflow emergency lock available for escalation (delegated, not duplicated)

## Alternatives considered

- Extend Security Platform only — rejected (attack monitoring ≠ incident response lifecycle)
- Per-module incident tracking — rejected (fragmentation)
- Autonomous containment — rejected (human-in-the-loop response required)
