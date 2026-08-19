# MEOS Incident Response

**Status:** Procedure documented; **production IR not active** (P314 go-live not approved).  
**Date:** 2026-08-18T05:54:44Z · **P329 overlay:** [MEOS_CRISIS_MANAGEMENT.md](./MEOS_CRISIS_MANAGEMENT.md) · declared crises **0**.

This is the IR playbook to use **after** `GO_LIVE = APPROVED`. It is not evidence of a live on-call rotation.

## Current incident log

No production incidents. There is no production traffic.

Workstation / demo failures must not be filed as production P0.

## Severity

| Class | Meaning | Response |
|-------|---------|----------|
| P0 | System, security, or data critical | Immediate contain → diagnose → recover → PIR |
| P1 | Major business or production impact | Same loop, after P0 |
| P2 | Important, non-critical | Scheduled fix with change control |
| P3 | Minor / backlog | Backlog |

## Loop (production only)

DETECT → CLASSIFY → CONTAIN → DIAGNOSE → RECOVER → VERIFY → DOCUMENT → POST-INCIDENT REVIEW

Distinguish **root cause** from **symptom**. Do not patch production without a traceable release.

## Resume condition

Activate this playbook as the live IR path only when [MEOS_P314_GO_LIVE_REPORT.md](./MEOS_P314_GO_LIVE_REPORT.md) records `GO_LIVE = APPROVED` and [MEOS_P315_PRODUCTION_STABILIZATION.md](./MEOS_P315_PRODUCTION_STABILIZATION.md) is in Hypercare.
