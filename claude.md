# TOM Demand Management System

Demand prioritization system for CTT (Portuguese Post). Python 3.9+, CLI-first, with a FastAPI REST layer and early-stage React frontend.

## CRITICAL: European CSV Format

All CSV files use **semicolon (`;`) delimiter**, comma decimal (`0,088`), dot thousands (`1.000,45`).
Configured in `config/config.yaml`. See `docs/EUROPEAN_FORMAT.md`.

**Never use comma as delimiter. Never switch to US format.**

## Architecture

- `tom_demand.py` — CLI entry point (adds `src/` to path)
- `src/algorithms/` — Sainte-Laguë, D'Hondt, WSJF implementations
- `src/api/` — FastAPI layer; auth **disabled by default** (`AUTH_ENABLED=true` to enable)
- `src/services/` — orchestration pipeline used by both CLI and API
- `src/validator.py`, `src/loader.py`, `src/prioritizer.py`, `src/exporter.py` — core pipeline
- `config/config.yaml` — all configuration (Revenue Streams, defaults, format settings)

## Queue-Based Prioritization

IDEAs ranked within sequential queues determined by `MicroPhase`:

1. **NOW** (active development) → ranks 1–N
2. **NEXT** (ready for development) → ranks N+1–M
3. **LATER** (planning phases) → ranks M+1–P
4. **PRODUCTION** (deployed) → no rank

Per-queue method flags: `--now-method`, `--next-method`, `--later-method`.
**Cannot be combined with `--all-methods`** (raises UsageError).

## Domain Glossary

- **IDEA**: demand item to prioritize
- **RA**: Requesting Area (submitting department)
- **RS**: Revenue Stream (business area)
- **BG**: Budget Group
- **WSJF**: (Value + Urgency + Risk Reduction) / Job Size

## Known Behaviors

- `PriorityRA == 999`: IDEA silently excluded (disabled marker) — intentional, not configurable
- `Weight == 999` in `weights_ra.csv`: entire RA and its IDEAs excluded with a warning
- Ideas files follow `ideas<YYYYMM>.csv` naming — always passed explicitly, never hardcoded
- Modules use `try/except` import fallbacks for CLI vs API invocation — don't restructure imports without testing both modes
- Output uses `print()` throughout — intentional for CLI UX, do not replace with logging

## Commands

```bash
# Validate
python3 tom_demand.py validate \
  --ideas data/input/ideas202602.csv \
  --ra-weights data/input/weights_ra.csv \
  --rs-weights data/input/weights_rs.csv

# Prioritize (all methods)
python3 tom_demand.py prioritize \
  --ideas data/input/ideas202602.csv \
  --ra-weights data/input/weights_ra.csv \
  --rs-weights data/input/weights_rs.csv \
  --all-methods --output-dir data/output

# API tests
pytest tests/
```
