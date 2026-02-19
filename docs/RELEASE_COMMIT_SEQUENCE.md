# Suggested Release Commit Sequence

Use this sequence to create clean, reviewable commits.

## 1) Core Refactor + API foundation (D0-D2)

```bash
git add src/services src/cli.py src/api/main.py src/api/errors.py src/api/models/common.py src/api/models/workflows.py src/api/routers/system.py src/api/routers/workflows.py src/api/__init__.py src/api/models/__init__.py src/api/routers/__init__.py src/__init__.py src/prioritizer.py requirements.txt README.md
git commit -m "refactor: add shared service layer and workflow FastAPI endpoints"
```

## 2) Reference Data + Async Jobs (D3-D4)

```bash
git add src/services/reference_data_service.py src/api/models/reference_data.py src/api/models/jobs.py src/api/jobs.py src/api/routers/reference_data.py src/api/routers/jobs.py src/api/main.py
git commit -m "feat(api): add CSV reference-data APIs and async jobs endpoints"
```

## 3) Security + Audit + Deployment (D7)

```bash
git add src/api/auth.py src/api/config.py src/api/audit.py Dockerfile.api docker-compose.yml
git commit -m "feat(security): add api-key auth, roles, audit logging, and docker deployment"
```

## 4) Tests + Runbook + Planning artifacts (D8)

```bash
git add tests/test_api_endpoints.py docs/RUNBOOK.md docs/RELEASE_COMMIT_SEQUENCE.md PLAN.md
git commit -m "test(docs): add API integration tests and operational runbook"
```

## Optional: workspace file

Only include if you want to share IDE config:

```bash
git add tom_demand.code-workspace
git commit -m "chore: add workspace configuration"
```
