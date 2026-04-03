# User Guide

## Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Prepare Input Files

You need four CSV files (European format — semicolon delimiter, comma decimal separator).

#### ideas\<YYYYMM\>.csv

Contains the IDEAs (development requests).

```csv
ID;Name;RequestingArea;RevenueStream;BudgetGroup;MicroPhase;PriorityRA;Value;Urgency;Risk;Size
IDEA001;New eCommerce Portal;DIR_eCommerce_Commercial;eCommerce;Commercial;In Development;1;9;8;5;250
```

**Required columns:**

| Column | Description |
|--------|-------------|
| `ID` | Unique identifier |
| `Name` | IDEA name |
| `RequestingArea` | Requesting direction/department |
| `RevenueStream` | Target Revenue Stream |
| `BudgetGroup` | Associated Budget Group |
| `PriorityRA` | Priority within Requesting Area (sequential: 1, 2, 3, …) |

**Optional columns (with defaults):**

| Column | Default | Description |
|--------|---------|-------------|
| `MicroPhase` | `Backlog` | Lifecycle phase — determines Queue assignment |
| `Value` | `1` | Business value (1–10) |
| `Urgency` | `1` | Time criticality (1–10) |
| `Risk` | `1` | Risk reduction value (1–10) |
| `Size` | `100` | Estimated size in story points (> 0) |

**Valid MicroPhase values:**
Backlog, In Definition, Pitch, Ready for Solution, High Level Design, Ready for Approval, In Approval, Ready for Development, In Development, Ready for Acceptance, In Acceptance, Selected for Production, In Rollout, In Production

#### weights\_ra.csv

Weights for Requesting Areas within each Revenue Stream and Budget Group.

```csv
RevenueStream;BudgetGroup;RequestingArea;Weight
eCommerce;Commercial;DIR_eCommerce_Commercial;30
```

Weights are normalized to sum 100 per (RS + BudgetGroup).

#### weights\_bg\_rs.csv

Budget Group weights within each Revenue Stream.

```csv
RevenueStream;BudgetGroup;Weight
eCommerce;Commercial;20
eCommerce;Technology;20
```

Weights are normalized to sum 100 per RS.

#### weights\_rs.csv

Strategic weights for Revenue Streams.

```csv
RevenueStream;Weight
eCommerce;25
Mail;20
```

Weights are normalized to sum 100.

---

## Commands

### validate

Validate input files without running prioritization.

```bash
python3 tom_demand.py validate \
  --ideas data/input/ideas202602.csv \
  --ra-weights data/input/weights_ra.csv \
  --rs-weights data/input/weights_rs.csv \
  --bg-rs-weights data/input/weights_bg_rs.csv \
  [--config path/to/config.yaml]
```

### prioritize

Run complete prioritization (Levels 2A, 2B, and 3).

```bash
# Default method (Sainte-Laguë)
python3 tom_demand.py prioritize \
  --ideas data/input/ideas202602.csv \
  --ra-weights data/input/weights_ra.csv \
  --rs-weights data/input/weights_rs.csv \
  --bg-rs-weights data/input/weights_bg_rs.csv \
  --output-dir data/output

# Specific method
python3 tom_demand.py prioritize ... --method dhondt --output-dir data/output

# All three methods
python3 tom_demand.py prioritize ... --all-methods --output-dir data/output

# Per-queue methods (v3.3+)
python3 tom_demand.py prioritize ... \
  --now-method wsjf \
  --next-method wsjf \
  --later-method sainte-lague \
  --output-dir data/output
```

**Options:**

| Flag | Default | Description |
|------|---------|-------------|
| `--ideas` | — | Path to ideas CSV (required) |
| `--ra-weights` | — | Path to weights_ra.csv (required) |
| `--rs-weights` | — | Path to weights_rs.csv (required) |
| `--bg-rs-weights` | — | Path to weights_bg_rs.csv (required) |
| `--method` | `sainte-lague` | Algorithm: `sainte-lague`, `dhondt`, or `wsjf` |
| `--all-methods` | — | Run all three methods |
| `--now-method` | — | Algorithm for NOW queue (v3.3+) |
| `--next-method` | — | Algorithm for NEXT queue (v3.3+) |
| `--later-method` | — | Algorithm for LATER queue (v3.3+) |
| `--output-dir` | `./data/output` | Output directory |
| `--config` | `config/config.yaml` | Custom config path |

