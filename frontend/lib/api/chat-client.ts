// =============================================================================
// forge / frontend / lib / api / chat-client
// =============================================================================
// Description : HTTP and SSE client for sessions and conversation messages.
// Layer       : API
// Feature     : F005 — Basic Conversation Interface
// Author      : cursor + KSR (reviewed by)
// Created     : 2026-06-17
// Modified    : 2026-06-17
// Version     : 0.1.0
// =============================================================================

import { API_BASE } from "@/lib/api-config";

export type ChatMessage = {
  id: string;
  session_id: string;
  role: "user" | "assistant" | "system";
  content: string;
  created_at: string;
  model_alias?: string | null;
};

export type SessionCreateResponse = {
  id: string;
  budget_remaining_usd: number;
  expires_at: string;
  model_alias: string;
};

export type SessionStatus = {
  id: string;
  status: string;
  token_count: number;
  budget_remaining_usd: number;
  model_alias: string;
};

export async function createSession(): Promise<SessionCreateResponse> {
  const res = await fetch(`${API_BASE}/api/sessions`, { method: "POST" });
  if (!res.ok) throw new Error(`Session create failed: ${res.status}`);
  return res.json() as Promise<SessionCreateResponse>;
}

export async function getSessionStatus(sessionId: string): Promise<SessionStatus> {
  const res = await fetch(`${API_BASE}/api/sessions/${sessionId}`);
  if (!res.ok) throw new Error(`Session status failed: ${res.status}`);
  return res.json() as Promise<SessionStatus>;
}

export async function listMessages(sessionId: string): Promise<ChatMessage[]> {
  const res = await fetch(`${API_BASE}/api/sessions/${sessionId}/messages`);
  if (!res.ok) throw new Error(`List messages failed: ${res.status}`);
  return res.json() as Promise<ChatMessage[]>;
}

export async function clearMessages(sessionId: string): Promise<void> {
  const res = await fetch(`${API_BASE}/api/sessions/${sessionId}/messages`, {
    method: "DELETE",
  });
  if (!res.ok) throw new Error(`Clear messages failed: ${res.status}`);
}

export type StreamHandlers = {
  onDelta: (delta: string) => void;
  onDone: (usage?: { cost_usd?: number }) => void;
  onError: (message: string) => void;
};

/** Parse SSE stream from POST /messages. */
export async function streamMessage(
  sessionId: string,
  content: string,
  handlers: StreamHandlers,
): Promise<void> {
  const res = await fetch(`${API_BASE}/api/sessions/${sessionId}/messages`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ content }),
  });
  if (!res.ok) {
    const body = await res.text();
    handlers.onError(body || `Send failed: ${res.status}`);
    return;
  }
  const reader = res.body?.getReader();
  if (!reader) {
    handlers.onError("No response body");
    return;
  }
  const decoder = new TextDecoder();
  let buffer = "";
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    const parts = buffer.split("\n\n");
    buffer = parts.pop() ?? "";
    for (const part of parts) {
      const line = part.trim();
      if (!line.startsWith("data:")) continue;
      const json = line.slice(5).trim();
      try {
        const payload = JSON.parse(json) as {
          delta?: string;
          done?: boolean;
          usage?: { cost_usd?: number };
        };
        if (payload.delta) handlers.onDelta(payload.delta);
        if (payload.done) handlers.onDone(payload.usage);
      } catch {
        /* ignore malformed chunks */
      }
    }
  }
}

export async function regenerateMessage(
  sessionId: string,
  handlers: StreamHandlers,
): Promise<void> {
  const res = await fetch(
    `${API_BASE}/api/sessions/${sessionId}/messages/regenerate`,
    { method: "POST" },
  );
  if (!res.ok) {
    handlers.onError(`Regenerate failed: ${res.status}`);
    return;
  }
  const reader = res.body?.getReader();
  if (!reader) return;
  const decoder = new TextDecoder();
  let buffer = "";
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    const parts = buffer.split("\n\n");
    buffer = parts.pop() ?? "";
    for (const part of parts) {
      const line = part.trim();
      if (!line.startsWith("data:")) continue;
      const payload = JSON.parse(line.slice(5).trim()) as {
        delta?: string;
        done?: boolean;
        usage?: { cost_usd?: number };
      };
      if (payload.delta) handlers.onDelta(payload.delta);
      if (payload.done) handlers.onDone(payload.usage);
    }
  }
}
