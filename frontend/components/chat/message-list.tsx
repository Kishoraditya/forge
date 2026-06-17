// =============================================================================
// forge / frontend / components / chat / message-list
// =============================================================================
// Description : Scrollable list of conversation messages.
// Layer       : Infra
// Feature     : F005 — Basic Conversation Interface
// Author      : cursor + KSR (reviewed by)
// Created     : 2026-06-17
// Modified    : 2026-06-17
// Version     : 0.1.0
// =============================================================================

"use client";

import { MessageBubble } from "@/components/chat/message-bubble";
import type { UiMessage } from "@/hooks/use-chat";

type Props = { messages: UiMessage[]; streaming: boolean };

export function MessageList({ messages, streaming }: Props) {
  return (
    <div className="flex-1 space-y-4 overflow-y-auto px-4 py-4">
      {messages.length === 0 && (
        <p className="text-center text-zinc-500">Ask anything to start the conversation.</p>
      )}
      {messages.map((m) => (
        <MessageBubble key={m.id} message={m} />
      ))}
      {streaming && (
        <p className="text-center text-sm text-zinc-500 animate-pulse">Assistant is typing…</p>
      )}
    </div>
  );
}
