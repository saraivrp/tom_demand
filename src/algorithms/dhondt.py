"""
D'Hondt proportional allocation method.

This method uses natural divisors (1, 2, 3, 4, ...) for seat allocation,
which tends to favor larger parties/groups with higher weights.
"""

from typing import Dict, List

from ._base import group_items_by_entity, has_remaining_items, get_next_item


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
    allocated_ids: set = set()

    # Group items by entity and sort by internal priority
    items_by_entity = group_items_by_entity(items, level)

    # Allocate each position
    for position in range(1, len(items) + 1):
        # Calculate quotients for each entity
        quotients = {}
        for entity in entities:
            if has_remaining_items(entity, items_by_entity, allocated_ids):
                # D'Hondt formula: Weight / (Seats + 1)
                quotients[entity] = weights[entity] / (seats[entity] + 1)
            else:
                quotients[entity] = 0

        # Select entity with highest quotient
        selected_entity = max(quotients, key=quotients.get)

        # Get next unallocated item from selected entity
        next_item = get_next_item(selected_entity, items_by_entity, allocated_ids)

        # Assign rank and method
        next_item['Rank'] = position
        next_item['Method'] = 'DHondt'
        allocation.append(next_item)
        allocated_ids.add(next_item['ID'])

        # Increment seat counter for selected entity
        seats[selected_entity] += 1

    return allocation
