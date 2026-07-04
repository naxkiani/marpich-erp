import {
  Controller,
  Get,
  Post,
  Param,
  Body,
  Query,
  BadRequestException,
  Inject,
} from "@nestjs/common";
import { ApiTags, ApiOperation, ApiBearerAuth, ApiHeader, ApiQuery } from "@nestjs/swagger";
import { v4 as uuidv4 } from "uuid";
import { RequirePermissions } from "../decorators/permissions.decorator";
import { CurrentUser, TenantHeader, CorrelationId } from "../decorators/current-user.decorator";
import type { TokenPayload } from "../../domain/ports/identity.ports";
import { USER_REPOSITORY, type IUserRepository } from "../../domain/ports/identity.ports";
import { SetupMfaDto } from "../dto/identity.dto";
import { SetupMfaHandler } from "../../application/commands/setup-mfa.handler";
import { UniqueEntityId } from "@marpich/shared-kernel";
import { translateError } from "../../infrastructure/i18n/messages";
import { Headers } from "@nestjs/common";

@ApiTags("Users")
@ApiBearerAuth()
@ApiHeader({ name: "X-Tenant-ID", required: true })
@Controller("users")
export class UsersController {
  constructor(
    @Inject(USER_REPOSITORY) private readonly users: IUserRepository,
    private readonly mfaHandler: SetupMfaHandler,
  ) {}

  @Get()
  @RequirePermissions("identity.users.read")
  @ApiOperation({ summary: "List users with search and filters" })
  @ApiQuery({ name: "search", required: false })
  @ApiQuery({ name: "limit", required: false })
  @ApiQuery({ name: "offset", required: false })
  async list(
    @TenantHeader() tenantId: string,
    @Query("search") search?: string,
    @Query("limit") limit?: string,
    @Query("offset") offset?: string,
  ) {
    const items = await this.users.list(tenantId, {
      ...(search !== undefined ? { search } : {}),
      limit: limit ? Number(limit) : 50,
      offset: offset ? Number(offset) : 0,
    });
    return {
      data: items.map((u) => u.toSnapshot()),
      meta: {
        count: items.length,
        exportFormats: ["csv", "xlsx", "json"],
        aiInsightsEnabled: true,
        notificationsEnabled: true,
      },
    };
  }

  @Get("me")
  @RequirePermissions("identity.users.read")
  @ApiOperation({ summary: "Current user profile" })
  me(@CurrentUser() user: TokenPayload) {
    return {
      data: {
        id: user.sub,
        tenantId: user.tenantId,
        email: user.email,
        roles: user.roles,
        permissions: user.permissions,
        locale: user.locale,
        direction: user.locale.startsWith("fa") || user.locale.startsWith("ar") ? "rtl" : "ltr",
        preferences: {
          darkMode: "system",
          aiAssistant: true,
          notifications: true,
        },
      },
    };
  }

  @Get(":id")
  @RequirePermissions("identity.users.read")
  @ApiOperation({ summary: "Get user by ID" })
  async getOne(@TenantHeader() tenantId: string, @Param("id") id: string) {
    const user = await this.users.findById(tenantId, UniqueEntityId.create(id));
    if (!user) throw new BadRequestException("identity.errors.user_not_found");
    return { data: user.toSnapshot() };
  }

  @Post("me/mfa/setup")
  @RequirePermissions("identity.mfa.manage")
  @ApiOperation({ summary: "Initiate MFA setup — returns QR code" })
  async initiateMfa(@CurrentUser() user: TokenPayload) {
    const result = await this.mfaHandler.initiate({
      tenantId: user.tenantId,
      userId: user.sub,
      email: user.email,
    });
    return { data: result };
  }

  @Post("me/mfa/verify")
  @RequirePermissions("identity.mfa.manage")
  @ApiOperation({ summary: "Verify and enable MFA" })
  async verifyMfa(
    @CurrentUser() user: TokenPayload,
    @Body() dto: SetupMfaDto,
    @CorrelationId() correlationId: string,
    @Headers("accept-language") locale?: string,
  ) {
    const pendingSecret = await this.mfaHandler.getPendingSecret(user.tenantId, user.sub);
    if (!pendingSecret) {
      throw new BadRequestException("identity.errors.mfa_setup_expired");
    }

    const result = await this.mfaHandler.execute({
      tenantId: user.tenantId,
      userId: user.sub,
      correlationId,
      verifyCode: dto.verifyCode,
      pendingSecret,
    });

    if (!result.succeeded) {
      throw new BadRequestException({
        error: result.error,
        message: translateError(result.error ?? "", locale ?? user.locale),
      });
    }

    return { data: result.getValue() };
  }
}
