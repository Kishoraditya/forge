// =============================================================================
// forge / frontend / hooks / use-session
// =============================================================================
// Description : Bootstrap anonymous session on mount and sync budget state.
// Layer       : Infra
// Feature     : F004 — Session Management
// Author      : cursor + KSR (reviewed by)
// Created     : 2026-06-17
// Modified    : 2026-06-17
// Version     : 0.1.0
// =============================================================================

"use client";

import { useEffect, useState } from "react";

import { createSession, getSessionStatus } from "@/lib/api/chat-client";
import { useSessionStore } from "@/lib/stores/session-store";

const STORAGE_KEY = "forge_session_id";

export function useSession() {
  const { sessionId, setSession, updateFromStatus } = useSessionStore();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    async function init() {
      try {
        const stored = localStorage.getItem(STORAGE_KEY);
        if (stored) {
          const status = await getSessionStatus(stored);
          if (!cancelled) {
            setSession({
              sessionId: stored,
              budgetRemainingUsd: status.budget_remaining_usd,
              modelAlias: status.model_alias,
            });
            updateFromStatus(status);
            setLoading(false);
            return;
          }
        }
        const created = await createSession();
        localStorage.setItem(STORAGE_KEY, created.id);
        if (!cancelled) {
          setSession({
            sessionId: created.id,
            budgetRemainingUsd: created.budget_remaining_usd,
            modelAlias: created.model_alias,
          });
        }
      } catch (e) {
        if (!cancelled) setError(e instanceof Error ? e.message : "Session error");
      } finally {
        if (!cancelled) setLoading(false);
      }
    }
    void init();
    return () => {
      cancelled = true;
    };
  }, [setSession, updateFromStatus]);

  const refreshStatus = async () => {
    if (!sessionId) return;
    const status = await getSessionStatus(sessionId);
    updateFromStatus(status);
  };

  return { sessionId, loading, error, refreshStatus };
}
