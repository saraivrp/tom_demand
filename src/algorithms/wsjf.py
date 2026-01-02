"""
WSJF (Weighted Shortest Job First) prioritization method.

SAFe method that prioritizes work based on cost of delay divided by job size.
Focuses on economic value independent of organizational structure.
"""

from typing import Dict, List
import pandas as pd


def calculate_wsjf(idea: Dict) -> float:
    """
    Calculate WSJF score: (Value + Urgency + Risk) / Size

    Args:
        idea: Dictionary with IDEA attributes (Value, Urgency, Risk, Size)

    Returns:
        WSJF score (float)
    """
    cost_of_delay = idea['Value'] + idea['Urgency'] + idea['Risk']
    size = idea['Size']

    if size <= 0:
        raise ValueError(f"IDEA {idea['ID']}: Size must be > 0")

    return cost_of_delay / size


def wsjf_prioritize(
    ideas: pd.DataFrame,
    weights: Dict[str, float],
    level: str
) -> List[Dict]:
    """
    Prioritize using WSJF method.

    Algorithm:
    Level 2 (RS):
    1. Calculate WSJF_Score for each IDEA
    2. Apply RA weight: Adjusted_WSJF = WSJF_Score × Weight_RA
    3. Sort by Adjusted_WSJF (descending)
    4. Assign ranks

    Level 3 (Global):
    1. Use Level 2 Adjusted_WSJF
    2. Apply RS weight: Final_WSJF = Adjusted_WSJF × Weight_RS
    3. Sort by Final_WSJF (descending)
    4. Assign global ranks

    Args:
        ideas: DataFrame with IDEAs
        weights: Dictionary with entity weights
        level: Calculation level ('RS' or 'Global')

    Returns:
        List of items with WSJF-based ranks
    """
    # Convert DataFrame to list of dictionaries for processing
    items = ideas.to_dict('records')

    # Calculate base WSJF score if not already present
    for item in items:
        if 'WSJF_Score' not in item or pd.isna(item.get('WSJF_Score')):
            item['WSJF_Score'] = calculate_wsjf(item)

    # Apply weights based on level
    if level == 'RS':
        # Apply RA weight
        entity_key = 'RequestingArea'
        score_key = 'Adjusted_WSJF'

        for item in items:
            entity = item[entity_key]
            if entity in weights:
                item[score_key] = item['WSJF_Score'] * weights[entity]
            else:
                # If weight not found, use weight of 0
                item[score_key] = 0

    else:  # Global
        # Apply RS weight to Adjusted_WSJF from Level 2
        entity_key = 'RevenueStream'
        score_key = 'Final_WSJF'

        for item in items:
            entity = item[entity_key]
            adjusted_wsjf = item.get('Adjusted_WSJF', item['WSJF_Score'])
            if entity in weights:
                item[score_key] = adjusted_wsjf * weights[entity]
            else:
                item[score_key] = 0

    # Sort by the appropriate score (descending)
    sort_key = 'Adjusted_WSJF' if level == 'RS' else 'Final_WSJF'
    items_sorted = sorted(items, key=lambda x: x.get(sort_key, 0), reverse=True)

    # Assign ranks
    for rank, item in enumerate(items_sorted, start=1):
        item['Rank'] = rank
        item['Method'] = 'WSJF'

    return items_sorted
