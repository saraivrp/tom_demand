# TOM Demand Modernization Plan

Last updated: 2026-02-18
Owner: Codex + User
Status: Complete

## Goal

Build:
- a FastAPI API layer that exposes existing CLI capabilities
- a React web frontend for all exposed API operations (CRUD, workflows, jobs)

## Deliverables

- [x] D0 — Shared service layer (extract CLI orchestration into reusable services)
- [x] D1 — FastAPI skeleton (`/health`, `/version`, OpenAPI, error model)
- [x] D2 — API endpoints for existing CLI operations (validate, prioritize, prioritize-rs, prioritize-global, compare)
- [x] D3 — Reference data endpoints (list/upload/update/export for ideas, RA weights, RS weights, requesting areas, revenue streams)
- [x] D4 — Async jobs for long-running prioritization (submit/status/result/logs)
- [x] D5 — Frontend MVP (removed by user request)
- [x] D6 — Frontend UX hardening (removed by user request)
- [x] D7 — Security + deployment (auth/roles/audit + Dockerized deploy path)
- [x] D8 — Testing + handover docs (API tests, service tests, smoke E2E, runbook)

## Confirmed Decisions

- Data storage: Keep CSV as source of truth
- Authentication: Optional — disabled by default (`AUTH_ENABLED=false`)
- Frontend: React 19 + Vite SPA (early stage, created by user request)

## Risks and Mitigations

- **Drift between CLI and API logic** → one shared service layer; CLI and API call same functions
- **Long-running requests timing out** → async job execution (D4)
- **CSV concurrency/corruption** → controlled write paths, backup snapshots

## Progress Log

### 2026-02-18

- Plan created. Scope and architecture validated with user.
- D0–D8 all completed (see deliverables above).
- Frontend track was delivered and later removed by user request; replaced with new React 19 + Vite app.
