# ADR 595 — Enterprise Autonomous Human Resource & Workforce Intelligence Platform (P235)

## Status
Accepted

## Context
P234 established EAEHCEP (education & human capability evolution). P235 opens the Enterprise Autonomous Human Resource & Workforce Intelligence Platform (EAHRWIP) for workforce intelligence, talent, recruitment, planning, performance, career, org analytics and human-AI collaboration under MEOS 11.0. HR remains employment SoR; Payroll remains compensation SoR; P234 remains learning/capability journey SoR — EAHRWIP federates workforce intelligence rather than replacing them.

## Decision
1. SoR `workforce_intelligence`; fabric `meos_enterprise_autonomous_human_resource_workforce_intelligence_platform_framework`; API `/api/v1/workforce-intelligence*`; capability `CAP-PLT-EAHRWIP-001`.
2. Ten logical BCs inside one SoR: HR Management projections, Talent, Recruitment, Workforce Planning, Performance, Career, Employee Experience, Organization Intelligence, Human-AI Collaboration, Governance.
3. Federate with hr, payroll, P234, P230, P228, P227, P224, P231 via ACL/events — never replace them.
4. Inference only via P214-Z; employment/comp mutations via Workflow + HR/Payroll; privacy via P230; fairness/explainability mandatory on scoring; ATS/HRIS via Integration Platform.
5. Never duplicate P234 as LMS; never module-local LLM; never silent hire/promote/terminate/comp mutation; never opaque discriminatory scores; never dual-write HR tables.
6. Roadmap: P235 foundation → P235-A…D (talent/recruit → AI/twin → optimization → civilization-scale gated workforce intel).

## Consequences
Positive: governed workforce control-tower intelligence across HR and learning peers.  
Negative: employment and payroll truth remain peer-owned — EAHRWIP stores talent/recruitment/planning/performance projections with peer employee refs only.

## Links
Law: `ENTERPRISE_AUTONOMOUS_HUMAN_RESOURCE_WORKFORCE_INTELLIGENCE_PLATFORM.md` · Prior: ADR 594 · Next: P235-A · Peer: ADR 596 (P236 EAMII)
