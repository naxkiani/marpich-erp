import { Injectable } from "@nestjs/common";
import { ITenantRepository } from "../../domain/ports/tenant.repository.port";
import { Tenant, TenantProps } from "../../domain/tenant.aggregate";
import { UniqueEntityId } from "@marpich/shared-kernel";
import { TenantId } from "@marpich/shared-kernel";

/**
 * In-memory repository for bootstrap. Production uses PostgresTenantRepository
 * with schema-per-tenant or row-level isolation.
 */
@Injectable()
export class InMemoryTenantRepository implements ITenantRepository {
  private readonly byId = new Map<string, Tenant>();
  private readonly bySlug = new Map<string, string>();

  async findBySlug(slug: string): Promise<Tenant | null> {
    const id = this.bySlug.get(slug.toLowerCase());
    if (!id) return null;
    return this.byId.get(id) ?? null;
  }

  async findById(id: UniqueEntityId): Promise<Tenant | null> {
    return this.byId.get(id.toString()) ?? null;
  }

  async save(tenant: Tenant): Promise<void> {
    this.byId.set(tenant.id.toString(), tenant);
    this.bySlug.set(tenant.slug, tenant.id.toString());
  }

  async listByTenantId(_tenantId: TenantId): Promise<Tenant[]> {
    return Array.from(this.byId.values());
  }

  async existsBySlug(slug: string): Promise<boolean> {
    return this.bySlug.has(slug.toLowerCase());
  }
}
