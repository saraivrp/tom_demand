"""CSV-backed reference data operations."""

from __future__ import annotations

import os
import tempfile
from typing import Dict, List, Optional

import pandas as pd
import yaml


class ReferenceDataService:
    """Manages CRUD-like operations for CSV reference data."""

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or self._default_config_path()
        with open(self.config_path, "r") as cfg_file:
            cfg = yaml.safe_load(cfg_file)
        locale = cfg.get("locale", {})
        self.csv_delimiter = locale.get("csv_delimiter", ";")
        self.decimal_separator = locale.get("decimal_separator", ",")

    def read_rows(self, path: str, limit: Optional[int] = None, offset: int = 0) -> Dict:
        df = self._read_csv(path)
        total = len(df)
        if offset < 0:
            offset = 0
        if limit is not None and limit >= 0:
            view = df.iloc[offset : offset + limit]
        else:
            view = df.iloc[offset:]
        return {"path": path, "total": total, "rows": view.to_dict("records")}

    def overwrite_rows(self, path: str, rows: List[Dict]) -> Dict:
        df = pd.DataFrame(rows)
        self._write_csv_atomic(df, path)
        return {"path": path, "count": len(df)}

    def upsert_row(self, path: str, key_column: str, row: Dict) -> Dict:
        if key_column not in row:
            raise ValueError(f"Missing key column '{key_column}' in row payload.")

        key_value = row[key_column]
        df = self._read_csv(path)
        if key_column not in df.columns:
            raise ValueError(f"Key column '{key_column}' not found in CSV.")

        mask = df[key_column].astype(str) == str(key_value)
        if mask.any():
            idx = df.index[mask][0]
            for column, value in row.items():
                if column in df.columns:
                    df.at[idx, column] = value
                else:
                    df[column] = None
                    df.at[idx, column] = value
            action = "updated"
        else:
            for column in row.keys():
                if column not in df.columns:
                    df[column] = None
            df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
            action = "created"

        self._write_csv_atomic(df, path)
        return {"path": path, "action": action, "key": str(key_value)}

    def delete_row(self, path: str, key_column: str, key_value: str) -> Dict:
        df = self._read_csv(path)
        if key_column not in df.columns:
            raise ValueError(f"Key column '{key_column}' not found in CSV.")

        before = len(df)
        df = df[df[key_column].astype(str) != str(key_value)]
        after = len(df)
        deleted = before - after
        self._write_csv_atomic(df, path)
        return {"path": path, "deleted": deleted, "key": str(key_value)}

    def list_requesting_areas(self, ideas_path: str, ra_weights_path: Optional[str] = None) -> Dict:
        ideas_df = self._read_csv(ideas_path)
        values = set(ideas_df.get("RequestingArea", pd.Series(dtype=str)).dropna().astype(str).tolist())
        if ra_weights_path:
            ra_df = self._read_csv(ra_weights_path)
            values.update(
                ra_df.get("RequestingArea", pd.Series(dtype=str)).dropna().astype(str).tolist()
            )
        data = sorted([value for value in values if value])
        return {"count": len(data), "values": data}

    def list_revenue_streams(
        self,
        ideas_path: str,
        rs_weights_path: Optional[str] = None,
        ra_weights_path: Optional[str] = None,
    ) -> Dict:
        ideas_df = self._read_csv(ideas_path)
        values = set(ideas_df.get("RevenueStream", pd.Series(dtype=str)).dropna().astype(str).tolist())
        if rs_weights_path:
            rs_df = self._read_csv(rs_weights_path)
            values.update(
                rs_df.get("RevenueStream", pd.Series(dtype=str)).dropna().astype(str).tolist()
            )
        if ra_weights_path:
            ra_df = self._read_csv(ra_weights_path)
            values.update(
                ra_df.get("RevenueStream", pd.Series(dtype=str)).dropna().astype(str).tolist()
            )
        data = sorted([value for value in values if value])
        return {"count": len(data), "values": data}

    def rename_value(self, files: List[Dict[str, str]], column: str, old_value: str, new_value: str) -> Dict:
        updated_files = []
        total_replaced = 0
        for file_ref in files:
            path = file_ref["path"]
            target_column = file_ref.get("column", column)
            df = self._read_csv(path)
            if target_column not in df.columns:
                continue
            mask = df[target_column].astype(str) == old_value
            replaced = int(mask.sum())
            if replaced > 0:
                df.loc[mask, target_column] = new_value
                self._write_csv_atomic(df, path)
                updated_files.append(path)
                total_replaced += replaced
        return {"updated_files": updated_files, "replaced": total_replaced}

    def _read_csv(self, path: str) -> pd.DataFrame:
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
        return pd.read_csv(path, sep=self.csv_delimiter, decimal=self.decimal_separator)

    def _write_csv_atomic(self, df: pd.DataFrame, path: str) -> None:
        directory = os.path.dirname(path) or "."
        os.makedirs(directory, exist_ok=True)
        fd, temp_path = tempfile.mkstemp(prefix=".tmp_", suffix=".csv", dir=directory)
        os.close(fd)
        try:
            df.to_csv(
                temp_path,
                index=False,
                sep=self.csv_delimiter,
                decimal=self.decimal_separator,
            )
            os.replace(temp_path, path)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    @staticmethod
    def _default_config_path() -> str:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        return os.path.join(base_dir, "config", "config.yaml")
