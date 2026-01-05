# TOM Demand Management System - v3.3.0 Release Notes

**Release Date**: January 5, 2026

## New Feature: Per-Queue Prioritization Methods

Version 3.3 introduces the ability to apply different prioritization methods (Sainte-Laguë, D'Hondt, WSJF) to each queue (NOW, NEXT, LATER), providing greater flexibility in prioritization strategies.

### What's New

#### CLI Flags for Queue-Specific Methods

Three new command-line options allow you to specify which prioritization method to use for each queue:

```bash
--now-method [sainte-lague|dhondt|wsjf]      # Method for NOW queue
--next-method [sainte-lague|dhondt|wsjf]     # Method for NEXT queue
--later-method [sainte-lague|dhondt|wsjf]    # Method for LATER queue
```

#### Example Usage

```bash
# Use WSJF for active development (NOW), Sainte-Laguë for planning (LATER)
python3 tom_demand.py prioritize \
  --ideas data/input/ideias.csv \
  --ra-weights data/input/weights_ra.csv \
  --rs-weights data/input/weights_rs.csv \
  --now-method wsjf \
  --next-method wsjf \
  --later-method sainte-lague \
  --output-dir data/output
```

### Key Benefits

1. **Strategic Flexibility**: Apply economic optimization (WSJF) to active work while maintaining balanced planning
2. **Queue-Appropriate Methods**: Use different algorithms that match each queue's objectives
3. **Granular Control**: Override methods at the queue level while maintaining global defaults

### How It Works

**Precedence Rules**:
1. Per-queue flags (`--now-method`, etc.) → Highest priority
2. Global `--method` flag → Applies to unconfigured queues
3. Default (`sainte-lague`) → Lowest priority

**Example Scenarios**:

```bash
# Scenario 1: Only NOW queue specified
python3 tom_demand.py prioritize --now-method wsjf ...
# Result: NOW uses WSJF, NEXT and LATER use default (Sainte-Laguë)

# Scenario 2: Global method with NOW override
python3 tom_demand.py prioritize --method dhondt --now-method wsjf ...
# Result: NOW uses WSJF, NEXT and LATER use D'Hondt

# Scenario 3: All queues specified
python3 tom_demand.py prioritize --now-method wsjf --next-method dhondt --later-method sainte-lague ...
# Result: Each queue uses its specified method
```

### Output Changes

#### Console Output
The prioritization output now shows which method is being used for each queue:

```
  → Using per-queue methods:
     • NOW: Wsjf
     • NEXT: Wsjf
     • Other queues: Sainte Lague
  → Processing NOW queue: 8 IDEAs
    ✓ NOW: Ranks 1-8 (wsjf)
  → Processing NEXT queue: 1 IDEAs
    ✓ NEXT: Ranks 9-9 (wsjf)
  → Processing LATER queue: 9 IDEAs
    ✓ LATER: Ranks 10-18 (sainte-lague)
```

#### CSV Output
- File naming uses `mixed` when per-queue methods are used: `demand_mixed.csv`
- Method column shows the actual method used for each IDEA

#### Metadata JSON
New fields capture the queue method configuration:

```json
{
  "queue_methods": {
    "NOW": "wsjf",
    "NEXT": "wsjf",
    "LATER": "sainte-lague"
  },
  "default_method": "sainte-lague"
}
```

### Important Notes

**Incompatibility with --all-methods**:
Per-queue method flags cannot be used with `--all-methods`. This prevents exponential combinations and keeps the feature simple:

```bash
# This will error
python3 tom_demand.py prioritize --all-methods --now-method wsjf ...
# ❌ Usage Error: Per-queue method flags cannot be used with --all-methods
```

**Backward Compatibility**:
All existing commands continue to work unchanged. The new flags are optional and don't affect default behavior.

### Use Cases

**Use Case 1: Economic Focus on Active Work**
```bash
--now-method wsjf --next-method wsjf --later-method sainte-lague
```
Maximize ROI on in-flight development while maintaining balanced planning pipeline.

**Use Case 2: Strategic Development, Balanced Planning**
```bash
--now-method dhondt --later-method sainte-lague
```
Focus resources on strategic development areas, ensure fair representation in planning.

**Use Case 3: Uniform Economic Optimization**
```bash
--now-method wsjf --next-method wsjf --later-method wsjf
```
Consistently optimize for economic value across all queues.

## Technical Changes

### Modified Files

1. **src/prioritizer.py**
   - Updated `prioritize_with_queues()` to accept `queue_methods` and `default_method` parameters
   - Added queue method resolution logic
   - Enhanced output messages to show method per queue

2. **src/cli.py**
   - Added three new CLI options (`--now-method`, `--next-method`, `--later-method`)
   - Added validation for incompatibility with `--all-methods`
   - Updated execution logic to pass queue methods to prioritizer
   - Enhanced metadata with queue method information

3. **src/exporter.py**
   - No changes required (automatically handles new metadata fields)

### Testing

All 5 test scenarios passed successfully:
- ✅ Backward compatibility (existing commands unchanged)
- ✅ Per-queue method specification
- ✅ Partial queue configuration with defaults
- ✅ Precedence rules (per-queue vs global)
- ✅ Error handling for conflicting flags

## Migration Guide

No migration required. This is a backward-compatible feature addition.

**To adopt the new feature**:
1. Update to v3.3.0
2. Add per-queue method flags to your prioritize commands as needed
3. Review output files with `_mixed` suffix

**To continue using existing behavior**:
- No changes needed. Existing commands work identically.

## Documentation Updates

- ✅ README.md - Added feature to overview and examples
- ✅ USAGE_GUIDE.md - Detailed usage instructions and examples
- ✅ CLAUDE.md - Updated for development reference
- ✅ docs/PROJECT_SUMMARY.md - Added to feature list

## Version History

- **v3.3.0** (January 5, 2026): Per-queue prioritization methods
- **v3.2.0** (January 5, 2026): Three-queue prioritization system
- **v3.0.0** (January 2026): Initial production release

---

For questions or issues, please refer to the [USAGE_GUIDE.md](USAGE_GUIDE.md) or [Functional Specification](docs/TOM%20Demand%20Management%20System%20-%20Functional%20Specification.md).
