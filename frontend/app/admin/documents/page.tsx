// =============================================================================
// forge / frontend / app / admin / documents / page
// =============================================================================
// Description : Admin document upload and management for RAG knowledge base.
// Layer       : Infra
// Feature     : F007 — Basic RAG Foundation
// Author      : cursor + KSR (reviewed by)
// Created     : 2026-06-17
// Modified    : 2026-06-17
// Version     : 0.1.0
// =============================================================================

"use client";

import { useEffect, useState } from "react";

import { Button } from "@/components/ui/button";

type DocumentRecord = {
  id: string;
  filename: string;
  mime_type: string;
  size_bytes: number;
  created_at: string;
};

export default function AdminDocumentsPage() {
  const [documents, setDocuments] = useState<DocumentRecord[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);

  const reload = async () => {
    const res = await fetch("/api/admin/documents");
    if (!res.ok) {
      setError(`Failed to load documents (${res.status})`);
      return;
    }
    setDocuments((await res.json()) as DocumentRecord[]);
  };

  useEffect(() => {
    let cancelled = false;
    void (async () => {
      const res = await fetch("/api/admin/documents");
      if (!res.ok) {
        if (!cancelled) setError(`Failed to load documents (${res.status})`);
        return;
      }
      if (!cancelled) setDocuments((await res.json()) as DocumentRecord[]);
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  const upload = async (file: File | null) => {
    if (!file) return;
    setUploading(true);
    setError(null);
    const body = new FormData();
    body.append("file", file);
    const res = await fetch("/api/admin/documents", { method: "POST", body });
    setUploading(false);
    if (!res.ok) {
      setError(`Upload failed (${res.status})`);
      return;
    }
    await reload();
  };

  const remove = async (id: string) => {
    const res = await fetch(`/api/admin/documents/${id}`, { method: "DELETE" });
    if (!res.ok) {
      setError(`Delete failed (${res.status})`);
      return;
    }
    await reload();
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold">Knowledge documents</h1>
      <p className="text-sm text-zinc-600">Upload PDF, TXT, MD, or CSV files for RAG context.</p>
      <div>
        <input
          type="file"
          accept=".pdf,.txt,.md,.csv,text/plain,text/markdown,text/csv,application/pdf"
          onChange={(e) => void upload(e.target.files?.[0] ?? null)}
          disabled={uploading}
        />
      </div>
      {error && <p className="text-sm text-red-600">{error}</p>}
      <ul className="divide-y rounded-md border">
        {documents.map((doc) => (
          <li key={doc.id} className="flex items-center justify-between gap-4 p-3 text-sm">
            <div>
              <p className="font-medium">{doc.filename}</p>
              <p className="text-zinc-500">
                {doc.mime_type} · {doc.size_bytes} bytes
              </p>
            </div>
            <Button type="button" variant="outline" onClick={() => void remove(doc.id)}>
              Delete
            </Button>
          </li>
        ))}
        {documents.length === 0 && (
          <li className="p-3 text-sm text-zinc-500">No documents uploaded yet.</li>
        )}
      </ul>
    </div>
  );
}
