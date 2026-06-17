// =============================================================================
// forge / frontend / lib / stores / session-store
// =============================================================================
// Description : Zustand store for anonymous session id and budget display.
// Layer       : Infra
// Feature     : F004 — Session Management
// Author      : cursor + KSR (reviewed by)
// Created     : 2026-06-17
// Modified    : 2026-06-17
// Version     : 0.1.0
// =============================================================================

import { create } from "zustand";

export type SessionState = {
  sessionId: string | null;
  budgetRemainingUsd: number;
  tokenCount: number;
  modelAlias: string;
  status: string;
  setSession: (data: {
    sessionId: string;
    budgetRemainingUsd: number;
    modelAlias: string;
    expiresAt?: string;
  }) => void;
  updateFromStatus: (data: {
    budget_remaining_usd: number;
    token_count: number;
    model_alias: string;
    status: string;
  }) => void;
  clear: () => void;
};

export const useSessionStore = create<SessionState>((set) => ({
  sessionId: null,
  budgetRemainingUsd: 0,
  tokenCount: 0,
  modelAlias: "fast",
  status: "active",
  setSession: (data) =>
    set({
      sessionId: data.sessionId,
      budgetRemainingUsd: data.budgetRemainingUsd,
      modelAlias: data.modelAlias,
      status: "active",
    }),
  updateFromStatus: (data) =>
    set({
      budgetRemainingUsd: data.budget_remaining_usd,
      tokenCount: data.token_count,
      modelAlias: data.model_alias,
      status: data.status,
    }),
  clear: () =>
    set({
      sessionId: null,
      budgetRemainingUsd: 0,
      tokenCount: 0,
      modelAlias: "fast",
      status: "active",
    }),
}));
