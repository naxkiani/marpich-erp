import { Injectable } from "@nestjs/common";
import { Pool, QueryResultRow } from "pg";
import { User, UserProps, UserStatus } from "../../domain/user.aggregate";
import { Role, RoleProps } from "../../domain/role.aggregate";
import { UniqueEntityId } from "@marpich/shared-kernel";
import type {
  IUserRepository,
  IRoleRepository,
  IPermissionRepository,
  ISessionRepository,
  IAbacPolicyRepository,
} from "../../domain/ports/identity.ports";
import type { AbacPolicy } from "@marpich/platform-core";
import { hydrateUser, hydrateRole } from "./in-memory.repositories";

function mapUserRow(row: Record<string, unknown>, roleIds: string[]): User {
  const props: UserProps = {
    tenantId: row.tenant_id as string,
    email: row.email as string,
    passwordHash: row.password_hash as string,
    displayName: row.display_name as string,
    status: row.status as UserStatus,
    locale: (row.locale as string) ?? "en-US",
    attributes: (row.attributes as Record<string, unknown>) ?? {},
    mfaEnabled: Boolean(row.mfa_enabled),
    mfaSecret: (row.mfa_secret as string) ?? undefined,
    backupCodes: (row.backup_codes as string[]) ?? [],
    roleIds,
    failedLoginAttempts: Number(row.failed_login_attempts ?? 0),
    lockedUntil: row.locked_until ? new Date(row.locked_until as string) : undefined,
    lastLoginAt: row.last_login_at ? new Date(row.last_login_at as string) : undefined,
    createdAt: new Date(row.created_at as string),
    updatedAt: new Date(row.updated_at as string),
  };
  return hydrateUser(props, row.id as string);
}

@Injectable()
export class PostgresUserRepository implements IUserRepository {
  constructor(private readonly pool: Pool) {}

  async findByEmail(tenantId: string, email: string): Promise<User | null> {
    const result = await this.pool.query(
      `SELECT * FROM identity.users WHERE tenant_id = $1 AND email = $2`,
      [tenantId, email.toLowerCase()],
    );
    if (result.rows.length === 0) return null;
    const roleIds = await this.loadRoleIds(tenantId, result.rows[0].id as string);
    return mapUserRow(result.rows[0], roleIds);
  }

  async findById(tenantId: string, id: UniqueEntityId): Promise<User | null> {
    const result = await this.pool.query(
      `SELECT * FROM identity.users WHERE tenant_id = $1 AND id = $2`,
      [tenantId, id.toString()],
    );
    if (result.rows.length === 0) return null;
    const roleIds = await this.loadRoleIds(tenantId, id.toString());
    return mapUserRow(result.rows[0], roleIds);
  }

  async save(user: User): Promise<void> {
    const snap = user.toSnapshot();
    const client = await this.pool.connect();
    try {
      await client.query("BEGIN");
      await client.query(
        `INSERT INTO identity.users (
          id, tenant_id, email, password_hash, display_name, status, locale,
          attributes, mfa_enabled, mfa_secret, backup_codes, last_login_at,
          failed_login_attempts, locked_until, created_at, updated_at
        ) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16)
        ON CONFLICT (id) DO UPDATE SET
          email = EXCLUDED.email,
          password_hash = EXCLUDED.password_hash,
          display_name = EXCLUDED.display_name,
          status = EXCLUDED.status,
          locale = EXCLUDED.locale,
          attributes = EXCLUDED.attributes,
          mfa_enabled = EXCLUDED.mfa_enabled,
          mfa_secret = EXCLUDED.mfa_secret,
          backup_codes = EXCLUDED.backup_codes,
          last_login_at = EXCLUDED.last_login_at,
          failed_login_attempts = EXCLUDED.failed_login_attempts,
          locked_until = EXCLUDED.locked_until,
          updated_at = EXCLUDED.updated_at`,
        [
          snap.id,
          snap.tenantId,
          snap.email,
          user.passwordHash,
          snap.displayName,
          snap.status,
          snap.locale,
          JSON.stringify(snap.attributes),
          snap.mfaEnabled,
          user.mfaSecret ?? null,
          JSON.stringify(user.backupCodes),
          snap.lastLoginAt ?? null,
          user.failedLoginAttempts,
          user.lockedUntil ?? null,
          snap.createdAt,
          snap.updatedAt,
        ],
      );

      await client.query(
        `DELETE FROM identity.user_roles WHERE tenant_id = $1 AND user_id = $2`,
        [snap.tenantId, snap.id],
      );
      for (const roleId of user.roleIds) {
        await client.query(
          `INSERT INTO identity.user_roles (tenant_id, user_id, role_id)
           VALUES ($1, $2, $3) ON CONFLICT DO NOTHING`,
          [snap.tenantId, snap.id, roleId],
        );
      }
      await client.query("COMMIT");
    } catch (err) {
      await client.query("ROLLBACK");
      throw err;
    } finally {
      client.release();
    }
  }

