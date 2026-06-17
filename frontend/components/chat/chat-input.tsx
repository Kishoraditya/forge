// =============================================================================
// forge / frontend / components / chat / chat-input
// =============================================================================
// Description : Message input with send and action buttons.
// Layer       : Infra
// Feature     : F005 — Basic Conversation Interface
// Author      : cursor + KSR (reviewed by)
// Created     : 2026-06-17
// Modified    : 2026-06-17
// Version     : 0.1.0
// =============================================================================

"use client";

import { useState } from "react";

import { Button } from "@/components/ui/button";

type Props = {
  disabled: boolean;
  onSend: (text: string) => void;
  onRegenerate: () => void;
  onClear: () => void;
};

export function ChatInput({ disabled, onSend, onRegenerate, onClear }: Props) {
  const [text, setText] = useState("");

  const submit = () => {
    if (!text.trim()) return;
    onSend(text);
    setText("");
  };

  return (
    <div className="border-t border-zinc-200 p-4 dark:border-zinc-800">
      <div className="mb-2 flex gap-2">
        <Button type="button" variant="outline" size="sm" onClick={onRegenerate} disabled={disabled}>
          Regenerate
        </Button>
        <Button type="button" variant="outline" size="sm" onClick={onClear} disabled={disabled}>
          Clear
        </Button>
      </div>
      <div className="flex gap-2">
        <textarea
          className="min-h-[44px] flex-1 resize-none rounded-md border border-zinc-300 bg-white px-3 py-2 text-sm dark:border-zinc-700 dark:bg-zinc-950"
          placeholder="Type a message…"
          value={text}
          disabled={disabled}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              submit();
            }
          }}
        />
        <Button type="button" onClick={submit} disabled={disabled || !text.trim()}>
          Send
        </Button>
      </div>
    </div>
  );
}
