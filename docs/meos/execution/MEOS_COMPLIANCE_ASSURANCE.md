# MEOS Compliance Assurance

**Date:** 2026-08-18T05:56:36Z  
**Overall:** **NOT_AVAILABLE** — no production deployment, no mapped legal jurisdiction.

Do **not** read this as SOC 2, ISO 27001, HIPAA, GDPR, or any other certification.

| CONTROL_ID | Description | Implementation | Evidence | Status | Review |
|------------|-------------|----------------|----------|--------|--------|
| C-AUTH | Authentication required on business APIs | JWT + permissions | P313 G02 | PARTIAL (candidate only) | After prod |
| C-AUTHZ | Authorization checks | `require_permissions` | P313 G03 | PARTIAL | After prod |
| C-TENANT | Tenant isolation | Header + tests | P313 G04 | PARTIAL | After prod |
| C-AUDIT | Auditable actions | Audit API / events | P313 G17 | PARTIAL | After prod |
| C-BACKUP | Recoverable SoR | Demo MinIO drill | P313 G07–G09 | PARTIAL (not production) | After prod |
| C-PRIVACY | Data-subject rights | Policy smoke only | P313 G19 FAIL | FAIL / GAP | Before prod PII |
| C-AI | Governed AI | Stub | P313 G18 FAIL | FAIL / GAP | Before AI activation |
| C-REG | Jurisdiction-specific regs | — | None mapped | NOT_APPLICABLE until deploy region known | — |

Owner/responsibility: **NOT_AVAILABLE**.
