# TOM Demand Modernization Plan

Last updated: 2026-02-18
Owner: Codex + User
Status: In progress

## Confirmed Decisions

- Data storage: Keep CSV as source of truth (initially).
- Authentication: Add after MVP.
- Frontend: React web app requested and implemented.

## Goal

Build:
- a FastAPI API layer that exposes existing CLI capabilities
- a React web frontend for all exposed API operations (CRUD, workflows, jobs)

## Deliverables and Status

- [x] D0 - Shared service layer (extract CLI orchestration into reusable services)
- [x] D1 - FastAPI skeleton (`/health`, `/version`, OpenAPI, error model)
- [x] D2 - API endpoints for existing CLI operations (`validate`, `prioritize`, `prioritize-rs`, `prioritize-global`, `compare`)
- [x] D3 - Reference data endpoints (list/upload/update/export for ideas, RA weights, RS weights, requesting areas, revenue streams)
- [x] D4 - Async jobs for long-running prioritization (submit/status/result/logs)
- [x] D5 - Frontend MVP (removed by user request)
- [x] D6 - Frontend UX hardening (removed by user request)
- [x] D7 - Security + deployment (auth/roles/audit + Dockerized deploy path)
- [x] D8 - Testing + handover docs (API tests, service tests, smoke E2E, runbook)

## Recommended Sequence

1. D0 -> D1 -> D2 -> D3
2. D4 -> D7 -> D8

## Current Sprint Focus

- [x] Start D0: create service module(s) used by both CLI and API
- [x] Ensure CLI behavior remains unchanged after refactor
- [x] Start D1: scaffold FastAPI app and base routes
- [x] Start D2: expose existing CLI operations via API routes
- [x] Start D3: reference data endpoints (CSV-backed)
- [x] Start D4: async jobs API
- [x] Start D5/D6: frontend track (later removed by user request)
- [x] Start D7: auth/roles/audit and Docker assets
- [x] Start D8: tests and runbook

## Progress Log

### 2026-02-18

- Plan created.
- Scope and architecture validated with user.
- Decisions locked:
  - CSV remains system of record
  - Auth deferred until after MVP
- Frontend app removed by user request; project currently backend-only.
- New React web frontend created by user request, replacing previous frontend track.
- D0 completed:
  - Added shared service layer in `src/services/demand_service.py`.
  - Added package export in `src/services/__init__.py`.
  - Refactored CLI commands in `src/cli.py` to use `DemandService`.
  - Ran smoke checks:
    - `python3 tom_demand.py --help`
    - `python3 tom_demand.py validate --ideas data/input/ideias.csv --ra-weights data/input/weights_ra.csv --rs-weights data/input/weights_rs.csv`
    - `python3 tom_demand.py prioritize --ideas data/input/ideias.csv --ra-weights data/input/weights_ra.csv --rs-weights data/input/weights_rs.csv --method sainte-lague --output-dir /tmp/tom_demand_out`
- D1 completed:
  - Added FastAPI app entrypoint: `src/api/main.py`.
  - Added version/health router: `src/api/routers/system.py`.
  - Added shared API models: `src/api/models/common.py`.
  - Added structured API error handlers: `src/api/errors.py`.
  - Added API dependencies to `requirements.txt` (`fastapi`, `uvicorn`).
  - Added README API run instructions.
  - Verified endpoints via TestClient:
    - `GET /api/v1/health`
    - `GET /api/v1/version`
- D2 completed:
  - Added workflow models in `src/api/models/workflows.py`.
  - Added workflow router in `src/api/routers/workflows.py`.
  - Wired workflow router in `src/api/main.py`.
  - Added package init files for API modules.
  - Improved import compatibility for CLI/API execution modes in `src/__init__.py` and `src/services/demand_service.py`.
  - Fixed comparison generation bug in `src/prioritizer.py` (`comparison_data.append(row)` was missing).
  - Added workflow endpoint list in `README.md`.
  - Verified workflow endpoints via TestClient:
    - `POST /api/v1/workflows/validate`
    - `POST /api/v1/workflows/prioritize`
    - `POST /api/v1/workflows/prioritize-rs`
    - `POST /api/v1/workflows/prioritize-global`
    - `POST /api/v1/workflows/compare`
- D3 completed:
  - Added CSV reference-data service in `src/services/reference_data_service.py`.
  - Added reference-data models and router:
    - `src/api/models/reference_data.py`
    - `src/api/routers/reference_data.py`
  - Added endpoints for listing/upsert/delete/overwrite and entity rename/list operations.
- D4 completed:
  - Added in-memory async job manager: `src/api/jobs.py`.
  - Added job models and router:
    - `src/api/models/jobs.py`
    - `src/api/routers/jobs.py`
  - Added submit/status/list job endpoints for validate, prioritize, compare.
- D5 and D6 completed:
  - Frontend track was delivered and later removed by user request.
- D7 completed:
  - Added role/API-key auth (`src/api/auth.py`, `src/api/config.py`).
  - Added audit logging middleware (`src/api/audit.py`).
  - Added deployment assets:
    - `Dockerfile.api`
    - `docker-compose.yml`
- D8 completed:
  - Added API integration tests: `tests/test_api_endpoints.py`.
  - Added operations runbook: `docs/RUNBOOK.md`.
  - Test result: `3 passed`.

## Risks and Mitigations

- Risk: drift between CLI and API logic  
  Mitigation: keep one shared service layer; CLI and API call same functions.

- Risk: long-running prioritization requests timing out  
  Mitigation: introduce async job execution in D4.

- Risk: CSV concurrency/corruption  
  Mitigation: controlled write paths, atomic writes, backup snapshots.

## Definition of Done (Project)

- Users can upload/update reference data and run prioritization through API endpoints.
- API covers all existing CLI functions.
- Outputs are consistent with current CLI behavior.
- Basic operational docs and tests are in place.

## How to Update This File

At the end of each work session:
1. Update `Last updated`.
2. Mark completed deliverables and current sprint tasks.
3. Append a short entry under `Progress Log`.
4. Add blockers/risks if discovered.