  async existsByEmail(tenantId: string, email: string): Promise<boolean> {
    const result = await this.pool.query(
      `SELECT 1 FROM identity.users WHERE tenant_id = $1 AND email = $2 LIMIT 1`,
      [tenantId, email.toLowerCase()],
    );
    return result.rows.length > 0;
  }

  async list(
    tenantId: string,
    options?: { search?: string; limit?: number; offset?: number },
  ): Promise<User[]> {
    const limit = options?.limit ?? 50;
    const offset = options?.offset ?? 0;
    const params: unknown[] = [tenantId];
    let searchClause = "";
    if (options?.search) {
      params.push(`%${options.search.toLowerCase()}%`);
      searchClause = ` AND (LOWER(email) LIKE $2 OR LOWER(display_name) LIKE $2)`;
    }
    params.push(limit, offset);
    const limitIdx = params.length - 1;
    const offsetIdx = params.length;

    const result = await this.pool.query(
      `SELECT * FROM identity.users WHERE tenant_id = $1${searchClause}
       ORDER BY created_at DESC LIMIT $${limitIdx} OFFSET $${offsetIdx}`,
      params,
    );

    const users: User[] = [];
    for (const row of result.rows) {
      const roleIds = await this.loadRoleIds(tenantId, row.id as string);
      users.push(mapUserRow(row, roleIds));
    }
    return users;
  }

  private async loadRoleIds(tenantId: string, userId: string): Promise<string[]> {
    const result = await this.pool.query(
      `SELECT role_id FROM identity.user_roles WHERE tenant_id = $1 AND user_id = $2`,
      [tenantId, userId],
    );
    return result.rows.map((r: QueryResultRow) => r.role_id as string);
  }
}

@Injectable()
export class PostgresRoleRepository implements IRoleRepository {
  constructor(private readonly pool: Pool) {}

  async findById(tenantId: string, id: UniqueEntityId): Promise<Role | null> {
    const result = await this.pool.query(
      `SELECT * FROM identity.roles WHERE tenant_id = $1 AND id = $2`,
      [tenantId, id.toString()],
    );
    if (result.rows.length === 0) return null;
    const permissionIds = await this.loadPermissionIds(tenantId, id.toString());
    return this.mapRole(result.rows[0], permissionIds);
  }

  async findByCode(tenantId: string, code: string): Promise<Role | null> {
    const result = await this.pool.query(
      `SELECT * FROM identity.roles WHERE tenant_id = $1 AND code = $2`,
      [tenantId, code.toLowerCase()],
    );
    if (result.rows.length === 0) return null;
    const permissionIds = await this.loadPermissionIds(tenantId, result.rows[0].id as string);
    return this.mapRole(result.rows[0], permissionIds);
  }

  async save(role: Role): Promise<void> {
    const snap = role.toSnapshot();
    const client = await this.pool.connect();
    try {
      await client.query("BEGIN");
      await client.query(
        `INSERT INTO identity.roles (id, tenant_id, code, name, description, is_system, created_at, updated_at)
         VALUES ($1,$2,$3,$4,$5,$6,$7,$8)
         ON CONFLICT (id) DO UPDATE SET
           name = EXCLUDED.name,
           description = EXCLUDED.description,
           updated_at = EXCLUDED.updated_at`,
        [
          snap.id,
          snap.tenantId,
          snap.code,
          snap.name,
          snap.description ?? null,
          snap.isSystem,
          snap.createdAt,
          snap.updatedAt,
        ],
      );

      await client.query(
        `DELETE FROM identity.role_permissions WHERE tenant_id = $1 AND role_id = $2`,
        [snap.tenantId, snap.id],
      );
      for (const permissionId of role.permissionIds) {
        await client.query(
          `INSERT INTO identity.role_permissions (tenant_id, role_id, permission_id)
           VALUES ($1, $2, $3) ON CONFLICT DO NOTHING`,
          [snap.tenantId, snap.id, permissionId],
        );
      }
      await client.query("COMMIT");
    } catch (err) {
      await client.query("ROLLBACK");
      throw err;
    } finally {
      client.release();
    }
  }

  async list(tenantId: string): Promise<Role[]> {
    const result = await this.pool.query(
      `SELECT * FROM identity.roles WHERE tenant_id = $1 ORDER BY name`,
      [tenantId],
    );
    const roles: Role[] = [];
    for (const row of result.rows) {
      const permissionIds = await this.loadPermissionIds(tenantId, row.id as string);
      roles.push(this.mapRole(row, permissionIds));
    }
    return roles;
  }

  private mapRole(row: Record<string, unknown>, permissionIds: string[]): Role {
    const props: RoleProps = {
      tenantId: row.tenant_id as string,
      code: row.code as string,
      name: row.name as string,
      description: (row.description as string) ?? undefined,
      isSystem: Boolean(row.is_system),
      permissionIds,
      createdAt: new Date(row.created_at as string),
      updatedAt: new Date(row.updated_at as string),
    };
    return hydrateRole(props, row.id as string);
  }

