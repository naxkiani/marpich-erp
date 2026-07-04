import { Injectable } from "@nestjs/common";
import { User, UserProps } from "../../domain/user.aggregate";
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

const PERMISSION_SEED: { id: string; code: string }[] = [
  { id: "00000000-0000-4000-8000-000000000001", code: "identity.users.read" },
  { id: "00000000-0000-4000-8000-000000000002", code: "identity.users.write" },
  { id: "00000000-0000-4000-8000-000000000003", code: "identity.users.delete" },
  { id: "00000000-0000-4000-8000-000000000004", code: "identity.roles.read" },
  { id: "00000000-0000-4000-8000-000000000005", code: "identity.roles.write" },
  { id: "00000000-0000-4000-8000-000000000006", code: "identity.mfa.manage" },
  { id: "00000000-0000-4000-8000-000000000007", code: "identity.sessions.read" },
  { id: "00000000-0000-4000-8000-000000000008", code: "identity.sessions.revoke" },
  { id: "00000000-0000-4000-8000-000000000009", code: "identity.audit.read" },
  { id: "00000000-0000-4000-8000-000000000010", code: "identity.policies.write" },
];

@Injectable()
export class InMemoryUserRepository implements IUserRepository {
  private readonly users = new Map<string, User>();

  async findByEmail(tenantId: string, email: string): Promise<User | null> {
    for (const user of this.users.values()) {
      if (user.tenantId === tenantId && user.email === email.toLowerCase()) return user;
    }
    return null;
  }

  async findById(tenantId: string, id: UniqueEntityId): Promise<User | null> {
    const user = this.users.get(id.toString());
    if (!user || user.tenantId !== tenantId) return null;
    return user;
  }

  async save(user: User): Promise<void> {
    this.users.set(user.id.toString(), user);
  }

  async existsByEmail(tenantId: string, email: string): Promise<boolean> {
    return (await this.findByEmail(tenantId, email)) !== null;
  }

  async list(
    tenantId: string,
    options?: { search?: string; limit?: number; offset?: number },
  ): Promise<User[]> {
    let items = [...this.users.values()].filter((u) => u.tenantId === tenantId);
    if (options?.search) {
      const q = options.search.toLowerCase();
      items = items.filter(
        (u) => u.email.includes(q) || u.displayName.toLowerCase().includes(q),
      );
    }
    const offset = options?.offset ?? 0;
    const limit = options?.limit ?? 50;
    return items.slice(offset, offset + limit);
  }
}

const rolePermissionIndex = new Map<string, Set<string>>();

@Injectable()
export class InMemoryRoleRepository implements IRoleRepository {
  private readonly roles = new Map<string, Role>();

  async findById(tenantId: string, id: UniqueEntityId): Promise<Role | null> {
    const role = this.roles.get(id.toString());
    if (!role || role.tenantId !== tenantId) return null;
    return role;
  }

  async findByCode(tenantId: string, code: string): Promise<Role | null> {
    for (const role of this.roles.values()) {
      if (role.tenantId === tenantId && role.code === code.toLowerCase()) return role;
    }
    return null;
  }

  async save(role: Role): Promise<void> {
    this.roles.set(role.id.toString(), role);
    rolePermissionIndex.set(
      `${role.tenantId}:${role.id.toString()}`,
      new Set([...role.permissionIds]),
    );
  }

  async list(tenantId: string): Promise<Role[]> {
    return [...this.roles.values()].filter((r) => r.tenantId === tenantId);
  }
}

@Injectable()
export class InMemoryPermissionRepository implements IPermissionRepository {
  async findCodesByRoleIds(tenantId: string, roleIds: string[]): Promise<string[]> {
    const codes = new Set<string>();
    for (const roleId of roleIds) {
      const ids = rolePermissionIndex.get(`${tenantId}:${roleId}`);
      if (!ids) continue;
      for (const pid of ids) {
        const perm = PERMISSION_SEED.find((p) => p.id === pid);
        if (perm) codes.add(perm.code);
      }
    }
    return [...codes];
  }

  async findAllCodes(): Promise<{ id: string; code: string }[]> {
    return PERMISSION_SEED;
  }

  async findIdByCode(code: string): Promise<string | null> {
    return PERMISSION_SEED.find((p) => p.code === code)?.id ?? null;
  }
}

@Injectable()
export class InMemorySessionRepository implements ISessionRepository {
  private readonly sessions = new Map<string, {
    id: string;
    tenantId: string;
    userId: string;
    refreshTokenHash: string;
    expiresAt: Date;
    revokedAt?: Date;
  }>();

  async create(session: {
    id: string;
    tenantId: string;
    userId: string;
    refreshTokenHash: string;
    ipAddress?: string;
    userAgent?: string;
    expiresAt: Date;
  }): Promise<void> {
    this.sessions.set(session.id, session);
  }

  async findByRefreshTokenHash(hash: string) {
    for (const s of this.sessions.values()) {
      if (s.refreshTokenHash === hash && !s.revokedAt) return s;
    }
    return null;
  }

  async revoke(id: string): Promise<void> {
    const s = this.sessions.get(id);
    if (s) s.revokedAt = new Date();
  }

  async revokeAllForUser(tenantId: string, userId: string): Promise<void> {
    for (const s of this.sessions.values()) {
      if (s.tenantId === tenantId && s.userId === userId) s.revokedAt = new Date();
    }
  }

  async deleteExpired(): Promise<number> {
    const now = new Date();
    let count = 0;
    for (const [id, s] of this.sessions) {
      if (s.expiresAt < now) {
        this.sessions.delete(id);
        count++;
      }
    }
    return count;
  }
}

@Injectable()
export class InMemoryAbacPolicyRepository implements IAbacPolicyRepository {
  private readonly policies: AbacPolicy[] = [];

  async findByTenant(tenantId: string): Promise<AbacPolicy[]> {
    return this.policies.filter((p) => p.tenantId === tenantId);
  }
}

export function hydrateUser(props: UserProps, id: string): User {
  return User.reconstitute(props, UniqueEntityId.create(id));
}

export function hydrateRole(props: RoleProps, id: string): Role {
  return Role.reconstitute(props, UniqueEntityId.create(id));
}
