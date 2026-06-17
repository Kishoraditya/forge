// =============================================================================
// forge / frontend / app / admin / page
// =============================================================================
// Description : Admin home dashboard (placeholder until F002 BYOK UI).
// Layer       : Infra
// Feature     : F006 — Single Admin Authentication
// Author      : cursor + KSR (reviewed by)
// Created     : 2026-06-17
// Modified    : 2026-06-17
// Version     : 0.1.0
// =============================================================================

"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { Button } from "@/components/ui/button";
import { createSupabaseBrowserClient } from "@/lib/supabase/client";
import { getSupabasePublicEnv, SUPABASE_ENV_SETUP_HINT } from "@/lib/supabase/env";

export default function AdminHomePage() {
  const router = useRouter();
  const supabaseEnv = getSupabasePublicEnv();
  const [email, setEmail] = useState<string | null>(null);

  useEffect(() => {
    if (!supabaseEnv) return;
    void createSupabaseBrowserClient()
      .auth.getUser()
      .then(({ data }) => setEmail(data.user?.email ?? null));
  }, [supabaseEnv]);

  const logout = async () => {
    if (!supabaseEnv) return;
    await createSupabaseBrowserClient().auth.signOut();
    router.replace("/admin/login");
    router.refresh();
  };

  if (!supabaseEnv) {
    return (
      <div className="space-y-2 rounded-md border border-amber-300 bg-amber-50 p-4 text-sm text-amber-900">
        <p className="font-medium">Supabase is not configured for the frontend.</p>
        <p>{SUPABASE_ENV_SETUP_HINT}</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-semibold">Admin dashboard</h1>
      <p className="text-zinc-600 dark:text-zinc-400">
        Signed in as {email ?? "…"}
      </p>
      <p className="text-sm text-zinc-500">
        BYOK configuration (F002) and document upload (F007) will appear here.
      </p>
      <Button type="button" variant="outline" onClick={() => void logout()}>
        Sign out
      </Button>
    </div>
  );
}
