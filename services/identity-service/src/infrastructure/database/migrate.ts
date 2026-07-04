import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { createPool } from "@marpich/platform-core";

const MIGRATIONS = [
  resolve(__dirname, "../../../../../infrastructure/docker/migrations/002_identity_full.sql"),
];

async function migrate(): Promise<void> {
  const pool = createPool();
  console.log("[identity-migrate] connecting to database...");

  for (const file of MIGRATIONS) {
    const sql = readFileSync(file, "utf8");
    console.log(`[identity-migrate] applying ${file}`);
    await pool.query(sql);
  }

  console.log("[identity-migrate] done");
  await pool.end();
}

migrate().catch((err: unknown) => {
  console.error("[identity-migrate] failed:", err);
  process.exit(1);
});
