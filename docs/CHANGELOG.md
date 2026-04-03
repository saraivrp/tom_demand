# Changelog

## v3.3.0 — January 5, 2026

### New Feature: Per-Queue Prioritization Methods

Apply different algorithms (Sainte-Laguë, D'Hondt, WSJF) to each queue (NOW, NEXT, LATER) independently.

#### CLI flags

```bash
--now-method [sainte-lague|dhondt|wsjf]
--next-method [sainte-lague|dhondt|wsjf]
--later-method [sainte-lague|dhondt|wsjf]
```

#### Example

```bash
python3 tom_demand.py prioritize \
  --ideas data/input/ideas202602.csv \
  --ra-weights data/input/weights_ra.csv \
  --rs-weights data/input/weights_rs.csv \
  --bg-rs-weights data/input/weights_bg_rs.csv \
  --now-method wsjf \
  --next-method wsjf \
  --later-method sainte-lague \
  --output-dir data/output
```

#### Precedence rules

1. Per-queue flags (highest priority)
2. Global `--method` flag
3. Default `sainte-lague` (lowest priority)

#### Output changes

- Per-queue results use `mixed` naming: `demand_mixed.csv`, `prioritization_rs_mixed.csv`
- Method column shows the actual algorithm used per IDEA
- `metadata.json` includes new `queue_methods` and `default_method` fields

#### Constraint

Per-queue flags cannot be combined with `--all-methods` (raises UsageError).

#### Modified files

- `src/prioritizer.py` — queue method resolution and dispatch
- `src/cli.py` — new flags and validation

### Also in v3.3: API + Service Layer

- FastAPI REST layer (`src/api/`) with workflow, reference data, and async job endpoints
- Shared `DemandService` pipeline used by both CLI and API
- Role-based access control (viewer / editor / executor / admin)
- Audit logging to `data/output/api_audit.jsonl`
- Docker Compose for API + Frontend deployment
- React 19 + Vite frontend (early stage)

---

## v3.2.0 — January 5, 2026

### New Feature: Queue-Based Sequential Ranking

IDEAs are assigned to queues based on `MicroPhase` and ranked sequentially:

| Queue | MicroPhases | Ranks |
|-------|-------------|-------|
| NOW | In Development, Ready for Acceptance, In Acceptance, Selected for Production | 1–N |
| NEXT | Ready for Development | N+1–M |
| LATER | Backlog, In Definition, Pitch, Ready for Solution, High Level Design, Ready for Approval, In Approval | M+1–P |
| PRODUCTION | In Rollout, In Production | None |

This ensures active development work is always ranked before execution-ready items, which rank before planning work.

---

## v3.0.0 — January 2026

Initial production release.

- Three prioritization algorithms: Sainte-Laguë, D'Hondt, WSJF
- Multi-level prioritization: Level 1 (RA) → Level 2 (RS) → Level 3 (Global)
- CSV-based input/output with European format
- Comprehensive validation engine
- Method comparison reports
- CLI with 5 commands
- Configuration via `config/config.yaml`
