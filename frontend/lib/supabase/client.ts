// =============================================================================
// forge / frontend / lib / supabase / client
// =============================================================================
// Description : Browser Supabase client for admin authentication.
// Layer       : Infra
// Feature     : F006 — Single Admin Authentication
// Author      : cursor + KSR (reviewed by)
// Created     : 2026-06-17
// Modified    : 2026-06-17
// Version     : 0.1.0
// =============================================================================

import { createBrowserClient } from "@supabase/ssr";

import { getSupabasePublicEnv, SUPABASE_ENV_SETUP_HINT } from "@/lib/supabase/env";

export function createSupabaseBrowserClient() {
  const config = getSupabasePublicEnv();
  if (!config) {
    throw new Error(`Missing Supabase public env. ${SUPABASE_ENV_SETUP_HINT}`);
  }
  return createBrowserClient(config.url, config.anonKey);
}
