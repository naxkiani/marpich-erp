# Azure adapter (ONE path)

**Chosen target:** Azure Linux VM + Docker Compose — same package as `../vps/`.

**Not created:** Container Apps revision, Bicep product fork, or a second domain.  
**AKS:** use `../kubernetes/` (existing Helm).

| Need | Resource | Status |
|------|----------|--------|
| Compute | Azure VM | READY_FOR_CREDENTIALS |
| Database | Azure Database for PostgreSQL | READY_FOR_CREDENTIALS |
| Secrets | Key Vault | MISSING |
| TLS | public CA on Caddy or App Gateway | READY_FOR_CREDENTIALS |
| Registry | GHCR | READY_FOR_CREDENTIALS |
| Backup / rollback | existing scripts + previous digest | READY_FOR_CREDENTIALS |

AZURE_STATUS = **READY_FOR_CREDENTIALS**.
