# TOM Demand API/Web Runbook

## Services

- API: FastAPI (`src.api.main:app`)
- Frontend: React + Vite (`frontend/`)

## Local Startup

1. API:
```bash
pip install -r requirements.txt
uvicorn src.api.main:app --reload
```

2. Frontend:
```bash
cd frontend
npm install
npm run dev
```

## Auth Configuration

Environment variables:
- `AUTH_ENABLED` (`true`/`false`)
- `API_KEY` (required if auth enabled)
- `AUDIT_LOG_PATH` (default: `data/output/api_audit.jsonl`)

Role model (`X-Role` header):
- `viewer`: read-only and validate/list jobs
- `editor`: reference-data write operations
- `executor`: prioritization and compare
- `admin`: reserved highest privilege

## Key Operational Endpoints

- Liveness: `GET /api/v1/health`
- Version: `GET /api/v1/version`
- Jobs list: `GET /api/v1/jobs`
- Job status: `GET /api/v1/jobs/{job_id}`

## Incident Checklist

1. Check API health endpoint.
2. Verify audit logs at `AUDIT_LOG_PATH`.
3. Inspect failed jobs (`status=failed`, `error`, `traceback`).
4. Re-run workload using job endpoints.
5. If CSV corruption suspected, restore from backup and rerun.

## Backup Guidance

- Back up:
  - `data/input/*.csv`
  - `data/output/*.csv`
  - `data/output/api_audit.jsonl`
- Recommended cadence:
  - before bulk reference-data updates
  - after each prioritization cycle
