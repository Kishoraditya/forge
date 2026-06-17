// =============================================================================
// forge / frontend / components / chat / budget-bar
// =============================================================================
// Description : Header bar showing session budget and model alias.
// Layer       : Infra
// Feature     : F004 — Session Management
// Author      : cursor + KSR (reviewed by)
// Created     : 2026-06-17
// Modified    : 2026-06-17
// Version     : 0.1.0
// =============================================================================

"use client";

import { useSessionStore } from "@/lib/stores/session-store";

export function BudgetBar() {
  const { budgetRemainingUsd, tokenCount, modelAlias } = useSessionStore();
  return (
    <header className="flex items-center justify-between border-b border-zinc-200 px-4 py-2 text-sm dark:border-zinc-800">
      <span className="font-semibold text-zinc-900 dark:text-zinc-100">Forge</span>
      <div className="flex gap-4 text-zinc-600 dark:text-zinc-400">
        <span className="rounded bg-zinc-100 px-2 py-0.5 dark:bg-zinc-800">model: {modelAlias}</span>
        <span>Budget: ${budgetRemainingUsd.toFixed(4)}</span>
        <span>Tokens: {tokenCount}</span>
      </div>
    </header>
  );
}
