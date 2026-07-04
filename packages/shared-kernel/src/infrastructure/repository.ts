import { AggregateRoot } from "../domain/aggregate-root";
import { UniqueEntityId } from "../domain/unique-entity-id";
import { TenantId } from "../domain/tenant-id";

export interface IRepository<TAggregate extends AggregateRoot<unknown>> {
  findById(tenantId: TenantId, id: UniqueEntityId): Promise<TAggregate | null>;
  save(aggregate: TAggregate): Promise<void>;
  delete(tenantId: TenantId, id: UniqueEntityId): Promise<void>;
}
