"""
Export module for TOM Demand Management System.

This module provides functions to export results to CSV files and metadata to JSON.
"""

from typing import Dict, Optional
import pandas as pd
import json
import os
from datetime import datetime
import yaml


class Exporter:
    """Export prioritization results to CSV and metadata to JSON."""

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize exporter with configuration.

        Args:
            config_path: Path to config.yaml file. If None, uses default config.
        """
        if config_path is None:
            # Use default config path
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            config_path = os.path.join(base_dir, 'config', 'config.yaml')

        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        self.output_config = self.config['output']

        # Get locale settings for European CSV format
        self.locale = self.config.get('locale', {})
        self.csv_delimiter = self.locale.get('csv_delimiter', ';')
        self.decimal_separator = self.locale.get('decimal_separator', ',')

    def export_rs_prioritization(
        self,
        data: pd.DataFrame,
        filepath: str,
        metadata: Optional[Dict] = None
    ) -> None:
        """
        Export Level 2 prioritization to CSV.

        Args:
            data: DataFrame with RS-level prioritization
            filepath: Output file path
            metadata: Optional metadata to include
        """
        # Select and order columns for output
        output_columns = [
            'Queue', 'RevenueStream', 'Method', 'Rank_RS', 'ID', 'Name',
            'RequestingArea', 'BudgetGroup', 'MicroPhase', 'WSJF_Score',
            'Value', 'Urgency', 'Risk', 'Size'
        ]

        # Only include columns that exist
        available_columns = [col for col in output_columns if col in data.columns]

        output_df = data[available_columns].copy()

        # Round decimal values
        precision = self.output_config['decimal_precision']
        if 'WSJF_Score' in output_df.columns:
            output_df['WSJF_Score'] = output_df['WSJF_Score'].round(precision)

        # Sort by RevenueStream and Rank
        output_df.sort_values(['RevenueStream', 'Method', 'Rank_RS'], inplace=True)

        # Ensure output directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        # Export to CSV with European format
        output_df.to_csv(filepath, index=False, sep=self.csv_delimiter, decimal=self.decimal_separator)
        print(f"    ✓ Exported to {filepath}")

    def export_demand(
        self,
        data: pd.DataFrame,
        filepath: str,
        metadata: Optional[Dict] = None
    ) -> None:
        """
        Export Level 3 global prioritization to CSV.

        Args:
            data: DataFrame with global prioritization
            filepath: Output file path
            metadata: Optional metadata to include
        """
        # Select and order columns for output
        output_columns = [
            'Queue', 'Method', 'GlobalRank', 'ID', 'Name',
            'RequestingArea', 'RevenueStream', 'BudgetGroup',
            'MicroPhase', 'PriorityRA', 'WSJF_Score',
            'Value', 'Urgency', 'Risk', 'Size'
        ]

        # Only include columns that exist
        available_columns = [col for col in output_columns if col in data.columns]

        output_df = data[available_columns].copy()

        # Round decimal values
        precision = self.output_config['decimal_precision']
        if 'WSJF_Score' in output_df.columns:
            output_df['WSJF_Score'] = output_df['WSJF_Score'].round(precision)

        # Sort by Queue order (NOW, NEXT, PRODUCTION) then Method and GlobalRank
        if 'Queue' in output_df.columns:
            queue_order = {'NOW': 0, 'NEXT': 1, 'PRODUCTION': 2}
            output_df['_queue_sort'] = output_df['Queue'].map(queue_order)
            output_df.sort_values(
                ['Method', '_queue_sort', 'GlobalRank'],
                na_position='last',
                inplace=True
            )
            output_df.drop('_queue_sort', axis=1, inplace=True)
        else:
            # Fallback to original sorting
            output_df.sort_values(['Method', 'GlobalRank'], inplace=True)

        # Ensure output directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        # Export to CSV with European format
        output_df.to_csv(filepath, index=False, sep=self.csv_delimiter, decimal=self.decimal_separator)
        print(f"    ✓ Exported to {filepath}")

    def export_comparison_report(
        self,
        data: pd.DataFrame,
        filepath: str
    ) -> None:
        """
        Export comparison report of all 3 methods.

        Args:
            data: DataFrame with comparison results
            filepath: Output file path
        """
        # Ensure output directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        # Round decimal values
        precision = self.output_config['decimal_precision']
        numeric_columns = data.select_dtypes(include=['float64']).columns
        for col in numeric_columns:
            data[col] = data[col].round(precision)

        # Export to CSV with European format
        data.to_csv(filepath, index=False, sep=self.csv_delimiter, decimal=self.decimal_separator)
        print(f"    ✓ Comparison report exported to {filepath}")

    def export_metadata(
        self,
        execution_params: Dict,
        filepath: str
    ) -> None:
        """
        Export execution metadata (parameters, timestamps, etc.).

        Args:
            execution_params: Dictionary with execution parameters
            filepath: Output file path (JSON)
        """
        metadata = {
            'execution_timestamp': datetime.now().strftime(self.output_config['date_format']),
            'system_version': '3.0.0',
            **execution_params
        }

        # Ensure output directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        # Export to JSON
        with open(filepath, 'w') as f:
            json.dump(metadata, f, indent=2)

        print(f"    ✓ Metadata exported to {filepath}")

    def export_all(
        self,
        results: Dict[str, Dict[str, pd.DataFrame]],
        output_dir: str,
        execution_params: Optional[Dict] = None
    ) -> None:
        """
        Export all results (Level 2, Level 3, comparison, metadata).

        Args:
            results: Dictionary with results from all methods
            output_dir: Output directory path
            execution_params: Optional execution parameters for metadata
        """
        print("\nExporting results...")

        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Export each method's results
        for method, method_results in results.items():
            method_name = method.replace('-', '_')

            # Export Level 2
            level2_path = os.path.join(output_dir, f'prioritization_rs_{method_name}.csv')
            self.export_rs_prioritization(method_results['level2'], level2_path)

            # Export Level 3
            level3_path = os.path.join(output_dir, f'demand_{method_name}.csv')
            self.export_demand(method_results['level3'], level3_path)

        # Export combined demand file with all methods
        all_demand = []
        for method, method_results in results.items():
            all_demand.append(method_results['level3'])

        combined_demand = pd.concat(all_demand, ignore_index=True)
        
        combined_demand = combined_demand.sort_values(['GlobalRank', 'Queue'], ascending=True, na_position='last', ignore_index=True)
        #print(combined_demand.head(10))

        combined_path = os.path.join(output_dir, 'demand.csv')
        self.export_demand(combined_demand, combined_path)

        # Export metadata if parameters provided
        if execution_params and self.output_config['include_metadata']:
            metadata_path = os.path.join(output_dir, 'metadata.json')
            self.export_metadata(execution_params, metadata_path)

        print("✓ All results exported successfully\n")

        print("top 10 rows of combined demand file:")
        print(combined_demand.head(10))