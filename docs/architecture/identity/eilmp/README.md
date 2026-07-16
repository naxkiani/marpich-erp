# P201 — Enterprise Identity Lifecycle Management Platform (EILMP)

**SoR:** `backend/contexts/identity_lifecycle/` — do **not** create `contexts/eilmp/`  
**ADR series:** 227+ · Prior: ADR-192

## Series map

| Phase | Title | Status |
|-------|-------|--------|
| **P201-A** | Registration & Onboarding | **Done — ADR-227** |
| P201-A2 | Provisioning ACL + Workflow approvals | Pending |
| P201-A3 | Credential lifecycle orchestration | Pending |
| P201-A4 | Sync (SCIM/LDAP via Directory) | Pending |
| P201-A5 | Zero Trust continuous hooks | Pending |
| P201-A6 | AI / KG / Twin contracts | Pending |
| P201-A7 | Ops + series DoD | Pending |

## Boundaries

| Concern | Owner |
|---------|--------|
| Registration / JML / lifecycle state | identity_lifecycle |
| IGA reviews | identity_governance |
| Federation | identity_federation |
| AuthZ Permit/Deny | authorization |

Law: [`ENTERPRISE_IDENTITY_LIFECYCLE_MANAGEMENT_PLATFORM.md`](../../ENTERPRISE_IDENTITY_LIFECYCLE_MANAGEMENT_PLATFORM.md)
