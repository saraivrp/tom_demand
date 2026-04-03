# Development Guide

## Setup

```bash
git clone <repo>
cd tom_demand
pip install -r requirements.txt
```

### Dependency overview

| Group | Packages |
|-------|----------|
| Core | `pandas`, `numpy`, `pyyaml`, `click`, `colorama`, `tqdm` |
| API | `fastapi`, `uvicorn`, `python-multipart` |
| Dev | `pytest`, `pytest-cov`, `pytest-mock`, `black`, `flake8`, `mypy` |

See [requirements.txt](../../requirements.txt) for pinned versions.

---

## Running the System

### CLI

```bash
python3 tom_demand.py --help
python3 tom_demand.py validate --help
python3 tom_demand.py prioritize --help
```

### API

```bash
uvicorn src.api.main:app --reload
# Interactive docs: http://127.0.0.1:8000/docs
```

### Frontend

```bash
cd frontend
npm install
npm run dev
# Available at: http://localhost:5173
```

### Docker Compose (API + Frontend)

```bash
docker compose up --build
```

---

## Testing

```bash
# API integration tests
pytest tests/

# With coverage
pytest --cov=src tests/

# Smoke test — validate with sample data
python3 tom_demand.py validate \
  --ideas data/input/ideas202602.csv \
  --ra-weights data/input/weights_ra.csv \
  --rs-weights data/input/weights_rs.csv \
  --bg-rs-weights data/input/weights_bg_rs.csv

# Smoke test — full prioritization
python3 tom_demand.py prioritize \
  --ideas data/input/ideas202602.csv \
  --ra-weights data/input/weights_ra.csv \
  --rs-weights data/input/weights_rs.csv \
  --bg-rs-weights data/input/weights_bg_rs.csv \
  --all-methods \
  --output-dir data/output
```

---

## Code Style

```bash
black src/
flake8 src/
mypy src/
```

Conventions:
- Python 3.9+
- `snake_case` for functions/variables
- `PascalCase` for classes
- `UPPER_SNAKE_CASE` for constants
- Type hints on all functions
- Follow existing docstring patterns
- Line length: readable (no strict limit)

---

## Common Tasks

### Adding a validation rule

1. Edit `src/validator.py`
2. Add to the appropriate method
3. Provide a clear, actionable error message
4. Test: `python3 tom_demand.py validate --ideas data/input/ideas202602.csv ...`

### Adding a new algorithm

1. Create `src/algorithms/<name>.py` — implement the same interface as existing algorithms
2. Register in `src/prioritizer.py`
3. Add CLI option in `src/cli.py`
4. Test with `--method <name>` and verify `--all-methods` still works

### Modifying CSV output

1. Edit `src/exporter.py`
2. Maintain European format: `sep=';', decimal=','`
3. Verify with a full prioritization run

### Changing configuration

1. Edit `config/config.yaml`
2. Update `src/loader.py` or `src/validator.py` if the structure changes
3. Test with validate command

---

## Architecture Notes

- **Both CLI and API use the same `DemandService`** — if you change the service layer, test both interfaces.
- **Import path fallback**: modules use `try/except` imports to work in both `python3 tom_demand.py` (CLI) and `from src.xxx import ...` (API). Do not restructure imports without testing both modes.
- **`print()` is intentional** — CLI output uses `print()` for UX. Do not replace with logging silently.
- **`data/input/*.csv` is the system of record** — no database.
- **`PriorityRA == 999`** — IDEAs with this value are silently excluded (disabled flag).
- **`Weight == 999`** — RAs with this weight are excluded entirely; their IDEAs are skipped with a warning.

---

## Environment Variables (API)

| Variable | Default | Description |
|----------|---------|-------------|
| `AUTH_ENABLED` | `false` | Enable API key + role authentication |
| `API_KEY` | — | Required when `AUTH_ENABLED=true` |
| `AUDIT_LOG_PATH` | `data/output/api_audit.jsonl` | Audit log location |

---

## Questions to Ask Before Making Changes

For non-trivial changes:
1. Does this affect the European CSV format?
2. Will this impact existing input files or workflows?
3. Should this be configurable via `config/config.yaml`?
4. Does this require updating documentation?
5. Should all three algorithms support this change?