> Per-queue flags (`--now-method`, `--next-method`, `--later-method`) cannot be combined with `--all-methods`.

### prioritize-rs

Run Level 2 prioritization only (by Revenue Stream).

```bash
python3 tom_demand.py prioritize-rs \
  --ideas data/input/ideas202602.csv \
  --ra-weights data/input/weights_ra.csv \
  --method sainte-lague \
  --output prioritization_rs.csv
```

### prioritize-global

Run Level 3 prioritization only (global), from a pre-generated RS file.

```bash
python3 tom_demand.py prioritize-global \
  --rs-prioritized prioritization_rs.csv \
  --rs-weights data/input/weights_rs.csv \
  --method sainte-lague \
  --output demand.csv
```

### compare

Generate a comparison report across all three methods.

```bash
python3 tom_demand.py compare \
  --ideas data/input/ideas202602.csv \
  --ra-weights data/input/weights_ra.csv \
  --rs-weights data/input/weights_rs.csv \
  --bg-rs-weights data/input/weights_bg_rs.csv \
  --output comparison_report.csv \
  --top-n 50
```

---

## Output Files

| File | Description |
|------|-------------|
| `demand.csv` | Combined global prioritization |
| `demand_[method].csv` | Global prioritization for a specific method |
| `demand_mixed.csv` | Global result when using per-queue methods |
| `prioritization_rs_[method].csv` | Revenue Stream level results |
| `metadata.json` | Execution metadata (timestamps, parameters, statistics) |

---

## Queue-Based Prioritization

IDEAs are automatically assigned to queues by `MicroPhase`. Queues rank sequentially:

| Queue | MicroPhases | Ranking |
|-------|-------------|---------|
| **NOW** | In Development, Ready for Acceptance, In Acceptance, Selected for Production | Ranks 1–N |
| **NEXT** | Ready for Development | Ranks N+1–M |
| **LATER** | Backlog, In Definition, Pitch, Ready for Solution, High Level Design, Ready for Approval, In Approval | Ranks M+1–P |
| **PRODUCTION** | In Rollout, In Production | No ranking |

### Per-Queue Methods (v3.3+)

Apply different algorithms to each queue:

```bash
# WSJF for active work, Sainte-Laguë for planning
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

**Method precedence:**
1. Per-queue flags (highest)
2. Global `--method` flag
3. Default `sainte-lague` (lowest)

**Common patterns:**

| Pattern | Flags | Effect |
|---------|-------|--------|
| Economic focus on active work | `--now-method wsjf --next-method wsjf --later-method sainte-lague` | ROI on in-flight items, balanced planning |
| Strategic development | `--now-method dhondt --later-method sainte-lague` | Reinforce key development areas |
| Uniform economic optimization | `--now-method wsjf --next-method wsjf --later-method wsjf` | Consistent ROI across all queues |

---

## Understanding the Algorithms

### Sainte-Laguë (Default)
- **Divisors**: 1, 3, 5, 7, …
- **Effect**: Balanced allocation — gives smaller areas fair representation
- **Use when**: You want proportional, unbiased distribution

### D'Hondt
- **Divisors**: 1, 2, 3, 4, …
- **Effect**: "Winner takes more" — reinforces areas with higher weights
- **Use when**: You want to focus resources on key strategic priorities

### WSJF
- **Formula**: (Value + Urgency + Risk) / Size, adjusted by RA and RS weights
- **Effect**: Pure economic optimization — ranks high-value, quick-win work first
- **Use when**: ROI is the primary decision criterion

---

## Configuration

Edit `config/config.yaml` to customize Revenue Streams, Budget Groups, default values, validation ranges, and output formatting. See [docs/reference/ALGORITHMS.md](../reference/ALGORITHMS.md) for algorithm details.

---

## Troubleshooting

**"PriorityRA not sequential"**
Each Requesting Area must have priorities 1, 2, 3, … with no gaps or duplicates.

**"Invalid Revenue Stream values"**
Revenue Stream names in the ideas file must match those defined in `config/config.yaml`.

**"Weights sum to X, not 100.0"**
Warning only — weights are auto-normalized by default.

**"ModuleNotFoundError"**
```bash
pip install -r requirements.txt
```

For further detail, see the [Functional Specification](../TOM%20Demand%20Management%20System%20-%20Functional%20Specification.md).
