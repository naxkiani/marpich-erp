import {
  Injectable,
  NestMiddleware,
  BadRequestException,
} from "@nestjs/common";
import { Request, Response, NextFunction } from "express";
import { TenantId } from "@marpich/shared-kernel";
import { AsyncLocalStorage } from "node:async_hooks";

export interface RequestTenantContext {
  tenantId: TenantId;
  tenantSlug: string;
  correlationId: string;
}

export const tenantContextStorage = new AsyncLocalStorage<RequestTenantContext>();

@Injectable()
export class TenantResolutionMiddleware implements NestMiddleware {
  use(req: Request, res: Response, next: NextFunction): void {
    const correlationId =
      (req.headers["x-correlation-id"] as string) ?? crypto.randomUUID();

    const host = req.headers.host ?? "";
    const subdomain = host.split(".")[0];

    const headerTenant = req.headers["x-tenant-id"] as string | undefined;
    const slug = headerTenant ?? (subdomain !== "localhost" ? subdomain : undefined);

    if (!slug) {
      throw new BadRequestException(
        "Tenant required: set X-Tenant-ID header or use tenant subdomain",
      );
    }

    let tenantId: TenantId;
    try {
      tenantId = TenantId.create(slug);
    } catch {
      throw new BadRequestException(`Invalid tenant identifier: ${slug}`);
    }

    res.setHeader("X-Correlation-ID", correlationId);

    const context: RequestTenantContext = {
      tenantId,
      tenantSlug: slug,
      correlationId,
    };

    tenantContextStorage.run(context, () => next());
  }
}
