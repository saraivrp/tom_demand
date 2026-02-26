# TOM Demand Management System - Usage Guide

## Quick Start

### 1. Installation

```bash
# Install required dependencies
pip install -r requirements.txt
```

### 2. Prepare Input Files

You need four CSV files:

#### ideias.csv
Contains the IDEAs (development requests) with required and optional attributes.

```csv
ID;Name;RequestingArea;RevenueStream;BudgetGroup;MicroPhase;PriorityRA;Value;Urgency;Risk;Size
IDEA001;New eCommerce Portal;DIR_eCommerce_Commercial;eCommerce;Commercial;In Development;1;9;8;5;250
```

> **Note**: CSV files use European format with semicolon (`;`) delimiter.

**Required columns:**
- ID: Unique identifier
- Name: IDEA name
- RequestingArea: Requesting direction/department
- RevenueStream: Target Revenue Stream
- BudgetGroup: Associated Budget Group
- PriorityRA: Priority within Requesting Area (sequential: 1, 2, 3, ...)

**Optional columns (with defaults):**
- MicroPhase: Lifecycle phase (determines Queue assignment, default: Backlog)
  - Valid values: Backlog, In Definition, Pitch, Ready for Solution, High Level Design, Ready for Approval, In Approval, Ready for Execution, In Development, Ready for Acceptance, In Acceptance, Selected for Production, In Rollout, In Production
- Value: Business value (1-10, default: 1)
- Urgency: Time criticality (1-10, default: 1)
- Risk: Risk reduction (1-10, default: 1)
- Size: Estimated size in story points (>0, default: 100)

#### weights_ra.csv
Contains weights for Requesting Areas within each Revenue Stream and Budget Group.

```csv
RevenueStream;BudgetGroup;RequestingArea;Weight
eCommerce;Commercial;DIR_eCommerce_Commercial;30
```

**Columns:**
- RevenueStream: Revenue Stream name
- BudgetGroup: Budget Group name
- RequestingArea: Requesting Area identifier
- Weight: Relative weight (will be normalized to sum 100 per RS+BudgetGroup)

#### weights_bg_rs.csv
Contains Budget Group weights within each Revenue Stream.

```csv
RevenueStream;BudgetGroup;Weight
eCommerce;Commercial;20
eCommerce;Technology;20
```

**Columns:**
- RevenueStream: Revenue Stream name
- BudgetGroup: Budget Group name
- Weight: Relative weight (will be normalized to sum 100 per RS)

#### weights_rs.csv
Contains strategic weights for Revenue Streams.

```csv
RevenueStream;Weight
eCommerce;25
Mail;20
```

**Columns:**
- RevenueStream: Revenue Stream name
- Weight: Strategic weight (will be normalized to sum 100)

### 3. Run Prioritization

#### Configuration File (Optional)

By default, the system uses `config/config.yaml` for configuration. You can specify a custom configuration file using the `--config` parameter:

```bash
python3 tom_demand.py prioritize \
  --ideas data/input/ideias.csv \
  --ra-weights data/input/weights_ra.csv \
  --rs-weights data/input/weights_rs.csv \
  --bg-rs-weights data/input/weights_bg_rs.csv \
  --config path/to/custom_config.yaml \
  --output-dir data/output
```

#### Validate Input Files

Before running prioritization, validate your input files:

```bash
python3 tom_demand.py validate \
  --ideas data/input/ideias.csv \
  --ra-weights data/input/weights_ra.csv \
  --rs-weights data/input/weights_rs.csv \
  --bg-rs-weights data/input/weights_bg_rs.csv

# With custom config
python3 tom_demand.py validate \
  --ideas data/input/ideias.csv \
  --ra-weights data/input/weights_ra.csv \
  --rs-weights data/input/weights_rs.csv \
  --bg-rs-weights data/input/weights_bg_rs.csv \
  --config path/to/custom_config.yaml
```

#### Execute Complete Prioritization

Run prioritization with the default method (Sainte-Laguë):

```bash
python3 tom_demand.py prioritize \
  --ideas data/input/ideias.csv \
  --ra-weights data/input/weights_ra.csv \
  --rs-weights data/input/weights_rs.csv \
  --bg-rs-weights data/input/weights_bg_rs.csv \
  --output-dir data/output
```

Run with a specific method:

