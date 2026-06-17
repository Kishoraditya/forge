# Turn 14 — Start

## Goal
Fix Turbopack global-error React Client Manifest error on GET /.

## Root cause
`turbopack.root` in next.config.ts broke module resolution; stale `.next` from HMR made it worse.

## Fix
- Remove turbopack.root
- Delete empty root package-lock.json
- Add app/global-error.tsx
- Dev script: next dev --webpack
