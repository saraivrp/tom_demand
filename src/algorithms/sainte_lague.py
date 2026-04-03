"""
Sainte-Laguë (Webster) proportional allocation method.

This method uses odd divisors (1, 3, 5, 7, ...) for seat allocation,
which tends to favor balanced distribution across all entities.
"""

from typing import Dict, List

from ._base import group_items_by_entity, has_remaining_items, get_next_item


def sainte_lague_allocate(
    entities: List[str],
    weights: Dict[str, float],
    items: List[Dict],
    level: str
) -> List[Dict]:
    """
    Allocate items using Sainte-Laguë method.

    Algorithm:
    1. Initialize seat counters to 0 for all entities
    2. For each position from 1 to N:
       a. Calculate quotient for each entity: Q = Weight / (2 * Seats + 1)
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
    if not entities:
        raise ValueError("Sainte-Laguë allocation called with no entities (RA list empty) for level=%r" % (level,))

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
                # Sainte-Laguë formula: Weight / (2 * Seats + 1)
                quotients[entity] = weights[entity] / (2 * seats[entity] + 1)
            else:
                quotients[entity] = 0

        # Select entity with highest quotient
        selected_entity = max(quotients, key=quotients.get)

        # Get next unallocated item from selected entity
        next_item = get_next_item(selected_entity, items_by_entity, allocated_ids)

        # Assign rank and method
        next_item['Rank'] = position
        next_item['Method'] = 'SainteLague'
        allocation.append(next_item)
        allocated_ids.add(next_item['ID'])

        # Increment seat counter for selected entity
        seats[selected_entity] += 1

    return allocation
