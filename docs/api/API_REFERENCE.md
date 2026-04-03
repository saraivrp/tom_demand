# API Reference

The TOM Demand Management System exposes a FastAPI REST API that covers all CLI operations.

## Starting the API

```bash
uvicorn src.api.main:app --reload
# Base URL: http://127.0.0.1:8000
# Interactive docs: http://127.0.0.1:8000/docs
```

---

## Authentication

Authentication is **disabled by default**.

To enable:

```bash
AUTH_ENABLED=true API_KEY=<key> uvicorn src.api.main:app
```

When enabled, include these headers on every request:

```
X-API-Key: <key>
X-Role: viewer | editor | executor | admin
```

### Role Permissions

| Role | Allowed Operations |
|------|-------------------|
| `viewer` | Read-only endpoints, validate, list jobs |
| `editor` | Reference data write operations |
| `executor` | Prioritization and compare workflows |
| `admin` | All operations |

---

## System Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/health` | Liveness check |
| GET | `/api/v1/version` | Version information |

---

## Workflow Endpoints

Workflow endpoints mirror the CLI commands. They accept multipart form data with CSV file uploads.

| Method | Path | CLI equivalent | Description |
|--------|------|---------------|-------------|
| POST | `/api/v1/workflows/validate` | `validate` | Validate input files |
| POST | `/api/v1/workflows/prioritize` | `prioritize` | Full prioritization (Levels 2 + 3) |
| POST | `/api/v1/workflows/prioritize-rs` | `prioritize-rs` | Level 2 only (by Revenue Stream) |
| POST | `/api/v1/workflows/prioritize-global` | `prioritize-global` | Level 3 only (global) |
| POST | `/api/v1/workflows/compare` | `compare` | Compare all methods |

---

## Reference Data Endpoints

Manage IDEAS and weight files via the API.

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/reference-data/ideas` | List all IDEAS |
| GET | `/api/v1/reference-data/ra-weights` | List RA weights |
| GET | `/api/v1/reference-data/rs-weights` | List RS weights |
| POST | `/api/v1/reference-data/upsert` | Insert or update records |
| POST | `/api/v1/reference-data/delete` | Delete records |
| POST | `/api/v1/reference-data/requesting-areas/list` | List Requesting Areas |
| POST | `/api/v1/reference-data/requesting-areas/rename` | Rename a Requesting Area |
| POST | `/api/v1/reference-data/revenue-streams/list` | List Revenue Streams |
| POST | `/api/v1/reference-data/revenue-streams/rename` | Rename a Revenue Stream |

---

## Async Job Endpoints

For long-running operations, submit as async jobs and poll for completion.

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/jobs/workflows/prioritize` | Submit async prioritization |
| POST | `/api/v1/jobs/workflows/compare` | Submit async comparison |
| POST | `/api/v1/jobs/workflows/validate` | Submit async validation |
| GET | `/api/v1/jobs` | List all jobs |
| GET | `/api/v1/jobs/{job_id}` | Get job status, result, and logs |

### Job Status Values

| Status | Meaning |
|--------|---------|
| `pending` | Job queued, not yet started |
| `running` | Job in progress |
| `completed` | Finished successfully |
| `failed` | Finished with error — check `error` and `traceback` fields |

---

## Audit Logging

All API requests are logged to `data/output/api_audit.jsonl` (configurable via `AUDIT_LOG_PATH` env var).

Log format: JSONL, one entry per request, with timestamp, method, path, status code, and role.

---

## OpenAPI / Swagger

Full interactive documentation is available when the API is running:

```
http://127.0.0.1:8000/docs
```

This includes request/response schemas for all endpoints.
