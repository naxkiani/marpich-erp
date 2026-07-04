import type { Provider } from "@nestjs/common";
import Redis from "ioredis";
import {
  AUDIT_LOGGER,
  CACHE_SERVICE,
  ConsoleAuditLogger,
  ConsoleOutboxPublisher,
  createPool,
  InMemoryCacheService,
  OUTBOX_PUBLISHER,
  PostgresAuditLogger,
  PostgresOutboxPublisher,
  RedisCacheService,
} from "@marpich/platform-core";
import {
  USER_REPOSITORY,
  ROLE_REPOSITORY,
  PERMISSION_REPOSITORY,
  SESSION_REPOSITORY,
  ABAC_POLICY_REPOSITORY,
} from "../domain/ports/identity.ports";
import {
  InMemoryUserRepository,
  InMemoryRoleRepository,
  InMemoryPermissionRepository,
  InMemorySessionRepository,
  InMemoryAbacPolicyRepository,
} from "./persistence/in-memory.repositories";
import {
  PostgresUserRepository,
  PostgresRoleRepository,
  PostgresPermissionRepository,
  PostgresSessionRepository,
  PostgresAbacPolicyRepository,
} from "./persistence/postgres.repositories";

export function usePostgresPersistence(): boolean {
  return process.env.IDENTITY_PERSISTENCE === "postgres";
}

export function buildPersistenceProviders(): Provider[] {
  if (usePostgresPersistence()) {
    const pool = createPool();
    return [
      { provide: USER_REPOSITORY, useFactory: () => new PostgresUserRepository(pool) },
      { provide: ROLE_REPOSITORY, useFactory: () => new PostgresRoleRepository(pool) },
      { provide: PERMISSION_REPOSITORY, useFactory: () => new PostgresPermissionRepository(pool) },
      { provide: SESSION_REPOSITORY, useFactory: () => new PostgresSessionRepository(pool) },
      { provide: ABAC_POLICY_REPOSITORY, useFactory: () => new PostgresAbacPolicyRepository(pool) },
      { provide: AUDIT_LOGGER, useFactory: () => new PostgresAuditLogger(pool) },
      { provide: OUTBOX_PUBLISHER, useFactory: () => new PostgresOutboxPublisher(pool) },
    ];
  }

  return [
    { provide: USER_REPOSITORY, useClass: InMemoryUserRepository },
    { provide: ROLE_REPOSITORY, useClass: InMemoryRoleRepository },
    { provide: PERMISSION_REPOSITORY, useClass: InMemoryPermissionRepository },
    { provide: SESSION_REPOSITORY, useClass: InMemorySessionRepository },
    { provide: ABAC_POLICY_REPOSITORY, useClass: InMemoryAbacPolicyRepository },
    { provide: AUDIT_LOGGER, useClass: ConsoleAuditLogger },
    { provide: OUTBOX_PUBLISHER, useClass: ConsoleOutboxPublisher },
  ];
}

export function buildCacheProvider(): Provider {
  const redisUrl = process.env.REDIS_URL;
  if (usePostgresPersistence() && redisUrl) {
    const redis = new Redis(redisUrl);
    return { provide: CACHE_SERVICE, useFactory: () => new RedisCacheService(redis) };
  }
  return { provide: CACHE_SERVICE, useClass: InMemoryCacheService };
}
