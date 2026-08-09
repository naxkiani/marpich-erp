# ADR 590 — Enterprise Privacy, Digital Rights & Trust Intelligence Platform (P230)

## Status
Accepted

## Context
P229 established EFDMIFP (federated data mesh & intelligence fabric). P230 opens the Enterprise Privacy, Digital Rights & Trust Intelligence Platform (EPDRTIP) for privacy protection, digital rights, consent, trust intelligence, AI ethics and human-centric digital governance under MEOS 11.0. Identity, AuthZ, Audit, Compliance and Policy Engine remain authoritative platform SoRs — EPDRTIP federates privacy/trust intelligence rather than forking them.

## Decision
1. SoR `privacy_trust`; fabric `meos_enterprise_privacy_digital_rights_trust_intelligence_platform_framework`; API `/api/v1/privacy-trust*`; capability `CAP-PLT-EPDRTIP-001`.
2. Ten logical BCs inside one SoR: Privacy Management, Digital Rights, Consent Governance, Trust Intelligence, AI Ethics, Compliance Management, Identity Rights, Privacy Risk, Audit Governance, Trust Evolution.
3. Federate with Identity, AuthZ, Audit, Compliance, Policy, P212, P229, P228, P226 via ACL/events — never replace them.
4. Inference only via P214-Z; consent/rights mutations subject-sovereign + Policy/Workflow; audit evidence via Audit; violations via Compliance.
5. Never module-local LLM; never local audit/compliance SoR; never silent consent override; never ungated rights fulfillment.
6. Roadmap: P230 foundation → P230-A…D (consent/trust → AI/rights → ethics/regulatory → civilization-scale gated trust).

## Consequences
Positive: unified privacy/rights/trust intelligence with explainable AI ethics gates.  
Negative: identity accounts, authz decisions, immutable audit and compliance violations remain peer-owned — EPDRTIP stores profiles, consent, rights cases, trust models and governance decisions with peer refs only.

## Links
Law: `ENTERPRISE_PRIVACY_DIGITAL_RIGHTS_TRUST_INTELLIGENCE_PLATFORM.md` · Prior: ADR 589 · Next: P230-A · Peer: ADR 591 (P231 EAFIEOP)
