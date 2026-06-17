// =============================================================================
// forge / frontend / components / chat / chat-container
// =============================================================================
// Description : Main chat layout wiring session bootstrap and message flow.
// Layer       : Infra
// Feature     : F005 — Basic Conversation Interface
// Author      : cursor + KSR (reviewed by)
// Created     : 2026-06-17
// Modified    : 2026-06-17
// Version     : 0.1.0
// =============================================================================

"use client";

import { BudgetBar } from "@/components/chat/budget-bar";
import { ChatInput } from "@/components/chat/chat-input";
import { MessageList } from "@/components/chat/message-list";
import { useChat } from "@/hooks/use-chat";
import { useSession } from "@/hooks/use-session";

export function ChatContainer() {
  const { sessionId, loading, error: sessionError, refreshStatus } = useSession();
  const { messages, streaming, error, send, regenerate, clear } = useChat(
    sessionId,
    refreshStatus,
  );

  if (loading) {
    return <div className="flex flex-1 items-center justify-center text-zinc-500">Loading session…</div>;
  }

  if (sessionError) {
    return <div className="flex flex-1 items-center justify-center text-red-600">{sessionError}</div>;
  }

  return (
    <div className="flex min-h-screen flex-col bg-white dark:bg-black">
      <BudgetBar />
      {error && <p className="bg-red-50 px-4 py-2 text-sm text-red-700">{error}</p>}
      <MessageList messages={messages} streaming={streaming} />
      <ChatInput
        disabled={streaming || !sessionId}
        onSend={(t) => void send(t)}
        onRegenerate={() => void regenerate()}
        onClear={() => void clear()}
      />
    </div>
  );
}
