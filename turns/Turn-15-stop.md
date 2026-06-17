# Turn 15 — Stop

## Fix
- `scripts/with-root-env.mjs` loads root `.env.local` into process.env before Next starts
- Maps SUPABASE_* → NEXT_PUBLIC_* for client bundle inlining
- `npm run dev` / `npm run build` use the wrapper script
- Admin login shows config hint instead of throw on submit
