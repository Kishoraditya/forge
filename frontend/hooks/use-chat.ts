// =============================================================================
// forge / frontend / hooks / use-chat
// =============================================================================
// Description : Chat state, send/regenerate/clear with SSE streaming.
// Layer       : Infra
// Feature     : F005 — Basic Conversation Interface
// Author      : cursor + KSR (reviewed by)
// Created     : 2026-06-17
// Modified    : 2026-06-17
// Version     : 0.1.0
// =============================================================================

"use client";

import { useCallback, useEffect, useState } from "react";

import {
  clearMessages,
  listMessages,
  regenerateMessage,
  streamMessage,
  type ChatMessage,
} from "@/lib/api/chat-client";
import { useSessionStore } from "@/lib/stores/session-store";

export type UiMessage = {
  id: string;
  role: "user" | "assistant";
  content: string;
  createdAt: string;
};

export function useChat(sessionId: string | null, refreshStatus: () => Promise<void>) {
  const modelAlias = useSessionStore((s) => s.modelAlias);
  const [messages, setMessages] = useState<UiMessage[]>([]);
  const [streaming, setStreaming] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!sessionId) return;
    void listMessages(sessionId).then((rows: ChatMessage[]) => {
      setMessages(
        rows
          .filter((m) => m.role === "user" || m.role === "assistant")
          .map((m) => ({
            id: m.id,
            role: m.role as "user" | "assistant",
            content: m.content,
            createdAt: m.created_at,
          })),
      );
    });
  }, [sessionId]);

  const send = useCallback(
    async (content: string) => {
      if (!sessionId || !content.trim()) return;
      setError(null);
      const userMsg: UiMessage = {
        id: `local-${Date.now()}`,
        role: "user",
        content: content.trim(),
        createdAt: new Date().toISOString(),
      };
      const assistantId = `local-a-${Date.now()}`;
      setMessages((prev) => [...prev, userMsg, { id: assistantId, role: "assistant", content: "", createdAt: new Date().toISOString() }]);
      setStreaming(true);
      await streamMessage(sessionId, content.trim(), {
        onDelta: (delta) => {
          setMessages((prev) =>
            prev.map((m) => (m.id === assistantId ? { ...m, content: m.content + delta } : m)),
          );
        },
        onDone: async () => {
          setStreaming(false);
          await refreshStatus();
          const rows = await listMessages(sessionId);
          setMessages(
            rows
              .filter((m) => m.role === "user" || m.role === "assistant")
              .map((m) => ({
                id: m.id,
                role: m.role as "user" | "assistant",
                content: m.content,
                createdAt: m.created_at,
              })),
          );
        },
        onError: (msg) => {
          setStreaming(false);
          setError(msg);
        },
      });
    },
    [sessionId, refreshStatus],
  );

  const regenerate = useCallback(async () => {
    if (!sessionId) return;
    setStreaming(true);
    setError(null);
    setMessages((prev) => {
      const lastUserIdx = [...prev].reverse().findIndex((m) => m.role === "user");
      if (lastUserIdx < 0) return prev;
      const cut = prev.length - lastUserIdx;
      return [...prev.slice(0, cut), { ...prev[prev.length - 1], content: "", role: "assistant" as const }];
    });
    await regenerateMessage(sessionId, {
      onDelta: (delta) => {
        setMessages((prev) => {
          const next = [...prev];
          const last = next[next.length - 1];
          if (last?.role === "assistant") next[next.length - 1] = { ...last, content: last.content + delta };
          return next;
        });
      },
      onDone: async () => {
        setStreaming(false);
        await refreshStatus();
      },
      onError: (msg) => {
        setStreaming(false);
        setError(msg);
      },
    });
  }, [sessionId, refreshStatus]);

  const clear = useCallback(async () => {
    if (!sessionId) return;
    if (!confirm("Clear the entire conversation?")) return;
    await clearMessages(sessionId);
    setMessages([]);
  }, [sessionId]);

  return { messages, streaming, error, modelAlias, send, regenerate, clear };
}
