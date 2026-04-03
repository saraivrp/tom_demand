"""
Tests for the Prioritizer class — level 2, level 3, budget groups, queues, compare.
"""

import pandas as pd
import pytest

from src.prioritizer import Prioritizer


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def prioritizer():
    return Prioritizer()


def _make_ideas(rows):
    """Build a minimal ideas DataFrame from a list of partial row dicts."""
    defaults = {
        "Name": "Test Idea",
        "RevenueStream": "eCommerce",
        "BudgetGroup": "Commercial",
        "MicroPhase": "Backlog",
        "Queue": "LATER",
        "Value": 5,
        "Urgency": 3,
        "Risk": 2,
        "Size": 100,
    }
    records = [{**defaults, **row} for row in rows]
    return pd.DataFrame(records)


def _make_ra_weights(rows):
    return pd.DataFrame(rows)


def _make_rs_weights(rows):
    return pd.DataFrame(rows)


def _make_bg_rs_weights(rows):
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# prioritize_level2 — method validation
# ---------------------------------------------------------------------------

class TestPrioritizeLevel2MethodValidation:
    def test_raises_on_invalid_method(self, prioritizer):
        ideas = _make_ideas([{"ID": "A1", "RequestingArea": "RA1", "PriorityRA": 1}])
        ra_weights = _make_ra_weights([{"RevenueStream": "eCommerce", "RequestingArea": "RA1", "Weight": 100}])
        with pytest.raises(ValueError, match="Invalid method"):
            prioritizer.prioritize_level2(ideas, ra_weights, method="unknown")

    def test_accepts_sainte_lague(self, prioritizer):
        ideas = _make_ideas([{"ID": "A1", "RequestingArea": "RA1", "PriorityRA": 1}])
        ra_weights = _make_ra_weights([{"RevenueStream": "eCommerce", "RequestingArea": "RA1", "Weight": 100}])
        result = prioritizer.prioritize_level2(ideas, ra_weights, method="sainte-lague")
        assert not result.empty

    def test_accepts_dhondt(self, prioritizer):
        ideas = _make_ideas([{"ID": "A1", "RequestingArea": "RA1", "PriorityRA": 1}])
        ra_weights = _make_ra_weights([{"RevenueStream": "eCommerce", "RequestingArea": "RA1", "Weight": 100}])
        result = prioritizer.prioritize_level2(ideas, ra_weights, method="dhondt")
        assert not result.empty

    def test_accepts_wsjf(self, prioritizer):
        ideas = _make_ideas([{"ID": "A1", "RequestingArea": "RA1", "PriorityRA": 1}])
        ra_weights = _make_ra_weights([{"RevenueStream": "eCommerce", "RequestingArea": "RA1", "Weight": 100}])
        result = prioritizer.prioritize_level2(ideas, ra_weights, method="wsjf")
        assert not result.empty


# ---------------------------------------------------------------------------
# prioritize_level2 — filtering behaviours
# ---------------------------------------------------------------------------

