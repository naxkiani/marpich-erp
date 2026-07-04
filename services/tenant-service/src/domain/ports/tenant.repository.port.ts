import { Tenant } from "../tenant.aggregate";
import { UniqueEntityId } from "@marpich/shared-kernel";
import { TenantId } from "@marpich/shared-kernel";

export interface ITenantRepository {
  findBySlug(slug: string): Promise<Tenant | null>;
  findById(id: UniqueEntityId): Promise<Tenant | null>;
  save(tenant: Tenant): Promise<void>;
  listByTenantId(tenantId: TenantId): Promise<Tenant[]>;
  existsBySlug(slug: string): Promise<boolean>;
}

export const TENANT_REPOSITORY = Symbol("TENANT_REPOSITORY");
