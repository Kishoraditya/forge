# Manual Testing Protocols

## Overview
This document contains step-by-step manual test flows for each feature. Add a new section when a feature ships.

## Prerequisites
- Backend running on :8000 (`make dev`)
- Frontend running on :3000 (`make dev`)
- All services healthy (check Docker logs)

## The Two-Terminal Workflow
- Terminal 1: `make dev` (all services running, logs visible)
- Terminal 2: your commands, curl calls, database checks
- Browser: http://localhost:3000

---

## Phase 0 — Core Engine

### F001 — Project Scaffolding & Monorepo
<!-- Add test flows when feature ships -->

### F002 — BYOK Configuration System
<!-- Add test flows when feature ships -->

### F003 — LLM Routing & Inference Core
<!-- Add test flows when feature ships -->

### F004 — Session Management
<!-- Add test flows when feature ships -->

### F005 — Basic Conversation Interface
<!-- Add test flows when feature ships -->

### F006 — Single Admin Authentication
<!-- Add test flows when feature ships -->

### F007 — Basic RAG Foundation
<!-- Add test flows when feature ships -->

### F008 — Supabase Schema Foundation
<!-- Add test flows when feature ships -->

---

## Phase 1 — Agent Intelligence Layer

### F009 — LangGraph Conversation Graph
<!-- Add test flows when feature ships -->

### F010 — Query Breakdown & Task Decomposition
<!-- Add test flows when feature ships -->

### F011 — Human-in-Loop Approval Gate
<!-- Add test flows when feature ships -->

### F012 — Planning & Control Logic
<!-- Add test flows when feature ships -->

### F013 — Skill System
<!-- Add test flows when feature ships -->

### F014 — Personality System
<!-- Add test flows when feature ships -->

### F015 — DSPy Prompt Directory
<!-- Add test flows when feature ships -->

### F016 — MCP Tool Integration
<!-- Add test flows when feature ships -->

### F017 — Custom Python Tool Scripts
<!-- Add test flows when feature ships -->

### F018 — Sandboxed Code Execution Environment
<!-- Add test flows when feature ships -->

### F019 — Webhook & WebSocket Tool Types
<!-- Add test flows when feature ships -->

### F020 — Non-LLM Output Pipeline
<!-- Add test flows when feature ships -->

---

## Phase 2 — Observability & Control Plane

### F021 — Structured Decision Log
<!-- Add test flows when feature ships -->

### F022 — Token Budget Tracking & Enforcement
<!-- Add test flows when feature ships -->

### F023 — OpenTelemetry Tracing
<!-- Add test flows when feature ships -->

### F024 — Jaeger Trace Visualization
<!-- Add test flows when feature ships -->

### F025 — Sentry Error Tracking Integration
<!-- Add test flows when feature ships -->

### F026 — PostHog Analytics Integration
<!-- Add test flows when feature ships -->

### F027 — Admin Dashboard — Live Session View
<!-- Add test flows when feature ships -->

### F028 — Admin Dashboard — Cost & Usage Analytics
<!-- Add test flows when feature ships -->

### F029 — GrowthBook Feature Flags
<!-- Add test flows when feature ships -->

### F030 — Health Check & Readiness Probes
<!-- Add test flows when feature ships -->

---

## Phase 3 — Graph, Memory & Self-Reflection

### F031 — Neo4j Knowledge Graph Schema
<!-- Add test flows when feature ships -->

### F032 — Entity & Relationship Extraction Pipeline
<!-- Add test flows when feature ships -->

### F033 — Graph-Augmented Retrieval
<!-- Add test flows when feature ships -->

### F034 — Episodic Memory (Session Summaries)
<!-- Add test flows when feature ships -->

### F035 — Semantic Memory (Cross-Session Knowledge)
<!-- Add test flows when feature ships -->

### F036 — Self-Reflection & Output Critique
<!-- Add test flows when feature ships -->

### F037 — Temporal Workflow Orchestration
<!-- Add test flows when feature ships -->

### F038 — Contradiction Detection
<!-- Add test flows when feature ships -->

### F039 — Memory Decay & Relevance Scoring
<!-- Add test flows when feature ships -->

---

## Phase 4 — Investor Demo Layer

### F040 — Demo Landing Page
<!-- Add test flows when feature ships -->

### F041 — Guided Demo Flow (Scripted Walkthrough)
<!-- Add test flows when feature ships -->

### F042 — Real-Time Graph Visualization
<!-- Add test flows when feature ships -->

### F043 — Decision Trace Replay
<!-- Add test flows when feature ships -->

### F044 — Multi-Provider Model Comparison View
<!-- Add test flows when feature ships -->

### F045 — One-Click Demo Reset
<!-- Add test flows when feature ships -->

---

## Phase 5 — Hardening & Scale

### F046 — Load Testing & Performance Benchmarks
<!-- Add test flows when feature ships -->

### F047 — Rate Limiting & Abuse Prevention
<!-- Add test flows when feature ships -->

### F048 — Backup & Disaster Recovery
<!-- Add test flows when feature ships -->

### F049 — CI/CD Pipeline (GitHub Actions)
<!-- Add test flows when feature ships -->

### F050 — Production Deployment Configuration
<!-- Add test flows when feature ships -->

---

## Database Check Commands
```sql
-- Supabase (via psql or dashboard SQL editor)
SELECT * FROM sessions ORDER BY created_at DESC LIMIT 5;
SELECT * FROM messages WHERE session_id = '[uuid]';
```

```cypher
-- Neo4j (via browser at localhost:7474)
MATCH (n) RETURN n LIMIT 25;
MATCH (s:Session)-[:CONTAINS]->(m:Message) RETURN s, m LIMIT 10;
```

```bash
# Redis (via redis-cli)
redis-cli keys "session:*"
redis-cli get "session:[uuid]:budget"
```
