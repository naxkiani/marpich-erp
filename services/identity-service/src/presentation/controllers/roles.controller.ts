import { Controller, Get, Post, Body, Param, BadRequestException, Inject } from "@nestjs/common";
import { ApiTags, ApiOperation, ApiBearerAuth, ApiHeader } from "@nestjs/swagger";
import { v4 as uuidv4 } from "uuid";
import { RequirePermissions } from "../decorators/permissions.decorator";
import { CurrentUser, TenantHeader } from "../decorators/current-user.decorator";
import { CreateRoleDto, AssignRoleDto } from "../dto/identity.dto";
import { CreateRoleHandler, AssignRoleHandler } from "../../application/commands/role.handlers";
import {
  ROLE_REPOSITORY,
  PERMISSION_REPOSITORY,
  type IRoleRepository,
  type IPermissionRepository,
} from "../../domain/ports/identity.ports";
import type { TokenPayload } from "../../domain/ports/identity.ports";
import { translateError } from "../../infrastructure/i18n/messages";
import { Headers } from "@nestjs/common";

@ApiTags("Roles")
@ApiBearerAuth()
@ApiHeader({ name: "X-Tenant-ID", required: true })
@Controller("roles")
export class RolesController {
  constructor(
    @Inject(CreateRoleHandler) private readonly createRole: CreateRoleHandler,
    @Inject(AssignRoleHandler) private readonly assignRole: AssignRoleHandler,
    @Inject(ROLE_REPOSITORY) private readonly roles: IRoleRepository,
    @Inject(PERMISSION_REPOSITORY) private readonly permissions: IPermissionRepository,
  ) {}

  @Get()
  @RequirePermissions("identity.roles.read")
  @ApiOperation({ summary: "List tenant roles" })
  async list(@TenantHeader() tenantId: string) {
    const items = await this.roles.list(tenantId);
    return {
      data: items.map((r) => r.toSnapshot()),
      meta: { exportFormats: ["csv", "json"] },
    };
  }

  @Get("permissions")
  @RequirePermissions("identity.roles.read")
  @ApiOperation({ summary: "List available permission catalog" })
  async listPermissions() {
    return { data: await this.permissions.findAllCodes() };
  }

  @Post()
  @RequirePermissions("identity.roles.write")
  @ApiOperation({ summary: "Create a new role" })
  async create(
    @TenantHeader() tenantId: string,
    @CurrentUser() user: TokenPayload,
    @Body() dto: CreateRoleDto,
    @Headers("accept-language") locale?: string,
  ) {
    const result = await this.createRole.execute({
      tenantId,
      code: dto.code,
      name: dto.name,
      description: dto.description,
      permissionCodes: dto.permissionCodes,
      correlationId: uuidv4(),
      actorId: user.sub,
    });

    if (!result.succeeded) {
      throw new BadRequestException({
        error: result.error,
        message: translateError(result.error ?? "", locale ?? user.locale),
      });
    }

    return { data: result.getValue() };
  }

  @Post(":userId/assign")
  @RequirePermissions("identity.roles.write")
  @ApiOperation({ summary: "Assign role to user" })
  async assign(
    @TenantHeader() tenantId: string,
    @Param("userId") userId: string,
    @CurrentUser() user: TokenPayload,
    @Body() dto: AssignRoleDto,
    @Headers("accept-language") locale?: string,
  ) {
    const result = await this.assignRole.execute({
      tenantId,
      userId,
      roleId: dto.roleId,
      correlationId: uuidv4(),
      actorId: user.sub,
    });

    if (!result.succeeded) {
      throw new BadRequestException({
        error: result.error,
        message: translateError(result.error ?? "", locale ?? user.locale),
      });
    }

    return { data: { assigned: true } };
  }
}
