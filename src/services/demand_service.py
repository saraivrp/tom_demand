"""Shared orchestration services for CLI and API layers."""

from __future__ import annotations

import os
import time
from typing import Dict, Optional

import pandas as pd
import yaml

try:
    # Package import path (e.g. `src.services`)
    from ..exporter import Exporter
    from ..loader import Loader
    from ..prioritizer import Prioritizer
except ImportError:
    # Flat import path used by CLI entrypoint (`tom_demand.py`)
    from exporter import Exporter
    from loader import Loader
    from prioritizer import Prioritizer


class DemandService:
    """Coordinates loading, prioritization, validation, and export workflows."""

    def __init__(self, config: Optional[str] = None):
        self.config = config
        self.loader = Loader(config)
        self.prioritizer = Prioritizer(config)
        self.exporter = Exporter(config)

    def prioritize(
        self,
        ideas: str,
        ra_weights: str,
        rs_weights: str,
        output_dir: str,
        method: str = "sainte-lague",
        all_methods: bool = False,
        now_method: Optional[str] = None,
        next_method: Optional[str] = None,
        later_method: Optional[str] = None,
    ) -> Dict:
        """Execute full prioritization with optional per-queue methods."""
        start_time = time.time()

        queue_methods = {}
        if now_method:
            queue_methods["NOW"] = now_method.lower()
        if next_method:
            queue_methods["NEXT"] = next_method.lower()
        if later_method:
            queue_methods["LATER"] = later_method.lower()

        default_method = method.lower() if method else "sainte-lague"

        ideas_df, ra_weights_df, rs_weights_df = self.loader.load_all(ideas, ra_weights, rs_weights)

        if all_methods:
            results = self.prioritizer.prioritize_all_methods_with_queues(
                ideas_df, ra_weights_df, rs_weights_df
            )
        else:
            combined_result = self.prioritizer.prioritize_with_queues(
                ideas_df,
                ra_weights_df,
                rs_weights_df,
                queue_methods=queue_methods,
                default_method=default_method,
            )

            result_name = "mixed" if queue_methods else default_method
            results = {
                result_name: {
                    "level2": combined_result[combined_result["Queue"] != "PRODUCTION"].copy(),
                    "level3": combined_result,
                }
            }

        queue_stats = {}
        if "Queue" in ideas_df.columns:
            for queue_name in ["NOW", "NEXT", "LATER", "PRODUCTION"]:
                queue_stats[f"{queue_name.lower()}_queue"] = len(
                    ideas_df[ideas_df["Queue"] == queue_name]
                )

        execution_params = {
            "input_files": {
                "ideas": ideas,
                "ra_weights": ra_weights,
                "rs_weights": rs_weights,
            },
            "output_directory": output_dir,
            "methods_executed": list(results.keys()),
            "queue_mode": "sequential",
            "queue_methods": queue_methods if queue_methods else None,
            "default_method": default_method,
            "statistics": {
                "total_ideas": len(ideas_df),
                "total_requesting_areas": ideas_df["RequestingArea"].nunique(),
                "total_revenue_streams": ideas_df["RevenueStream"].nunique(),
                **queue_stats,
            },
        }

        self.exporter.export_all(results, output_dir, execution_params)

        return {
            "elapsed_time": time.time() - start_time,
            "ideas_count": len(ideas_df),
            "requesting_areas_count": ideas_df["RequestingArea"].nunique(),
            "revenue_streams_count": ideas_df["RevenueStream"].nunique(),
            "queue_counts": queue_stats,
            "methods_executed": list(results.keys()),
            "output_directory": output_dir,
            "queue_methods": queue_methods,
            "default_method": default_method,
            "all_methods": all_methods,
        }

    def prioritize_rs(
        self,
        ideas: str,
        ra_weights: str,
        output: str,
        method: str = "sainte-lague",
    ) -> Dict:
        """Execute Level 2 prioritization only."""
        ideas_df = self.loader.load_ideas(ideas)
        ra_weights_df = self.loader.load_ra_weights(ra_weights)
        result = self.prioritizer.prioritize_level2(ideas_df, ra_weights_df, method)
        self.exporter.export_rs_prioritization(result, output)
        return {"output": output, "count": len(result)}

    def prioritize_global(
        self,
        rs_prioritized: str,
        rs_weights: str,
        output: str,
        method: str = "sainte-lague",
    ) -> Dict:
        """Execute Level 3 prioritization only."""
        csv_delimiter, decimal_separator = self._resolve_locale_settings()
        rs_df = pd.read_csv(rs_prioritized, sep=csv_delimiter, decimal=decimal_separator)
        rs_weights_df = self.loader.load_rs_weights(rs_weights)
        result = self.prioritizer.prioritize_level3(rs_df, rs_weights_df, method)
        self.exporter.export_demand(result, output)
        return {"output": output, "count": len(result)}

    def compare(
        self,
        ideas: str,
        ra_weights: str,
        rs_weights: str,
        output: str,
        top_n: Optional[int] = None,
    ) -> Dict:
        """Compare all methods and export report."""
        ideas_df, ra_weights_df, rs_weights_df = self.loader.load_all(ideas, ra_weights, rs_weights)
        results = self.prioritizer.prioritize_all_methods(ideas_df, ra_weights_df, rs_weights_df)
        comparison = self.prioritizer.compare_methods(results, top_n)
        self.exporter.export_comparison_report(comparison, output)
        return {"output": output, "count": len(comparison), "comparison": comparison}

    def validate(self, ideas: str, ra_weights: str, rs_weights: str) -> Dict:
        """Validate all inputs and return summary stats."""
        ideas_df, _, _ = self.loader.load_all(ideas, ra_weights, rs_weights)
        return {
            "ideas_count": len(ideas_df),
            "requesting_areas_count": ideas_df["RequestingArea"].nunique(),
            "revenue_streams_count": ideas_df["RevenueStream"].nunique(),
            "average_size": ideas_df["Size"].mean(),
        }

    def _resolve_locale_settings(self) -> tuple[str, str]:
        """Read locale CSV settings from configuration."""
        config_path = self.config
        if config_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            config_path = os.path.join(base_dir, "config", "config.yaml")

        with open(config_path, "r") as cfg_file:
            cfg = yaml.safe_load(cfg_file)

        locale = cfg.get("locale", {})
        return locale.get("csv_delimiter", ";"), locale.get("decimal_separator", ",")
