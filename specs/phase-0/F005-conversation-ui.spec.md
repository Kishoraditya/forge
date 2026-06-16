# F005 — Basic Conversation Interface
<!-- Spec version: 1.0.0 | Author: cursor | Date: 2026-06-17 -->

## Feature Reference
- **Feature ID**: F005
- **Phase**: Phase 0
- **Depends on**: F003, F004
- **Blocks**: none (Phase 0 E2E)
- **Feature registry entry**: docs/FEATURES.md
- **Estimated tasks**: 10

## What This Does (One Paragraph)
Delivers the primary chat UI: message list with user/assistant bubbles, streaming
responses via SSE, markdown rendering (code blocks, lists, tables), typing
indicator, model badge, per-message copy, timestamps, regenerate last response,
and clear conversation with confirmation.

## What This Does NOT Do
- Graph visualization (Phase 3)
- Tool call UI (Phase 1)
- WebSocket transport (SSE sufficient for Phase 0; Socket.io optional later)
- Multi-tab session sync

## Acceptance Criteria
- [ ] AC1: Chat page at `/` shows message input and history
- [ ] AC2: Submit sends user message; streams assistant reply via SSE
- [ ] AC3: Markdown rendered safely (no raw HTML injection)
- [ ] AC4: Copy button copies message text to clipboard
- [ ] AC5: Timestamps shown per message
- [ ] AC6: Regenerate resends last user turn and replaces last assistant message
- [ ] AC7: Clear conversation prompts confirm then resets UI and calls backend clear
- [ ] AC8: Model badge shows active `model_alias`
- [ ] AC9: Budget bar from F004 visible in header

## Data Model
**ConversationMessage** (frontend): `id`, `role`, `content`, `createdAt`, `modelAlias?`

Backend persists via F008 `messages` table through conversation service.

## Agent State Impact
UI reflects `messages` list; persistence via message service.

## API Contract
`POST /api/sessions/{session_id}/messages` — body: `{ "content": str }` → streams via linked inference
`GET /api/sessions/{session_id}/messages` → list messages
`DELETE /api/sessions/{session_id}/messages` → clear history
`POST /api/sessions/{session_id}/messages/regenerate` → regenerate last

## Files to Create
| File | Type | Purpose |
|------|------|---------|
| `backend/app/services/message_service.py` | New | Message CRUD |
| `backend/app/db/message_repository.py` | New | DB layer |
| `backend/app/api/messages.py` | New | Message routes |
| `backend/tests/unit/test_message_service.py` | New | Tests |
| `backend/tests/integration/test_messages_api.py` | New | API tests |
| `frontend/app/page.tsx` | Modify | Chat layout |
| `frontend/components/chat/chat-container.tsx` | New | Main chat |
| `frontend/components/chat/message-list.tsx` | New | Message list |
| `frontend/components/chat/message-bubble.tsx` | New | Single message |
| `frontend/components/chat/chat-input.tsx` | New | Input + send |
| `frontend/components/chat/markdown-content.tsx` | New | Safe markdown |
| `frontend/components/chat/budget-bar.tsx` | New | Budget display |
| `frontend/lib/api/chat-client.ts` | New | SSE client |
| `frontend/hooks/use-chat.ts` | New | Chat state hook |

## Files to Modify
| File | Change |
|------|--------|
| `backend/app/main.py` | Register messages router |
| `frontend/package.json` | Add `react-markdown`, `zustand` if needed |

## Security & Secrets
Sanitize markdown rendering. XSS prevention via react-markdown without raw HTML.

## Dependencies
- `react-markdown` — markdown rendering
- `remark-gfm` — tables/lists

## Test Cases
### Happy Path
- Send message → streamed response appears in list

### Edge Cases
- Empty submit → validation error
- Budget exceeded mid-stream → error banner

### Should Not Happen
- Script execution from assistant markdown

## Manual Test Flow
1. Open `/`, type question, submit
2. Watch streamed markdown response
3. Copy, regenerate, clear — each works

## Phase/Feature Exit Signal
Phase 0 E2E demo: anonymous user chats with live LLM.

## Notes & Assumptions
- Replace default create-next-app home page
- Developer signature headers on new TSX files per CONVENTIONS.md
