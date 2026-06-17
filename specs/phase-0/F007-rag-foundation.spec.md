# F007 — Basic RAG Foundation
<!-- Spec version: 1.0.0 | Author: cursor | Date: 2026-06-17 -->

## Feature Reference
- **Feature ID**: F007
- **Phase**: Phase 0
- **Depends on**: F003, F006, F008
- **Blocks**: none
- **Feature registry entry**: docs/FEATURES.md
- **Estimated tasks**: 9

## What This Does (One Paragraph)
Enables admin document upload (PDF, TXT, MD, CSV), chunks content via
RecursiveCharacterTextSplitter, embeds chunks with configurable embedding model
via LiteLLM, stores vectors in pgvector, retrieves top-k by cosine similarity,
and injects retrieved chunks into the system prompt for inference calls when RAG
is enabled for a session.

## What This Does NOT Do
- User-facing document upload
- Advanced reranking or hybrid search
- Multi-collection knowledge bases
- Automatic chunk updates on file change

## Acceptance Criteria
- [ ] AC1: Admin uploads document → stored in `documents` table
- [ ] AC2: Chunking pipeline produces sized chunks with overlap config
- [ ] AC3: Embeddings stored in `document_chunks.embedding`
- [ ] AC4: `retrieve(query, k)` returns top-k chunks by cosine similarity
- [ ] AC5: Inference prepends retrieved context to system message when `rag_enabled`
- [ ] AC6: Admin UI lists documents with delete action
- [ ] AC7: Unit tests mock embeddings; integration test with test vectors

## Data Model
**Document**: `id`, `filename`, `mime_type`, `size_bytes`, `created_at`

**DocumentChunk**: `id`, `document_id`, `content`, `embedding: vector(1536)`, `chunk_index`

**RetrievalResult**: `chunks: list[str]`, `scores: list[float]`

## Agent State Impact
`memory_refs` may list chunk IDs when RAG used (Phase 1 alignment).

## API Contract
`POST /api/admin/documents` — multipart upload → 201 `Document`
`GET /api/admin/documents` → list
`DELETE /api/admin/documents/{id}` → 204
`POST /api/admin/documents/{id}/reindex` → triggers re-embed

Internal: `RAGService.retrieve(session_id, query, k)` used by inference_service.

## Files to Create
| File | Type | Purpose |
|------|------|---------|
| `backend/app/services/rag_service.py` | New | Orchestration |
| `backend/app/services/chunking_service.py` | New | Text splitting |
| `backend/app/services/embedding_service.py` | New | LiteLLM embeddings |
| `backend/app/db/document_repository.py` | New | Document/chunk DB |
| `backend/app/api/admin_documents.py` | New | Admin routes |
| `backend/app/models/document.py` | New | Pydantic (extend ORM) |
| `backend/tests/unit/test_chunking_service.py` | New | Chunk tests |
| `backend/tests/unit/test_rag_service.py` | New | Retrieval tests |
| `frontend/app/admin/documents/page.tsx` | New | Upload UI |

## Files to Modify
| File | Change |
|------|--------|
| `backend/app/services/inference_service.py` | Optional RAG context injection |
| `backend/app/main.py` | Register documents router |

## Security & Secrets
Admin-only upload. Scan file size limits. No executable uploads.

## Dependencies
- `pypdf` or `pymupdf` — PDF text extraction
- Justification: required for PDF upload AC

## Test Cases
### Happy Path
- Upload TXT → chunks created → retrieve returns relevant chunk

### Edge Cases
- Empty file → validation error
- k > chunk count → returns all

### Should Not Happen
- Public user uploading documents

## Manual Test Flow
1. Admin uploads README.md
2. Ask chat question about README content
3. Answer references uploaded content

## Phase/Feature Exit Signal
Retrieval integration test passes; manual RAG question succeeds.

## Notes & Assumptions
- Default embedding: OpenAI text-embedding-3-small via LiteLLM
- PDF parser choice finalized in P0-F007-002 task
