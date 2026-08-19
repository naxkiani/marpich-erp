# GCP adapter (ONE path)

**Chosen target:** Compute Engine (Ubuntu) + Docker Compose — same package as `../vps/`.

**Not created:** Cloud Run service YAML as a second product, or a second domain.  
**GKE:** use `../kubernetes/` (existing Helm).

| Need | Resource | Status |
|------|----------|--------|
| Compute | GCE VM | READY_FOR_CREDENTIALS |
| Database | Cloud SQL PostgreSQL | READY_FOR_CREDENTIALS |
| Secrets | Secret Manager | MISSING |
| TLS | public CA | READY_FOR_CREDENTIALS |
| Registry | GHCR | READY_FOR_CREDENTIALS |
| Backup / rollback | existing scripts + previous digest | READY_FOR_CREDENTIALS |

GCP_STATUS = **READY_FOR_CREDENTIALS**.
