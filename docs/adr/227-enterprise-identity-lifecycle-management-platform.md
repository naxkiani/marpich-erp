# ADR-227: Enterprise Identity Lifecycle Management Platform (EILMP) — P201 Series

## Status

Accepted — P201 series SoR + P201-A Registration & Onboarding foundation

## Context

P201 ultra-prompt defines EILMP as the authoritative identity lifecycle engine for MEOS. ADR-192 already shipped SoR `identity_lifecycle`. P200-B (EIFTP) forbids inventing product-named sibling BCs (`eiftp`). The same rule applies to EILMP.

P201-A focuses on **Identity Registration & Onboarding** — the authoritative entry point for every identity type.

## Decision

1. SoR remains `backend/contexts/identity_lifecycle/` — **never** create `contexts/eilmp/`
2. Law: `docs/architecture/ENTERPRISE_IDENTITY_LIFECYCLE_MANAGEMENT_PLATFORM.md`
3. Catalogs: `docs/architecture/identity/eilmp/*.v1.yaml`
4. P201-A surface: registration · validation · duplicate detection · approval · profile init · onboarding orchestration under `/api/v1/identity-lifecycle/registration/*` (+ `/eilmp/*` discovery)
5. Approvals via Workflow Engine; rules via Policy Engine; Audit via integration events; Permit/Deny stays Authorization PDP
6. Federation supplies trust facts only; Directory performs SCIM/LDAP sync; Identity owns user records; IGA owns access reviews
7. Shared port: `IIdentityLifecycleStatus` for peer fact reads
8. Series roadmap: P201-A … P201-A7 in `P201_MASTER_SERIES_ROADMAP.v1.yaml`

## Consequences

- Existing ADR-192 APIs remain; P201-A extends without rewrite
- Registration is policy/Zero Trust gated; unmanaged duplicates rejected
- Later phases (provisioning ACL, credentials, sync, ZT continuous, AI/KG/Twin, ops DoD) deepen the same SoR

## References

ADR-192 · 161 (IGA) · 190 (EIF) · 212–226 (EIFTP) · Workflow · Policy · Audit · Directory
