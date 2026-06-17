// =============================================================================
// forge / frontend / components / admin / admin-login-form
// =============================================================================
// Description : Email/password form for Supabase admin authentication.
// Layer       : Infra
// Feature     : F006 — Single Admin Authentication
// Author      : cursor + KSR (reviewed by)
// Created     : 2026-06-17
// Modified    : 2026-06-17
// Version     : 0.1.0
// =============================================================================

"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { useState } from "react";

import { Button } from "@/components/ui/button";
import { createSupabaseBrowserClient } from "@/lib/supabase/client";
import { getSupabasePublicEnv, SUPABASE_ENV_SETUP_HINT } from "@/lib/supabase/env";

export function AdminLoginForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const configError = getSupabasePublicEnv() ? null : SUPABASE_ENV_SETUP_HINT;

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (configError) return;
    setError(null);
    setLoading(true);
    try {
      const supabase = createSupabaseBrowserClient();
      const { error: signInError } = await supabase.auth.signInWithPassword({
        email,
        password,
      });
      if (signInError) {
        setError(signInError.message);
        return;
      }
      const next = searchParams.get("next") || "/admin";
      router.replace(next);
      router.refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed");
    } finally {
      setLoading(false);
    }
  };

  if (configError) {
    return (
      <div className="mx-auto max-w-md space-y-2 rounded-md border border-amber-300 bg-amber-50 p-4 text-sm text-amber-900">
        <h1 className="text-2xl font-semibold text-amber-950">Admin login</h1>
        <p className="font-medium">Supabase is not configured for the frontend.</p>
        <p>{configError}</p>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-md">
      <h1 className="mb-6 text-2xl font-semibold">Admin login</h1>
      <form onSubmit={(e) => void submit(e)} className="space-y-4">
        <div>
          <label htmlFor="email" className="mb-1 block text-sm">
            Email
          </label>
          <input
            id="email"
            type="email"
            required
            className="w-full rounded-md border border-zinc-300 px-3 py-2 dark:border-zinc-700 dark:bg-zinc-900"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <div>
          <label htmlFor="password" className="mb-1 block text-sm">
            Password
          </label>
          <input
            id="password"
            type="password"
            required
            className="w-full rounded-md border border-zinc-300 px-3 py-2 dark:border-zinc-700 dark:bg-zinc-900"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        {error && <p className="text-sm text-red-600">{error}</p>}
        <Button type="submit" disabled={loading} className="w-full">
          {loading ? "Signing in…" : "Sign in"}
        </Button>
      </form>
    </div>
  );
}
