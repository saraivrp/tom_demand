# Claude Code Guidelines for TOM Demand Management System

## Project Overview

This is the **TOM Demand Management System v3.0** - a production-ready demand prioritization system for CTT (Portuguese Post) that implements three proportional allocation algorithms: Sainte-Laguë, D'Hondt, and WSJF.

**Status**: ✅ Production Ready (January 2026)

## Key Project Characteristics

### 1. European/Iberian Standards
- **CSV Format**: Semicolon (`;`) delimiter, NOT comma
- **Decimal Separator**: Comma (`,`) e.g., `0,088`
- **Thousands Separator**: Dot (`.`) e.g., `1.000,45`
- **Metric System**: All measurements in metric units
- **Date Format**: DD/MM/YYYY or ISO 8601

⚠️ **CRITICAL**: When reading or writing CSV files, always use European format as configured in [config/config.yaml](config/config.yaml). See [docs/EUROPEAN_FORMAT.md](docs/EUROPEAN_FORMAT.md) for details.

### 2. Codebase Architecture

```
src/
├── algorithms/          # Prioritization algorithms (Sainte-Laguë, D'Hondt, WSJF)
├── validator.py        # Centralized validation logic (320 lines)
├── loader.py           # Data ingestion with validation (175 lines)
├── prioritizer.py      # Orchestration and coordination (220 lines)
├── exporter.py         # Result formatting and output (185 lines)
├── cli.py              # Command-line interface (340 lines)
└── utils.py            # Shared utilities (40 lines)
```

**Total**: ~1,735 lines of well-structured, modular Python code

### 3. Queue-Based Prioritization (v3.2)

The system now supports **sequential queue-based ranking** that separates IDEAs by their lifecycle phase:

**Queue Priority Order** (most important to least important):
1. **NOW Queue** (Development phase) → **Ranks 1-N** (highest priority)
   - In Development → Ready for Acceptance → In Acceptance → Selected for Production
   - These are active development items that should be prioritized first

2. **NEXT Queue** (Ready for Execution) → **Ranks N+1-M** (next in line)
   - Ready for Execution
   - Solution is fully defined and approved, ready to start development

3. **LATER Queue** (Planning phases) → **Ranks M+1-P** (future work)
   - Need: Backlog → In Definition → Pitch → Ready for Solution
   - Solution: High Level Design → Ready for Approval → In Approval
   - These are items still in planning/design stages

4. **PRODUCTION Queue** → **No ranking** (already deployed)
   - In Rollout → In Production
   - No prioritization needed, just tracked

**How It Works:**
- IDEAs are automatically assigned to queues based on their `MicroPhase` field
- NOW items get ranks 1-8, NEXT items get ranks 9-9, LATER items get ranks 10-18, PRODUCTION items have null rank
- Sequential ranking ensures: development > execution-ready > planning > production (tracking only)
- This allows prioritization of solution-defined work separately from early planning work

### 4. Core Modules

#### Validation ([src/validator.py](src/validator.py))
- Validates IDEAS with required/optional attributes including MicroPhase
- Validates RA and RS weights with referential integrity
- Auto-normalizes weights
- Provides clear, actionable error messages

#### Data Loading ([src/loader.py](src/loader.py))
- Loads IDEAs from CSV with default values
- Determines Queue from MicroPhase automatically
- Loads and validates RA/RS weights
- Cross-validation between files
- Integrated validation engine

#### Algorithms ([src/algorithms/](src/algorithms/))
- **Sainte-Laguë**: Balanced allocation (odd divisor: 1, 3, 5, 7...)
- **D'Hondt**: Strategic focus (natural divisor: 1, 2, 3, 4...)
- **WSJF**: Economic optimization ((Value + Urgency + Risk) / Size)

#### Prioritizer ([src/prioritizer.py](src/prioritizer.py))
- Coordinates Level 2 (Revenue Stream) prioritization
- Coordinates Level 3 (Global) prioritization
- Executes multiple methods for comparison

#### Exporter ([src/exporter.py](src/exporter.py))
- Exports Level 2 results: `prioritization_rs.csv`
- Exports Level 3 results: `demand.csv`
- Exports comparison reports
- Exports execution metadata (JSON)

## Development Guidelines

### When Making Changes

1. **Read Before Modifying**: Always read files before suggesting modifications
2. **Preserve European Format**: Maintain semicolon delimiters and comma decimals in CSV operations
3. **Type Hints**: All functions should have proper type hints
4. **Docstrings**: Follow existing docstring patterns
5. **Error Handling**: Provide clear, actionable error messages
6. **Validation**: Use the validation engine for data integrity checks

### Code Style

