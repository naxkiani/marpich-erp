# AWS adapter (ONE path)

**Chosen target:** Amazon EC2 (Ubuntu) + Docker Compose — same package as `../vps/`.

**Not created:** ECS task defs, CDK apps, or a second domain model.  
**EKS:** use `../kubernetes/` (existing Helm). That is the Kubernetes adapter, not a second AWS architecture.

| Need | Resource | Status |
|------|----------|--------|
| Compute | EC2 | READY_FOR_CREDENTIALS |
| Database | RDS PostgreSQL (or Postgres on the VM for DEMO only) | READY_FOR_CREDENTIALS |
| Secrets | AWS Secrets Manager → env injection | MISSING |
| TLS | ACM or Caddy public CA | READY_FOR_CREDENTIALS |
| Registry | existing GHCR | READY_FOR_CREDENTIALS |
| Backup | RDS snapshot or `meos-postgres-backup.sh` | READY_FOR_CREDENTIALS |
| Rollback | `MEOS_PREVIOUS_IMAGE` digest | READY_FOR_CREDENTIALS |

AWS_STATUS = **READY_FOR_CREDENTIALS**. No provision in this phase.
