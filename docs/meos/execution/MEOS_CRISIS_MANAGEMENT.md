# MEOS Crisis Management

**Date:** 2026-08-18T13:20:00Z  
**SoR (IR):** [MEOS_INCIDENT_RESPONSE.md](./MEOS_INCIDENT_RESPONSE.md) — **do not fork a second incident platform.**  
**Machine:** [MEOS_CRISIS_REGISTRY.v1.yaml](./MEOS_CRISIS_REGISTRY.v1.yaml)  
**Architecture (not runtime):** P305 MEIRRE blueprint — `incident_reliability_operating` is **not** in `contexts/registry.py`. **Do not implement it here.**

`declared_count: 0` · `production_ir_active: false` · `command_staffed: false` · `resilience_score: NOT_SCORED`

G26 is a **launch P0**, not a declared live-site crisis (P316). Do not file workstation failures as production P0.

## Classification (vocabulary)

IR already uses P0–P3. P329 overlay: `NORMAL` · `ELEVATED` · `MAJOR` · `CRITICAL`.

**Current declared crisis class:** **none** (`NONE`).  
P316 production quality label **CRITICAL** means launch telemetry gap — **not** a crisis declaration.

## Lifecycle

```
DETECT → DECLARE → ASSESS → COMMAND → RESPOND → STABILIZE → RECOVER → VALIDATE → CLOSE → LEARN
```

IR loop (SoR): DETECT → CLASSIFY → CONTAIN → DIAGNOSE → RECOVER → VERIFY → DOCUMENT → PIR.

Production transitions: **NOT_IN_FORCE**. No auditable CRISIS_DECLARED events (no production, no crisis API).

## Declaration

Requires authorized actor **or** policy. Identity/AuthZ exist; **no** `crisis.declare` runtime. Arbitrary users must not declare enterprise crises. Until `GO_LIVE = APPROVED`, declaration remains **documentary**.

## Command structure

| Role | Staffing |
|------|----------|
| INCIDENT_COMMANDER | **NOT_AVAILABLE** |
| TECHNICAL_LEAD | **NOT_AVAILABLE** |
| BUSINESS_LEAD | **NOT_AVAILABLE** |
| SECURITY_LEAD | **NOT_AVAILABLE** |
| COMMUNICATION_LEAD | **NOT_AVAILABLE** |
| RECOVERY_LEAD | **NOT_AVAILABLE** |

Reuse Identity + `require_permissions`. No invented people. No on-call rotation (P315/P316).

## Command center UX

Existing home `KpiStrip` + AppShell + [MEOS_EXECUTIVE_COMMAND_CENTER.md](./MEOS_EXECUTIVE_COMMAND_CENTER.md). Observability desk is candidate UI, production **NOT_AVAILABLE** (G23). **No second dashboard.** Do not show invented ACTIVE_INCIDENTS.

## Escalation

Based on IR severity. Paths: **not staffed**. Duration/SLA-based auto-escalate: **NOT_IMPLEMENTED**. G23: no production alerting to start DETECT.

## Continuity modes

P316 labels: HEALTHY · DEGRADED · AT_RISK · CRITICAL (quality).  
P329 modes: NORMAL · DEGRADED · CONTINUITY · RECOVERY — **NOT_IN_FORCE** (no policy-controlled runtime switch).

## Decision / AI

P327 decisions remain DECIDE-only. AI stub **must not** assume command. Output would be AI-generated if used — not FACT. `AUTO-INC-001` **NOT_IMPLEMENTED**. High-impact automation **BLOCK_AUTOMATION**.
