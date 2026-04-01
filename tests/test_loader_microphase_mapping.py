from pathlib import Path

import yaml

from src.loader import Loader


def test_loader_maps_microphase_column_to_micro_phase(tmp_path: Path):
    ideas_csv = tmp_path / "ideas_microphase.csv"
    ideas_csv.write_text(
        "\n".join(
            [
                "ID;Name;RequestingArea;RevenueStream;BudgetGroup;PriorityRA;Microphase",
                "I1;Idea 1;RA1;eCommerce;Commercial;1;In Development",
                "I2;Idea 2;RA1;eCommerce;Commercial;2;Ready for Development",
                "I3;Idea 3;RA1;eCommerce;Commercial;3;Backlog",
                "I4;Idea 4;RA1;eCommerce;Commercial;4;In Production",
            ]
        ),
        encoding="utf-8-sig",
    )

    loader = Loader()
    df = loader.load_ideas(str(ideas_csv))

    assert "MicroPhase" in df.columns
    assert list(df["Queue"]) == ["NOW", "NEXT", "LATER", "PRODUCTION"]


def test_loader_uses_column_aliases_from_config(tmp_path: Path):
    ideas_csv = tmp_path / "ideas_custom_alias.csv"
    ideas_csv.write_text(
        "\n".join(
            [
                "ID;Name;RequestingArea;RevenueStream;BudgetGroup;PriorityRA;My Micro Phase",
                "I1;Idea 1;RA1;eCommerce;Commercial;1;In Development",
            ]
        ),
        encoding="utf-8-sig",
    )

    base_config = Path("config/config.yaml")
    cfg = yaml.safe_load(base_config.read_text(encoding="utf-8"))
    cfg.setdefault("input", {}).setdefault("column_aliases", {})
    cfg["input"]["column_aliases"]["My Micro Phase"] = "MicroPhase"

    custom_config = tmp_path / "config.yaml"
    custom_config.write_text(yaml.safe_dump(cfg, sort_keys=False), encoding="utf-8")

    loader = Loader(config_path=str(custom_config))
    df = loader.load_ideas(str(ideas_csv))

    assert "MicroPhase" in df.columns
    assert df.loc[0, "MicroPhase"] == "In Development"
    assert df.loc[0, "Queue"] == "NOW"
