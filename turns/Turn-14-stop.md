# Turn 14 — Stop

## Done
- Removed `turbopack.root` from next.config.ts (caused `[project]/frontend/node_modules/...` manifest paths)
- Deleted empty repo-root `package-lock.json` (duplicate workspace root warning)
- Added `app/global-error.tsx` for proper error boundary
- `npm run dev` now uses `--webpack` (avoids Turbopack HMR manifest bugs on Next 16)
- Verified GET / and GET /admin return 200; build passes

## User action
Stop any old dev server, then:
```powershell
cd c:\q\forge\frontend
Remove-Item -Recurse -Force .next -ErrorAction SilentlyContinue
npm run dev
```
