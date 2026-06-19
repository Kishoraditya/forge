// =============================================================================
// forge / frontend / app / admin / byok / page
// =============================================================================
// Description : Admin BYOK provider key and model alias configuration UI.
// Layer       : Infra
// Feature     : F002 — BYOK Configuration System
// Author      : cursor + KSR (reviewed by)
// Created     : 2026-06-17
// Modified    : 2026-06-17
// Version     : 0.1.0
// =============================================================================

"use client";

import { useEffect, useState } from "react";

import { Button } from "@/components/ui/button";

type ProviderKey = { provider: string; is_active: boolean };
type ModelAlias = { alias: string; provider: string; model_name: string; is_default: boolean };

export default function AdminByokPage() {
  const [keys, setKeys] = useState<ProviderKey[]>([]);
  const [aliases, setAliases] = useState<ModelAlias[]>([]);
  const [provider, setProvider] = useState("openrouter");
  const [apiKey, setApiKey] = useState("");
  const [error, setError] = useState<string | null>(null);

  const reload = async () => {
    const [keysRes, aliasRes] = await Promise.all([
      fetch("/api/admin/byok/keys"),
      fetch("/api/admin/byok/aliases"),
    ]);
    if (keysRes.ok) setKeys((await keysRes.json()) as ProviderKey[]);
    if (aliasRes.ok) setAliases((await aliasRes.json()) as ModelAlias[]);
  };

  useEffect(() => {
    let cancelled = false;
    void (async () => {
      const [keysRes, aliasRes] = await Promise.all([
        fetch("/api/admin/byok/keys"),
        fetch("/api/admin/byok/aliases"),
      ]);
      if (cancelled) return;
      if (keysRes.ok) setKeys((await keysRes.json()) as ProviderKey[]);
      if (aliasRes.ok) setAliases((await aliasRes.json()) as ModelAlias[]);
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  const saveKey = async () => {
    setError(null);
    const res = await fetch("/api/admin/byok/keys", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ provider, api_key: apiKey }),
    });
    if (!res.ok) {
      setError(`Save failed (${res.status})`);
      return;
    }
    setApiKey("");
    await reload();
  };

  return (
    <div className="mx-auto max-w-2xl space-y-8">
      <h1 className="text-2xl font-semibold">BYOK configuration</h1>
      <section className="space-y-3">
        <h2 className="text-lg font-medium">Provider keys</h2>
        <div className="grid gap-2 sm:grid-cols-2">
          <input
            className="rounded-md border px-3 py-2"
            value={provider}
            onChange={(e) => setProvider(e.target.value)}
            placeholder="provider"
          />
          <input
            className="rounded-md border px-3 py-2"
            type="password"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            placeholder="API key"
          />
        </div>
        <Button type="button" onClick={() => void saveKey()}>
          Validate & save
        </Button>
        <ul className="text-sm text-zinc-600">
          {keys.map((key) => (
            <li key={key.provider}>
              {key.provider} — {key.is_active ? "active" : "inactive"}
            </li>
          ))}
        </ul>
      </section>
      <section className="space-y-2">
        <h2 className="text-lg font-medium">Model aliases</h2>
        <ul className="text-sm">
          {aliases.map((alias) => (
            <li key={alias.alias}>
              {alias.alias} → {alias.provider}/{alias.model_name}
            </li>
          ))}
          {aliases.length === 0 && <li className="text-zinc-500">No custom aliases yet.</li>}
        </ul>
      </section>
      {error && <p className="text-sm text-red-600">{error}</p>}
    </div>
  );
}
