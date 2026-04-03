# European Format

The system uses European (Iberia/EU) notation for all CSV files and numbers, in compliance with Portuguese and EU standards.

## Format Specifications

| Setting | Value | Example |
|---------|-------|---------|
| CSV delimiter | Semicolon `;` | `ID;Name;Value` |
| Decimal separator | Comma `,` | `0,088` |
| Thousands separator | Dot `.` | `1.000,45` |
| Date format | ISO 8601 | `2026-02-24 14:30:00` |
| Encoding | UTF-8 | — |

## Configuration

Defined in `config/config.yaml`:

```yaml
locale:
  csv_delimiter: ";"
  decimal_separator: ","
  thousands_separator: "."
```

## Example Files

**ideas.csv:**
```csv
ID;Name;RequestingArea;RevenueStream;BudgetGroup;PriorityRA;Value;Urgency;Risk;Size
IDEA001;New eCommerce Portal;DIR_eCommerce_Commercial;eCommerce;Commercial;1;9;8;5;250
IDEA002;Checkout Optimization;DIR_eCommerce_Commercial;eCommerce;Commercial;2;7;9;3;100
```

**weights_ra.csv:**
```csv
RevenueStream;BudgetGroup;RequestingArea;Weight
eCommerce;Commercial;DIR_eCommerce_Commercial;30
eCommerce;Technology;DIR_eCommerce_Tech;25
```

**weights_rs.csv:**
```csv
RevenueStream;Weight
eCommerce;25
Mail;20
```

**weights_bg_rs.csv:**
```csv
RevenueStream;BudgetGroup;Weight
eCommerce;Commercial;20
eCommerce;Technology;20
```

## Output Files

**demand_sainte_lague.csv:**
```csv
Queue;Method;GlobalRank;ID;Name;RequestingArea;RevenueStream;BudgetGroup;MicroPhase;PriorityRA;WSJF_Score
NOW;sainte-lague;1;IDEA001;New eCommerce Portal;DIR_eCommerce_Commercial;eCommerce;Commercial;In Development;1;0,088
NEXT;sainte-lague;2;IDEA005;Customer Portal;DIR_BS_Tech;Business Solutions;Technology;Ready for Development;1;0,075
```

Note: `WSJF_Score` uses comma as decimal separator (e.g., `0,088`).

## Opening in Excel / LibreOffice

**Excel (European locale):** Double-click the CSV file — Excel automatically recognises `;` delimiter and `,` decimal.

**Excel (non-European locale):** Use Data → From Text/CSV, then set:
- Delimiter: Semicolon
- Locale: Portuguese (Portugal) or Spanish (Spain)

**LibreOffice Calc:** The import dialog appears automatically. Set:
- Separator: Semicolon
- Language: Portuguese or Spanish

## Technical Implementation

| File | Operation |
|------|-----------|
| `src/loader.py` | Reads CSV: `pd.read_csv(filepath, sep=';', decimal=',')` |
| `src/exporter.py` | Writes CSV: `df.to_csv(filepath, sep=';', decimal=',')` |

All input and output CSV files use European format consistently. No manual conversion is required when using the system in an Iberia/EU context.
