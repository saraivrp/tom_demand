#!/usr/bin/env python3
"""
Command-line interface for TOM Demand Management System.

This module provides CLI commands for executing prioritization and validation.
"""

import click
import sys

from loader import DataLoadError
from services import DemandService


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
@click.option('--ideas', type=click.Path(exists=True), help='Path to ideas.csv')
@click.option('--ra-weights', type=click.Path(exists=True), help='Path to weights_ra.csv')
@click.option('--rs-weights', type=click.Path(exists=True), help='Path to weights_rs.csv')
@click.option('--method', default='sainte-lague', type=click.Choice(['sainte-lague', 'dhondt', 'wsjf'], case_sensitive=False), help='Prioritization method')
@click.option('--all-methods', is_flag=True, help='Execute all 3 methods')
@click.option('--now-method', type=click.Choice(['sainte-lague', 'dhondt', 'wsjf'], case_sensitive=False), help='Prioritization method for NOW queue')
@click.option('--next-method', type=click.Choice(['sainte-lague', 'dhondt', 'wsjf'], case_sensitive=False), help='Prioritization method for NEXT queue')
@click.option('--later-method', type=click.Choice(['sainte-lague', 'dhondt', 'wsjf'], case_sensitive=False), help='Prioritization method for LATER queue')
@click.option('--output-dir', default='./data/output', help='Output directory')
@click.option('--config', type=click.Path(exists=True), help='Configuration file path')
def prioritize(ideas, ra_weights, rs_weights, method, all_methods, now_method, next_method, later_method, output_dir, config):
    """
    Execute complete prioritization (Levels 2 and 3).

    This command loads IDEAS and weights, executes the prioritization algorithm(s),
    and exports results to the output directory.
    """
    try:
        click.clear()
        click.echo("=" * 60)
        click.echo("TOM Demand Management System - Queue-Based Prioritization")
        click.echo("=" * 60)
        click.echo()

        # If paths not provided via CLI, prompt user interactively
        if not ideas:
            ideas = click.prompt("Caminho para o ficheiro de IDEIAs (ideas.csv)", type=click.Path(exists=True))
        if not ra_weights:
            ra_weights = click.prompt("Caminho para o ficheiro de pesos RA (weights_ra.csv)", type=click.Path(exists=True))
        if not rs_weights:
            rs_weights = click.prompt("Caminho para o ficheiro de pesos RS (weights_rs.csv)", type=click.Path(exists=True))

        # Validate: per-queue methods are incompatible with --all-methods
        queue_method_flags = [now_method, next_method, later_method]
        if all_methods and any(queue_method_flags):
            raise click.UsageError(
                "Per-queue method flags (--now-method, --next-method, --later-method) "
                "cannot be used with --all-methods. Please use one or the other."
            )

        service = DemandService(config)

        click.echo("Starting queue-based prioritization process...")

        if all_methods:
            click.echo("  → Executing all methods (Sainte-Laguë, D'Hondt, WSJF)")
        else:
            queue_methods = {}
            if now_method:
                queue_methods['NOW'] = now_method.lower()
            if next_method:
                queue_methods['NEXT'] = next_method.lower()
            if later_method:
                queue_methods['LATER'] = later_method.lower()

            default_method = method.lower() if method else 'sainte-lague'

            if queue_methods:
                click.echo("  → Using per-queue methods:")
                for queue, queue_method in queue_methods.items():
                    click.echo(f"     • {queue}: {queue_method.replace('-', ' ').title()}")
                if len(queue_methods) < 3:
                    click.echo(f"     • Other queues: {default_method.replace('-', ' ').title()}")
            else:
                click.echo(f"  → Executing {default_method.replace('-', ' ').title()} method")

        run_result = service.prioritize(
            ideas=ideas,
            ra_weights=ra_weights,
            rs_weights=rs_weights,
            output_dir=output_dir,
            method=method,
            all_methods=all_methods,
            now_method=now_method,
            next_method=next_method,
            later_method=later_method,
        )

        click.echo("✓ Prioritization complete")
        click.echo()

        click.echo("Summary:")
        click.echo(f"  - Total IDEAs: {run_result['ideas_count']}")
        click.echo(f"  - Requesting Areas: {run_result['requesting_areas_count']}")
        click.echo(f"  - Revenue Streams: {run_result['revenue_streams_count']}")
        click.echo()

        if run_result['queue_counts']:
            click.echo("Queue Distribution:")
            for queue_name in ['NOW', 'NEXT', 'PRODUCTION']:
                key = f"{queue_name.lower()}_queue"
                if run_result['queue_counts'].get(key, 0) > 0:
                    click.echo(f"  - {queue_name}: {run_result['queue_counts'][key]} IDEAs")
            click.echo()

        click.echo(f"Execution time: {run_result['elapsed_time']:.2f} seconds")
        click.echo()
        click.echo("=" * 60)

    except click.UsageError as e:
        click.echo(f"❌ Usage Error: {str(e)}", err=True)
        sys.exit(1)
    except (FileNotFoundError, DataLoadError) as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Unexpected error: {str(e)}", err=True)
        import traceback
        traceback.print_exc()
        sys.exit(1)


@cli.command()
@click.option('--ideas', required=True, type=click.Path(exists=True), help='Path to ideas.csv')
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

        service = DemandService(config)
        service.prioritize_rs(ideas=ideas, ra_weights=ra_weights, method=method, output=output)

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

        service = DemandService(config)
        service.prioritize_global(
            rs_prioritized=rs_prioritized,
            rs_weights=rs_weights,
            method=method,
            output=output,
        )

        click.echo("✓ Level 3 prioritization complete")

    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--ideas', required=True, type=click.Path(exists=True), help='Path to ideas.csv')
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

        service = DemandService(config)
        result = service.compare(
            ideas=ideas,
            ra_weights=ra_weights,
            rs_weights=rs_weights,
            output=output,
            top_n=top_n,
        )

        click.echo("✓ Comparison complete")

        comparison = result['comparison']
        if top_n is None or top_n > 10:
            click.echo("\nTop 10 IDEAs (by average rank):")
            click.echo(comparison.head(10).to_string(index=False))

    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--ideas', required=True, type=click.Path(exists=True), help='Path to ideas.csv')
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

        service = DemandService(config)
        summary = service.validate(ideas, ra_weights, rs_weights)

        click.echo("✓ All validations passed")
        click.echo()
        click.echo("Summary:")
        click.echo(f"  - Total IDEAs: {summary['ideas_count']}")
        click.echo(f"  - Requesting Areas: {summary['requesting_areas_count']}")
        click.echo(f"  - Revenue Streams: {summary['revenue_streams_count']}")
        click.echo(f"  - Average IDEA Size: {summary['average_size']:.1f} story points")

    except (FileNotFoundError, DataLoadError) as e:
        click.echo(f"❌ Validation failed: {str(e)}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Unexpected error: {str(e)}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    cli()
