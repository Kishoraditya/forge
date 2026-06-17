# Turn 13 — Start

## Goal
Fix frontend missing Supabase env when vars are only in root `.env.local`.

## Changes
- `frontend/next.config.ts`: load root `.env.local`, map SUPABASE_* → NEXT_PUBLIC_*
- `frontend/lib/supabase/env.ts`: shared public env getter
- Harden SSE JSON.parse in chat-client
- Friendly admin page when env missing

## Test plan
- `cd frontend && npm run build`
