// =============================================================================
// forge / frontend / app / global-error
// =============================================================================
// Description : Root error boundary for uncaught client/runtime failures.
// Layer       : Infra
// Feature     : F005 — Basic Conversation Interface
// Author      : cursor + KSR (reviewed by)
// Created     : 2026-06-17
// Modified    : 2026-06-17
// Version     : 0.1.0
// =============================================================================

"use client";

type GlobalErrorProps = {
  error: Error & { digest?: string };
  reset: () => void;
};

/**
 * Render a minimal fallback when the app shell fails outside route error boundaries.
 */
export default function GlobalError({ error, reset }: GlobalErrorProps) {
  return (
    <html lang="en">
      <body className="flex min-h-screen flex-col items-center justify-center gap-4 p-8">
        <h2 className="text-lg font-semibold">Something went wrong</h2>
        <p className="max-w-md text-center text-sm text-zinc-600">{error.message}</p>
        <button
          type="button"
          className="rounded-md border border-zinc-300 px-4 py-2 text-sm"
          onClick={() => reset()}
        >
          Try again
        </button>
      </body>
    </html>
  );
}