```bash
python3 tom_demand.py prioritize \
  --ideas data/input/ideias.csv \
  --ra-weights data/input/weights_ra.csv \
  --rs-weights data/input/weights_rs.csv \
  --bg-rs-weights data/input/weights_bg_rs.csv \
  --method dhondt \
  --output-dir data/output
```

Run all three methods:

```bash
python3 tom_demand.py prioritize \
  --ideas data/input/ideias.csv \
  --ra-weights data/input/weights_ra.csv \
  --rs-weights data/input/weights_rs.csv \
  --bg-rs-weights data/input/weights_bg_rs.csv \
  --all-methods \
  --output-dir data/output
```

Run with different methods per queue (v3.3+):

```bash
# Use WSJF for NOW queue, Sainte-Laguë for others
python3 tom_demand.py prioritize \
  --ideas data/input/ideias.csv \
  --ra-weights data/input/weights_ra.csv \
  --rs-weights data/input/weights_rs.csv \
  --bg-rs-weights data/input/weights_bg_rs.csv \
  --now-method wsjf \
  --output-dir data/output

# Specify different methods for each queue
python3 tom_demand.py prioritize \
  --ideas data/input/ideias.csv \
  --ra-weights data/input/weights_ra.csv \
  --rs-weights data/input/weights_rs.csv \
  --bg-rs-weights data/input/weights_bg_rs.csv \
  --now-method wsjf \
  --next-method wsjf \
  --later-method sainte-lague \
  --output-dir data/output
```

### 4. Output Files

After execution, you'll find these files in the output directory:

- **demand.csv**: Combined global prioritization from all executed methods
- **demand_[method].csv**: Global prioritization for specific method
- **prioritization_rs_[method].csv**: Revenue Stream level prioritization
- **metadata.json**: Execution metadata (timestamps, parameters, statistics)

### 5. Compare Methods

Generate a comparison report:

```bash
python3 tom_demand.py compare \
  --ideas data/input/ideias.csv \
  --ra-weights data/input/weights_ra.csv \
  --rs-weights data/input/weights_rs.csv \
  --bg-rs-weights data/input/weights_bg_rs.csv \
  --output comparison_report.csv \
  --top-n 50
```

## Available Commands

### validate
Validate input files without executing prioritization.

```bash
python3 tom_demand.py validate \
  --ideas <path> \
  --ra-weights <path> \
  --rs-weights <path> \
  --bg-rs-weights <path> \
  [--config <path>]
```

### prioritize
Execute complete prioritization (Levels 2A, 2B, and 3).

**Options:**
- `--ideas`: Path to ideias.csv (required)
- `--ra-weights`: Path to weights_ra.csv (required)
- `--rs-weights`: Path to weights_rs.csv (required)
- `--bg-rs-weights`: Path to weights_bg_rs.csv (required)
- `--method`: Method to use: `sainte-lague`, `dhondt`, or `wsjf` (default: sainte-lague)
- `--all-methods`: Execute all 3 methods (flag)
- `--now-method`: Method for NOW queue: `sainte-lague`, `dhondt`, or `wsjf` (v3.3+)
- `--next-method`: Method for NEXT queue: `sainte-lague`, `dhondt`, or `wsjf` (v3.3+)
- `--later-method`: Method for LATER queue: `sainte-lague`, `dhondt`, or `wsjf` (v3.3+)
- `--output-dir`: Output directory (default: ./data/output)
- `--config`: Custom configuration file path (optional, default: config/config.yaml)

**Note**: Per-queue method flags (`--now-method`, `--next-method`, `--later-method`) cannot be used with `--all-methods`.

### prioritize-rs
Execute Level 2 prioritization only (by Revenue Stream).

```bash
python3 tom_demand.py prioritize-rs \
  --ideas data/input/ideias.csv \
  --ra-weights data/input/weights_ra.csv \
  --method sainte-lague \
  --output prioritization_rs.csv \
  [--config <path>]
```

### prioritize-global
Execute Level 3 prioritization only (global).

```bash
python3 tom_demand.py prioritize-global \
  --rs-prioritized prioritization_rs.csv \
  --rs-weights data/input/weights_rs.csv \
  --method sainte-lague \
  --output demand.csv \
  [--config <path>]
```

### compare
Compare all 3 prioritization methods.

