# MEOS Investment Prioritization Standard

**Date:** 2026-08-19T06:06:00Z  
**P335 overlay** on [MEOS_INITIATIVE_PORTFOLIO.md](./MEOS_INITIATIVE_PORTFOLIO.md). **Not** a scored optimizer or a new decision engine. Decision Fabric (P318) remains SoR for HITL decisions.

## Law

Do not emit a rank, score, or ROI unless every input dimension is measured **and** the method is documented. Missing dimension → **NOT_MEASURED**; do not impute zero or a default weight.

## Dimensions (intended vs actual)

| Dimension | Intended use | Production actual |
|-----------|--------------|-------------------|
| STRATEGIC_ALIGNMENT | Objective contribution | PLATFORM_GATE DRAFT only |
| BUSINESS_VALUE | Expected vs realized | **NOT_MEASURED** |
| RISK | Probability × impact | Qualitative R-01…R-07; no scores |
| URGENCY | Time criticality | G26 is current (no cluster) — evidenced |
| DEPENDENCIES | Blocked-by graph | YAML `depends_on` / BLK-G26 |
| CAPABILITY_READINESS | P333 | **NOT_MEASURED** |
| CHANGE_READINESS | P334 | **BLOCKED** |
| COST | Budget / actual | **NOT_MEASURED** |
| EFFORT | People / time | **NOT_MEASURED** |
| REVERSIBILITY | Rollback | G27 **NOT_EXERCISED** |

## Method in force now

**Name:** `P325_P313_P0_CHAIN`  
**Inputs:** open P0/P1 debt, P313 gates, change `depends_on`.  
**Assumptions:** no production → no measured value; G26 precedes all production work.  
**Result:** G26 → G25 → G27 then G23/G18/G19.  
**Confidence:** `HIGH_FOR_SEQUENCE_ONLY` (blocker evidence). **NOT_AVAILABLE** for money or value rank.  
**Owner:** **NOT_AVAILABLE**.

P1 trust work (alerting, AI stub, DSAR) is **not** ranked against each other with weights — all DEFER until G26.

## Transparency record

Every recommendation in [MEOS_PORTFOLIO_INTELLIGENCE.v1.yaml](./MEOS_PORTFOLIO_INTELLIGENCE.v1.yaml) `items[]` must include `inputs`, `assumptions`, `method`, `result`, `confidence`, `owner`.

## Forbidden

- Arbitrary 0–100 scores  
- Ranking unused marketplace SKUs or stub-AI “value” above G26  
- Treating catalog counts, login, or demo loops as value  
- Policy Engine fork (business rules stay in Policy)
