# TOM Demand Management System

Demand prioritization system for CTT (Portuguese Post) — v3.3.0

Implements three proportional allocation algorithms (**Sainte-Laguë**, **D'Hondt**, **WSJF**) with queue-based sequential ranking across four lifecycle phases: NOW → NEXT → LATER → PRODUCTION.

## Quick Start

```bash
pip install -r requirements.txt

# Validate input files
python3 tom_demand.py validate \
  --ideas data/input/ideas202602.csv \
  --ra-weights data/input/weights_ra.csv \
  --rs-weights data/input/weights_rs.csv \
  --bg-rs-weights data/input/weights_bg_rs.csv

# Run prioritization (all methods)
python3 tom_demand.py prioritize \
  --ideas data/input/ideas202602.csv \
  --ra-weights data/input/weights_ra.csv \
  --rs-weights data/input/weights_rs.csv \
  --bg-rs-weights data/input/weights_bg_rs.csv \
  --all-methods \
  --output-dir data/output
```

## Interfaces

| Interface | Command | Purpose |
|-----------|---------|---------|
| **CLI** | `python3 tom_demand.py <command>` | Primary production use |
| **REST API** | `uvicorn src.api.main:app --reload` | Integration / programmatic access |
| **Frontend** | `cd frontend && npm run dev` | Web UI (early stage) |
| **Docker** | `docker compose up --build` | API + Frontend together |

## Modules

| Module | Purpose |
|--------|---------|
| `src/validator.py` | Data validation engine |
| `src/loader.py` | CSV ingestion with auto-queue assignment |
| `src/prioritizer.py` | Orchestration — Level 2 → Level 3 |
| `src/algorithms/` | Sainte-Laguë, D'Hondt, WSJF |
| `src/exporter.py` | Result formatting and CSV export |
| `src/cli.py` | CLI commands (validate, prioritize, compare) |
| `src/api/` | FastAPI REST layer |
| `src/services/` | Shared pipeline (CLI + API) |

## Documentation

| Document | Description |
|----------|-------------|
| [docs/guides/USER_GUIDE.md](docs/guides/USER_GUIDE.md) | CLI usage, input format, all commands |
| [docs/architecture/ARCHITECTURE.md](docs/architecture/ARCHITECTURE.md) | System architecture with diagrams |
| [docs/api/API_REFERENCE.md](docs/api/API_REFERENCE.md) | REST API endpoints and authentication |
| [docs/deployment/DEPLOYMENT.md](docs/deployment/DEPLOYMENT.md) | Deployment and operations |
| [docs/guides/DEVELOPMENT.md](docs/guides/DEVELOPMENT.md) | Developer setup, testing, contribution |
| [docs/reference/ALGORITHMS.md](docs/reference/ALGORITHMS.md) | Algorithm details and comparison |
| [docs/reference/EUROPEAN_FORMAT.md](docs/reference/EUROPEAN_FORMAT.md) | CSV format (`;` delimiter, `,` decimal) |
| [docs/CHANGELOG.md](docs/CHANGELOG.md) | Release notes |
| [EXEMPLOS_USO.md](EXEMPLOS_USO.md) | Exemplos de uso — Windows `.exe` (Português) |
| [docs/TOM Demand Management System - Functional Specification.md](docs/TOM%20Demand%20Management%20System%20-%20Functional%20Specification.md) | Complete functional specification |

## Requirements

- Python 3.9+
- See [requirements.txt](requirements.txt) for pinned versions

## License

Copyright © 2026 CTT - Correios de Portugal
