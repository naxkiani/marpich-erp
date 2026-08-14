# MEOS Wave 04 — Privacy Activation Runbook

**Status:** ACTIVATED (operational pack) · **Date:** 2026-08-13  
**Law:** Privacy is a platform concern — never fork local privacy tables in business modules. See `ENTERPRISE_COMPLIANCE_FRAMEWORK.md` / P269 roadmap.

## Activation checklist

1. **Enable Policy domains** for privacy retention / lawful basis via Policy Engine (`POST /api/v1/policies/evaluate`).
2. **Register retention policies** as versioned Policy Engine entries (effective date + expiration) — not hardcoded module limits.
3. **Audit every PII read/export** — integration events → Audit Platform (immutable).
4. **Document classes with personal data** use Document Exchange encryption + retention hooks — modules store `document_id` only.
5. **Feature flag** `privacy.rights.enabled` via Feature Flag System (tenant scope) before exposing DSAR UI.

## DSAR / rights (minimum path)

| Right | Platform path |
|-------|----------------|
| Access / export | Audit + Documents export APIs with AuthZ |
| Erasure request | Workflow definition `privacy.erasure.request` → human approval → owning context command |
| Restrict processing | Policy evaluate `privacy.processing.restricted` |

## Forbidden

- Module-local “privacy_requests” tables
- Silent PII logs
- Soft-delete only without audit event

## Verification

```bash
# Policy evaluate (authenticated)
curl -s -X POST "$API_URL/api/v1/policies/evaluate" \
  -H "Authorization: Bearer $TOKEN" -H "X-Tenant-ID: $TENANT" \
  -H "Content-Type: application/json" \
  -d '{"domain":"privacy","policy_key":"export_pii","facts":{"resource":"contact"}}'
```

Record HTTP outcome in Wave 04 smoke (`scripts/meos-wave04-governance-loop.sh`).
