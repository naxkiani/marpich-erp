import {
  Controller,
  Post,
  Get,
  Body,
  Param,
  HttpCode,
  HttpStatus,
  NotFoundException,
  BadRequestException,
} from "@nestjs/common";
import { v4 as uuidv4 } from "uuid";
import { TenantId } from "@marpich/shared-kernel";
import { ProvisionTenantDto } from "./dto/provision-tenant.dto";
import { ProvisionTenantCommand } from "../application/commands/provision-tenant.command";
import { ProvisionTenantHandler } from "../application/commands/provision-tenant.handler";
import { TENANT_REPOSITORY } from "../domain/ports/tenant.repository.port";
import { Inject } from "@nestjs/common";
import { ITenantRepository } from "../domain/ports/tenant.repository.port";

@Controller("tenants")
export class TenantController {
  constructor(
    private readonly provisionHandler: ProvisionTenantHandler,
    @Inject(TENANT_REPOSITORY)
    private readonly tenantRepository: ITenantRepository,
  ) {}

  @Post()
  @HttpCode(HttpStatus.CREATED)
  async provision(@Body() dto: ProvisionTenantDto) {
    const correlationId = uuidv4();
    const command = new ProvisionTenantCommand({
      correlationId,
      tenantId: TenantId.create(dto.slug),
      name: dto.name,
      slug: dto.slug,
      industryPack: dto.industryPack,
      ...(dto.tier !== undefined ? { tier: dto.tier } : {}),
      ...(dto.optionalModules !== undefined
        ? { optionalModules: dto.optionalModules }
        : {}),
    });

    const result = await this.provisionHandler.execute(command);
    if (!result.succeeded) {
      throw new BadRequestException(result.error);
    }

    return {
      data: result.getValue(),
      meta: { correlationId },
    };
  }

  @Get(":slug")
  async getBySlug(@Param("slug") slug: string) {
    const tenant = await this.tenantRepository.findBySlug(slug);
    if (!tenant) {
      throw new NotFoundException(`Tenant not found: ${slug}`);
    }
    return { data: tenant.toSnapshot() };
  }

  @Get()
  async list() {
    const tenants = await this.tenantRepository.listByTenantId(
      TenantId.create("platform"),
    );
    return {
      data: tenants.map((t) => t.toSnapshot()),
    };
  }
}
