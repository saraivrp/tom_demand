#!/usr/bin/env python3
"""
Command-line interface for TOM Demand Management System.

This module provides CLI commands for executing prioritization and validation.
"""

import click
import os
import sys
import time
from datetime import datetime
from typing import Optional

from loader import Loader, DataLoadError
from prioritizer import Prioritizer
from exporter import Exporter
from validator import Validator


@click.group()
@click.version_option(version='3.0.0', prog_name='TOM Demand Manager')
def cli():
    """
    TOM Demand Management System - Prioritization CLI

    A demand prioritization system based on three proportional allocation methods:
    Sainte-Laguë (default), D'Hondt, and WSJF.
    """
    pass


@cli.command()
@click.option('--ideas', required=True, type=click.Path(exists=True), help='Path to ideias.csv')
@click.option('--ra-weights', required=True, type=click.Path(exists=True), help='Path to weights_ra.csv')
@click.option('--rs-weights', required=True, type=click.Path(exists=True), help='Path to weights_rs.csv')
@click.option('--method', default='sainte-lague', type=click.Choice(['sainte-lague', 'dhondt', 'wsjf'], case_sensitive=False), help='Prioritization method')
@click.option('--all-methods', is_flag=True, help='Execute all 3 methods')
@click.option('--output-dir', default='./data/output', help='Output directory')
@click.option('--config', type=click.Path(exists=True), help='Configuration file path')
def prioritize(ideas, ra_weights, rs_weights, method, all_methods, output_dir, config):
    """
    Execute complete prioritization (Levels 2 and 3).

    This command loads IDEAS and weights, executes the prioritization algorithm(s),
    and exports results to the output directory.
    """
    start_time = time.time()

    try:
        click.echo("=" * 60)
        click.echo("TOM Demand Management System - Queue-Based Prioritization")
        click.echo("=" * 60)
        click.echo()

        # Initialize components
        loader = Loader(config)
        prioritizer = Prioritizer(config)
        exporter = Exporter(config)

        # Load data
        ideas_df, ra_weights_df, rs_weights_df = loader.load_all(ideas, ra_weights, rs_weights)

        # Display summary with queue distribution
        click.echo(f"Summary:")
        click.echo(f"  - Total IDEAs: {len(ideas_df)}")
        click.echo(f"  - Requesting Areas: {ideas_df['RequestingArea'].nunique()}")
        click.echo(f"  - Revenue Streams: {ideas_df['RevenueStream'].nunique()}")
        click.echo()

        # Display queue distribution if Queue column exists
        if 'Queue' in ideas_df.columns:
            click.echo(f"Queue Distribution:")
            for queue_name in ['NOW', 'NEXT', 'PRODUCTION']:
                count = len(ideas_df[ideas_df['Queue'] == queue_name])
                if count > 0:
                    click.echo(f"  - {queue_name}: {count} IDEAs")
            click.echo()

        # Execute prioritization
        click.echo("Starting queue-based prioritization process...")

        if all_methods:
            click.echo("  → Executing all methods (Sainte-Laguë, D'Hondt, WSJF)")
            results = prioritizer.prioritize_all_methods_with_queues(ideas_df, ra_weights_df, rs_weights_df)
        else:
            click.echo(f"  → Executing {method.replace('-', ' ').title()} method")
            combined_result = prioritizer.prioritize_with_queues(ideas_df, ra_weights_df, rs_weights_df, method)
            results = {
                method: {
                    'level2': combined_result[combined_result['Queue'] != 'PRODUCTION'].copy(),
                    'level3': combined_result
                }
            }

        click.echo("✓ Prioritization complete")
        click.echo()

        # Export results
        queue_stats = {}
        if 'Queue' in ideas_df.columns:
            for queue_name in ['NOW', 'NEXT', 'PRODUCTION']:
                queue_stats[f'{queue_name.lower()}_queue'] = len(ideas_df[ideas_df['Queue'] == queue_name])

        execution_params = {
            'input_files': {
                'ideas': ideas,
                'ra_weights': ra_weights,
                'rs_weights': rs_weights
            },
            'output_directory': output_dir,
            'methods_executed': list(results.keys()),
            'queue_mode': 'sequential',
            'statistics': {
                'total_ideas': len(ideas_df),
                'total_requesting_areas': ideas_df['RequestingArea'].nunique(),
                'total_revenue_streams': ideas_df['RevenueStream'].nunique(),
                **queue_stats
            }
        }

        exporter.export_all(results, output_dir, execution_params)

        # Display execution time
        elapsed_time = time.time() - start_time
        click.echo(f"Execution time: {elapsed_time:.2f} seconds")
        click.echo()
        click.echo("=" * 60)

    except (FileNotFoundError, DataLoadError) as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Unexpected error: {str(e)}", err=True)
        import traceback
        traceback.print_exc()
        sys.exit(1)


