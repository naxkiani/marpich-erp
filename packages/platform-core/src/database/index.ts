import { Pool } from "pg";

let pool: Pool | null = null;

export function createPool(connectionString?: string): Pool {
  const url =
    connectionString ?? process.env.DATABASE_URL ?? "postgresql://marpich:marpich@localhost:5432/marpich_platform";
  pool = new Pool({
    connectionString: url,
    min: Number(process.env.DATABASE_POOL_MIN ?? 2),
    max: Number(process.env.DATABASE_POOL_MAX ?? 20),
  });
  return pool;
}

export function getPool(): Pool {
  if (!pool) return createPool();
  return pool;
}

export const DATABASE_POOL = Symbol("DATABASE_POOL");
