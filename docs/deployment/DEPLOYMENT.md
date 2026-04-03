# Deployment Guide

## Local Development

### API

```bash
pip install -r requirements.txt
uvicorn src.api.main:app --reload
# Available at: http://127.0.0.1:8000
# Docs: http://127.0.0.1:8000/docs
```

### Frontend

```bash
cd frontend
npm install
npm run dev
# Available at: http://localhost:5173
```

### Frontend Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `VITE_API_BASE_URL` | `http://127.0.0.1:8000` | API base URL |
| `VITE_API_KEY` | — | API key (if auth enabled) |
| `VITE_API_ROLE` | `admin` | Role for API requests |

---

## Docker Compose (API + Frontend)

```bash
docker compose up --build
```

This starts both the API and the frontend together. Use `docker compose down` to stop.

---

## Environment Variables (API)

| Variable | Default | Description |
|----------|---------|-------------|
| `AUTH_ENABLED` | `false` | Enable API key + role-based auth |
| `API_KEY` | — | Required when `AUTH_ENABLED=true` |
| `AUDIT_LOG_PATH` | `data/output/api_audit.jsonl` | Audit log path |

### Role Model

When `AUTH_ENABLED=true`, clients must pass `X-API-Key` and `X-Role` headers:

| Role | Permissions |
|------|-------------|
| `viewer` | Read-only, validate, list jobs |
| `editor` | Reference data writes |
| `executor` | Prioritization and compare |
| `admin` | All operations |

---

## Key Operational Endpoints

| Endpoint | Purpose |
|----------|---------|
| `GET /api/v1/health` | Liveness check |
| `GET /api/v1/version` | Version info |
| `GET /api/v1/jobs` | List jobs |
| `GET /api/v1/jobs/{job_id}` | Job status and result |

---

## Backup

Back up before bulk changes or after each prioritization cycle:

- `data/input/*.csv` — source of truth (IDEAS and weights)
- `data/output/*.csv` — generated results
- `data/output/api_audit.jsonl` — audit log

---

## Incident Checklist

1. Check `GET /api/v1/health` — confirm API is running.
2. Review audit log at `AUDIT_LOG_PATH` for recent errors.
3. Inspect failed jobs: `GET /api/v1/jobs` — filter by `status=failed`, check `error` and `traceback` fields.
4. Re-run the workload via the job endpoints.
5. If CSV corruption is suspected, restore from backup and re-run prioritization.

---

## CLI-only Deployment

The system runs fully without the API or frontend. For CLI-only use:

```bash
pip install -r requirements.txt

python3 tom_demand.py prioritize \
  --ideas data/input/ideas202602.csv \
  --ra-weights data/input/weights_ra.csv \
  --rs-weights data/input/weights_rs.csv \
  --bg-rs-weights data/input/weights_bg_rs.csv \
  --all-methods \
  --output-dir data/output
```

For Windows users, a standalone `.exe` is available — see [EXEMPLOS_USO.md](../../EXEMPLOS_USO.md) for Windows-specific examples.
