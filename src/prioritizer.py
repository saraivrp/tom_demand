"""
Main prioritization module for TOM Demand Management System.

This module coordinates the execution of prioritization algorithms
at both Level 2 (by Revenue Stream) and Level 3 (Global).
"""

from typing import Dict, List, Optional
import pandas as pd
import yaml
import os
from algorithms.sainte_lague import sainte_lague_allocate
from algorithms.dhondt import dhondt_allocate
from algorithms.wsjf import wsjf_prioritize, calculate_wsjf


class Prioritizer:
    """Execute prioritization algorithms at different levels."""

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the prioritizer.

        Args:
            config_path: Path to config.yaml file. If None, uses default config.
        """
        if config_path is None:
            # Use default config path
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            config_path = os.path.join(base_dir, 'config', 'config.yaml')

        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        self.queues = self.config.get('queues', {})

    def prioritize_level2(
        self,
        ideas: pd.DataFrame,
        ra_weights: pd.DataFrame,
        method: str = 'sainte-lague'
    ) -> pd.DataFrame:
        """
        Prioritize IDEAs by Revenue Stream using specified method.

        Args:
            ideas: DataFrame with IDEAs
            ra_weights: DataFrame with RA weights
            method: Prioritization method ('sainte-lague', 'dhondt', 'wsjf')

        Returns:
            DataFrame with prioritized IDEAs per RS and method
        """
        method = method.lower()
        if method not in ['sainte-lague', 'dhondt', 'wsjf']:
            raise ValueError(f"Invalid method: {method}. Must be 'sainte-lague', 'dhondt', or 'wsjf'")

        # Calculate WSJF scores for all IDEAs
        ideas_copy = ideas.copy()
        ideas_copy['WSJF_Score'] = ideas_copy.apply(
            lambda row: calculate_wsjf(row.to_dict()),
            axis=1
        )

        all_results = []

        # Process each Revenue Stream separately
        for rs in ideas_copy['RevenueStream'].unique():
            rs_ideas = ideas_copy[ideas_copy['RevenueStream'] == rs].copy()

            # Get RA weights for this RS
            rs_weights_df = ra_weights[ra_weights['RevenueStream'] == rs]

            # Create weights dictionary
            ra_weight_dict = {}
            for _, row in rs_weights_df.iterrows():
                ra = row['RequestingArea']
                if ra in ra_weight_dict:
                    ra_weight_dict[ra] += row['Weight']
                else:
                    ra_weight_dict[ra] = row['Weight']

            # Get list of unique RAs in this RS
            entities = list(ra_weight_dict.keys())

            # Skip this RS if no weights are defined
            if not entities:
                print(f"    ⚠ Warning: No RA weights defined for Revenue Stream '{rs}' - skipping {len(rs_ideas)} IDEAs")
                continue

            # Filter out IDEAs from RAs that don't have weights
            rs_ideas_filtered = rs_ideas[rs_ideas['RequestingArea'].isin(entities)].copy()

            # Check if any IDEAs were excluded
            excluded_count = len(rs_ideas) - len(rs_ideas_filtered)
            if excluded_count > 0:
                excluded_ras = rs_ideas[~rs_ideas['RequestingArea'].isin(entities)]['RequestingArea'].unique()
                print(f"    ⚠ Warning: {excluded_count} IDEAs excluded from '{rs}' (no weights for RAs: {', '.join(excluded_ras)})")

            # Skip if no valid IDEAs remain after filtering
            if len(rs_ideas_filtered) == 0:
                print(f"    ⚠ Warning: No valid IDEAs for Revenue Stream '{rs}' after filtering - skipping")
                continue

            # Convert ideas to list of dicts
            items = rs_ideas_filtered.to_dict('records')

            # Apply the selected method
            if method == 'wsjf':
                ranked_items = wsjf_prioritize(rs_ideas_filtered, ra_weight_dict, level='RS')
            elif method == 'sainte-lague':
                ranked_items = sainte_lague_allocate(entities, ra_weight_dict, items, level='RS')
            else:  # dhondt
                ranked_items = dhondt_allocate(entities, ra_weight_dict, items, level='RS')

            # Store RS-level rank for Level 3 processing
            for item in ranked_items:
                item['Rank_RS'] = item['Rank']

            all_results.extend(ranked_items)

        # Convert back to DataFrame
        result_df = pd.DataFrame(all_results)

        return result_df

    def prioritize_level3(
        self,
        rs_prioritized: pd.DataFrame,
        rs_weights: pd.DataFrame,
        method: str = 'sainte-lague'
    ) -> pd.DataFrame:
        """
        Prioritize IDEAs globally using specified method.

        Args:
            rs_prioritized: DataFrame from Level 2 with Rank_RS column
            rs_weights: DataFrame with RS weights
            method: Prioritization method ('sainte-lague', 'dhondt', 'wsjf')

        Returns:
            DataFrame with global prioritization
        """
        method = method.lower()
        if method not in ['sainte-lague', 'dhondt', 'wsjf']:
            raise ValueError(f"Invalid method: {method}. Must be 'sainte-lague', 'dhondt', or 'wsjf'")

        # Create RS weights dictionary
        rs_weight_dict = dict(zip(rs_weights['RevenueStream'], rs_weights['Weight']))

        # Get list of Revenue Streams
        entities = rs_weights['RevenueStream'].tolist()

        # Convert to list of dicts
        items = rs_prioritized.to_dict('records')

        # Apply the selected method
        if method == 'wsjf':
            ranked_items = wsjf_prioritize(rs_prioritized, rs_weight_dict, level='Global')
        elif method == 'sainte-lague':
            ranked_items = sainte_lague_allocate(entities, rs_weight_dict, items, level='Global')
        else:  # dhondt
            ranked_items = dhondt_allocate(entities, rs_weight_dict, items, level='Global')

        # Convert to DataFrame
        result_df = pd.DataFrame(ranked_items)

        # Rename Rank to GlobalRank for clarity
        result_df['GlobalRank'] = result_df['Rank']
        result_df.drop('Rank', axis=1, inplace=True, errors='ignore')

        return result_df

    def prioritize_all_methods(
        self,
        ideas: pd.DataFrame,
        ra_weights: pd.DataFrame,
        rs_weights: pd.DataFrame
    ) -> Dict[str, pd.DataFrame]:
        """
        Execute all three prioritization methods.

        Args:
            ideas: DataFrame with IDEAs
            ra_weights: DataFrame with RA weights
            rs_weights: DataFrame with RS weights

        Returns:
            Dictionary with results from all methods
            {
                'sainte-lague': DataFrame,
                'dhondt': DataFrame,
                'wsjf': DataFrame
            }
        """
        results = {}

        for method in ['sainte-lague', 'dhondt', 'wsjf']:
            print(f"  → Executing {method.replace('-', ' ').title()} method...")

            # Level 2: By Revenue Stream
            level2_result = self.prioritize_level2(ideas, ra_weights, method)

            # Level 3: Global
            level3_result = self.prioritize_level3(level2_result, rs_weights, method)

            results[method] = {
                'level2': level2_result,
                'level3': level3_result
            }

            print(f"    ✓ {method.replace('-', ' ').title()}: {len(level3_result)} IDEAs prioritized")

        return results

    def compare_methods(
        self,
        results: Dict[str, Dict[str, pd.DataFrame]],
        top_n: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Compare results from different methods.

        Args:
            results: Dictionary with results from all methods
            top_n: Optional limit to top N results

        Returns:
            DataFrame comparing ranks across methods
        """
        comparison_data = []

        # Get all unique IDEA IDs
        idea_ids = set()
        for method_results in results.values():
            idea_ids.update(method_results['level3']['ID'].tolist())

        for idea_id in idea_ids:
            row = {'ID': idea_id}

            for method, method_results in results.items():
                level3_df = method_results['level3']
                idea_row = level3_df[level3_df['ID'] == idea_id]

                if not idea_row.empty:
                    rank = idea_row.iloc[0]['GlobalRank']
                    row[f'{method}_rank'] = rank

                    # Add IDEA details from first method
                    if 'Name' not in row:
                        row['Name'] = idea_row.iloc[0]['Name']
                        row['RevenueStream'] = idea_row.iloc[0]['RevenueStream']
                        row['RequestingArea'] = idea_row.iloc[0]['RequestingArea']
                        row['WSJF_Score'] = idea_row.iloc[0].get('WSJF_Score', 0)

        comparison_df = pd.DataFrame(comparison_data)

        # Calculate rank variance
        rank_columns = [col for col in comparison_df.columns if col.endswith('_rank')]
        if rank_columns:
            comparison_df['rank_variance'] = comparison_df[rank_columns].std(axis=1)

        # Sort by average rank
        if rank_columns:
            comparison_df['avg_rank'] = comparison_df[rank_columns].mean(axis=1)
            comparison_df.sort_values('avg_rank', inplace=True)

        if top_n:
            comparison_df = comparison_df.head(top_n)

        return comparison_df

    def prioritize_with_queues(
        self,
        ideas: pd.DataFrame,
        ra_weights: pd.DataFrame,
        rs_weights: pd.DataFrame,
        queue_methods: Optional[Dict[str, str]] = None,
        default_method: str = 'sainte-lague'
    ) -> pd.DataFrame:
        """
        Prioritize IDEAs with queue-based sequential ranking.

        Each queue can use a different prioritization method at both Level 2 and Level 3.

        - NOW queue: ranks 1 to N (highest priority - development work)
        - NEXT queue: ranks N+1 to M (ready for execution - solution defined)
        - LATER queue: ranks M+1 to P (lower priority - planning work)
        - PRODUCTION: no ranking (null)

        Args:
            ideas: DataFrame with all IDEAs (including Queue column)
            ra_weights: RA weights
            rs_weights: RS weights
            queue_methods: Optional dict mapping queue names to methods (e.g., {'NOW': 'wsjf', 'NEXT': 'dhondt'})
            default_method: Method to use for queues not in queue_methods

        Returns:
            Combined DataFrame with sequential global ranking
        """
        # Helper function to resolve method for each queue
        def get_queue_method(queue_name: str) -> str:
            """Get the method to use for a specific queue."""
            if queue_methods and queue_name in queue_methods:
                return queue_methods[queue_name]
            return default_method

        all_results = []
        current_rank_offset = 0

        # Process queues in order: NOW → NEXT → LATER → PRODUCTION
        queue_order = ['NOW', 'NEXT', 'LATER', 'PRODUCTION']

        for queue_name in queue_order:
            if queue_name not in self.queues:
                continue

            queue_config = self.queues[queue_name]

            # Filter IDEAs for this queue
            queue_ideas = ideas[ideas['Queue'] == queue_name].copy()

            if len(queue_ideas) == 0:
                print(f"  ⚠ No IDEAs in {queue_name} queue")
                continue

            print(f"  → Processing {queue_name} queue: {len(queue_ideas)} IDEAs")

            # Determine method for this queue
            queue_method = get_queue_method(queue_name)

            # Check if this queue should be prioritized
            if not queue_config.get('prioritize', True):
                # PRODUCTION: No ranking
                queue_ideas['GlobalRank'] = None
                queue_ideas['Rank_RS'] = None
                queue_ideas['Method'] = queue_method
                all_results.append(queue_ideas)
                print(f"    ✓ {queue_name}: No ranking (production items)")
                continue

            # Execute prioritization with queue-specific method
            level2_result = self.prioritize_level2(queue_ideas, ra_weights, queue_method)
            level3_result = self.prioritize_level3(level2_result, rs_weights, queue_method)

            # Apply rank offset for sequential ranking
            if current_rank_offset > 0:
                level3_result['GlobalRank'] = level3_result['GlobalRank'] + current_rank_offset

            # Update offset for next queue
            current_rank_offset = level3_result['GlobalRank'].max()

            all_results.append(level3_result)
            print(f"    ✓ {queue_name}: Ranks {int(level3_result['GlobalRank'].min())}-{int(level3_result['GlobalRank'].max())} ({queue_method})")

        # Combine all results
        if not all_results:
            raise ValueError("No IDEAs to prioritize across all queues")

        combined_df = pd.concat(all_results, ignore_index=True)

        # Sort by GlobalRank (nulls last)
        combined_df.sort_values('GlobalRank', na_position='last', inplace=True)

        return combined_df

    def prioritize_all_methods_with_queues(
        self,
        ideas: pd.DataFrame,
        ra_weights: pd.DataFrame,
        rs_weights: pd.DataFrame
    ) -> Dict[str, Dict[str, pd.DataFrame]]:
        """
        Execute all three methods with queue-based ranking.

        Args:
            ideas: DataFrame with all IDEAs (including Queue column)
            ra_weights: RA weights
            rs_weights: RS weights

        Returns:
            Dictionary with results from all methods
        """
        results = {}

        for method in ['sainte-lague', 'dhondt', 'wsjf']:
            print(f"  → Executing {method.replace('-', ' ').title()} method...")

            combined_result = self.prioritize_with_queues(
                ideas, ra_weights, rs_weights, method
            )

            # Split back into level2 and level3 for export compatibility
            results[method] = {
                'level2': combined_result[combined_result['Queue'] != 'PRODUCTION'].copy(),
                'level3': combined_result
            }

            print(f"    ✓ {method.replace('-', ' ').title()}: {len(combined_result)} IDEAs processed")

        return results