class TestPrioritizeLevel2Filtering:
    def test_excludes_ideas_with_priority_ra_999(self, prioritizer):
        ideas = _make_ideas([
            {"ID": "A1", "RequestingArea": "RA1", "PriorityRA": 1},
            {"ID": "A2", "RequestingArea": "RA1", "PriorityRA": 999},
        ])
        ra_weights = _make_ra_weights([{"RevenueStream": "eCommerce", "RequestingArea": "RA1", "Weight": 100}])
        result = prioritizer.prioritize_level2(ideas, ra_weights, method="sainte-lague")
        assert "A2" not in result["ID"].values
        assert "A1" in result["ID"].values

    def test_skips_rs_with_no_ra_weights(self, prioritizer, capsys):
        ideas = _make_ideas([
            {"ID": "A1", "RevenueStream": "eCommerce", "RequestingArea": "RA1", "PriorityRA": 1},
            {"ID": "B1", "RevenueStream": "Mail", "RequestingArea": "RA_MAIL", "PriorityRA": 1},
        ])
        # Only weights for eCommerce — Mail has no weights
        ra_weights = _make_ra_weights([{"RevenueStream": "eCommerce", "RequestingArea": "RA1", "Weight": 100}])
        result = prioritizer.prioritize_level2(ideas, ra_weights, method="sainte-lague")
        assert "A1" in result["ID"].values
        assert "B1" not in result["ID"].values

    def test_excludes_ideas_from_ras_without_weights(self, prioritizer):
        ideas = _make_ideas([
            {"ID": "A1", "RequestingArea": "RA1", "PriorityRA": 1},
            {"ID": "A2", "RequestingArea": "RA_MISSING", "PriorityRA": 1},
        ])
        ra_weights = _make_ra_weights([{"RevenueStream": "eCommerce", "RequestingArea": "RA1", "Weight": 100}])
        result = prioritizer.prioritize_level2(ideas, ra_weights, method="sainte-lague")
        assert "A2" not in result["ID"].values

    def test_result_has_rank_rs_column(self, prioritizer):
        ideas = _make_ideas([{"ID": "A1", "RequestingArea": "RA1", "PriorityRA": 1}])
        ra_weights = _make_ra_weights([{"RevenueStream": "eCommerce", "RequestingArea": "RA1", "Weight": 100}])
        result = prioritizer.prioritize_level2(ideas, ra_weights, method="sainte-lague")
        assert "Rank_RS" in result.columns

    def test_wsjf_score_is_calculated(self, prioritizer):
        ideas = _make_ideas([
            {"ID": "A1", "RequestingArea": "RA1", "PriorityRA": 1, "Value": 5, "Urgency": 3, "Risk": 2, "Size": 100},
        ])
        ra_weights = _make_ra_weights([{"RevenueStream": "eCommerce", "RequestingArea": "RA1", "Weight": 100}])
        result = prioritizer.prioritize_level2(ideas, ra_weights, method="sainte-lague")
        assert "WSJF_Score" in result.columns
        assert result.iloc[0]["WSJF_Score"] == pytest.approx((5 + 3 + 2) / 100)


# ---------------------------------------------------------------------------
# prioritize_level3 — method validation
# ---------------------------------------------------------------------------

class TestPrioritizeLevel3:
    def _level2_output(self):
        """Minimal output that would come from prioritize_level2."""
        return pd.DataFrame([
            {"ID": "A1", "RevenueStream": "eCommerce", "Rank_RS": 1, "WSJF_Score": 0.1},
            {"ID": "B1", "RevenueStream": "Mail", "Rank_RS": 1, "WSJF_Score": 0.2},
        ])

    def test_raises_on_invalid_method(self, prioritizer):
        rs_weights = _make_rs_weights([{"RevenueStream": "eCommerce", "Weight": 50}])
        with pytest.raises(ValueError, match="Invalid method"):
            prioritizer.prioritize_level3(self._level2_output(), rs_weights, method="bad")

    def test_returns_global_rank_column(self, prioritizer):
        rs_weights = _make_rs_weights([
            {"RevenueStream": "eCommerce", "Weight": 60},
            {"RevenueStream": "Mail", "Weight": 40},
        ])
        result = prioritizer.prioritize_level3(self._level2_output(), rs_weights, method="sainte-lague")
        assert "GlobalRank" in result.columns
        assert "Rank" not in result.columns

    def test_all_items_appear_in_result(self, prioritizer):
        rs_weights = _make_rs_weights([
            {"RevenueStream": "eCommerce", "Weight": 60},
            {"RevenueStream": "Mail", "Weight": 40},
        ])
        result = prioritizer.prioritize_level3(self._level2_output(), rs_weights, method="dhondt")
        assert set(result["ID"]) == {"A1", "B1"}


# ---------------------------------------------------------------------------
# prioritize_level2_budget_groups
# ---------------------------------------------------------------------------

