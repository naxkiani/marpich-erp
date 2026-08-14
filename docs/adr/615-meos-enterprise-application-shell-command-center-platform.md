# ADR 615 — MEOS Enterprise Application Shell & Command Center Platform (P258)

## Status
Accepted

## Context
P257 established MERAF (`enterprise_runtime`) as the runtime productization layer. P258 opens the human-interaction Operating Layer: Application Shell, Command Center, Workspace Engine and intelligent launcher. Existing AppShell (`frontend/core/shell`), Enterprise Search, Notifications, Workflow and Identity already own adjacent UX/platform concerns — MESCC must compose experience contracts, not fork those platforms. P259 is planned for deeper module activation/lifecycle productization.

## Decision
1. SoR `enterprise_experience`; fabric `meos_enterprise_application_shell_command_center_platform_framework`; API `/api/v1/enterprise-experience*`; capability `CAP-PLT-MESCC-001`; acronym **MESCC**.
2. Logical BCs inside one SoR: Experience Management, Command Center, Application Shell, Personalization, Experience Governance.
3. Federate with P257, Module Registry, Plugin Platform, AppShell implementation, Search, Notifications, Workflow, Identity, Feature Flags, P214-Z, Policy, Audit — never replace them; never dual-write `enterprise_runtime_*`; never reimplement shell widgets in modules.
4. Inference only via P214-Z; launches/actions permission-aware and Policy/Workflow gated; UI_PAGE_STANDARD (a11y, dark mode, RTL/LTR) binding mandatory.
5. Roadmap: P258 foundation → P258-A Shell Foundation → P258-B Command Center → P258-C AI Experience → P258-D Autonomous Experience; unblocks P259.

## Consequences
Positive: unified AI-native enterprise operating experience over runtime activations.  
Negative: module lifecycle depth deferred to P259; catalog/runtime truth remains peer-owned — MESCC stores workspaces, commands, preferences and peer refs only.

## Links
Law: `ENTERPRISE_MEOS_APPLICATION_SHELL_COMMAND_CENTER_PLATFORM.md` · Prior: ADR 614 · Next: P258-A · Peer: ADR 616 (P259 MDMAL)
