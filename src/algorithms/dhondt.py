"""
D'Hondt proportional allocation method.

This method uses natural divisors (1, 2, 3, 4, ...) for seat allocation,
which tends to favor larger parties/groups with higher weights.
"""

from typing import Dict, List
import pandas as pd


def dhondt_allocate(
    entities: List[str],
    weights: Dict[str, float],
    items: List[Dict],
    level: str
) -> List[Dict]:
    """
    Allocate items using D'Hondt method.

    Algorithm:
    1. Initialize seat counters to 0 for all entities
    2. For each position from 1 to N:
       a. Calculate quotient for each entity: Q = Weight / (Seats + 1)
       b. Select entity with highest quotient
       c. Allocate next item from that entity
       d. Increment seat counter
    3. Return allocated items with ranks

    Args:
        entities: List of entity identifiers (RAs or RSs)
        weights: Dictionary mapping entities to weights
        items: List of items to allocate
        level: Allocation level ('RS' or 'Global')

    Returns:
        List of items with assigned ranks
    """
    # Initialize seat counters
    seats = {entity: 0 for entity in entities}
    allocation = []

    # Group items by entity and sort by internal priority
    items_by_entity = _group_items_by_entity(items, level)

    # Allocate each position
    for position in range(1, len(items) + 1):
        # Calculate quotients for each entity
        quotients = {}
        for entity in entities:
            if _has_remaining_items(entity, items_by_entity, allocation):
                # D'Hondt formula: Weight / (Seats + 1)
                quotients[entity] = weights[entity] / (seats[entity] + 1)
            else:
                quotients[entity] = 0

        # Select entity with highest quotient
        # In case of tie, use tiebreaker (could be configured)
        selected_entity = max(quotients, key=quotients.get)

        # Get next unallocated item from selected entity
        next_item = _get_next_item(selected_entity, items_by_entity, allocation)

        # Assign rank and method
        next_item['Rank'] = position
        next_item['Method'] = 'DHondt'
        allocation.append(next_item)

        # Increment seat counter for selected entity
        seats[selected_entity] += 1

    return allocation


def _group_items_by_entity(items: List[Dict], level: str) -> Dict[str, List[Dict]]:
    """
    Group items by entity (RA or RS) sorted by internal priority.

    Args:
        items: List of items to group
        level: 'RS' (group by RequestingArea), 'BudgetGroup' (group by BudgetGroup),
            or 'Global' (group by RevenueStream)

    Returns:
        Dictionary mapping entity to sorted list of items
    """
    grouped = {}
    if level == 'RS':
        entity_key = 'RequestingArea'
    elif level == 'BudgetGroup':
        entity_key = 'BudgetGroup'
    else:
        entity_key = 'RevenueStream'

    for item in items:
        entity = item[entity_key]
        if entity not in grouped:
            grouped[entity] = []
        grouped[entity].append(item)

    # Sort items within each entity by internal priority
    if level == 'RS':
        # Sort by PriorityRA
        for entity in grouped:
            grouped[entity].sort(key=lambda x: x['PriorityRA'])
    else:
        # Sort by RS-level rank (used by BudgetGroup and Global steps)
        for entity in grouped:
            grouped[entity].sort(key=lambda x: x['Rank_RS'])

    return grouped


def _has_remaining_items(entity: str, items_by_entity: Dict, allocation: List) -> bool:
    """
    Check if entity has items not yet allocated.

    Args:
        entity: Entity identifier
        items_by_entity: Dictionary of items grouped by entity
        allocation: List of already allocated items

    Returns:
        True if entity has remaining items, False otherwise
    """
    if entity not in items_by_entity:
        return False

    allocated_ids = {item['ID'] for item in allocation}
    entity_items = items_by_entity[entity]

    for item in entity_items:
        if item['ID'] not in allocated_ids:
            return True

    return False


def _get_next_item(entity: str, items_by_entity: Dict, allocation: List) -> Dict:
    """
    Get next unallocated item from entity.

    Args:
        entity: Entity identifier
        items_by_entity: Dictionary of items grouped by entity
        allocation: List of already allocated items

    Returns:
        Next item to allocate (as a copy)
    """
    allocated_ids = {item['ID'] for item in allocation}
    entity_items = items_by_entity[entity]

    for item in entity_items:
        if item['ID'] not in allocated_ids:
            return item.copy()

    raise ValueError(f"No remaining items for entity {entity}")