  private async loadPermissionIds(tenantId: string, roleId: string): Promise<string[]> {
    const result = await this.pool.query(
      `SELECT permission_id FROM identity.role_permissions WHERE tenant_id = $1 AND role_id = $2`,
      [tenantId, roleId],
    );
    return result.rows.map((r: QueryResultRow) => r.permission_id as string);
  }
}

@Injectable()
export class PostgresPermissionRepository implements IPermissionRepository {
  constructor(private readonly pool: Pool) {}

  async findCodesByRoleIds(tenantId: string, roleIds: string[]): Promise<string[]> {
    if (roleIds.length === 0) return [];
    const result = await this.pool.query(
      `SELECT DISTINCT p.code FROM identity.permissions p
       JOIN identity.role_permissions rp ON rp.permission_id = p.id
       WHERE rp.tenant_id = $1 AND rp.role_id = ANY($2::uuid[])`,
      [tenantId, roleIds],
    );
    return result.rows.map((r: QueryResultRow) => r.code as string);
  }

  async findAllCodes(): Promise<{ id: string; code: string }[]> {
    const result = await this.pool.query(
      `SELECT id, code FROM identity.permissions ORDER BY code`,
    );
    return result.rows.map((r: QueryResultRow) => ({
      id: r.id as string,
      code: r.code as string,
    }));
  }

  async findIdByCode(code: string): Promise<string | null> {
    const result = await this.pool.query(
      `SELECT id FROM identity.permissions WHERE code = $1`,
      [code],
    );
    return result.rows[0]?.id ?? null;
  }
}

@Injectable()
export class PostgresSessionRepository implements ISessionRepository {
  constructor(private readonly pool: Pool) {}

  async create(session: {
    id: string;
    tenantId: string;
    userId: string;
    refreshTokenHash: string;
    ipAddress?: string | undefined;
    userAgent?: string | undefined;
    expiresAt: Date;
  }): Promise<void> {
    await this.pool.query(
      `INSERT INTO identity.sessions (id, tenant_id, user_id, refresh_token_hash, ip_address, user_agent, expires_at)
       VALUES ($1,$2,$3,$4,$5,$6,$7)`,
      [
        session.id,
        session.tenantId,
        session.userId,
        session.refreshTokenHash,
        session.ipAddress ?? null,
        session.userAgent ?? null,
        session.expiresAt,
      ],
    );
  }

  async findByRefreshTokenHash(hash: string): Promise<{
    id: string;
    tenantId: string;
    userId: string;
    expiresAt: Date;
    revokedAt?: Date;
  } | null> {
    const result = await this.pool.query(
      `SELECT id, tenant_id, user_id, expires_at, revoked_at
       FROM identity.sessions
       WHERE refresh_token_hash = $1 AND revoked_at IS NULL
       LIMIT 1`,
      [hash],
    );
    if (result.rows.length === 0) return null;
    const row = result.rows[0] as QueryResultRow;
    return {
      id: row.id as string,
      tenantId: row.tenant_id as string,
      userId: row.user_id as string,
      expiresAt: new Date(row.expires_at as string),
    };
  }

  async revoke(id: string): Promise<void> {
    await this.pool.query(
      `UPDATE identity.sessions SET revoked_at = NOW() WHERE id = $1`,
      [id],
    );
  }

  async revokeAllForUser(tenantId: string, userId: string): Promise<void> {
    await this.pool.query(
      `UPDATE identity.sessions SET revoked_at = NOW()
       WHERE tenant_id = $1 AND user_id = $2 AND revoked_at IS NULL`,
      [tenantId, userId],
    );
  }

  async deleteExpired(): Promise<number> {
    const result = await this.pool.query(
      `DELETE FROM identity.sessions WHERE expires_at < NOW() OR revoked_at IS NOT NULL`,
    );
    return result.rowCount ?? 0;
  }
}

@Injectable()
export class PostgresAbacPolicyRepository implements IAbacPolicyRepository {
  constructor(private readonly pool: Pool) {}

  async findByTenant(tenantId: string): Promise<AbacPolicy[]> {
    const result = await this.pool.query(
      `SELECT * FROM identity.abac_policies
       WHERE tenant_id = $1 AND enabled = TRUE
       ORDER BY priority ASC`,
      [tenantId],
    );
    return result.rows.map((row: QueryResultRow) => ({
      id: row.id as string,
      tenantId: row.tenant_id as string,
      name: row.name as string,
      effect: row.effect as "allow" | "deny",
      resource: row.resource as string,
      action: row.action as string,
      conditions: (row.conditions as Record<string, unknown>) ?? {},
      priority: Number(row.priority),
      enabled: Boolean(row.enabled),
    }));
  }
}
