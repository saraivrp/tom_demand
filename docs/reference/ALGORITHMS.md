# Algorithms Reference

The system implements three proportional allocation algorithms. All algorithms operate at two levels:

- **Level 2**: Within each Revenue Stream (using RA and Budget Group weights)
- **Level 3**: Global ranking across all Revenue Streams (using RS weights)

---

## Sainte-Laguë (Default)

**Divisors**: 1, 3, 5, 7, … (odd numbers)

**How it works:**
Each area starts with a score = `weight × PriorityRA`. At each allocation step, the area with the highest quotient `score / divisor` receives the next rank. The divisor for that area then advances to the next odd number.

**Characteristics:**
- Balanced proportional allocation
- Gives smaller/lower-weight areas fair representation
- Prevents any single area from dominating the top ranks

**Best for:** Situations where fair representation across all areas matters.

---

## D'Hondt

**Divisors**: 1, 2, 3, 4, … (natural numbers)

**How it works:**
Same seat-allocation mechanism as Sainte-Laguë, but uses natural divisors. The natural progression causes the effective weight of an area to decrease more slowly than with odd divisors.

**Characteristics:**
- "Winner takes more" behaviour
- Reinforces areas with higher weights — they get proportionally more top ranks
- Smaller areas receive fewer high ranks compared to Sainte-Laguë

**Best for:** Situations where strategic focus on key areas is the goal.

---

## WSJF (Weighted Shortest Job First)

**Formula:**

```
WSJF_Score = (Value + Urgency + Risk) / Size
Adjusted_Score = WSJF_Score × RA_Weight × RS_Weight
```

Where:
- `Value`, `Urgency`, `Risk`: IDEA attributes (1–10)
- `Size`: Estimated effort in story points (> 0)
- `RA_Weight`: Normalized weight of the IDEA's Requesting Area within its RS + BudgetGroup
- `RS_Weight`: Normalized strategic weight of the Revenue Stream

**Characteristics:**
- Pure economic value optimization
- Prioritizes high-value, low-effort items regardless of area weights
- Does not use a divisor allocation mechanism — items are simply sorted by score

**Best for:** Maximizing ROI; situations where economic value is the primary criterion.

---

## Comparison

| Characteristic | Sainte-Laguë | D'Hondt | WSJF |
|---------------|:---:|:---:|:---:|
| Proportional allocation | ✓ | ✓ | — |
| Favors smaller areas | ✓ | — | — |
| Reinforces dominant areas | — | ✓ | — |
| Uses IDEA WSJF scores | — | — | ✓ |
| Area weights influence ranking | ✓ | ✓ | ✓ (adjusted) |
| Mathematical basis | Divisor method | Divisor method | Cost-of-delay |

---

## Per-Queue Method Selection

Starting in v3.3, each queue can use a different algorithm. Example:

```bash
python3 tom_demand.py prioritize \
  --ideas data/input/ideas202602.csv \
  --ra-weights data/input/weights_ra.csv \
  --rs-weights data/input/weights_rs.csv \
  --bg-rs-weights data/input/weights_bg_rs.csv \
  --now-method wsjf \       # Maximize ROI on active development
  --next-method wsjf \      # Maximize ROI on execution-ready items
  --later-method sainte-lague \  # Balanced allocation for planning
  --output-dir data/output
```

See [docs/guides/USER_GUIDE.md](../guides/USER_GUIDE.md) for full CLI options.

---

## Source Files

| Algorithm | File |
|-----------|------|
| Sainte-Laguë | `src/algorithms/sainte_lague.py` |
| D'Hondt | `src/algorithms/dhondt.py` |
| WSJF | `src/algorithms/wsjf.py` |
