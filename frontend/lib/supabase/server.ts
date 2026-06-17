// =============================================================================
// forge / frontend / lib / supabase / server
// =============================================================================
// Description : Server Supabase client for middleware and RSC.
// Layer       : Infra
// Feature     : F006 — Single Admin Authentication
// Author      : cursor + KSR (reviewed by)
// Created     : 2026-06-17
// Modified    : 2026-06-17
// Version     : 0.1.0
// =============================================================================

import { createServerClient } from "@supabase/ssr";
import { cookies } from "next/headers";

import { getSupabasePublicEnv } from "@/lib/supabase/env";

export async function createSupabaseServerClient() {
  const config = getSupabasePublicEnv();
  if (!config) {
    throw new Error("Missing Supabase public env");
  }
  const cookieStore = await cookies();
  return createServerClient(config.url, config.anonKey, {
    cookies: {
      getAll() {
        return cookieStore.getAll();
      },
      setAll(cookiesToSet) {
        try {
          cookiesToSet.forEach(({ name, value, options }) => {
            cookieStore.set(name, value, options);
          });
        } catch {
          /* setAll from Server Component — middleware handles refresh */
        }
      },
    },
  });
}
