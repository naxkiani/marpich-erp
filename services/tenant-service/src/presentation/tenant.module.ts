import { Module } from "@nestjs/common";
import { TenantController } from "./tenant.controller";
import { ProvisionTenantHandler } from "../application/commands/provision-tenant.handler";
import { TENANT_REPOSITORY } from "../domain/ports/tenant.repository.port";
import { EVENT_PUBLISHER } from "../application/ports/event-publisher.port";
import { InMemoryTenantRepository } from "../infrastructure/persistence/in-memory-tenant.repository";
import { ConsoleEventPublisher } from "../infrastructure/messaging/console-event.publisher";

@Module({
  controllers: [TenantController],
  providers: [
    ProvisionTenantHandler,
    { provide: TENANT_REPOSITORY, useClass: InMemoryTenantRepository },
    { provide: EVENT_PUBLISHER, useClass: ConsoleEventPublisher },
  ],
})
export class TenantModule {}
