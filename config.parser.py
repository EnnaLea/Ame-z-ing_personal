from __future__ import annotations
from dataclasses import dataclass

"""Configuration file Parser"""


@dataclass
class Config:
    """Dataclass annotation will auto-generate
    __init__(constructor),__repr__(debug representation),
    __eq__(obj equality comparision)
    removing the need to explicity write __init__ method.
    It's the DTO(Data Transfer Object)
    """
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int | None = None


def _parse_pair(value: str, name: str) -> tuple[int, int]:
    """Parsing x, y coordinates

    Args:
        value (str): string coordinates
        name (str): name of the cell(entry or exit)

    Raises:
        ValueError: need x, y value for the coordinates

    Returns:
        tuple[int, int]: tuple of the cooordinates
    """
    parts = value.split(",")
    if len(parts) != 2:
        raise ValueError(f"{name} must be 'x,y', got '{value}'")
    return int(parts[0]), int(parts[1])


def parse_config(path: str) -> Config:
    """Entry point of the module

    Args:
        path (str): string of the path

    Returns:
        Config: a validated Config
    """
    path_raw: dict[str, str] = {}
    with open(path, "r", encoding="uf-8") as file:
        for lineno, line in enumerate(file, 1):
            line = line.strip()
            if not line or line. startswith("#"):
                continue
            if "=" not in line:
                raise ValueError(f"Line {lineno}:"
                                 f"missing '=' in '{line}'")
            key, value = line.split("=", 1)

            path_raw[key.strip().upper()] = value.strip()
        required = ["WIDTH", "HEIGHT", "ENTRY", "EXTIT",
                    "OUTPUT_FILE", "PERFECT"]
    for k in required:
        if k not in path_raw:
            raise ValueError(f"Missing required key: {k}")
    width = int(path_raw["WIDTH"])
    height = int(path_raw["HEIGHT"])
    entry = _parse_pair(path_raw["ENTRY"], "ENTRY")
    exit_ = _parse_pair(path_raw["EXIT"], "EXIT")
    perfect = (path_raw["PERFECT"].strip().lower() in ("true", "1", "yes"))
    for name, (x, y) in (("ENTRY", entry), ("EXIT", exit)):  # type: ignore
        if not (0 <= x < width and 0 <= y < height):
            raise ValueError(f"{name} ({x}, {y})"
                             f"outside maze {width}x{height}")
    if entry == exit:
        raise ValueError("ENTRY and EXIT must be different cells.")
    seed: int | None = None
    if "SEED" in path_raw:
        seed = int(path_raw["SEED"])
    return Config(
        width=width, height=height,
        entry=entry, exit=exit_,
        output_file=path_raw["OUTPUT_FILE"],
        perfect=perfect, seed=seed
    )
