# ADR-376: Data Security — Strategy Foundation (P211-A)

## Status

Accepted — P211-A Enterprise Data Security & Privacy Intelligence Platform foundation

## Context

Volume 06 requires a centralized **data security & privacy intelligence control plane** spanning data discovery, classification, DSPM, privacy risk, access governance, protection controls (encryption/tokenization/masking/DLP intents), AI data security, lineage, and KG/twin bindings. `consent` owns consent ledger / DSAR / DPIA hooks. `secrets` (P209) owns KMS/PKI crypto material. `cyber_security` (P210) owns threat defense. Authorization (P208) owns PDP decisions. No existing SoR owns enterprise DSPM / data asset intelligence.

**Capability:** `CAP-PLT-DS-001` Enterprise Data Security & Privacy Intelligence

**Hard laws:** SoR is `data_security`. Surfaces under `/data-security/strategy*`. Never undiscoverable data assets. Never unclassifiable sensitive data. Never unmeasurable privacy risks. Never ungoverned data access. Never unprotected AI data. Never unavailable data lineage. Never non-generatable compliance evidence. Never invent sibling DSPM/privacy-intelligence BCs. Crypto material via P209. Consent/DSAR via `consent`. Detection handoff via P210.

## Decision

1. New platform SoR `backend/contexts/data_security/` (schema `data_security`)
2. Series roadmap: `P211_MASTER_SERIES_ROADMAP.v1.yaml` (A done; B–O planned)
3. Surfaces under `/api/v1/data-security/strategy*`
4. Law: `ENTERPRISE_DATA_SECURITY_STRATEGY.md`
5. Catalogs: `DATA_SECURITY_STRATEGY_*.v1.yaml`
6. Runtime: `ds_platform_strategy.py`; aggregates; ACL; foundation validator
7. Forbidden siblings: `dspm`, `dspm_platform`, `privacy_intelligence`, `data_classification`, `data_protection_platform`, `data_lineage_platform`

## Consequences

- P211-B–O deepen mission, domain, discovery, classification, protection, privacy, access, DSPM, AI data, KG/twin, ops, deploy, QA on the same SoR
- Complements — does not replace — `consent`, `secrets`, `cyber_security`, `authorization`, Compliance Framework

## References

ADR-159 · ADR-345 · ADR-361–375 · NIST Privacy Framework · ISO 27701 · GDPR · DSPM patterns
