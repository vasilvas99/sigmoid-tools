import json
import toml
import os
from pathlib import Path
from warnings import warn

basepath = Path(os.path.dirname(__file__))

JSON_T = "json"
TOML_T = "toml"

config_json = basepath / Path("config.json")
config_toml = basepath / Path("config.toml")


def find_config() -> Path:
    """Tries to find the config file and returns the path to either the TOML or JSON config.
    JSON will always take precedence if both config files exist.

    Returns:
        Path: Path to the found config file
    """
    if config_toml.exists() and config_json.exists():
        warn(
            "Both TOML and JSON configs exist. JSON will take precedence and TOML will be ignored.",
            category=RuntimeWarning,
        )
    if config_json.exists():
        return config_json, JSON_T

    if config_toml.exists():
        return config_toml, TOML_T

    raise FileNotFoundError(
        f"Configuration files not found. Expected to find {config_json} or {config_toml}"
    )


config_path, config_type = find_config()

with open(config_path, "r", encoding="utf-8") as f:
    if config_type == JSON_T:
        SIGMOID_CONFIG = json.load(f)
    elif config_type == TOML_T:
        SIGMOID_CONFIG = toml.load(f)
    else:
        raise ValueError(f"Unrecognized {config_type}. Expected {JSON_T} or {TOML_T}")
