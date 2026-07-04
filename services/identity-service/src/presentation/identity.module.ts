import { Module } from "@nestjs/common";
import { APP_FILTER, APP_GUARD } from "@nestjs/core";
import { JwtModule } from "@nestjs/jwt";
import { PassportModule } from "@nestjs/passport";
import { PASSWORD_HASHER, TOKEN_SERVICE, MFA_SERVICE, NOTIFICATION_SERVICE } from "../domain/ports/identity.ports";
import { BcryptPasswordHasher } from "../infrastructure/security/bcrypt-password.hasher";
import { JwtTokenService } from "../infrastructure/security/jwt-token.service";
import { TotpMfaService } from "../infrastructure/security/totp-mfa.service";
import { ConsoleNotificationService } from "../infrastructure/notifications/console-notification.service";
import { SessionCleanupJob } from "../infrastructure/jobs/session-cleanup.job";
import { RegisterUserHandler } from "../application/commands/register-user.handler";
import { LoginUserHandler } from "../application/commands/login-user.handler";
import { LogoutUserHandler } from "../application/commands/logout-user.handler";
import { RefreshTokenHandler } from "../application/commands/refresh-token.handler";
import { SetupMfaHandler } from "../application/commands/setup-mfa.handler";
import { CreateRoleHandler, AssignRoleHandler } from "../application/commands/role.handlers";
import { AuthController } from "./controllers/auth.controller";
import { UsersController } from "./controllers/users.controller";
import { RolesController } from "./controllers/roles.controller";
import { HealthController } from "./controllers/health.controller";
import { JwtStrategy } from "./strategies/jwt.strategy";
import { JwtAuthGuard } from "./guards/jwt-auth.guard";
import { RbacGuard } from "./guards/rbac.guard";
import { GlobalExceptionFilter } from "./filters/global-exception.filter";
import {
  buildCacheProvider,
  buildPersistenceProviders,
} from "../infrastructure/infrastructure.providers";

@Module({
  imports: [
    PassportModule.register({ defaultStrategy: "jwt" }),
    JwtModule.register({
      secret: process.env.JWT_SECRET ?? "change-me-in-production-use-256-bit-key",
      signOptions: { issuer: "marpich-identity" },
    }),
  ],
  controllers: [AuthController, UsersController, RolesController, HealthController],
  providers: [
    RegisterUserHandler,
    LoginUserHandler,
    LogoutUserHandler,
    RefreshTokenHandler,
    SetupMfaHandler,
    CreateRoleHandler,
    AssignRoleHandler,
    JwtStrategy,
    SessionCleanupJob,
    ...buildPersistenceProviders(),
    buildCacheProvider(),
    { provide: PASSWORD_HASHER, useClass: BcryptPasswordHasher },
    { provide: TOKEN_SERVICE, useClass: JwtTokenService },
    { provide: MFA_SERVICE, useClass: TotpMfaService },
    { provide: NOTIFICATION_SERVICE, useClass: ConsoleNotificationService },
    { provide: APP_GUARD, useClass: JwtAuthGuard },
    { provide: APP_GUARD, useClass: RbacGuard },
    { provide: APP_FILTER, useClass: GlobalExceptionFilter },
  ],
})
export class IdentityModule {}
