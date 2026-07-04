import {
  Controller,
  Get,
  All,
  Req,
  Res,
  HttpStatus,
} from "@nestjs/common";
import type { Request, Response } from "express";

const SERVICE_ROUTES: Record<string, string> = {
  "/auth": process.env.IDENTITY_SERVICE_URL ?? "http://localhost:4001",
  "/users": process.env.IDENTITY_SERVICE_URL ?? "http://localhost:4001",
  "/roles": process.env.IDENTITY_SERVICE_URL ?? "http://localhost:4001",
  "/tenants": process.env.TENANT_SERVICE_URL ?? "http://localhost:4002",
  "/industry-packs": process.env.MODULE_REGISTRY_URL ?? "http://localhost:4003",
  "/modules": process.env.MODULE_REGISTRY_URL ?? "http://localhost:4003",
};

@Controller()
export class GatewayController {
  @Get("health")
  health() {
    return {
      status: "ok",
      service: "api-gateway",
      version: process.env.PLATFORM_VERSION ?? "0.1.0",
      routes: Object.keys(SERVICE_ROUTES),
    };
  }

  @Get("platform")
  platformInfo() {
    return {
      name: "Marpich ERP",
      tagline: "Enterprise Operating System",
      principles: [
        "Enterprise First",
        "AI First",
        "Cloud Native",
        "API First",
        "Security First",
        "Event Driven",
        "Domain Driven Design",
      ],
      architecture: [
        "Clean Architecture",
        "Hexagonal Architecture",
        "CQRS",
        "Multi-Tenant",
        "Module Composition",
      ],
    };
  }

  @All("*path")
  async proxy(@Req() req: Request, @Res() res: Response): Promise<void> {
    const path = req.path.replace(/^\/api\/v1/, "");
    const routePrefix = Object.keys(SERVICE_ROUTES).find((prefix) =>
      path.startsWith(prefix),
    );

    if (!routePrefix) {
      res.status(HttpStatus.NOT_FOUND).json({
        error: "No upstream service for this route",
        path,
      });
      return;
    }

    const upstream = SERVICE_ROUTES[routePrefix];
    const targetUrl = `${upstream}/api/v1${path}`;

    try {
      const headers: Record<string, string> = {
        "Content-Type": "application/json",
      };
      if (req.headers["x-tenant-id"]) {
        headers["X-Tenant-ID"] = req.headers["x-tenant-id"] as string;
      }
      if (req.headers["x-correlation-id"]) {
        headers["X-Correlation-ID"] = req.headers["x-correlation-id"] as string;
      }
      if (req.headers["authorization"]) {
        headers["Authorization"] = req.headers["authorization"] as string;
      }
      if (req.headers["accept-language"]) {
        headers["Accept-Language"] = req.headers["accept-language"] as string;
      }

      const fetchOptions: RequestInit = {
        method: req.method,
        headers,
      };

      if (["POST", "PUT", "PATCH"].includes(req.method) && req.body) {
        fetchOptions.body = JSON.stringify(req.body);
      }

      const upstreamRes = await fetch(targetUrl, fetchOptions);
      const body = await upstreamRes.text();

      res.status(upstreamRes.status);
      res.setHeader("Content-Type", "application/json");
      res.send(body);
    } catch (err) {
      res.status(HttpStatus.BAD_GATEWAY).json({
        error: "Upstream service unavailable",
        service: routePrefix,
        detail: err instanceof Error ? err.message : "Unknown error",
      });
    }
  }
}
