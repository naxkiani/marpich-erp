export interface PermissionCheckContext {
  tenantId: string;
  userId: string;
  permissions: string[];
  roles: string[];
  attributes: Record<string, unknown>;
  resource?: string | undefined;
  action?: string | undefined;
}

export interface AbacPolicy {
  id: string;
  tenantId: string;
  name: string;
  effect: "allow" | "deny";
  resource: string;
  action: string;
  conditions: Record<string, unknown>;
  priority: number;
  enabled: boolean;
}

export interface IPermissionEvaluator {
  hasPermission(ctx: PermissionCheckContext, required: string): boolean;
  evaluateAbac(ctx: PermissionCheckContext, policies: AbacPolicy[]): boolean;
}

export class PermissionEvaluator implements IPermissionEvaluator {
  hasPermission(ctx: PermissionCheckContext, required: string): boolean {
    if (ctx.permissions.includes("*") || ctx.permissions.includes(required)) {
      return true;
    }
    const [resource, action] = required.split(".").slice(-2);
    if (resource && action) {
      const wildcard = `identity.${resource}.${action}`;
      if (ctx.permissions.includes(wildcard)) return true;
    }
    return ctx.permissions.some(
      (p) => p.endsWith(".*") && required.startsWith(p.slice(0, -1)),
    );
  }

  evaluateAbac(ctx: PermissionCheckContext, policies: AbacPolicy[]): boolean {
    const applicable = policies
      .filter(
        (p) =>
          p.enabled &&
          p.tenantId === ctx.tenantId &&
          (p.resource === "*" || p.resource === ctx.resource) &&
          (p.action === "*" || p.action === ctx.action),
      )
      .sort((a, b) => a.priority - b.priority);

    for (const policy of applicable) {
      if (this.matchesConditions(policy.conditions, ctx)) {
        return policy.effect === "allow";
      }
    }
    return true;
  }

  private matchesConditions(
    conditions: Record<string, unknown>,
    ctx: PermissionCheckContext,
  ): boolean {
    for (const [key, expected] of Object.entries(conditions)) {
      const actual = ctx.attributes[key] ?? ctx[key as keyof PermissionCheckContext];
      if (Array.isArray(expected)) {
        if (!expected.includes(actual)) return false;
      } else if (actual !== expected) {
        return false;
      }
    }
    return true;
  }
}
