# European Format Configuration

## Overview

The TOM Demand Management System has been configured to use European (Iberia) notation standards for CSV files and number formatting, in compliance with EU conventions.

## Format Specifications

### CSV Delimiter
- **Delimiter**: Semicolon (`;`)
- **Standard**: European CSV format (as used in Spain, Portugal, and other EU countries)

### Number Formatting
- **Decimal Separator**: Comma (`,`)
  - Example: `0,088` instead of `0.088`
- **Thousands Separator**: Dot (`.`)
  - Example: `1.000,45` instead of `1,000.45`

## Configuration

The European format is configured in [config/config.yaml](config/config.yaml):

```yaml
# Locale settings (European/Iberia format)
locale:
  csv_delimiter: ";"          # Semicolon for European CSV format
  decimal_separator: ","      # Comma for decimal separator (e.g., 1,23)
  thousands_separator: "."    # Dot for thousands separator (e.g., 1.000,45)
```

## Example Files

### Input Files (European Format)

**ideias.csv**:
```csv
ID;Name;RequestingArea;RevenueStream;BudgetGroup;PriorityRA;Value;Urgency;Risk;Size
IDEA001;New eCommerce Portal;DIR_eCommerce_Commercial;eCommerce;Commercial;1;9;8;5;250
IDEA002;Checkout Optimization;DIR_eCommerce_Commercial;eCommerce;Commercial;2;7;9;3;100
```

**weights_ra.csv**:
```csv
RevenueStream;BudgetGroup;RequestingArea;Weight
eCommerce;Commercial;DIR_eCommerce_Commercial;30
eCommerce;Technology;DIR_eCommerce_Tech;25
```

**weights_rs.csv**:
```csv
RevenueStream;Weight
eCommerce;25
Mail;20
```

**weights_bg_rs.csv**:
```csv
RevenueStream;BudgetGroup;Weight
eCommerce;Commercial;20
eCommerce;Technology;20
```

### Output Files (European Format)

**demand_sainte_lague.csv** (v3.2+ with Queue column):
```csv
Queue;Method;GlobalRank;ID;Name;RequestingArea;RevenueStream;BudgetGroup;MicroPhase;PriorityRA;WSJF_Score;Value;Urgency;Risk;Size
NOW;sainte-lague;1;IDEA001;New eCommerce Portal;DIR_eCommerce_Commercial;eCommerce;Commercial;In Development;1;0,088;9;8;5;250
NOW;sainte-lague;2;IDEA003;Mail Sorting Automation;DIR_Mail_Operations;Mail;Operations;In Acceptance;1;0,083;8;10;7;300
NEXT;sainte-lague;3;IDEA005;Customer Portal;DIR_BS_Tech;Business Solutions;Technology;Ready for Execution;1;0,075;7;6;8;200
LATER;sainte-lague;4;IDEA007;API Integration;DIR_Tech;Fulfilment;Technology;Backlog;1;0,065;6;5;4;150
```

Note the decimal scores like `0,088` and `0,083` using comma as decimal separator.

**prioritization_rs_sainte_lague.csv**:
```csv
Queue;RevenueStream;Method;Rank_RS;ID;Name;RequestingArea;BudgetGroup;MicroPhase;WSJF_Score;Value;Urgency;Risk;Size
NOW;eCommerce;sainte-lague;1;IDEA001;New eCommerce Portal;DIR_eCommerce_Commercial;Commercial;In Development;0,088;9;8;5;250
```

## Opening Files in Excel (European Locale)

When opening CSV files in Microsoft Excel or LibreOffice Calc with European locale settings:

1. **Excel (European locale)**: Simply double-click the CSV file. Excel will automatically recognize the semicolon delimiter and comma decimal separator.

2. **Excel (Non-European locale)**: Use "Data" → "From Text/CSV" and manually select:
   - Delimiter: Semicolon
   - Locale: Portuguese (Portugal) or Spanish (Spain)

3. **LibreOffice Calc**: The import dialog will appear automatically. Select:
   - Separator: Semicolon
   - Language: Portuguese or Spanish

## Technical Implementation

The European format support is implemented in:

1. **[src/loader.py](src/loader.py)**: Reads CSV files with European format
   - Uses `pd.read_csv(filepath, sep=';', decimal=',')`

2. **[src/exporter.py](src/exporter.py)**: Writes CSV files with European format
   - Uses `df.to_csv(filepath, sep=';', decimal=',')`

3. **[src/cli.py](src/cli.py)**: Handles European format in CLI operations
   - Loads locale settings from config for direct pandas operations

## Compatibility

### Metric System
The system uses metric units throughout:
- **Size**: Measured in person-days or hours
- **All numeric values**: Standard metric conventions

### EU Standards
- Date format: `YYYY-MM-DD HH:MM:SS` (ISO 8601)
- Character encoding: UTF-8
- CSV format: RFC 4180 compliant with European delimiter

## Migration from US Format

If you have existing CSV files in US format (comma-delimited with dot decimal separator), they have already been converted. The original format was:

```csv
ID,Name,Value
IDEA001,Project Name,0.088
```

Now converted to European format:

```csv
ID;Name;Value
IDEA001;Project Name;0,088
```

## Verification

To verify the European format is working correctly:

```bash
# Run prioritization
python3 tom_demand.py prioritize \
  --ideas data/input/ideias.csv \
  --ra-weights data/input/weights_ra.csv \
  --rs-weights data/input/weights_rs.csv \
  --bg-rs-weights data/input/weights_bg_rs.csv \
  --method sainte-lague \
  --output-dir data/output

# Check output format
head data/output/demand_sainte_lague.csv
```

The output should show:
- Semicolons (`;`) separating columns
- Commas (`,`) as decimal separators in WSJF_Score column
- Queue column (NOW, NEXT, LATER, or PRODUCTION) as the first column
- Method column indicating which algorithm was used

## Queue-Based Output (v3.2+)

Output files include a Queue column that categorizes IDEAs by their lifecycle phase:

| Queue | Description | Ranking |
|-------|-------------|---------|
| NOW | Active development (In Development, In Acceptance, etc.) | Ranks 1-N |
| NEXT | Ready for execution | Ranks N+1-M |
| LATER | Planning phases (Backlog, In Definition, etc.) | Ranks M+1-P |
| PRODUCTION | Already deployed (In Rollout, In Production) | No ranking |

This allows sorting and filtering by execution phase while maintaining European format for all numeric values.

## Support

All input and output CSV files use European format consistently throughout the system. No manual conversion is required when using the system in Iberia/EU context.