- **Python Version**: 3.9+
- **Type Hints**: Throughout codebase
- **Imports**: Standard library → Third-party → Local modules
- **Line Length**: Reasonable (no strict limit, but keep it readable)
- **Naming**:
  - Functions/variables: `snake_case`
  - Classes: `PascalCase`
  - Constants: `UPPER_SNAKE_CASE`

### Testing & Validation

Always test changes with the example data:
```bash
# Validation
python3 tom_demand.py validate \
  --ideas data/input/ideias.csv \
  --ra-weights data/input/weights_ra.csv \
  --rs-weights data/input/weights_rs.csv

# Full prioritization
python3 tom_demand.py prioritize \
  --ideas data/input/ideias.csv \
  --ra-weights data/input/weights_ra.csv \
  --rs-weights data/input/weights_rs.csv \
  --all-methods \
  --output-dir data/output
```

## Configuration

All configuration is centralized in [config/config.yaml](config/config.yaml):
- Revenue Streams and Budget Groups
- Default values for IDEA attributes
- Validation ranges
- European format settings
- Output formatting
- Logging configuration

**When modifying**: Always validate YAML syntax and maintain backward compatibility.

## File References

When referencing code locations in responses, use this format:
- Files: [validator.py](src/validator.py)
- Specific lines: [validator.py:150](src/validator.py#L150)
- Line ranges: [validator.py:100-120](src/validator.py#L100-L120)

## Common Tasks

### Adding a New Validation Rule
1. Edit [src/validator.py](src/validator.py)
2. Add rule to appropriate validation method
3. Test with example data
4. Update error messages for clarity

### Adding a New Algorithm
1. Create new file in [src/algorithms/](src/algorithms/)
2. Implement required interface (see existing algorithms)
3. Add to [src/prioritizer.py](src/prioritizer.py)
4. Update CLI in [src/cli.py](src/cli.py)
5. Test with all methods

### Modifying CSV Output
1. Edit [src/exporter.py](src/exporter.py)
2. Maintain European format (semicolon delimiter, comma decimal)
3. Update metadata export if needed
4. Verify output with example data

### Changing Configuration
1. Edit [config/config.yaml](config/config.yaml)
2. Update loader/validator if structure changes
3. Test with validation command
4. Document changes if significant

## Documentation Files

- [README.md](README.md) - Quick start and overview
- [USAGE_GUIDE.md](USAGE_GUIDE.md) - Detailed usage instructions
- [docs/PROJECT_SUMMARY.md](docs/PROJECT_SUMMARY.md) - Implementation status and features
- [docs/EUROPEAN_FORMAT.md](docs/EUROPEAN_FORMAT.md) - European format details
- [docs/TOM Demand Management System - Functional Specification.md](docs/TOM%20Demand%20Management%20System%20-%20Functional%20Specification.md) - Complete specification v3.0

## What NOT to Do

- ❌ Don't change CSV format to US format (comma delimiter)
- ❌ Don't break backward compatibility without explicit approval
- ❌ Don't add dependencies without checking requirements.txt
- ❌ Don't modify core algorithms without understanding the mathematical basis
- ❌ Don't skip validation when loading data
- ❌ Don't add features from "Next Steps" section without explicit request
- ❌ Don't create new documentation files unless explicitly requested

## Dependencies

Current dependencies (see [requirements.txt](requirements.txt)):
- pandas >= 1.3.0
- numpy >= 1.21.0
- pyyaml >= 5.4.0
- click >= 8.0.0

## Git Workflow

- **Main Branch**: `main` (use for PRs)
- **Current Branch**: Check git status
- Follow standard commit message conventions
- Include co-authorship footer when requested

## Questions to Ask Before Starting

For non-trivial changes, clarify:
1. Does this change affect the European format?
2. Will this impact existing CSV files or workflows?
3. Should this be configurable via config.yaml?
4. Does this require updating documentation?
5. Should all three algorithms support this change?

## Context and Domain

**Domain**: Portfolio management and demand prioritization for CTT (Portuguese postal service)

**Key Concepts**:
- **IDEA**: An initiative/demand item to be prioritized
- **RA**: Requesting Area (department submitting the IDEA)
- **RS**: Revenue Stream (business area)
- **BG**: Budget Group (for constraint management)
- **Level 1**: RA-level prioritization
- **Level 2**: RS-level prioritization (within Revenue Stream)
- **Level 3**: Global prioritization (across all Revenue Streams)
- **WSJF**: (Value + Urgency + Risk Reduction) / Job Size

## Success Criteria

Code changes should:
✓ Maintain European format compliance
✓ Pass validation with example data
✓ Include proper type hints and docstrings
✓ Provide clear error messages
✓ Follow existing architectural patterns
✓ Be tested with actual prioritization runs
✓ Preserve backward compatibility (unless explicitly approved)

---

**Version**: 3.0.0
**Last Updated**: January 4, 2026
**Status**: Production System - Handle with Care
