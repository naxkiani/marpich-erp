# MEOS Customer Onboarding (P355)

Reuses Identity, Organization, Settings, Feature Flags, Audit, and Notifications. **No second tenant or identity engine.**

```
TENANT_CREATED
  → IDENTITY_CONFIGURED
  → EDITION_ASSIGNED
  → LICENSE_ASSIGNED
  → CONFIGURATION_INITIALIZED
  → ADMIN_CREATED
  → SECURITY_CONFIGURED
  → READY
```

Planner: `python3 scripts/meos-onboard.py` (PLAN_ONLY).

| Step | Existing capability |
|------|---------------------|
| TENANT_CREATED | Identity / platform tenant provision event |
| IDENTITY_CONFIGURED | `contexts.identity` |
| EDITION_ASSIGNED | Feature Flags + edition model |
| LICENSE_ASSIGNED | License contract (DESIGN); payment READY_FOR_CREDENTIALS |
| CONFIGURATION_INITIALIZED | Settings |
| ADMIN_CREATED | Identity register / roles |
| SECURITY_CONFIGURED | Authorization + audit |
| READY | Application `/api/v1/ready` — not G26 |

No production tenant is created without explicit authorization **and** EXT-G26. Demo data must be marked **DEMO**. No fake customers.
