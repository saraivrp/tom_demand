# TOM Demand Management System

A demand prioritization system for CTT (Portuguese Post) based on three proportional allocation methods: **Sainte-Laguë** (default), **D'Hondt**, and **WSJF** (Weighted Shortest Job First).

## Overview

This system implements a multi-level prioritization framework that aligns organizational demand with strategic priorities:

- **Level 1**: Each Requesting Area prioritizes their own IDEAs
- **Level 2A**: IDEAs are prioritized by Requesting Area within each Revenue Stream
- **Level 2B**: IDEAs are reprioritized by Budget Group within each Revenue Stream
- **Level 3**: Global prioritization across all Revenue Streams using RS weights

## Features

✓ **Multi-level prioritization** (Requesting Area → Budget Group → Revenue Stream → Global)
✓ **Three allocation algorithms** with different characteristics
✓ **Per-queue prioritization methods** - different methods for NOW, NEXT, LATER queues
✓ **CSV-based input/output** for easy integration
✓ **European format support** (semicolon delimiter, comma decimal separator)
✓ **Metric system** and EU standards compliance
✓ **Automated weight normalization**
✓ **Comprehensive validation engine**
✓ **Audit trail and logging**
✓ **Method comparison reports**

## Prioritization Methods

### 1. Sainte-Laguë (Default)
Balanced allocation using odd divisors. Best for fair representation across all areas.

### 2. D'Hondt
Strategic focus using natural divisors. Best for reinforcing key initiatives.

### 3. WSJF (Weighted Shortest Job First)
Economic value optimization. Best for maximizing ROI.

## European Format (Iberia/EU Standards)

This system uses European notation for CSV files and numbers:

- **CSV Delimiter**: Semicolon (`;`) instead of comma
- **Decimal Separator**: Comma (`,`) e.g., `0,088`
- **Thousands Separator**: Dot (`.`) e.g., `1.000,45`

**Example CSV format**:
```csv
ID;Name;RevenueStream;WSJF_Score
IDEA001;New eCommerce Portal;eCommerce;0,088
```

The European format is configured in [config/config.yaml](config/config.yaml) and can be modified if needed. See [docs/EUROPEAN_FORMAT.md](docs/EUROPEAN_FORMAT.md) for detailed information.

## Installation

```bash
# Clone or download the repository
cd tom_demand

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

### 1. Validate Your Input Files

> **Note**: Ideas files follow the naming convention `ideas<YYYYMM>.csv` (e.g., `ideas202602.csv`).

```bash
python3 tom_demand.py validate \
  --ideas data/input/ideas202602.csv \
  --ra-weights data/input/weights_ra.csv \
  --rs-weights data/input/weights_rs.csv \
  --bg-rs-weights data/input/weights_bg_rs.csv

# With custom configuration file
python3 tom_demand.py validate \
  --ideas data/input/ideas202602.csv \
  --ra-weights data/input/weights_ra.csv \
  --rs-weights data/input/weights_rs.csv \
  --bg-rs-weights data/input/weights_bg_rs.csv \
  --config path/to/custom_config.yaml
```

### 2. Run Prioritization

```bash
# Run with default method (Sainte-Laguë)
python3 tom_demand.py prioritize \
  --ideas data/input/ideas202602.csv \
  --ra-weights data/input/weights_ra.csv \
  --rs-weights data/input/weights_rs.csv \
  --bg-rs-weights data/input/weights_bg_rs.csv \
  --output-dir data/output

# Run all three methods
python3 tom_demand.py prioritize \
  --ideas data/input/ideas202602.csv \
  --ra-weights data/input/weights_ra.csv \
  --rs-weights data/input/weights_rs.csv \
  --bg-rs-weights data/input/weights_bg_rs.csv \
  --all-methods \
  --output-dir data/output

# Use different methods per queue (v3.3+)
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

### 3. View Results

Results are saved in the output directory:
- `demand.csv` - Global prioritization (all methods combined)
- `demand_[method].csv` - Results for specific method
- `prioritization_rs_[method].csv` - Revenue Stream level results
- `metadata.json` - Execution metadata

### 4. Run API (FastAPI)

```bash
uvicorn src.api.main:app --reload
```

Base endpoints:
- `GET /api/v1/health`
- `GET /api/v1/version`
- API docs: `GET /docs`

Workflow endpoints:
- `POST /api/v1/workflows/validate`
- `POST /api/v1/workflows/prioritize`
- `POST /api/v1/workflows/prioritize-rs`
- `POST /api/v1/workflows/prioritize-global`
- `POST /api/v1/workflows/compare`

