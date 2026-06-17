// =============================================================================
// forge / frontend / lib / api-config
// =============================================================================
// Description : API base URL for browser calls to the Forge backend.
// Layer       : Infra
// Feature     : F005 — Basic Conversation Interface
// Author      : cursor + KSR (reviewed by)
// Created     : 2026-06-17
// Modified    : 2026-06-17
// Version     : 0.1.0
// =============================================================================

/** Backend API base; empty string uses Next.js rewrites to localhost:8000. */
export const API_BASE =
  process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, "") ?? "";
