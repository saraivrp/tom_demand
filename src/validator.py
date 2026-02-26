"""
Data validation module for TOM Demand Management System.

This module provides comprehensive validation for IDEAS, RA weights, BG/RS weights, and RS weights.
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import pandas as pd
import yaml
import os


@dataclass
class ValidationResult:
    """Result of a validation operation."""
    is_valid: bool
    errors: List[str]
    warnings: List[str]

    def __str__(self) -> str:
        if self.is_valid:
            msg = "✓ Validation passed"
            if self.warnings:
                msg += f" with {len(self.warnings)} warning(s)"
        else:
            msg = f"✗ Validation failed with {len(self.errors)} error(s)"
        return msg


class Validator:
    """Centralized data validation for TOM Demand System."""

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize validator with configuration.

        Args:
            config_path: Path to config.yaml file. If None, uses default config.
        """
        if config_path is None:
            # Use default config path
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            config_path = os.path.join(base_dir, 'config', 'config.yaml')

        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        self.revenue_streams = self.config['revenue_streams']
        self.budget_groups = self.config['budget_groups']
        self.validation_config = self.config['validation']

    def validate_ideas(self, df: pd.DataFrame, ra_weights: Optional[pd.DataFrame] = None) -> ValidationResult:
        """
        Validate IDEAS dataframe.

        Args:
            df: DataFrame with IDEAs
            ra_weights: Optional DataFrame with RA weights for referential integrity

        Returns:
            ValidationResult with validation status and messages
        """
        errors = []
        warnings = []

        # Check required columns
        required_cols = ['ID', 'Name', 'RequestingArea', 'RevenueStream', 'BudgetGroup', 'PriorityRA']
        optional_cols = ['Value', 'Urgency', 'Risk', 'Size']

        for col in required_cols:
            if col not in df.columns:
                errors.append(f"Missing required column: {col}")

        if errors:
            return ValidationResult(False, errors, warnings)

        # Check for empty values in required columns
        for col in required_cols:
            if df[col].isna().any():
                null_count = df[col].isna().sum()
                errors.append(f"Column '{col}' has {null_count} null value(s)")

        # Check ID uniqueness
        if df['ID'].duplicated().any():
            duplicates = df[df['ID'].duplicated()]['ID'].tolist()
            errors.append(f"Duplicate IDs found: {', '.join(str(d) for d in duplicates[:5])}")

        # Validate RevenueStream values
        invalid_rs = df[~df['RevenueStream'].isin(self.revenue_streams)]
        if not invalid_rs.empty:
            invalid_values = invalid_rs['RevenueStream'].unique().tolist()
            errors.append(f"Invalid Revenue Stream values: {', '.join(str(v) for v in invalid_values)}")
            errors.append(f"Valid values are: {', '.join(self.revenue_streams)}")

        # Validate BudgetGroup values
        invalid_bg = df[~df['BudgetGroup'].isin(self.budget_groups)]
        if not invalid_bg.empty:
            invalid_values = invalid_bg['BudgetGroup'].unique().tolist()
            errors.append(f"Invalid Budget Group values: {', '.join(str(v) for v in invalid_values)}")
            errors.append(f"Valid values are: {', '.join(self.budget_groups)}")

        # Validate PriorityRA sequencing within each RA
        # SARAIVA - IGNORAR PRIO 999, POIS É USADO PARA IDEAS QUE NÃO DEVEM SER CONSIDERADAS NA PRIORITIZAÇÃO (EX: IDEAS DE BAIXA PRIORIDADE OU IDEAS QUE FORAM REJEITADAS)
        for ra in df['RequestingArea'].unique():
            ra_data = df[df['RequestingArea'] == ra]

            # Filter out rows with PriorityRA = 999
            ra_data = ra_data[ra_data['PriorityRA'] != 999].sort_values('PriorityRA')
            
            priorities = ra_data['PriorityRA'].tolist()
            expected = list(range(1, len(priorities) + 1))

            if priorities != expected:
                #errors.append(                    
                warnings.append(
                    f"RequestingArea '{ra}': PriorityRA not sequential. "
                    f"Expected 1-{len(priorities)}, got {priorities}"
                )

        # Validate optional columns if present
        if 'Value' in df.columns:
            value_range = self.validation_config['value_range']
            invalid_value = df[(df['Value'] < value_range[0]) | (df['Value'] > value_range[1])]
            if not invalid_value.empty:
                for idx, row in invalid_value.iterrows():
                    errors.append(
                        f"IDEA {row['ID']}: Value={row['Value']} outside range {value_range}"
                    )

        if 'Urgency' in df.columns:
            urgency_range = self.validation_config['urgency_range']
            invalid_urgency = df[(df['Urgency'] < urgency_range[0]) | (df['Urgency'] > urgency_range[1])]
            if not invalid_urgency.empty:
                for idx, row in invalid_urgency.iterrows():
                    errors.append(
                        f"IDEA {row['ID']}: Urgency={row['Urgency']} outside range {urgency_range}"
                    )

        if 'Risk' in df.columns:
            risk_range = self.validation_config['risk_range']
            invalid_risk = df[(df['Risk'] < risk_range[0]) | (df['Risk'] > risk_range[1])]
            if not invalid_risk.empty:
                for idx, row in invalid_risk.iterrows():
                    errors.append(
                        f"IDEA {row['ID']}: Risk={row['Risk']} outside range {risk_range}"
                    )

        if 'Size' in df.columns:
            size_min = self.validation_config['size_min']
            invalid_size = df[df['Size'] < size_min]
            if not invalid_size.empty:
                for idx, row in invalid_size.iterrows():
                    errors.append(
                        f"IDEA {row['ID']}: Size={row['Size']} must be >= {size_min}"
                    )

        # Validate MicroPhase field
        if 'MicroPhase' not in df.columns:
            warnings.append("MicroPhase column missing - will use default 'Backlog'")
        else:
            valid_phases = self.validation_config.get('valid_micro_phases', [])
            if valid_phases:
                invalid_phases_mask = ~df['MicroPhase'].isin(valid_phases)
                if invalid_phases_mask.any():
                    invalid_phase_values = df[invalid_phases_mask]['MicroPhase'].unique().tolist()
                    errors.append(
                        f"Invalid MicroPhase values found: {', '.join(str(v) for v in invalid_phase_values)}. "
                        f"Valid phases: {', '.join(valid_phases)}"
                    )

        # Check referential integrity with RA weights if provided
        if ra_weights is not None:
            valid_ras = ra_weights['RequestingArea'].unique()
            invalid_ras = df[~df['RequestingArea'].isin(valid_ras)]
            if not invalid_ras.empty:
                missing_ras = invalid_ras['RequestingArea'].unique().tolist()
                errors.append(
                    f"Requesting Areas not found in weights: {', '.join(str(v) for v in missing_ras)}"
                )

        is_valid = len(errors) == 0
        return ValidationResult(is_valid, errors, warnings)

    def validate_ra_weights(self, df: pd.DataFrame) -> ValidationResult:
        """
        Validate RA weights dataframe.

        Args:
            df: DataFrame with RA weights

        Returns:
            ValidationResult with validation status and messages
        """
        errors = []
        warnings = []

        # Check required columns
        required_cols = ['RevenueStream', 'BudgetGroup', 'RequestingArea', 'Weight']
        for col in required_cols:
            if col not in df.columns:
                errors.append(f"Missing required column: {col}")

        if errors:
            return ValidationResult(False, errors, warnings)

        # Check for duplicates
        duplicates = df.duplicated(subset=['RevenueStream', 'BudgetGroup', 'RequestingArea'])
        if duplicates.any():
            dup_rows = df[duplicates][['RevenueStream', 'BudgetGroup', 'RequestingArea']]
            errors.append(f"Duplicate combinations found: {len(dup_rows)} row(s)")

        # Validate weights are positive
        if (df['Weight'] <= 0).any():
            invalid = df[df['Weight'] <= 0]
            errors.append(f"Found {len(invalid)} weight(s) <= 0")

        # Validate RevenueStream values
        invalid_rs = df[~df['RevenueStream'].isin(self.revenue_streams)]
        if not invalid_rs.empty:
            invalid_values = invalid_rs['RevenueStream'].unique().tolist()
            errors.append(f"Invalid Revenue Stream values: {', '.join(str(v) for v in invalid_values)}")

        # Validate BudgetGroup values
        invalid_bg = df[~df['BudgetGroup'].isin(self.budget_groups)]
        if not invalid_bg.empty:
            invalid_values = invalid_bg['BudgetGroup'].unique().tolist()
            errors.append(f"Invalid Budget Group values: {', '.join(str(v) for v in invalid_values)}")

        # Check if weights sum to 100 per (RS, BG) (warning only)
        grouped = df.groupby(['RevenueStream', 'BudgetGroup'])['Weight'].sum()
        for (rs, bg), total in grouped.items():
            if abs(total - 100) > 0.01:  # Allow small floating point errors
                warnings.append(
                    f"Revenue Stream '{rs}' / Budget Group '{bg}': weights sum to {total:.2f}, not 100.0"
                )

        is_valid = len(errors) == 0
        return ValidationResult(is_valid, errors, warnings)

    def validate_bg_rs_weights(self, df: pd.DataFrame) -> ValidationResult:
        """
        Validate Budget Group weights by Revenue Stream dataframe.

        Args:
            df: DataFrame with BG weights per RS

        Returns:
            ValidationResult with validation status and messages
        """
        errors = []
        warnings = []

        # Check required columns
        required_cols = ['RevenueStream', 'BudgetGroup', 'Weight']
        for col in required_cols:
            if col not in df.columns:
                errors.append(f"Missing required column: {col}")

        if errors:
            return ValidationResult(False, errors, warnings)

        # Check for duplicates
        duplicates = df.duplicated(subset=['RevenueStream', 'BudgetGroup'])
        if duplicates.any():
            dup_rows = df[duplicates][['RevenueStream', 'BudgetGroup']]
            errors.append(f"Duplicate combinations found: {len(dup_rows)} row(s)")

        # Validate weights are positive
        if (df['Weight'] <= 0).any():
            invalid = df[df['Weight'] <= 0]
            errors.append(f"Found {len(invalid)} weight(s) <= 0")

        # Validate RevenueStream values
        invalid_rs = df[~df['RevenueStream'].isin(self.revenue_streams)]
        if not invalid_rs.empty:
            invalid_values = invalid_rs['RevenueStream'].unique().tolist()
            errors.append(f"Invalid Revenue Stream values: {', '.join(str(v) for v in invalid_values)}")

        # Validate BudgetGroup values
        invalid_bg = df[~df['BudgetGroup'].isin(self.budget_groups)]
        if not invalid_bg.empty:
            invalid_values = invalid_bg['BudgetGroup'].unique().tolist()
            errors.append(f"Invalid Budget Group values: {', '.join(str(v) for v in invalid_values)}")

        # Check if weights sum to 100 per RS (warning only)
        for rs in df['RevenueStream'].unique():
            total = df[df['RevenueStream'] == rs]['Weight'].sum()
            if abs(total - 100) > 0.01:
                warnings.append(
                    f"Revenue Stream '{rs}': BG weights sum to {total:.2f}, not 100.0"
                )

        is_valid = len(errors) == 0
        return ValidationResult(is_valid, errors, warnings)

    def validate_rs_weights(self, df: pd.DataFrame) -> ValidationResult:
        """
        Validate RS weights dataframe.

        Args:
            df: DataFrame with RS weights

        Returns:
            ValidationResult with validation status and messages
        """
        errors = []
        warnings = []

        # Check required columns
        required_cols = ['RevenueStream', 'Weight']
        for col in required_cols:
            if col not in df.columns:
                errors.append(f"Missing required column: {col}")

        if errors:
            return ValidationResult(False, errors, warnings)

        # Check for duplicates
        if df['RevenueStream'].duplicated().any():
            duplicates = df[df['RevenueStream'].duplicated()]['RevenueStream'].tolist()
            errors.append(f"Duplicate Revenue Streams: {', '.join(str(v) for v in duplicates)}")

        # Validate weights are positive
        if (df['Weight'] <= 0).any():
            invalid = df[df['Weight'] <= 0]
            errors.append(f"Found {len(invalid)} weight(s) <= 0")

        # Validate RevenueStream values
        invalid_rs = df[~df['RevenueStream'].isin(self.revenue_streams)]
        if not invalid_rs.empty:
            invalid_values = invalid_rs['RevenueStream'].unique().tolist()
            errors.append(f"Invalid Revenue Stream values: {', '.join(str(v) for v in invalid_values)}")

        # Check if weights sum to 100 (warning only)
        total_weight = df['Weight'].sum()
        if abs(total_weight - 100) > 0.01:
            warnings.append(f"Weights sum to {total_weight:.2f}, not 100.0")

        is_valid = len(errors) == 0
        return ValidationResult(is_valid, errors, warnings)

    def normalize_weights(self, df: pd.DataFrame, group_by: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Normalize weights to sum to 100 within groups.

        Args:
            df: DataFrame with Weight column
            group_by: Optional list of columns to group by. If None, normalizes all weights together.

        Returns:
            DataFrame with normalized weights
        """
        df = df.copy()

        if group_by:
            for group_values in df[group_by].drop_duplicates().values:
                # Create mask for this group
                mask = pd.Series([True] * len(df))
                for col, val in zip(group_by, group_values):
                    mask &= (df[col] == val)

                # Normalize weights in this group
                total = df.loc[mask, 'Weight'].sum()
                if total > 0:
                    df.loc[mask, 'Weight'] = (df.loc[mask, 'Weight'] / total) * 100
        else:
            # Normalize all weights
            total = df['Weight'].sum()
            if total > 0:
                df['Weight'] = (df['Weight'] / total) * 100

        return df