@cli.command()
@click.option('--ideas', required=True, type=click.Path(exists=True), help='Path to ideias.csv')
@click.option('--ra-weights', required=True, type=click.Path(exists=True), help='Path to weights_ra.csv')
@click.option('--method', default='sainte-lague', type=click.Choice(['sainte-lague', 'dhondt', 'wsjf'], case_sensitive=False), help='Prioritization method')
@click.option('--output', required=True, help='Output file path')
@click.option('--config', type=click.Path(exists=True), help='Configuration file path')
def prioritize_rs(ideas, ra_weights, method, output, config):
    """
    Execute Level 2 prioritization only (by Revenue Stream).
    """
    try:
        click.echo("Executing Level 2 prioritization...")

        loader = Loader(config)
        prioritizer = Prioritizer()
        exporter = Exporter(config)

        # Load data
        ideas_df = loader.load_ideas(ideas)
        ra_weights_df = loader.load_ra_weights(ra_weights)

        # Execute Level 2
        result = prioritizer.prioritize_level2(ideas_df, ra_weights_df, method)

        # Export
        exporter.export_rs_prioritization(result, output)

        click.echo("✓ Level 2 prioritization complete")

    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--rs-prioritized', required=True, type=click.Path(exists=True), help='Path to prioritization_rs.csv')
@click.option('--rs-weights', required=True, type=click.Path(exists=True), help='Path to weights_rs.csv')
@click.option('--method', default='sainte-lague', type=click.Choice(['sainte-lague', 'dhondt', 'wsjf'], case_sensitive=False), help='Prioritization method')
@click.option('--output', required=True, help='Output file path')
@click.option('--config', type=click.Path(exists=True), help='Configuration file path')
def prioritize_global(rs_prioritized, rs_weights, method, output, config):
    """
    Execute Level 3 prioritization only (global).
    """
    try:
        click.echo("Executing Level 3 prioritization...")

        loader = Loader(config)
        prioritizer = Prioritizer()
        exporter = Exporter(config)

        # Load data
        import pandas as pd
        import yaml
        # Load config to get locale settings
        if config is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            config_path = os.path.join(base_dir, 'config', 'config.yaml')
        else:
            config_path = config
        with open(config_path, 'r') as f:
            cfg = yaml.safe_load(f)
        locale = cfg.get('locale', {})
        csv_delimiter = locale.get('csv_delimiter', ';')
        decimal_separator = locale.get('decimal_separator', ',')

        rs_df = pd.read_csv(rs_prioritized, sep=csv_delimiter, decimal=decimal_separator)
        rs_weights_df = loader.load_rs_weights(rs_weights)

        # Execute Level 3
        result = prioritizer.prioritize_level3(rs_df, rs_weights_df, method)

        # Export
        exporter.export_demand(result, output)

        click.echo("✓ Level 3 prioritization complete")

    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--ideas', required=True, type=click.Path(exists=True), help='Path to ideias.csv')
@click.option('--ra-weights', required=True, type=click.Path(exists=True), help='Path to weights_ra.csv')
@click.option('--rs-weights', required=True, type=click.Path(exists=True), help='Path to weights_rs.csv')
@click.option('--output', required=True, help='Output file path')
@click.option('--top-n', type=int, default=None, help='Show only top N results')
@click.option('--config', type=click.Path(exists=True), help='Configuration file path')
def compare(ideas, ra_weights, rs_weights, output, top_n, config):
    """
    Compare all 3 prioritization methods.

    This command executes all methods and generates a comparison report
    showing how ranks differ across methods.
    """
    try:
        click.echo("Comparing all 3 prioritization methods...")

        loader = Loader(config)
        prioritizer = Prioritizer()
        exporter = Exporter(config)

        # Load data
        ideas_df, ra_weights_df, rs_weights_df = loader.load_all(ideas, ra_weights, rs_weights)

        # Execute all methods
        results = prioritizer.prioritize_all_methods(ideas_df, ra_weights_df, rs_weights_df)

        # Generate comparison
        comparison = prioritizer.compare_methods(results, top_n)

        # Export
        exporter.export_comparison_report(comparison, output)

        click.echo("✓ Comparison complete")

        # Display top 10 if top_n not specified
        if top_n is None or top_n > 10:
            click.echo("\nTop 10 IDEAs (by average rank):")
            click.echo(comparison.head(10).to_string(index=False))

    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--ideas', required=True, type=click.Path(exists=True), help='Path to ideias.csv')
@click.option('--ra-weights', required=True, type=click.Path(exists=True), help='Path to weights_ra.csv')
@click.option('--rs-weights', required=True, type=click.Path(exists=True), help='Path to weights_rs.csv')
@click.option('--config', type=click.Path(exists=True), help='Configuration file path')
def validate(ideas, ra_weights, rs_weights, config):
    """
    Validate input files without executing prioritization.

    This command checks all input files for structural and data validity.
    """
    try:
        click.echo("✓ Validating input files...")
        click.echo()

        loader = Loader(config)

        # This will validate everything
        ideas_df, ra_weights_df, rs_weights_df = loader.load_all(ideas, ra_weights, rs_weights)

        click.echo("✓ All validations passed")
        click.echo()
        click.echo("Summary:")
        click.echo(f"  - Total IDEAs: {len(ideas_df)}")
        click.echo(f"  - Requesting Areas: {ideas_df['RequestingArea'].nunique()}")
        click.echo(f"  - Revenue Streams: {ideas_df['RevenueStream'].nunique()}")
        avg_size = ideas_df['Size'].mean()
        click.echo(f"  - Average IDEA Size: {avg_size:.1f} story points")

    except (FileNotFoundError, DataLoadError) as e:
        click.echo(f"❌ Validation failed: {str(e)}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Unexpected error: {str(e)}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    cli()
