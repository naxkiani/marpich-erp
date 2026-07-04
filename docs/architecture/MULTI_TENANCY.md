# Multi-Tenancy

## Tenant Aggregate

```
Tenant
├── id: TenantId
├── name: string
├── slug: string (subdomain)
├── industryPack: string
├── tier: "starter" | "professional" | "enterprise"
├── isolationStrategy: "schema" | "row"
├── status: "provisioning" | "active" | "suspended" | "archived"
├── enabledModules: string[]
├── config: TenantConfig
├── subscription: Subscription
└── createdAt / updatedAt
```

## Isolation Strategies

### Schema-per-Tenant (Enterprise)

```sql
CREATE SCHEMA tenant_acme_hospital;
SET search_path TO tenant_acme_hospital;
-- All module tables created in tenant schema
```

**Pros:** Strong isolation, easy backup/restore per tenant, regulatory compliance  
**Cons:** Higher connection overhead, schema migration complexity

### Row-Level Security (Professional/Starter)

```sql
ALTER TABLE patients ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON patients
  USING (tenant_id = current_setting('app.tenant_id')::uuid);
```

**Pros:** Efficient for many small tenants, simpler migrations  
**Cons:** Requires careful RLS on every table

## Tenant Context Propagation

Every request carries tenant context through the entire call chain:

```
HTTP Request
  → API Gateway (resolve tenant from subdomain/header)
    → JWT validation (tenant claim)
      → TenantContext middleware (AsyncLocalStorage)
        → Command/Query (tenantId in constructor)
          → Repository (tenant-scoped queries)
            → Database (schema switch or RLS)
```

## Provisioning Saga

```
Command: ProvisionTenant
  1. Create Tenant aggregate (status: provisioning)
  2. Emit TenantProvisionRequested
  3. Identity Service: create admin user
  4. Database: create schema or seed RLS
  5. Module Registry: activate industry pack modules
  6. Seed default data (chart of accounts, roles, etc.)
  7. Update Tenant status → active
  8. Emit TenantProvisioned
```

## Data Residency

Enterprise tenants can specify:
- `dataRegion`: "us-east" | "eu-west" | "me-south" | etc.
- `encryptionKeyId`: customer-managed keys (CMK)
- `retentionPolicy`: configurable per data category

## Tenant Limits (by tier)

| Resource | Starter | Professional | Enterprise |
|----------|---------|-------------|------------|
| Users | 10 | 100 | Unlimited |
| Storage | 5 GB | 50 GB | Custom |
| API calls/min | 100 | 1,000 | Custom |
| Modules | Pack required only | + 5 optional | All |
| Isolation | Row-level | Row or schema | Schema |
| SLA | 99.5% | 99.9% | 99.99% |
