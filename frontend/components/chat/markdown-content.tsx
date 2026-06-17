// =============================================================================
// forge / frontend / components / chat / markdown-content
// =============================================================================
// Description : Safe markdown rendering for assistant messages.
// Layer       : Infra
// Feature     : F005 — Basic Conversation Interface
// Author      : cursor + KSR (reviewed by)
// Created     : 2026-06-17
// Modified    : 2026-06-17
// Version     : 0.1.0
// =============================================================================

"use client";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

type Props = { content: string };

export function MarkdownContent({ content }: Props) {
  return (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      components={{
        a: ({ href, children }) => (
          <a href={href} target="_blank" rel="noreferrer" className="text-blue-600 underline">
            {children}
          </a>
        ),
      }}
    >
      {content}
    </ReactMarkdown>
  );
}
