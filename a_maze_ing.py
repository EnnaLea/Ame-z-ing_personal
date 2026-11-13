from __future__  import annotations
import sys
from config_parser import parse_config, Config
from display import run_dislpay
from mazegen import MazeGenerator, solve, path_to_string


def write_output(
    cfg: Config,
    grid: list[list[int]],
    entry: tuple[int,int],
    exit_: tuple[int, int],
    path_str: str,
) -> None:
    """ Write Output file in the requested format

    Args:
        cgf (Config): configuration dto
        grid (list[list[int]]): matrix of the maze
        entry (tuple[int,int]): entry coordinates
        exit_ (tuple[int, int]): exit coordinates
        path_str (str): path of the file
    """
    gen = MazeGenerator(cfg.width, cfg.height, seed=None)
    gen._grid = grid
    lines = gen.to_hex_lines()
    with open(cfg.output_file, "w", encoding="utf-8") as file:
        for line in lines:
            file.write(line + "\n")
            file.write("\n")
            file.write(f"{entry[0]},{entry[1]}\n")
            file.write(f"{exit_[0]},{exit_[1]}\n")
            file.write(path_str + "\n")


def main() -> int:
    """Main of the maze code

    Returns:
        int: return 0 if no errors else 1
    """
    if len(sys.argv) < 2:
        print("Usage: python3 a_maze_ing.py config.txt", file= sys.stderr)
        return 1
    try:
        cfg = parse_config(sys.argv[1])
    except (OSError, ValueError) as e:
        print("f [error] Configuration: {e}", file=sys.stderr)
        return 1
    try:
        gen = MazeGenerator(
            cfg.width, cfg.height, seed=cfg.seed,
            perfect=cfg.perfect, draw_42=True
        )
        grid = gen.generate(

        )
    return 0

