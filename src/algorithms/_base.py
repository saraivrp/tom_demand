"""
Shared helpers for proportional allocation algorithms (Sainte-Laguë and D'Hondt).
"""

from typing import Dict, List, Set


def group_items_by_entity(items: List[Dict], level: str) -> Dict[str, List[Dict]]:
    """
    Group items by entity (RA or RS) sorted by internal priority.

    Args:
        items: List of items to group
        level: 'RS' (group by RequestingArea), 'BudgetGroup' (group by BudgetGroup),
            or 'Global' (group by RevenueStream)

    Returns:
        Dictionary mapping entity to sorted list of items
    """
    if level == 'RS':
        entity_key = 'RequestingArea'
    elif level == 'BudgetGroup':
        entity_key = 'BudgetGroup'
    else:
        entity_key = 'RevenueStream'

    grouped: Dict[str, List[Dict]] = {}
    for item in items:
        entity = item[entity_key]
        if entity not in grouped:
            grouped[entity] = []
        grouped[entity].append(item)

    # Sort items within each entity by internal priority
    if level == 'RS':
        for entity in grouped:
            grouped[entity].sort(key=lambda x: x['PriorityRA'])
    else:
        for entity in grouped:
            grouped[entity].sort(key=lambda x: x['Rank_RS'])

    return grouped


def has_remaining_items(
    entity: str,
    items_by_entity: Dict[str, List[Dict]],
    allocated_ids: Set,
) -> bool:
    """
    Check if entity has items not yet allocated.

    Args:
        entity: Entity identifier
        items_by_entity: Dictionary of items grouped by entity
        allocated_ids: Set of already-allocated item IDs

    Returns:
        True if entity has remaining items, False otherwise
    """
    if entity not in items_by_entity:
        return False
    return any(item['ID'] not in allocated_ids for item in items_by_entity[entity])


def get_next_item(
    entity: str,
    items_by_entity: Dict[str, List[Dict]],
    allocated_ids: Set,
) -> Dict:
    """
    Get next unallocated item from entity.

    Args:
        entity: Entity identifier
        items_by_entity: Dictionary of items grouped by entity
        allocated_ids: Set of already-allocated item IDs

    Returns:
        Next item to allocate (as a copy)
    """
    for item in items_by_entity[entity]:
        if item['ID'] not in allocated_ids:
            return item.copy()
    raise ValueError(f"No remaining items for entity {entity}")
