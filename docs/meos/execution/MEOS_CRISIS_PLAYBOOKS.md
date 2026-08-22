# MEOS Crisis Playbooks

**Date:** 2026-08-18T13:20:00Z  
**Machine:** [MEOS_CRISIS_PLAYBOOKS.v1.yaml](./MEOS_CRISIS_PLAYBOOKS.v1.yaml)  
**`active_count: 0`**

A markdown runbook is **not** an ACTIVE crisis playbook. Policy-controlled execution: **NOT_IN_FORCE**. Workflow Task Center exists; playbook steps are **not** wired as production tasks.

## Inventory (reuse only)

| ID | Hazard | Document | Production |
|----|--------|----------|------------|
| `PB-IR-001` | SERVICE_OUTAGE | [MEOS_INCIDENT_RESPONSE.md](./MEOS_INCIDENT_RESPONSE.md) | **NOT_ACTIVE** |
| `PB-DR-001` | DATABASE_FAILURE | [MEOS_WAVE04_DR_RUNBOOK.md](./MEOS_WAVE04_DR_RUNBOOK.md) | **NOT_VERIFIED** (local drill) |
| `PB-RB-001` | SERVICE_OUTAGE | [MEOS_ROLLBACK_STANDARD.md](./MEOS_ROLLBACK_STANDARD.md) | **BLOCKED** (G27) |
| `PB-OPS-001` | SERVICE_OUTAGE | [MEOS_PRODUCTION_RUNBOOK.md](./MEOS_PRODUCTION_RUNBOOK.md) | workstation profile only |
| `PB-SEC-001` | SECURITY_INCIDENT | IR P0 path | **NOT_ACTIVE** (no SOC) |
| `PB-DATA-001` | DATA_INCIDENT | [MEOS_WAVE04_PRIVACY_ACTIVATION.md](./MEOS_WAVE04_PRIVACY_ACTIVATION.md) | G19 **FAIL** |
| `PB-INT-001` | THIRD_PARTY_FAILURE | P321 | **NOT_APPLICABLE** (0 ACTIVE) |
| `PB-CAP-001` | CAPACITY_FAILURE | [MEOS_PRODUCTION_OPTIMIZATION.md](./MEOS_PRODUCTION_OPTIMIZATION.md) | **NOT_MEASURED** |
| `PB-AUTO-INC` | SERVICE_OUTAGE | `AUTO-INC-001` | **NOT_IMPLEMENTED** |

NATURAL_DISASTER / geographic failover: **not demonstrated**. Do not invent a weather playbook.

## Actions

ACTION / OWNER / DEADLINE: **NOT_AVAILABLE** for production crises (none declared). Connect to Workflow when IR is active — not now.

## Communication

Reuse Notification Center. Production INTERNAL/EXECUTIVE/TENANT crisis alerts: **NOT_AVAILABLE** (G23). No second notifier.

## Automated response

`DETECT → CLASSIFY → AUTHORIZE → EXECUTE → VERIFY` — high-impact **forbidden** without policy (P319). Do not auto-rollback financial/clinical paths (rollback standard).
