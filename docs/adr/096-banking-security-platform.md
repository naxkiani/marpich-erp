# ADR-096: Banking Security Platform

## Status

Accepted

## Context

Enterprise Banking Platform (ADR-087) delegates generic security to Financial Kernel (`/api/v1/financial-kernel/security`) and Treasury has its own security engine, but banking-specific controls — maker-checker on transfers, velocity limits, device verification for digital channels, emergency freeze, and policy-driven approval for critical actions — are not implemented in the banking context.

## Decision

Implement **Banking Security Platform** at `backend/contexts/banking/`:

- **API prefix:** `/api/v1/banking/security`
- **Controls:** RBAC, ABAC, maker-checker, four-eyes, transaction/daily/velocity limits, device verification, session monitoring, transaction monitoring, digital signature, encryption, risk-based authentication, emergency freeze, immutable audit trail
- **Policy gate:** `authorize_critical_action` enforces configurable approval via `security.critical.approval_required` and related `security.*` policy keys
- **Events:** `banking.security.approval.submitted`, `banking.security.approval.completed`, `banking.security.freeze.activated`, `banking.security.alert.raised`, `banking.security.audit.recorded`
- **Crypto:** Reuses Financial Kernel security engine helpers for signing, encryption, and tamper-chain audit

Kernel financial security remains the cross-industry canonical surface; banking security adds retail/corporate banking operational controls.

## Consequences

- Critical actions above policy thresholds require maker-checker approval before execution
- Emergency freeze blocks all authorize calls for the tenant
- Audit trail uses chained tamper hashes verifiable via `/audit/verify`
- Four-eyes enforced when amount exceeds `four_eyes_amount` policy parameter

## Alternatives considered

- Kernel security only — rejected (no banking-specific velocity, device, or freeze scope)
- Treasury security reuse — rejected (corporate vs retail boundary)
- Hardcoded approval thresholds — rejected (policy engine requirement)
