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

import { useCallback, useEffect, useState } from "react";

import {
  createSession,
  getSessionStatus,
  SessionNotFoundError,
} from "@/lib/api/chat-client";
import { useSessionStore } from "@/lib/stores/session-store";

const STORAGE_KEY = "forge_session_id";

export function useSession() {
  const { sessionId, setSession, updateFromStatus, clear } = useSessionStore();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const createAndStoreSession = useCallback(async () => {
    const created = await createSession();
    localStorage.setItem(STORAGE_KEY, created.id);
    setSession({
      sessionId: created.id,
      budgetRemainingUsd: created.budget_remaining_usd,
      modelAlias: created.model_alias ?? "fast",
    });
    const status = await getSessionStatus(created.id);
    updateFromStatus(status);
    return created.id;
  }, [setSession, updateFromStatus]);

  useEffect(() => {
    let cancelled = false;
    async function init() {
      try {
        const stored = localStorage.getItem(STORAGE_KEY);
        if (stored) {
          try {
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
          } catch (e) {
            if (!(e instanceof SessionNotFoundError)) throw e;
            localStorage.removeItem(STORAGE_KEY);
            clear();
          }
        }
        if (!cancelled) await createAndStoreSession();
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
  }, [clear, createAndStoreSession, setSession, updateFromStatus]);

  const refreshStatus = useCallback(async () => {
    if (!sessionId) return;
    try {
      const status = await getSessionStatus(sessionId);
      updateFromStatus(status);
    } catch (e) {
      if (e instanceof SessionNotFoundError) {
        localStorage.removeItem(STORAGE_KEY);
        clear();
        await createAndStoreSession();
        return;
      }
      throw e;
    }
  }, [sessionId, updateFromStatus, clear, createAndStoreSession]);

  return { sessionId, loading, error, refreshStatus };
}
