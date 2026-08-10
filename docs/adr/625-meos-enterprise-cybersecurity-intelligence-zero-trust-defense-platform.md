# ADR 625 — MEOS Enterprise Cybersecurity Intelligence & Zero Trust Defense Platform (P268)

## Status
Accepted

## Context
P267 established MEAOSH over P225 autonomous operations. P268 productizes Cybersecurity Intelligence & Zero Trust Defense as the MEOS Security Intelligence Operating Layer. P226 already owns `cyber_defense`; P246 owns `security_trust_intelligence`; P210 owns operational SOC/XDR/SOAR; Identity/AuthZ own IAM/PDP. MECZTD must federate those SoRs — never fork peer security APIs, never embed vendor security SDKs in domain, and never ungated critical containment. P269 is planned for Privacy, Compliance & Regulatory Intelligence over P230/Compliance.

## Decision
1. SoR `cyber_security_operating`; fabric `meos_enterprise_cybersecurity_intelligence_zero_trust_defense_platform_framework`; API `/api/v1/cyber-security-operating*`; capability `CAP-PLT-MECZTD-001`; acronym **MECZTD**.
2. Logical BCs inside one SoR: Identity Security Operating, Threat Intelligence Operating, Security Operations, Vulnerability Management, Zero Trust Operating, Security Governance.
3. Federate with P226, P246, P210, Identity, AuthZ, Secrets, P230, P267, P266, Workflow, Policy, Audit, P214-Z — never replace them; never dual-write peer security catalogs.
4. Inference only via P214-Z; critical contain/isolate/block require Workflow + human approval; simulation ≠ execute; no silent security actions without audit.
5. Roadmap: P268 foundation → P268-A…D; unblocks P269.

## Consequences
Positive: governed Security OS (AI-SOC, ZT overlays, response campaigns) over canonical cyber/trust SoRs.  
Negative: defense/trust/SOC truth remains peer-owned — MECZTD stores operating campaigns and peer refs only.

## Links
Law: `ENTERPRISE_MEOS_CYBERSECURITY_INTELLIGENCE_ZERO_TRUST_DEFENSE_PLATFORM.md` · Prior: ADR 624 · Next: P268-A · Peer: ADR 626 (P269 MEPCRI) · Canonical: P226 · P246 · P210
