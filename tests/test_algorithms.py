"""
Tests for proportional allocation algorithms: _base helpers, Sainte-Laguë, D'Hondt.
"""

import pytest

from src.algorithms._base import group_items_by_entity, has_remaining_items, get_next_item
from src.algorithms.sainte_lague import sainte_lague_allocate
from src.algorithms.dhondt import dhondt_allocate


# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------

def _rs_items():
    """Minimal items for RS-level (grouped by RequestingArea, sorted by PriorityRA)."""
    return [
        {"ID": "A1", "RequestingArea": "RA1", "PriorityRA": 1},
        {"ID": "A2", "RequestingArea": "RA1", "PriorityRA": 2},
        {"ID": "B1", "RequestingArea": "RA2", "PriorityRA": 1},
        {"ID": "B2", "RequestingArea": "RA2", "PriorityRA": 2},
    ]


def _global_items():
    """Minimal items for Global-level (grouped by RevenueStream, sorted by Rank_RS)."""
    return [
        {"ID": "A1", "RevenueStream": "eCommerce", "Rank_RS": 1},
        {"ID": "A2", "RevenueStream": "eCommerce", "Rank_RS": 2},
        {"ID": "B1", "RevenueStream": "Mail", "Rank_RS": 1},
    ]


def _bg_items():
    """Minimal items for BudgetGroup-level (grouped by BudgetGroup, sorted by Rank_RS)."""
    return [
        {"ID": "A1", "BudgetGroup": "Commercial", "Rank_RS": 1},
        {"ID": "B1", "BudgetGroup": "Operations", "Rank_RS": 1},
    ]


# ---------------------------------------------------------------------------
# _base: group_items_by_entity
# ---------------------------------------------------------------------------

class TestGroupItemsByEntity:
    def test_rs_level_groups_by_requesting_area(self):
        grouped = group_items_by_entity(_rs_items(), level="RS")
        assert set(grouped.keys()) == {"RA1", "RA2"}
        assert [i["ID"] for i in grouped["RA1"]] == ["A1", "A2"]

    def test_global_level_groups_by_revenue_stream(self):
        grouped = group_items_by_entity(_global_items(), level="Global")
        assert set(grouped.keys()) == {"eCommerce", "Mail"}
        assert [i["ID"] for i in grouped["eCommerce"]] == ["A1", "A2"]

    def test_budget_group_level_groups_by_budget_group(self):
        grouped = group_items_by_entity(_bg_items(), level="BudgetGroup")
        assert set(grouped.keys()) == {"Commercial", "Operations"}

    def test_rs_level_sorted_by_priority_ra(self):
        items = [
            {"ID": "A2", "RequestingArea": "RA1", "PriorityRA": 2},
            {"ID": "A1", "RequestingArea": "RA1", "PriorityRA": 1},
        ]
        grouped = group_items_by_entity(items, level="RS")
        assert grouped["RA1"][0]["ID"] == "A1"

    def test_global_level_sorted_by_rank_rs(self):
        items = [
            {"ID": "A3", "RevenueStream": "eCommerce", "Rank_RS": 3},
            {"ID": "A1", "RevenueStream": "eCommerce", "Rank_RS": 1},
            {"ID": "A2", "RevenueStream": "eCommerce", "Rank_RS": 2},
        ]
        grouped = group_items_by_entity(items, level="Global")
        assert [i["Rank_RS"] for i in grouped["eCommerce"]] == [1, 2, 3]

    def test_empty_items_returns_empty_dict(self):
        assert group_items_by_entity([], level="RS") == {}


# ---------------------------------------------------------------------------
# _base: has_remaining_items
# ---------------------------------------------------------------------------

class TestHasRemainingItems:
    def test_returns_true_when_entity_has_unallocated(self):
        grouped = group_items_by_entity(_rs_items(), level="RS")
        assert has_remaining_items("RA1", grouped, allocated_ids=set()) is True

    def test_returns_false_when_all_items_allocated(self):
        grouped = group_items_by_entity(_rs_items(), level="RS")
        assert has_remaining_items("RA1", grouped, allocated_ids={"A1", "A2"}) is False

    def test_returns_false_for_unknown_entity(self):
        grouped = group_items_by_entity(_rs_items(), level="RS")
        assert has_remaining_items("RA_MISSING", grouped, allocated_ids=set()) is False

    def test_returns_true_when_one_of_two_allocated(self):
        grouped = group_items_by_entity(_rs_items(), level="RS")
        assert has_remaining_items("RA1", grouped, allocated_ids={"A1"}) is True


# ---------------------------------------------------------------------------
# _base: get_next_item
# ---------------------------------------------------------------------------

class TestGetNextItem:
    def test_returns_first_unallocated_item(self):
        grouped = group_items_by_entity(_rs_items(), level="RS")
        item = get_next_item("RA1", grouped, allocated_ids=set())
        assert item["ID"] == "A1"

    def test_skips_already_allocated_items(self):
        grouped = group_items_by_entity(_rs_items(), level="RS")
        item = get_next_item("RA1", grouped, allocated_ids={"A1"})
        assert item["ID"] == "A2"

    def test_returns_a_copy_not_a_reference(self):
        grouped = group_items_by_entity(_rs_items(), level="RS")
        item = get_next_item("RA1", grouped, allocated_ids=set())
        item["ID"] = "MUTATED"
        assert grouped["RA1"][0]["ID"] == "A1"

    def test_raises_when_no_remaining_items(self):
        grouped = group_items_by_entity(_rs_items(), level="RS")
        with pytest.raises(ValueError, match="No remaining items"):
            get_next_item("RA1", grouped, allocated_ids={"A1", "A2"})


