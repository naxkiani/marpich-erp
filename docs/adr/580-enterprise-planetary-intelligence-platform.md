# ADR 580 — Enterprise Planetary Intelligence Platform (P220)

## Status
Accepted

## Context
P219-Z completed the Civilization OS series (Unified Enterprise Control Plane). P220 opens the next series: Enterprise Planetary Intelligence Platform (EPIP) — planetary-scale observation, climate intelligence, environmental awareness, sustainability governance, Earth Digital Twin integration and global decision support under MEOS 11.0.

## Decision
1. SoR `planetary`; fabric `meos_enterprise_planetary_intelligence_platform_framework`; API `/api/v1/planetary*`; capability `CAP-PLT-EPIP-001`.
2. Eight logical BCs inside one SoR: Observation, Climate, Environment, Sustainability, Earth Twin, Decision Support, Risk, EPIP Governance.
3. Federate with P219-D Civilization Planetary and P219-Z Unified Control via ACL/events — never replace them.
4. Inference only via P214-Z; approvals via Workflow; policy via Policy Engine; audit via Audit; external data via Integration Platform.
5. Never module-local LLM; never ungated planetary autonomy; never direct physical/orbital actuation from EPIP.
6. Series roadmap: P220 foundation → P220-A…G hardening.

## Consequences
Positive: dedicated planetary intelligence SoR with clear federation to Civilization OS.  
Negative: twin and sustainability authority remain shared with P219-D/N via contracts — dual-write forbidden.

## Links
Law: `ENTERPRISE_PLANETARY_INTELLIGENCE_PLATFORM.md` · Prior: ADR 579 · Next: P220-A · Peer: ADR 581 (P221 EGRCMP)