class TestPrioritizeLevel2BudgetGroups:
    def _rs_prioritized(self):
        return pd.DataFrame([
            {"ID": "A1", "RevenueStream": "eCommerce", "BudgetGroup": "Commercial", "Rank_RS": 1, "WSJF_Score": 0.1},
            {"ID": "A2", "RevenueStream": "eCommerce", "BudgetGroup": "Operations", "Rank_RS": 2, "WSJF_Score": 0.05},
        ])

    def test_empty_dataframe_returns_empty(self, prioritizer):
        result = prioritizer.prioritize_level2_budget_groups(
            pd.DataFrame(), pd.DataFrame(), method="sainte-lague"
        )
        assert result.empty

    def test_wsjf_skips_bg_weighting_keeps_rank_rs(self, prioritizer):
        bg_weights = _make_bg_rs_weights([
            {"RevenueStream": "eCommerce", "BudgetGroup": "Commercial", "Weight": 70},
            {"RevenueStream": "eCommerce", "BudgetGroup": "Operations", "Weight": 30},
        ])
        result = prioritizer.prioritize_level2_budget_groups(
            self._rs_prioritized(), bg_weights, method="wsjf"
        )
        assert "Rank_RS_RA" in result.columns
        assert set(result["ID"]) == {"A1", "A2"}

    def test_sainte_lague_reassigns_rank_rs_by_bg_weights(self, prioritizer):
        bg_weights = _make_bg_rs_weights([
            {"RevenueStream": "eCommerce", "BudgetGroup": "Commercial", "Weight": 70},
            {"RevenueStream": "eCommerce", "BudgetGroup": "Operations", "Weight": 30},
        ])
        result = prioritizer.prioritize_level2_budget_groups(
            self._rs_prioritized(), bg_weights, method="sainte-lague"
        )
        assert "Rank_RS" in result.columns
        assert set(result["ID"]) == {"A1", "A2"}

    def test_skips_rs_with_no_bg_weights(self, prioritizer):
        # No BG weights at all → should fall back to RA ranking
        result = prioritizer.prioritize_level2_budget_groups(
            self._rs_prioritized(),
            pd.DataFrame(columns=["RevenueStream", "BudgetGroup", "Weight"]),
            method="sainte-lague",
        )
        assert "Rank_RS_RA" in result.columns

class TestDemandServiceDiscardedOutput:
    def test_discarded_output_and_reasons(self, tmp_path):
        from src.services.demand_service import DemandService

        ideas = pd.DataFrame([
            {"ID": "A1", "Name": "I1", "RevenueStream": "eCommerce", "RequestingArea": "RA1", "BudgetGroup": "Commercial", "MicroPhase": "Backlog", "PriorityRA": 1, "Value": 1, "Urgency": 1, "Risk": 1, "Size": 10},
            {"ID": "A2", "Name": "I2", "RevenueStream": "eCommerce", "RequestingArea": "RA1", "BudgetGroup": "Commercial", "MicroPhase": "Backlog", "PriorityRA": 999, "Value": 1, "Urgency": 1, "Risk": 1, "Size": 10},
            {"ID": "A3", "Name": "I3", "RevenueStream": "eCommerce", "RequestingArea": "RA_MISS", "BudgetGroup": "Commercial", "MicroPhase": "Backlog", "PriorityRA": 1, "Value": 1, "Urgency": 1, "Risk": 1, "Size": 10},
            {"ID": "A4", "Name": "I4", "RevenueStream": "eCommerce", "RequestingArea": "RA1", "BudgetGroup": "Commercial", "MicroPhase": "Backlog", "PriorityRA": 2, "Value": 1, "Urgency": 1, "Risk": 1, "Size": 10},
        ])
        ra_weights = pd.DataFrame([
            {"RevenueStream": "eCommerce", "BudgetGroup": "Commercial", "RequestingArea": "RA1", "Weight": 100},
            {"RevenueStream": "Mail", "BudgetGroup": "Commercial", "RequestingArea": "RA_MISS", "Weight": 100},
        ])
        rs_weights = pd.DataFrame([{"RevenueStream": "eCommerce", "Weight": 100}])
        bg_weights = pd.DataFrame([{"RevenueStream": "eCommerce", "BudgetGroup": "Commercial", "Weight": 100}])

        ideas_file = tmp_path / 'ideas.csv'
        ra_file = tmp_path / 'weights_ra.csv'
        rs_file = tmp_path / 'weights_rs.csv'
        bg_file = tmp_path / 'weights_bg_rs.csv'

        ideas.to_csv(ideas_file, sep=';', index=False)
        ra_weights.to_csv(ra_file, sep=';', index=False)
        rs_weights.to_csv(rs_file, sep=';', index=False)
        bg_weights.to_csv(bg_file, sep=';', index=False)

        svc = DemandService()
        result = svc.prioritize(
            ideas=str(ideas_file),
            ra_weights=str(ra_file),
            rs_weights=str(rs_file),
            bg_rs_weights=str(bg_file),
            output_dir=str(tmp_path),
            method='sainte-lague',
            all_methods=False,
            include_discarded=True,
        )

        assert result['generated_rows'] == 2
        assert result['discarded_rows'] == 2
        assert result['discarded_reasons']['priority_ra_999'] == 1
        assert result['discarded_reasons']['missing_ra_weights'] == 1
        assert result['discarded_reasons']['unknown_queue'] == 0

        discarded_file = tmp_path / 'discarded_ideas.csv'
        assert discarded_file.exists()
        discarded_csv = pd.read_csv(discarded_file, sep=';')
        assert 'discard_reason' in discarded_csv.columns
        assert set(discarded_csv['discard_reason']) == {'priority_ra_999', 'missing_ra_weights'}

