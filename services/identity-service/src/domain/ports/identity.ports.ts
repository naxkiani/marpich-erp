import { User } from "../user.aggregate";
import { Role } from "../role.aggregate";
import { UniqueEntityId } from "@marpich/shared-kernel";
import type { AbacPolicy } from "@marpich/platform-core";

export interface IUserRepository {
  findByEmail(tenantId: string, email: string): Promise<User | null>;
  findById(tenantId: string, id: UniqueEntityId): Promise<User | null>;
  save(user: User): Promise<void>;
  existsByEmail(tenantId: string, email: string): Promise<boolean>;
  list(tenantId: string, options?: { search?: string; limit?: number; offset?: number }): Promise<User[]>;
}

export interface IRoleRepository {
  findById(tenantId: string, id: UniqueEntityId): Promise<Role | null>;
  findByCode(tenantId: string, code: string): Promise<Role | null>;
  save(role: Role): Promise<void>;
  list(tenantId: string): Promise<Role[]>;
}

export interface IPermissionRepository {
  findCodesByRoleIds(tenantId: string, roleIds: string[]): Promise<string[]>;
  findAllCodes(): Promise<{ id: string; code: string }[]>;
  findIdByCode(code: string): Promise<string | null>;
}

export interface IAbacPolicyRepository {
  findByTenant(tenantId: string): Promise<AbacPolicy[]>;
}

export interface ISessionRepository {
  create(session: {
    id: string;
    tenantId: string;
    userId: string;
    refreshTokenHash: string;
    ipAddress?: string | undefined;
    userAgent?: string | undefined;
    expiresAt: Date;
  }): Promise<void>;
  findByRefreshTokenHash(hash: string): Promise<{
    id: string;
    tenantId: string;
    userId: string;
    expiresAt: Date;
    revokedAt?: Date;
  } | null>;
  revoke(id: string): Promise<void>;
  revokeAllForUser(tenantId: string, userId: string): Promise<void>;
  deleteExpired(): Promise<number>;
}

export const USER_REPOSITORY = Symbol("USER_REPOSITORY");
export const ROLE_REPOSITORY = Symbol("ROLE_REPOSITORY");
export const PERMISSION_REPOSITORY = Symbol("PERMISSION_REPOSITORY");
export const ABAC_POLICY_REPOSITORY = Symbol("ABAC_POLICY_REPOSITORY");
export const SESSION_REPOSITORY = Symbol("SESSION_REPOSITORY");

export interface IPasswordHasher {
  hash(plain: string): Promise<string>;
  verify(plain: string, hash: string): Promise<boolean>;
}

export const PASSWORD_HASHER = Symbol("PASSWORD_HASHER");

export interface ITokenService {
  signAccess(payload: TokenPayload): string;
  signRefresh(payload: TokenPayload): string;
  verifyAccess(token: string): TokenPayload;
  verifyRefresh(token: string): TokenPayload;
  hashRefreshToken(token: string): string;
}

export interface TokenPayload {
  sub: string;
  tenantId: string;
  email: string;
  roles: string[];
  permissions: string[];
  locale: string;
  attributes: Record<string, unknown>;
}

export const TOKEN_SERVICE = Symbol("TOKEN_SERVICE");

export interface IMfaService {
  generateSecret(): string;
  generateUri(email: string, secret: string, issuer?: string): string;
  verifyToken(secret: string, token: string): boolean;
  generateBackupCodes(count?: number): string[];
}

export const MFA_SERVICE = Symbol("MFA_SERVICE");

export interface INotificationService {
  sendMfaEnabled(tenantId: string, email: string, locale: string): Promise<void>;
  sendLoginAlert(tenantId: string, email: string, ipAddress?: string): Promise<void>;
}

export const NOTIFICATION_SERVICE = Symbol("NOTIFICATION_SERVICE");
