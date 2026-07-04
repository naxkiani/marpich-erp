import {
  Controller,
  Post,
  Body,
  HttpCode,
  HttpStatus,
  BadRequestException,
  Headers,
} from "@nestjs/common";
import { ApiTags, ApiOperation, ApiHeader, ApiBearerAuth } from "@nestjs/swagger";
import { v4 as uuidv4 } from "uuid";
import { RegisterDto, LoginDto, RefreshTokenDto, LogoutDto } from "../dto/identity.dto";
import { RegisterUserHandler } from "../../application/commands/register-user.handler";
import { LoginUserHandler } from "../../application/commands/login-user.handler";
import { LogoutUserHandler } from "../../application/commands/logout-user.handler";
import { RefreshTokenHandler } from "../../application/commands/refresh-token.handler";
import { Public, RequirePermissions } from "../decorators/permissions.decorator";
import { TenantHeader, ClientIp, CurrentUser, CorrelationId } from "../decorators/current-user.decorator";
import { translateError } from "../../infrastructure/i18n/messages";
import type { TokenPayload } from "../../domain/ports/identity.ports";

@ApiTags("Auth")
@Controller("auth")
export class AuthController {
  constructor(
    private readonly registerHandler: RegisterUserHandler,
    private readonly loginHandler: LoginUserHandler,
    private readonly logoutHandler: LogoutUserHandler,
    private readonly refreshHandler: RefreshTokenHandler,
  ) {}

  @Public()
  @Post("register")
  @HttpCode(HttpStatus.CREATED)
  @ApiOperation({ summary: "Register a new user within tenant" })
  @ApiHeader({ name: "X-Tenant-ID", required: true })
  async register(
    @TenantHeader() tenantId: string,
    @Body() dto: RegisterDto,
    @ClientIp() ip: string | undefined,
    @Headers("accept-language") locale?: string,
  ) {
    if (!tenantId) throw new BadRequestException("X-Tenant-ID required");

    const result = await this.registerHandler.execute({
      tenantId,
      email: dto.email,
      password: dto.password,
      displayName: dto.displayName,
      locale: dto.locale,
      correlationId: uuidv4(),
      ipAddress: ip,
    });

    if (!result.succeeded) {
      throw new BadRequestException({
        error: result.error,
        message: translateError(result.error ?? "", locale ?? "en-US"),
      });
    }

    return { data: result.getValue(), meta: { tenantId } };
  }

  @Public()
  @Post("login")
  @HttpCode(HttpStatus.OK)
  @ApiOperation({ summary: "Authenticate user — returns JWT or MFA challenge" })
  @ApiHeader({ name: "X-Tenant-ID", required: true })
  async login(
    @TenantHeader() tenantId: string,
    @Body() dto: LoginDto,
    @ClientIp() ip: string | undefined,
    @Headers("user-agent") userAgent?: string,
    @Headers("accept-language") locale?: string,
  ) {
    if (!tenantId) throw new BadRequestException("X-Tenant-ID required");

    const result = await this.loginHandler.execute({
      tenantId,
      email: dto.email,
      password: dto.password,
      mfaCode: dto.mfaCode,
      mfaToken: dto.mfaToken,
      correlationId: uuidv4(),
      ipAddress: ip,
      userAgent,
    });

    if (!result.succeeded) {
      throw new BadRequestException({
        error: result.error,
        message: translateError(result.error ?? "", locale ?? "en-US"),
      });
    }

    return { data: result.getValue(), meta: { tenantId } };
  }

  @Public()
  @Post("refresh")
  @HttpCode(HttpStatus.OK)
  @ApiOperation({ summary: "Rotate refresh token and issue new access token" })
  @ApiHeader({ name: "X-Tenant-ID", required: true })
  async refresh(
    @TenantHeader() tenantId: string,
    @Body() dto: RefreshTokenDto,
    @ClientIp() ip: string | undefined,
    @Headers("user-agent") userAgent?: string,
    @Headers("accept-language") locale?: string,
  ) {
    if (!tenantId) throw new BadRequestException("X-Tenant-ID required");

    const result = await this.refreshHandler.execute({
      tenantId,
      refreshToken: dto.refreshToken,
      correlationId: uuidv4(),
      ipAddress: ip,
      userAgent,
    });

    if (!result.succeeded) {
      throw new BadRequestException({
        error: result.error,
        message: translateError(result.error ?? "", locale ?? "en-US"),
      });
    }

    return { data: result.getValue(), meta: { tenantId } };
  }

  @Post("logout")
  @HttpCode(HttpStatus.OK)
  @ApiBearerAuth()
  @RequirePermissions("identity.sessions.revoke")
  @ApiOperation({ summary: "Revoke session(s)" })
  @ApiHeader({ name: "X-Tenant-ID", required: true })
  async logout(
    @TenantHeader() tenantId: string,
    @CurrentUser() user: TokenPayload,
    @Body() dto: LogoutDto,
    @CorrelationId() correlationId: string,
    @ClientIp() ip: string | undefined,
    @Headers("accept-language") locale?: string,
  ) {
    const result = await this.logoutHandler.execute({
      tenantId,
      userId: user.sub,
      refreshToken: dto.refreshToken,
      revokeAll: dto.revokeAll,
      correlationId,
      ipAddress: ip,
    });

    if (!result.succeeded) {
      throw new BadRequestException({
        error: result.error,
        message: translateError(result.error ?? "", locale ?? user.locale),
      });
    }

    return { data: result.getValue(), meta: { tenantId } };
  }
}
