import {
  Injectable,
  CanActivate,
  ExecutionContext,
  ForbiddenException,
} from "@nestjs/common";
import { Reflector } from "@nestjs/core";
import { PermissionEvaluator } from "@marpich/platform-core";
import { PERMISSIONS_KEY } from "../decorators/permissions.decorator";
import type { TokenPayload } from "../../domain/ports/identity.ports";
import { translateError } from "../../infrastructure/i18n/messages";

@Injectable()
export class RbacGuard implements CanActivate {
  private readonly evaluator = new PermissionEvaluator();

  constructor(private readonly reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const required = this.reflector.getAllAndOverride<string[]>(PERMISSIONS_KEY, [
      context.getHandler(),
      context.getClass(),
    ]);

    if (!required || required.length === 0) return true;

    const request = context.switchToHttp().getRequest<{
      user: TokenPayload;
      headers: Record<string, string>;
    }>();
    const user = request.user;
    if (!user) return false;

    const locale = request.headers["accept-language"]?.split(",")[0] ?? user.locale ?? "en-US";

    const allowed = required.every((perm) =>
      this.evaluator.hasPermission(
        {
          tenantId: user.tenantId,
          userId: user.sub,
          permissions: user.permissions,
          roles: user.roles,
          attributes: user.attributes,
        },
        perm,
      ),
    );

    if (!allowed) {
      throw new ForbiddenException({
        error: "identity.errors.forbidden",
        message: translateError("identity.errors.forbidden", locale),
      });
    }

    return true;
  }
}
