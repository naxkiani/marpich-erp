import { Command } from "@marpich/shared-kernel";
import { TenantId } from "@marpich/shared-kernel";

export class ProvisionTenantCommand extends Command {
  readonly name: string;
  readonly slug: string;
  readonly industryPack: string;
  readonly tier?: "starter" | "professional" | "enterprise" | undefined;
  readonly optionalModules?: string[] | undefined;

  constructor(params: {
    correlationId: string;
    tenantId: TenantId;
    userId?: string;
    name: string;
    slug: string;
    industryPack: string;
    tier?: "starter" | "professional" | "enterprise" | undefined;
    optionalModules?: string[] | undefined;
  }) {
    super({
      correlationId: params.correlationId,
      tenantId: params.tenantId,
      userId: params.userId,
    });
    this.name = params.name;
    this.slug = params.slug;
    this.industryPack = params.industryPack;
    this.tier = params.tier;
    this.optionalModules = params.optionalModules;
  }
}