# ---------------------------------------------------------------------------
# prioritize_all_methods
# ---------------------------------------------------------------------------

class TestPrioritizeAllMethods:
    def _build_data(self):
        ideas = _make_ideas([
            {"ID": "A1", "RequestingArea": "RA1", "PriorityRA": 1},
            {"ID": "A2", "RequestingArea": "RA1", "PriorityRA": 2},
            {"ID": "B1", "RequestingArea": "RA2", "PriorityRA": 1},
        ])
        ra_weights = _make_ra_weights([
            {"RevenueStream": "eCommerce", "RequestingArea": "RA1", "Weight": 60},
            {"RevenueStream": "eCommerce", "RequestingArea": "RA2", "Weight": 40},
        ])
        rs_weights = _make_rs_weights([{"RevenueStream": "eCommerce", "Weight": 100}])
        bg_rs_weights = _make_bg_rs_weights([
            {"RevenueStream": "eCommerce", "BudgetGroup": "Commercial", "Weight": 100}
        ])
        return ideas, ra_weights, rs_weights, bg_rs_weights

    def test_returns_all_three_methods(self, prioritizer):
        ideas, ra_w, rs_w, bg_w = self._build_data()
        results = prioritizer.prioritize_all_methods(ideas, ra_w, rs_w, bg_w)
        assert set(results.keys()) == {"sainte-lague", "dhondt", "wsjf"}

    def test_each_method_has_level2_and_level3(self, prioritizer):
        ideas, ra_w, rs_w, bg_w = self._build_data()
        results = prioritizer.prioritize_all_methods(ideas, ra_w, rs_w, bg_w)
        for method_results in results.values():
            assert "level2" in method_results
            assert "level3" in method_results

    def test_all_ideas_present_in_each_result(self, prioritizer):
        ideas, ra_w, rs_w, bg_w = self._build_data()
        results = prioritizer.prioritize_all_methods(ideas, ra_w, rs_w, bg_w)
        for method, method_results in results.items():
            ids = set(method_results["level3"]["ID"])
            assert {"A1", "A2", "B1"} == ids, f"Missing IDs in {method}"


# ---------------------------------------------------------------------------
# compare_methods
# ---------------------------------------------------------------------------

