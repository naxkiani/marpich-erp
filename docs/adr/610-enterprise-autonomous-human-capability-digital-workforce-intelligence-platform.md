# ADR 610 — Enterprise Autonomous Human Capability & Digital Workforce Intelligence Platform (P251)

## Status
Accepted

## Context
P250 established EAKEGINP (knowledge economy). P251 opens the Enterprise Autonomous Human Capability & Digital Workforce Intelligence Platform (EAHCDWIP) for skills/career capability depth, digital workforce orchestration and human–AI collaboration assist under MEOS 11.0. P235 already owns SoR `workforce_intelligence` and `/api/v1/workforce-intelligence*`; P234 owns education/learning depth; HR/Payroll remain employment/comp SoRs — EAHCDWIP must not fork those SoRs and must never issue ungated hire/terminate/pay actions.

## Decision
1. SoR `human_capability_intelligence` (not `workforce_intelligence`); fabric `meos_enterprise_autonomous_human_capability_digital_workforce_intelligence_platform_framework`; API `/api/v1/human-capability-intelligence*`; capability `CAP-PLT-EAHCDWIP-001`.
2. Ten logical BCs inside one SoR: Human Capability Management, Talent Intelligence, Skills Management, Learning Management, Digital Workforce, Career Evolution, Workforce Analytics, Human-AI Collaboration, Organizational Capability, Workforce Governance.
3. Federate with P235, HR, Payroll, P234, P250, P230, P216, Identity, P227, P228, P229, P224, P243 via ACL/events — never replace them; never dual-write P235/HR/Payroll; never fork `/api/v1/workforce-intelligence*`; never duplicate LMS.
4. Inference only via P214-Z; deploy via Workflow + HR/P235/P234/P216; privacy via P230; DigitalWorker is orchestration profile only (never shadow employee master); simulation ≠ deploy.
5. Never local employee PII vaults; never opaque unfair ranking; never module-local LLM; never silent consent override; never ungated hire/terminate/pay.
6. Roadmap: P251 foundation → P251-A…D (capability domain → AI/KG/twin → autonomous assist → civilization-scale gated human capability intel).

## Consequences
Positive: governed human-capability control-tower intelligence federated with workforce, education and HR peers.  
Negative: employment, payroll, workforce intel and LMS remain peer-owned — EAHCDWIP stores capability models, digital-worker orchestration and peer refs only.

## Links
Law: `ENTERPRISE_AUTONOMOUS_HUMAN_CAPABILITY_DIGITAL_WORKFORCE_INTELLIGENCE_PLATFORM.md` · Prior: ADR 609 · Next: P251-A · Peer: ADR 611 (P252 EASIUIP)