# ---------------------------------------------------------------------------
# Sainte-Laguë
# ---------------------------------------------------------------------------

class TestSainteLague:
    def test_raises_on_empty_entities(self):
        with pytest.raises(ValueError, match="no entities"):
            sainte_lague_allocate([], {}, _rs_items(), level="RS")

    def test_returns_all_items_ranked(self):
        entities = ["RA1", "RA2"]
        weights = {"RA1": 60, "RA2": 40}
        result = sainte_lague_allocate(entities, weights, _rs_items(), level="RS")
        assert len(result) == 4
        ranks = sorted(r["Rank"] for r in result)
        assert ranks == [1, 2, 3, 4]

    def test_method_tag_is_sainte_lague(self):
        entities = ["RA1"]
        weights = {"RA1": 100}
        items = [{"ID": "A1", "RequestingArea": "RA1", "PriorityRA": 1}]
        result = sainte_lague_allocate(entities, weights, items, level="RS")
        assert result[0]["Method"] == "SainteLague"

    def test_higher_weight_entity_gets_more_slots(self):
        """RA1 has 3× the weight of RA2 → should claim more top positions."""
        entities = ["RA1", "RA2"]
        weights = {"RA1": 75, "RA2": 25}
        items = [
            {"ID": "A1", "RequestingArea": "RA1", "PriorityRA": 1},
            {"ID": "A2", "RequestingArea": "RA1", "PriorityRA": 2},
            {"ID": "A3", "RequestingArea": "RA1", "PriorityRA": 3},
            {"ID": "B1", "RequestingArea": "RA2", "PriorityRA": 1},
        ]
        result = sainte_lague_allocate(entities, weights, items, level="RS")
        ra1_ranks = sorted(r["Rank"] for r in result if r["RequestingArea"] == "RA1")
        ra2_ranks = sorted(r["Rank"] for r in result if r["RequestingArea"] == "RA2")
        assert min(ra1_ranks) < min(ra2_ranks)

    def test_single_entity_all_items_ranked_in_order(self):
        entities = ["RA1"]
        weights = {"RA1": 100}
        items = [
            {"ID": "A1", "RequestingArea": "RA1", "PriorityRA": 1},
            {"ID": "A2", "RequestingArea": "RA1", "PriorityRA": 2},
            {"ID": "A3", "RequestingArea": "RA1", "PriorityRA": 3},
        ]
        result = sainte_lague_allocate(entities, weights, items, level="RS")
        assert [r["ID"] for r in sorted(result, key=lambda x: x["Rank"])] == ["A1", "A2", "A3"]

    def test_global_level_groups_by_revenue_stream(self):
        entities = ["eCommerce", "Mail"]
        weights = {"eCommerce": 50, "Mail": 50}
        result = sainte_lague_allocate(entities, weights, _global_items(), level="Global")
        assert len(result) == 3
        assert all("Rank" in r for r in result)


# ---------------------------------------------------------------------------
# D'Hondt
# ---------------------------------------------------------------------------

class TestDHondt:
    def test_returns_all_items_ranked(self):
        entities = ["RA1", "RA2"]
        weights = {"RA1": 60, "RA2": 40}
        result = dhondt_allocate(entities, weights, _rs_items(), level="RS")
        assert len(result) == 4
        ranks = sorted(r["Rank"] for r in result)
        assert ranks == [1, 2, 3, 4]

    def test_method_tag_is_dhondt(self):
        entities = ["RA1"]
        weights = {"RA1": 100}
        items = [{"ID": "A1", "RequestingArea": "RA1", "PriorityRA": 1}]
        result = dhondt_allocate(entities, weights, items, level="RS")
        assert result[0]["Method"] == "DHondt"

    def test_higher_weight_entity_gets_rank_1(self):
        entities = ["RA1", "RA2"]
        weights = {"RA1": 80, "RA2": 20}
        items = [
            {"ID": "A1", "RequestingArea": "RA1", "PriorityRA": 1},
            {"ID": "B1", "RequestingArea": "RA2", "PriorityRA": 1},
        ]
        result = dhondt_allocate(entities, weights, items, level="RS")
        rank1_item = next(r for r in result if r["Rank"] == 1)
        assert rank1_item["RequestingArea"] == "RA1"

    def test_dhondt_favors_larger_weight_more_than_sainte_lague(self):
        """
        D'Hondt (natural divisors) rewards weight dominance more than Sainte-Laguë
        (odd divisors). With a 9:1 weight split and 10 items (9 from RA1, 1 from RA2),
        both allocate all of RA2's single item, but RA1 claims ranks faster under D'Hondt.
        """
        entities = ["RA1", "RA2"]
        weights = {"RA1": 90, "RA2": 10}
        items = (
            [{"ID": f"A{i}", "RequestingArea": "RA1", "PriorityRA": i} for i in range(1, 10)]
            + [{"ID": "B1", "RequestingArea": "RA2", "PriorityRA": 1}]
        )
        sl = sainte_lague_allocate(entities, weights, items, level="RS")
        dh = dhondt_allocate(entities, weights, items, level="RS")

        def rank_of_b1(result):
            return next(r["Rank"] for r in result if r["ID"] == "B1")

        # Under D'Hondt RA1 dominates even harder — B1 gets a later rank
        assert rank_of_b1(dh) >= rank_of_b1(sl)

    def test_single_item_gets_rank_1(self):
        entities = ["RA1"]
        weights = {"RA1": 100}
        items = [{"ID": "X1", "RequestingArea": "RA1", "PriorityRA": 1}]
        result = dhondt_allocate(entities, weights, items, level="RS")
        assert result[0]["Rank"] == 1
        assert result[0]["ID"] == "X1"