Reference data endpoints:
- `GET /api/v1/reference-data/ideas`
- `GET /api/v1/reference-data/ra-weights`
- `GET /api/v1/reference-data/rs-weights`
- `POST /api/v1/reference-data/upsert`
- `POST /api/v1/reference-data/delete`
- `POST /api/v1/reference-data/requesting-areas/list`
- `POST /api/v1/reference-data/requesting-areas/rename`
- `POST /api/v1/reference-data/revenue-streams/list`
- `POST /api/v1/reference-data/revenue-streams/rename`

Async jobs:
- `POST /api/v1/jobs/workflows/prioritize`
- `POST /api/v1/jobs/workflows/compare`
- `POST /api/v1/jobs/workflows/validate`
- `GET /api/v1/jobs`
- `GET /api/v1/jobs/{job_id}`

Security headers (when `AUTH_ENABLED=true`):
- `X-API-Key: <key>`
- `X-Role: viewer|editor|executor|admin`

### 5. Run React Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`

Environment variables (optional):
- `VITE_API_BASE_URL` (default: `http://127.0.0.1:8000`)
- `VITE_API_KEY`
- `VITE_API_ROLE` (default: `admin`)

### 6. Docker Compose (API + Frontend)

```bash
docker compose up --build
```

## Project Structure

```
tom_demand/
├── tom_demand.py            # Main entry point
├── requirements.txt
├── config/
│   └── config.yaml          # Centralized configuration
├── src/
│   ├── algorithms/          # Prioritization algorithms
│   │   ├── sainte_lague.py
│   │   ├── dhondt.py
│   │   └── wsjf.py
│   ├── api/                 # FastAPI REST layer
│   │   ├── main.py
│   │   ├── auth.py
│   │   ├── audit.py
│   │   ├── jobs.py
│   │   ├── errors.py
│   │   ├── routers/         # Endpoint groups
│   │   └── models/          # Pydantic schemas
│   ├── services/            # Service orchestration
│   │   ├── demand_service.py
│   │   └── reference_data_service.py
│   ├── loader.py            # Data loading
│   ├── validator.py         # Data validation
│   ├── prioritizer.py       # Main prioritization logic
│   ├── exporter.py          # Result export
│   ├── cli.py               # Command-line interface
│   └── utils.py             # Shared utilities
├── frontend/                # React 19 + Vite SPA
├── tests/
│   └── test_api_endpoints.py
├── data/
│   ├── input/               # Input files (ideas<YYYYMM>.csv, weights_*.csv)
│   └── output/              # Generated results
└── docs/
```

## Documentation

- [USAGE_GUIDE.md](USAGE_GUIDE.md) - Detailed usage instructions
- [docs/TOM Demand Management System - Functional Specification.md](docs/TOM%20Demand%20Management%20System%20-%20Functional%20Specification.md) - Complete specification
- [docs/PROJECT_SUMMARY.md](docs/PROJECT_SUMMARY.md) - Implementation status and features
- [docs/EUROPEAN_FORMAT.md](docs/EUROPEAN_FORMAT.md) - European format details
- [docs/RUNBOOK.md](docs/RUNBOOK.md) - API/web operations runbook

## Example Output

```
============================================================
TOM Demand Management System - Prioritization
============================================================

Loading input files...
  ✓ 20 IDEAs loaded successfully
  ✓ 30 Requesting Area weights loaded
  ✓ 42 Budget Group by Revenue Stream weights loaded
  ✓ 7 Revenue Stream weights loaded

Summary:
  - Total IDEAs: 20
  - Requesting Areas: 13
  - Revenue Streams: 7

Starting prioritization process...
  → Executing all methods (Sainte-Laguë, D'Hondt, WSJF)
  ✓ Sainte Lague: 20 IDEAs prioritized
  ✓ Dhondt: 20 IDEAs prioritized
  ✓ Wsjf: 20 IDEAs prioritized

✓ Prioritization complete

Execution time: 0.04 seconds
============================================================
```

## Requirements

- Python 3.9+
- pandas, numpy, pyyaml, click
- fastapi, uvicorn, python-multipart (for API)
- colorama, tqdm (for CLI UX)
- pytest, black, flake8, mypy (for development)

See [requirements.txt](requirements.txt) for pinned versions.

## License

Copyright © 2026 CTT - Correios de Portugal

## Version

Version 3.3.0 - February 2026

**Latest Updates**:
- **v3.3**: Per-queue prioritization methods - configure different algorithms (WSJF, Sainte-Laguë, D'Hondt) for each queue via CLI flags (`--now-method`, `--next-method`, `--later-method`)
- **v3.2**: Three-queue prioritization system (NOW → NEXT → LATER → PRODUCTION) separates execution-ready items from planning work for better resource allocation
