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

        # Get locale settings for European CSV format
        self.locale = self.config.get('locale', {})
        self.csv_delimiter = self.locale.get('csv_delimiter', ';')
        self.decimal_separator = self.locale.get('decimal_separator', ',')

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
