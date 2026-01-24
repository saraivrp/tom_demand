"""
Data loading module for TOM Demand Management System.

This module provides functions to load and validate input CSV files.
"""

from typing import Optional
import pandas as pd
import yaml
import os
from validator import Validator, ValidationResult


class DataLoadError(Exception):
    """Exception raised when data loading fails."""
    pass


class Loader:
    """Load and validate input data for TOM Demand System."""

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize loader with configuration.

        Args:
            config_path: Path to config.yaml file. If None, uses default config.
        """
        if config_path is None:
            # Use default config path
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            config_path = os.path.join(base_dir, 'config', 'config.yaml')

        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        self.validator = Validator(config_path)
        self.defaults = self.config['defaults']
        self.queues = self.config.get('queues', {})

        # Get locale settings for European CSV format
        self.locale = self.config.get('locale', {})
        self.csv_delimiter = self.locale.get('csv_delimiter', ';')
        self.decimal_separator = self.locale.get('decimal_separator', ',')

    def _determine_queue(self, micro_phase: str) -> str:
        """
        Determine queue (NEXT/NOW/PRODUCTION) based on micro phase.

        Args:
            micro_phase: The micro phase of the IDEA

        Returns:
            Queue name (NEXT, NOW, or PRODUCTION)
        """
        for queue_name, queue_config in self.queues.items():
            if micro_phase in queue_config.get('micro_phases', []):
                return queue_name
        return 'UNKNOWN'  # Will be caught by validation

    def load_ideas(self, filepath: str) -> pd.DataFrame:
        """
        Load and validate ideas from CSV file.

        Args:
            filepath: Path to ideias.csv

        Returns:
            DataFrame with validated IDEAs

        Raises:
            FileNotFoundError: If file doesn't exist
            DataLoadError: If data validation fails
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")

        try:
            df = pd.read_csv(filepath, sep=self.csv_delimiter, decimal=self.decimal_separator)
        except Exception as e:
            raise DataLoadError(f"Failed to read CSV file: {str(e)}")

        # Normalize column names - map common variations to standard names
        column_mapping = {
            'Revenue': 'RevenueStream',
            'Requesting': 'RequestingArea',
            'St Budget': 'BudgetGroup',
            'Gro Micro': 'MicroPhase',
            'Phas Priority': 'PriorityRA',
            'RA Value': 'Value',
            'RA_Value': 'Value'
        }
        
        # Apply column mapping
        for old_name, new_name in column_mapping.items():
            if old_name in df.columns and new_name not in df.columns:
                df.rename(columns={old_name: new_name}, inplace=True)

        # Convert all text columns to string to avoid float issues with empty cells
        text_columns = ['ID', 'Name', 'RequestingArea', 'RevenueStream', 'BudgetGroup', 'MicroPhase']
        for col in text_columns:
            if col in df.columns:
                df[col] = df[col].astype(str)
                # Replace 'nan' string with pandas NaN for proper handling
                df[col] = df[col].replace('nan', pd.NA)
                # Also handle empty strings
                df[col] = df[col].replace('', pd.NA)

        # Check for required columns with null/empty values and provide clear error
        required_cols = ['ID', 'Name', 'RequestingArea', 'RevenueStream', 'BudgetGroup', 'PriorityRA']
        missing_data_errors = []
        for col in required_cols:
            if col in df.columns:
                null_mask = df[col].isna()
                if null_mask.any():
                    null_indices = df[null_mask].index.tolist()
                    # Show first few problematic rows
                    if len(null_indices) <= 3:
                        missing_data_errors.append(
                            f"Column '{col}' has empty/null values in row(s): {null_indices}"
                        )
                    else:
                        missing_data_errors.append(
                            f"Column '{col}' has {len(null_indices)} empty/null values "
                            f"(first rows: {null_indices[:3]})"
                        )
        
        if missing_data_errors:
            error_msg = "Required columns have empty/null values:\n"
            error_msg += "\n".join([f"  - {err}" for err in missing_data_errors])
            error_msg += "\n\nPlease ensure all required columns (ID, Name, RequestingArea, "
            error_msg += "RevenueStream, BudgetGroup, PriorityRA) have values for all rows."
            raise DataLoadError(error_msg)

        # Add default values for optional columns
        if 'Value' not in df.columns:
            df['Value'] = self.defaults['value']
        elif df['Value'].isna().any():
            df['Value'] = df['Value'].fillna(self.defaults['value'])

        if 'Urgency' not in df.columns:
            df['Urgency'] = self.defaults['urgency']
        elif df['Urgency'].isna().any():
            df['Urgency'] = df['Urgency'].fillna(self.defaults['urgency'])

        if 'Risk' not in df.columns:
            df['Risk'] = self.defaults['risk']
        elif df['Risk'].isna().any():
            df['Risk'] = df['Risk'].fillna(self.defaults['risk'])

        if 'Size' not in df.columns:
            df['Size'] = self.defaults['size']
        elif df['Size'].isna().any():
            df['Size'] = df['Size'].fillna(self.defaults['size'])

        # Add default MicroPhase if not present
        if 'MicroPhase' not in df.columns:
            df['MicroPhase'] = self.defaults.get('micro_phase', 'Backlog')
        elif df['MicroPhase'].isna().any():
            df['MicroPhase'] = df['MicroPhase'].fillna(self.defaults.get('micro_phase', 'Backlog'))

        # Determine Queue based on MicroPhase
        df['Queue'] = df['MicroPhase'].apply(self._determine_queue)

        # Validate the dataframe
        validation_result = self.validator.validate_ideas(df)

        if not validation_result.is_valid:
            error_msg = "IDEAS validation failed:\n"
            error_msg += "\n".join([f"  - {err}" for err in validation_result.errors])
            raise DataLoadError(error_msg)

        # Print warnings if any
        if validation_result.warnings:
            print("⚠ Warnings during IDEAS loading:")
            for warning in validation_result.warnings:
                print(f"  - {warning}")

        return df

    def load_ra_weights(self, filepath: str) -> pd.DataFrame:
        """
        Load Requesting Area weights from CSV file.

        Args:
            filepath: Path to weights_ra.csv

        Returns:
            DataFrame with validated RA weights

        Raises:
            FileNotFoundError: If file doesn't exist
            DataLoadError: If data validation fails
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")

        try:
            df = pd.read_csv(filepath, sep=self.csv_delimiter, decimal=self.decimal_separator)
        except Exception as e:
            raise DataLoadError(f"Failed to read CSV file: {str(e)}")

        # Convert text columns to string to avoid float issues
        text_columns = ['RevenueStream', 'BudgetGroup', 'RequestingArea']
        for col in text_columns:
            if col in df.columns:
                df[col] = df[col].astype(str)
                df[col] = df[col].replace('nan', '')

        # Validate the dataframe
        validation_result = self.validator.validate_ra_weights(df)

        if not validation_result.is_valid:
            error_msg = "RA weights validation failed:\n"
            error_msg += "\n".join([f"  - {err}" for err in validation_result.errors])
            raise DataLoadError(error_msg)

        # Handle warnings (e.g., normalize weights if configured)
        if validation_result.warnings:
            print("⚠ Warnings during RA weights loading:")
            for warning in validation_result.warnings:
                print(f"  - {warning}")

            # Auto-normalize if configured
            if self.config['prioritization']['auto_normalize_weights']:
                print("  → Auto-normalizing weights to sum to 100 per Revenue Stream")
                df = self.validator.normalize_weights(df, group_by=['RevenueStream'])

        return df

    def load_rs_weights(self, filepath: str) -> pd.DataFrame:
        """
        Load Revenue Stream weights from CSV file.

        Args:
            filepath: Path to weights_rs.csv

        Returns:
            DataFrame with validated RS weights

        Raises:
            FileNotFoundError: If file doesn't exist
            DataLoadError: If data validation fails
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")

        try:
            df = pd.read_csv(filepath, sep=self.csv_delimiter, decimal=self.decimal_separator)
        except Exception as e:
            raise DataLoadError(f"Failed to read CSV file: {str(e)}")

        # Convert text columns to string to avoid float issues
        if 'RevenueStream' in df.columns:
            df['RevenueStream'] = df['RevenueStream'].astype(str)
            df['RevenueStream'] = df['RevenueStream'].replace('nan', '')

        # Validate the dataframe
        validation_result = self.validator.validate_rs_weights(df)

        if not validation_result.is_valid:
            error_msg = "RS weights validation failed:\n"
            error_msg += "\n".join([f"  - {err}" for err in validation_result.errors])
            raise DataLoadError(error_msg)

        # Handle warnings
        if validation_result.warnings:
            print("⚠ Warnings during RS weights loading:")
            for warning in validation_result.warnings:
                print(f"  - {warning}")

            # Auto-normalize if configured
            if self.config['prioritization']['auto_normalize_weights']:
                print("  → Auto-normalizing weights to sum to 100")
                df = self.validator.normalize_weights(df)

        return df

    def load_all(self, ideas_path: str, ra_weights_path: str, rs_weights_path: str) -> tuple:
        """
        Load all required input files.

        Args:
            ideas_path: Path to ideias.csv
            ra_weights_path: Path to weights_ra.csv
            rs_weights_path: Path to weights_rs.csv

        Returns:
            Tuple of (ideas_df, ra_weights_df, rs_weights_df)

        Raises:
            FileNotFoundError: If any file doesn't exist
            DataLoadError: If validation fails
        """
        print("Loading input files...")

        print(f"  → Loading IDEAS from {ideas_path}")
        ideas = self.load_ideas(ideas_path)
        print(f"    ✓ {len(ideas)} IDEAs loaded successfully")

        print(f"  → Loading RA weights from {ra_weights_path}")
        ra_weights = self.load_ra_weights(ra_weights_path)
        print(f"    ✓ {len(ra_weights)} Requesting Area weights loaded")

        print(f"  → Loading RS weights from {rs_weights_path}")
        rs_weights = self.load_rs_weights(rs_weights_path)
        print(f"    ✓ {len(rs_weights)} Revenue Stream weights loaded")

        # Cross-validate IDEAS with RA weights
        validation_result = self.validator.validate_ideas(ideas, ra_weights)
        if not validation_result.is_valid:
            error_msg = "Cross-validation failed:\n"
            error_msg += "\n".join([f"  - {err}" for err in validation_result.errors])
            raise DataLoadError(error_msg)

        print("✓ All files loaded and validated successfully\n")

        return ideas, ra_weights, rs_weights
