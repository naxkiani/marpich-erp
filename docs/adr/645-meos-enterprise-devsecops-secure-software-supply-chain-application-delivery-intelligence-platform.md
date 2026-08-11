# ADR 645 — MEOS Enterprise DevSecOps, Secure Software Supply Chain & Application Delivery Intelligence Platform (MEDSSAD)

- **Status:** Accepted
- **Date:** 2026-08-11
- **Deciders:** Chief Enterprise Architect · MEOS Architecture Board
- **Tags:** meos · p288 · medssad · devsecops · sbom · provenance · supply-chain · sast · sca · release-security · productization
- **Related:** [ADR 644](644-meos-enterprise-cloud-platform-engineering-infrastructure-automation-intelligence-platform.md) · [ADR 643](643-meos-enterprise-it-operations-infrastructure-observability-intelligence-platform.md) · [ADR 625](625-meos-enterprise-cybersecurity-intelligence-zero-trust-defense-platform.md) · [ADR 646](646-meos-enterprise-application-architecture-api-governance-software-architecture-intelligence-platform.md) · [Law P288](../architecture/ENTERPRISE_MEOS_DEVSECOPS_SECURE_SOFTWARE_SUPPLY_CHAIN_APPLICATION_DELIVERY_INTELLIGENCE_PLATFORM.md) · Governance Standard 11.0

## Context

MEOS needs a specialized **DevSecOps / Secure Software Supply Chain / Application Delivery Intelligence** productization layer — without replacing Platform Engineering (P287), Cybersecurity/Zero Trust (P268), Technology Operations (P286), or Secrets, and without ungated insecure production releases.

## Decision

1. Establish SoR **`devsecops_operating`** as MEDSSAD fabric under API **`/api/v1/devsecops-operating*`**, schema **`devsecops_operating_*`**.
2. Capability **`CAP-PLT-MEDSSAD-001`**; fabric id **`meos_enterprise_devsecops_secure_software_supply_chain_application_delivery_intelligence_platform_framework`**.
3. **Boundary law (hard):**
   - **P287** = Cloud / Platform Engineering / Infrastructure Automation (provision/deploy platforms)
   - **P288** = Secure Software Delivery / DevSecOps / Supply Chain Security (secure SDLC, gates, provenance)
   - **P268** = Enterprise Cybersecurity / Zero Trust — **never replace**
   - **P286** = IT Operations / Observability — runtime security signals via ACL
4. Federate-by-contract: P287, P286, P268, P269, P270, Secrets, Feature Flags, Integration, Workflow — never fork Platform Engineering or Cyber APIs; never local secret stores; never local approval engines.
5. SBOMs, provenance attestations, artifacts and security findings are **versioned, explainable, reproducible, auditable**. Production releases require **Security Validation + Policy Validation + Risk Evaluation + Required Approval + Provenance + Rollback readiness**.
6. Security Gate decisions: **ALLOW · DENY · WARN · REQUIRE APPROVAL**.
7. **No AI Agent may execute uncontrolled security remediation or production changes outside Policy + Delegation Authority.** AI-generated code must pass normal review/scan/policy/test gates.
8. Inference → **P214-Z** only; no module-local LLM.
9. Twin security scenarios via P265 are non-actuating unless Policy + Workflow + DoA (or autonomy threshold) approve.

## Consequences

- Unlocks Phase 1–4 MEDSSAD roadmap (P288-A…D) and **P289** Application Architecture / API Governance series (delivered as normative law + ADR 646).
- P287 remains provision/deploy SoR; P268 remains cyber SoR; MEDSSAD owns secure delivery, supply-chain security and gated release overlays.
- Ungated insecure release or merging P287+P288+P268 SoRs is an architecture failure.

## Alternatives considered

| Alternative | Rejected because |
|-------------|------------------|
| Embed SDLC security inside P268 Cyber | Violates cyber defense vs secure delivery split |
| Embed release gates only inside P287 Platform Engineering | Violates provision/deploy vs secure SDLC split |
| Store detected secrets in DevSecOps tables | Violates Secrets Platform law |
| Local approval for security gates | Violates Workflow Engine law |
| Ungated agent remediation/release | Violates human security governance |

## Compliance checklist

- [x] DDD · CQRS · events · hexagonal boundaries documented
- [x] Peer federation matrix (P287 · P286 · P268 · Secrets · Workflow · Policy · Audit)
- [x] Versioned SBOM/provenance · Security Gates · release law
- [x] P287 · P268 · P286 boundaries preserved explicitly
- [x] No ungated production release · no local secrets
- [x] P289 delivered — [ADR 646 / MEAAGSI](646-meos-enterprise-application-architecture-api-governance-software-architecture-intelligence-platform.md)
- [x] P290 delivered — [ADR 647 / MEDAMIA](647-meos-enterprise-data-architecture-master-data-information-architecture-intelligence-platform.md)
