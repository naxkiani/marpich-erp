# MEOS Risk Registry

**Date:** 2026-08-18T13:00:00Z  
**SoR (narrative):** [MEOS_RISK_REGISTER.md](./MEOS_RISK_REGISTER.md) — **do not fork a second GRC risk list.**  
**Machine:** [MEOS_RISK_REGISTRY.v1.yaml](./MEOS_RISK_REGISTRY.v1.yaml)

This file is the P328 overlay (states, control results, appetite). The seven launch risks are unchanged. **No new RISK_IDs.**

## Appetite / tolerance / threshold

**NOT_DECLARED.** No board or policy artifact sets appetite. Escalation of “exceeds tolerance” **cannot fire**. Qualitative launch severities are **not** a numeric score (`numeric_score: NOT_SCORED`).

## Ownership

Every row: `owner: NOT_AVAILABLE`. **Unowned material risks: 7. Unowned critical: R-01.** That is a finding, not an invented owner.

## States in use

All seven: **ASSESSED**. None MITIGATING (in production), MONITORED, ACCEPTED, ESCALATED, RESOLVED, or CLOSED.

## Control results (explainable, not scored)

| RISK | CONTROL_RESULT | Why |
|------|----------------|-----|
| R-01 | WEAK | Workstation demo is not a production cluster control |
| R-02 | WEAK | Local restore drill ≠ live rollback |
| R-03 | WEAK | `/health` without production alerting |
| R-04 | WEAK | Auth on stub does not make the stub a model |
| R-05 | FAILED | G19 DSAR runtime |
| R-06 | FAILED | Dirty SHA |
| R-07 | UNCONTROLLED | No control listed in launch register |

`grc` context: **DESIGNED** (no package). Do not implement it as a duplicate register.
