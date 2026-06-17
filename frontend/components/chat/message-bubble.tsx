// =============================================================================
// forge / frontend / components / chat / message-bubble
// =============================================================================
// Description : Single chat message with copy and timestamp.
// Layer       : Infra
// Feature     : F005 — Basic Conversation Interface
// Author      : cursor + KSR (reviewed by)
// Created     : 2026-06-17
// Modified    : 2026-06-17
// Version     : 0.1.0
// =============================================================================

"use client";

import { MarkdownContent } from "@/components/chat/markdown-content";
import type { UiMessage } from "@/hooks/use-chat";

type Props = { message: UiMessage };

export function MessageBubble({ message }: Props) {
  const isUser = message.role === "user";
  const time = new Date(message.createdAt).toLocaleTimeString();

  const copy = async () => {
    await navigator.clipboard.writeText(message.content);
  };

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-[85%] rounded-lg px-4 py-2 ${
          isUser
            ? "bg-zinc-900 text-white dark:bg-zinc-100 dark:text-zinc-900"
            : "bg-zinc-100 text-zinc-900 dark:bg-zinc-900 dark:text-zinc-100"
        }`}
      >
        <div className="prose prose-sm dark:prose-invert max-w-none">
          {isUser ? <p className="whitespace-pre-wrap">{message.content}</p> : <MarkdownContent content={message.content || "…"} />}
        </div>
        <div className="mt-2 flex items-center justify-between gap-2 text-xs opacity-70">
          <span>{time}</span>
          <button type="button" onClick={() => void copy()} className="hover:underline">
            Copy
          </button>
        </div>
      </div>
    </div>
  );
}