```bash
python3 tom_demand.py compare \
  --ideas data/input/ideias.csv \
  --ra-weights data/input/weights_ra.csv \
  --rs-weights data/input/weights_rs.csv \
  --bg-rs-weights data/input/weights_bg_rs.csv \
  --output comparison.csv \
  --top-n 50 \
  [--config <path>]
```

## Understanding the Methods

### Sainte-Laguë (Default)
- **Best for**: Balanced allocation across all areas
- **Characteristics**: Uses odd divisors (1, 3, 5, 7, ...)
- **Effect**: Favors proportional representation, gives smaller areas fair share
- **Use when**: You want balanced distribution and fair representation

### D'Hondt
- **Best for**: Reinforcing strategic areas with higher weights
- **Characteristics**: Uses natural divisors (1, 2, 3, 4, ...)
- **Effect**: "Winner takes more" - favors larger/strategic areas
- **Use when**: You want to focus resources on key strategic initiatives

### WSJF (Weighted Shortest Job First)
- **Best for**: Pure economic value optimization
- **Characteristics**: Sorts by (Value + Urgency + Risk) / Size, adjusted by weights
- **Effect**: Prioritizes high-value, low-effort work
- **Use when**: Economic ROI is the primary concern

## Configuration

Edit `config/config.yaml` to customize:

- Default values for IDEA attributes
- Validation ranges
- Auto-normalization settings
- Output formatting
- Logging levels

## Troubleshooting

### Validation Errors

**"PriorityRA not sequential"**
- Each Requesting Area must have sequential priorities: 1, 2, 3, ...
- No gaps or duplicates allowed

**"Invalid Revenue Stream values"**
- Check that all Revenue Streams in ideias.csv match those defined in config.yaml

**"Weights sum to X, not 100.0"**
- This is a warning, not an error
- Weights will be auto-normalized if configured (default: enabled)

### Import Errors

If you get "ModuleNotFoundError", ensure dependencies are installed:

```bash
pip install -r requirements.txt
```

## Examples

See the `data/input/` directory for example files that demonstrate proper formatting.

## Queue-Based Prioritization

The system uses a four-queue structure for sequential prioritization (v3.2):

1. **NOW Queue** (Highest Priority): Active development work
   - Ranks 1 to N
   - Micro Phases: In Development, Ready for Acceptance, In Acceptance, Selected for Production

2. **NEXT Queue** (Ready for Execution): Solution-complete items
   - Ranks N+1 to M
   - Micro Phase: Ready for Development
   - Items with complete solutions ready to be picked up by development teams

3. **LATER Queue** (Planning Work): Items still being defined
   - Ranks M+1 to P
   - Micro Phases: Backlog, In Definition, Pitch, Ready for Solution, High Level Design, Ready for Approval, In Approval

4. **PRODUCTION Queue** (No Ranking): Deployed items
   - No rank (null)
   - Micro Phases: In Rollout, In Production

This separation ensures development work is prioritized first, followed by execution-ready items, then planning work.

### Per-Queue Prioritization Methods (v3.3)

Starting in version 3.3, you can apply different prioritization methods to each queue:

```bash
# Example: Use WSJF for active development (NOW), Sainte-Laguë for planning (LATER)
python3 tom_demand.py prioritize \
  --ideas data/input/ideias.csv \
  --ra-weights data/input/weights_ra.csv \
  --rs-weights data/input/weights_rs.csv \
  --now-method wsjf \
  --next-method wsjf \
  --later-method sainte-lague \
  --output-dir data/output
```

**Benefits:**
- **NOW queue with WSJF**: Prioritize high-value, quick-win development work
- **NEXT queue with WSJF**: Focus on ROI for execution-ready items
- **LATER queue with Sainte-Laguë**: Balanced planning across all areas

**Precedence:**
1. Per-queue flags (`--now-method`, `--next-method`, `--later-method`) take highest priority
2. Global `--method` flag applies to queues without specific methods
3. Default (`sainte-lague`) used if neither specified

**Output:**
- Results are saved with `mixed` naming: `demand_mixed.csv`, `prioritization_rs_mixed.csv`
- Metadata JSON includes `queue_methods` and `default_method` fields
- CSV output includes the method used for each IDEA in the Method column

## Support

For detailed information, see the [Functional Specification](docs/TOM%20Demand%20Management%20System%20-%20Functional%20Specification.md).
