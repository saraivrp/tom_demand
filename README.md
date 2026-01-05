# TOM Demand Management System

A demand prioritization system for CTT (Portuguese Post) based on three proportional allocation methods: **Sainte-Laguë** (default), **D'Hondt**, and **WSJF** (Weighted Shortest Job First).

## Overview

This system implements a multi-level prioritization framework that aligns organizational demand with strategic priorities:

- **Level 1**: Each Requesting Area prioritizes their own IDEAs
- **Level 2**: IDEAs are prioritized within each Revenue Stream using RA weights
- **Level 3**: Global prioritization across all Revenue Streams using RS weights

## Features

✓ **Multi-level prioritization** (Requesting Area → Revenue Stream → Global)
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

```bash
python3 tom_demand.py validate \
  --ideas data/input/ideias.csv \
  --ra-weights data/input/weights_ra.csv \
  --rs-weights data/input/weights_rs.csv
```

### 2. Run Prioritization

```bash
# Run with default method (Sainte-Laguë)
python3 tom_demand.py prioritize \
  --ideas data/input/ideias.csv \
  --ra-weights data/input/weights_ra.csv \
  --rs-weights data/input/weights_rs.csv \
  --output-dir data/output

# Run all three methods
python3 tom_demand.py prioritize \
  --ideas data/input/ideias.csv \
  --ra-weights data/input/weights_ra.csv \
  --rs-weights data/input/weights_rs.csv \
  --all-methods \
  --output-dir data/output

# Use different methods per queue (v3.3+)
python3 tom_demand.py prioritize \
  --ideas data/input/ideias.csv \
  --ra-weights data/input/weights_ra.csv \
  --rs-weights data/input/weights_rs.csv \
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

## Project Structure

```
tom_demand/
├── src/
│   ├── algorithms/          # Prioritization algorithms
│   │   ├── sainte_lague.py
│   │   ├── dhondt.py
│   │   └── wsjf.py
│   ├── loader.py            # Data loading
│   ├── validator.py         # Data validation
│   ├── prioritizer.py       # Main prioritization logic
│   ├── exporter.py          # Result export
│   └── cli.py               # Command-line interface
├── config/
│   └── config.yaml          # Configuration
├── data/
│   ├── input/               # Example input files
│   └── output/              # Generated results
├── tom_demand.py            # Main entry point
└── README.md
```

## Documentation

- [USAGE_GUIDE.md](USAGE_GUIDE.md) - Detailed usage instructions
- [docs/TOM Demand Management System - Functional Specification.md](docs/TOM%20Demand%20Management%20System%20-%20Functional%20Specification.md) - Complete specification
- [docs/PROJECT_SUMMARY.md](docs/PROJECT_SUMMARY.md) - Implementation status and features
- [docs/EUROPEAN_FORMAT.md](docs/EUROPEAN_FORMAT.md) - European format details

## Example Output

```
============================================================
TOM Demand Management System - Prioritization
============================================================

Loading input files...
  ✓ 20 IDEAs loaded successfully
  ✓ 30 Requesting Area weights loaded
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
- pandas >= 1.3.0
- numpy >= 1.21.0
- pyyaml >= 5.4.0
- click >= 8.0.0

## License

Copyright © 2026 CTT - Correios de Portugal

## Version

Version 3.3.0 - January 2026

**Latest Updates**:
- **v3.3**: Per-queue prioritization methods - configure different algorithms (WSJF, Sainte-Laguë, D'Hondt) for each queue via CLI flags (`--now-method`, `--next-method`, `--later-method`)
- **v3.2**: Three-queue prioritization system (NOW → NEXT → LATER → PRODUCTION) separates execution-ready items from planning work for better resource allocation
