/**
 * Load repo root `.env.local` into process.env before Next.js starts.
 * Ensures NEXT_PUBLIC_* vars reach client bundles in the monorepo layout.
 */
import { spawn } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

import nextEnv from "@next/env";

const { loadEnvConfig } = nextEnv;

const frontendDir = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const repoRoot = path.resolve(frontendDir, "..");

loadEnvConfig(repoRoot);
loadEnvConfig(frontendDir);

if (!process.env.NEXT_PUBLIC_SUPABASE_URL && process.env.SUPABASE_URL) {
  process.env.NEXT_PUBLIC_SUPABASE_URL = process.env.SUPABASE_URL;
}
if (!process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY && process.env.SUPABASE_ANON_KEY) {
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY = process.env.SUPABASE_ANON_KEY;
}

const nextArgs = process.argv.slice(2);
const child = spawn("npx", ["next", ...nextArgs], {
  cwd: frontendDir,
  env: process.env,
  stdio: "inherit",
  shell: true,
});

child.on("exit", (code, signal) => {
  process.exit(code ?? (signal ? 1 : 0));
});