class TestCompareMethods:
    def _run_all(self, prioritizer):
        ideas = _make_ideas([
            {"ID": "A1", "RequestingArea": "RA1", "PriorityRA": 1},
            {"ID": "A2", "RequestingArea": "RA1", "PriorityRA": 2},
            {"ID": "B1", "RequestingArea": "RA2", "PriorityRA": 1},
        ])
        ra_weights = _make_ra_weights([
            {"RevenueStream": "eCommerce", "RequestingArea": "RA1", "Weight": 60},
            {"RevenueStream": "eCommerce", "RequestingArea": "RA2", "Weight": 40},
        ])
        rs_weights = _make_rs_weights([{"RevenueStream": "eCommerce", "Weight": 100}])
        bg_rs_weights = _make_bg_rs_weights([
            {"RevenueStream": "eCommerce", "BudgetGroup": "Commercial", "Weight": 100}
        ])
        return prioritizer.prioritize_all_methods(ideas, ra_weights, rs_weights, bg_rs_weights)

    def test_produces_rank_variance_column(self, prioritizer):
        results = self._run_all(prioritizer)
        comparison = prioritizer.compare_methods(results)
        assert "rank_variance" in comparison.columns

    def test_produces_avg_rank_column(self, prioritizer):
        results = self._run_all(prioritizer)
        comparison = prioritizer.compare_methods(results)
        assert "avg_rank" in comparison.columns

    def test_all_ideas_appear_in_comparison(self, prioritizer):
        results = self._run_all(prioritizer)
        comparison = prioritizer.compare_methods(results)
        assert set(comparison["ID"]) == {"A1", "A2", "B1"}

    def test_top_n_limits_rows(self, prioritizer):
        results = self._run_all(prioritizer)
        comparison = prioritizer.compare_methods(results, top_n=2)
        assert len(comparison) == 2


# ---------------------------------------------------------------------------
# prioritize_with_queues — sequential ranking
# ---------------------------------------------------------------------------

class TestPrioritizeWithQueues:
    def _build_queued_data(self):
        ideas = _make_ideas([
            {"ID": "N1", "RequestingArea": "RA1", "PriorityRA": 1, "MicroPhase": "In Development", "Queue": "NOW"},
            {"ID": "N2", "RequestingArea": "RA1", "PriorityRA": 2, "MicroPhase": "In Development", "Queue": "NOW"},
            {"ID": "X1", "RequestingArea": "RA1", "PriorityRA": 1, "MicroPhase": "Ready for Development", "Queue": "NEXT"},
            {"ID": "P1", "RequestingArea": "RA1", "PriorityRA": 1, "MicroPhase": "In Production", "Queue": "PRODUCTION"},
        ])
        ra_weights = _make_ra_weights([{"RevenueStream": "eCommerce", "RequestingArea": "RA1", "Weight": 100}])
        rs_weights = _make_rs_weights([{"RevenueStream": "eCommerce", "Weight": 100}])
        bg_rs_weights = _make_bg_rs_weights([
            {"RevenueStream": "eCommerce", "BudgetGroup": "Commercial", "Weight": 100}
        ])
        return ideas, ra_weights, rs_weights, bg_rs_weights

    def test_production_items_have_null_rank(self, prioritizer):
        ideas, ra_w, rs_w, bg_w = self._build_queued_data()
        result = prioritizer.prioritize_with_queues(ideas, ra_w, rs_w, bg_w)
        prod_rows = result[result["Queue"] == "PRODUCTION"]
        assert prod_rows["GlobalRank"].isna().all()

    def test_now_ranks_start_at_1(self, prioritizer):
        ideas, ra_w, rs_w, bg_w = self._build_queued_data()
        result = prioritizer.prioritize_with_queues(ideas, ra_w, rs_w, bg_w)
        now_ranks = result[result["Queue"] == "NOW"]["GlobalRank"].dropna()
        assert now_ranks.min() == 1

    def test_next_ranks_continue_after_now(self, prioritizer):
        ideas, ra_w, rs_w, bg_w = self._build_queued_data()
        result = prioritizer.prioritize_with_queues(ideas, ra_w, rs_w, bg_w)
        now_max = result[result["Queue"] == "NOW"]["GlobalRank"].max()
        next_min = result[result["Queue"] == "NEXT"]["GlobalRank"].min()
        assert next_min > now_max

    def test_all_rankable_ideas_have_unique_ranks(self, prioritizer):
        ideas, ra_w, rs_w, bg_w = self._build_queued_data()
        result = prioritizer.prioritize_with_queues(ideas, ra_w, rs_w, bg_w)
        ranked = result["GlobalRank"].dropna()
        assert ranked.nunique() == len(ranked)
