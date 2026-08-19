# MEOS Technical Debt Registry

**Date:** 2026-08-18T12:05:00Z  
**Machine:** [MEOS_TECHNICAL_DEBT_REGISTRY.v1.yaml](./MEOS_TECHNICAL_DEBT_REGISTRY.v1.yaml)  
**This is the P325 improvement backlog** (bugs / reliability / security / UX / debt). Do not fork a second backlog.  
**Risk companion:** [MEOS_RISK_REGISTER.md](./MEOS_RISK_REGISTER.md) — do not duplicate as a second risk system.

States: `IDENTIFIED` → `ASSESSED` → `PLANNED` → `IN_PROGRESS` → `RESOLVED` | `ACCEPTED`

Owners: **NOT_AVAILABLE** (not invented).

## Open critical (P0)

| DEBT_ID | AREA | STATUS | EVIDENCE |
|---------|------|--------|----------|
| `TD-G26-PROD-CLUSTER` | DEPLOYMENT | ASSESSED | P313 G26 |
| `TD-G25-DIRTY-SHA` | RELEASE | ASSESSED | `e941141-dirty` |
| `TD-G27-ROLLBACK` | RELIABILITY | ASSESSED | P313 G27 |

## Other open / accepted

`TD-G23-ALERTING`, `TD-G18-AI-STUB`, `TD-G19-DSAR`, `TD-G20-E2E`, `TD-G21-A11Y`, `TD-EVENT-PAYLOAD-SCHEMA` (IDENTIFIED).  
`TD-P319-AUTOMATION`, `TD-P321-INTEGRATIONS` (**ACCEPTED** until production exists — not fake “resolved”).

## Resolved this program (evidence)

| DEBT_ID | STATUS | Evidence |
|---------|--------|----------|
| `TD-SDK-STUB-SUCCESS` | **RESOLVED** | P323 `marpich-plugin pack` **exit 2** |

Do not mark G26/G25/G27 **RESOLVED**. Honesty test enforces that.
