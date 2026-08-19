# MEOS Decision Memory

**Date:** 2026-08-18T14:05:00Z  
**SoR:** [MEOS_DECISION_INTELLIGENCE.md](./MEOS_DECISION_INTELLIGENCE.md) + [MEOS_DECISION_REGISTRY.v1.yaml](./MEOS_DECISION_REGISTRY.v1.yaml)  
**Do not fork a second decision-memory product.**

P332 adds the **learning** overlay: DECISION → RATIONALE → RESULT → LEARNING.

## Actual

| Field | Production / program |
|-------|----------------------|
| Captured decisions | Four phase DECIDE records (P314, P319, P324, P326) |
| RESULT / actual_outcome | **NOT_MEASURED** or count-zero (no production follow-up) |
| LEARNING | **BLOCKED** until MEASURE |
| Similarity / reuse UX | **NOT_IMPLEMENTED** |
| Blind reuse | **Forbidden** — context_difference not computed |

Owners **NOT_AVAILABLE**. `executed_count: 0`. `measured_followup_count: 0`.

When similar situations arise, operators should **read the registry + evidence paths**, not an AI similarity score. Stub assist must not invent PREVIOUS_DECISION matches.
