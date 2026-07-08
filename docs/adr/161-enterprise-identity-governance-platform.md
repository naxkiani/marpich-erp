# ADR-161: Enterprise Identity Governance Platform

## Status

Accepted

## Context

Identity authentication and RBAC exist in `contexts/identity/`, but there is no enterprise identity governance (IGA) layer for access requests, periodic access reviews, privilege certification, segregation of duties enforcement, temporary access, emergency break-glass access, and governance audit trails.

Requirements:
- User and role lifecycle governance (delegated to identity)
- Access request workflow with approval
- Access and privilege reviews
- SoD conflict detection
- Time-limited temporary and emergency access
- Privilege certification attestation
- Identity governance dashboard

## Decision

Implement **Enterprise Identity Governance Platform** at `/api/v1/identity-governance`.

### New bounded context

`backend/contexts/identity_governance/` — orchestration over identity, workflow, and audit.

### Capabilities (12)

| Capability | Feature |
|------------|---------|
| User Lifecycle | Delegates to identity |
| Role Lifecycle | Delegates to identity |
| Access Request | Submit and approve role requests |
| Access Review | Periodic access certification campaigns |
| Privilege Review | Privilege attestation |
| Segregation of Duties | SoD conflict rules and enforcement |
| Temporary Access | Time-limited role grants |
| Emergency Access | Break-glass access (links to security incidents) |
| Certification | Privilege certification workflow |
| Approval | Approval workflow integration |
| Audit | Governance audit log |
| Identity Dashboard | Unified IGA overview |

### Aggregates

- `IdentityGovernanceProfile` — review frequency, SoD, access limits
- `AccessRequest` — role access requests with SoD validation
- `AccessReview` — periodic review campaigns
- `PrivilegeCertification` — attestation records
- `TemporaryAccessGrant` — time-limited access
- `EmergencyAccessGrant` — break-glass access
- `GovernanceAuditEntry` — governance audit trail

### Policy Keys

- `identity_governance.access_review.frequency_days`
- `identity_governance.certification.required`
- `identity_governance.sod.enforcement`
- `identity_governance.temporary_access.max_hours`
- `identity_governance.emergency_access.max_hours`

### Events

- `identity_governance.access_request.submitted`
- `identity_governance.access_request.approved`
- `identity_governance.access_review.completed`
- `identity_governance.sod.violation_detected`
- `identity_governance.emergency_access.granted`

### Permissions

- `identity_governance.read`
- `identity_governance.write`
- `identity_governance.approve`

## Consequences

- Seed creates sample access requests, quarterly review, and pending certification
- SoD rules block conflicting role combinations when enforcement enabled
- Emergency access limited to policy max hours (default 4h)
- Identity auth/RBAC not duplicated — delegated to identity context

## Alternatives considered

- Extend identity context only — rejected (auth ≠ governance workflows)
- Autonomous access provisioning — rejected (approval required)
