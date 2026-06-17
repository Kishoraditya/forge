// =============================================================================
// forge / frontend / lib / supabase / env
// =============================================================================
// Description : Public Supabase URL and anon key for browser/middleware clients.
// Layer       : Infra
// Feature     : F006 — Single Admin Authentication
// Author      : cursor + KSR (reviewed by)
// Created     : 2026-06-17
// Modified    : 2026-06-17
// Version     : 0.1.0
// =============================================================================

export type SupabasePublicEnv = {
  url: string;
  anonKey: string;
};

/**
 * Return Supabase public credentials when configured.
 *
 * Values are injected via next.config from root `.env.local` (SUPABASE_* or
 * NEXT_PUBLIC_SUPABASE_*). Restart `npm run dev` after changing env files.
 */
export function getSupabasePublicEnv(): SupabasePublicEnv | null {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const anonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
  if (!url || !anonKey) {
    return null;
  }
  return { url, anonKey };
}

export const SUPABASE_ENV_SETUP_HINT =
  "Set SUPABASE_URL and SUPABASE_ANON_KEY in the repo root .env.local, then restart npm run dev.";
