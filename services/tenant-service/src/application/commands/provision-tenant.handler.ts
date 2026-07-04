import { Injectable, Inject } from "@nestjs/common";
import { Result } from "@marpich/shared-kernel";
import { getIndustryPack } from "@marpich/shared-kernel";
import { ProvisionTenantCommand } from "./provision-tenant.command";
import {
  ITenantRepository,
  TENANT_REPOSITORY,
} from "../../domain/ports/tenant.repository.port";
import { Tenant } from "../../domain/tenant.aggregate";
import { IEventPublisher, EVENT_PUBLISHER } from "../ports/event-publisher.port";

export interface ProvisionTenantResult {
  tenantId: string;
  slug: string;
  status: string;
  enabledModules: string[];
}

@Injectable()
export class ProvisionTenantHandler {
  constructor(
    @Inject(TENANT_REPOSITORY)
    private readonly tenantRepository: ITenantRepository,
    @Inject(EVENT_PUBLISHER)
    private readonly eventPublisher: IEventPublisher,
  ) {}

  async execute(
    command: ProvisionTenantCommand,
  ): Promise<Result<ProvisionTenantResult>> {
    const pack = getIndustryPack(command.industryPack);
    if (!pack) {
      return Result.fail(`Unknown industry pack: ${command.industryPack}`);
    }

    const slug = command.slug.trim().toLowerCase();
    const exists = await this.tenantRepository.existsBySlug(slug);
    if (exists) {
      return Result.fail(`Tenant slug already exists: ${slug}`);
    }

    const enabledModules = [
      ...new Set([
        ...pack.requiredModules,
        ...(command.optionalModules ?? []).filter((m) =>
          pack.optionalModules.includes(m),
        ),
      ]),
    ];

    const tenant = Tenant.create({
      name: command.name,
      slug,
      industryPack: command.industryPack,
      ...(command.tier !== undefined ? { tier: command.tier } : {}),
      enabledModules,
      correlationId: command.correlationId,
    });

    tenant.activate();
    await this.tenantRepository.save(tenant);

    for (const event of tenant.domainEvents) {
      await this.eventPublisher.publish(event);
    }
    tenant.clearDomainEvents();

    return Result.ok({
      tenantId: tenant.id.toString(),
      slug: tenant.slug,
      status: tenant.status,
      enabledModules: [...tenant.enabledModules],
    });
  }
}
