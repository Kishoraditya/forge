// =============================================================================
// forge / frontend / app / admin / login / page
// =============================================================================
// Description : Admin email/password login via Supabase Auth.
// Layer       : Infra
// Feature     : F006 — Single Admin Authentication
// Author      : cursor + KSR (reviewed by)
// Created     : 2026-06-17
// Modified    : 2026-06-17
// Version     : 0.1.0
// =============================================================================

import { Suspense } from "react";

import { AdminLoginForm } from "@/components/admin/admin-login-form";

export default function AdminLoginPage() {
  return (
    <Suspense fallback={<p className="text-sm text-zinc-500">Loading login…</p>}>
      <AdminLoginForm />
    </Suspense>
  );
}
