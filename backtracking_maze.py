from __future__ import annotations
import sys
import random


# Codifica dei muri utilizzando i bit
N, E, S, W = 1, 2, 4, 8

# Tutti i quattro muri chiusi
ALL_WALLS = N | E | S | W

DIR_X :dict[int, int] = {E: 1, W: -1, N: 0, S: 0}
DIR_Y: dict[int, int] = {E: 0, W: 0, N: -1, S: 1}
OPPOSITE: dict[int, int] = {E: W, W: E, N: S, S: N}

# Creazione del pattern "42" con i bit (5 righe x 11 colonne e 1 colonna di spazion)
PATTERN_42: list[list[int]] = [
    [1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0],
    [1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0],
    [1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0],
    [0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0],
    [0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0],
]


class MazeGenerator:
    """Maze generator using the recusive backtracker algorithm

    Example:
        gen = MazeGenerator(width=20, height=15, seed=42)
        grid = gen.generate()
        gen.save_to_file("maze.txt", entry=(0, 0), exit=(19, 14))
    """

    def __init__(
        self, width: int, height: int, seed: int | None,
        perfect: bool = True, draw_42: bool = True,
        ) -> None:
        if width < 2 or height < 2:
            raise ValueError("Maze size must be at least 2x2")
        self.width = width
        self.height = height
        self.perfect = perfect
        self.draw_42 = draw_42
        self._rng = random.Random(seed)
        self._grid: list[list[int]] = [
            [ALL_WALLS for _ in range(width)] for _ in range(height)
        ]
        self._reserved: set[tuple[int, int]] = set()
        if draw_42:
            self.place_42()

    def place_42(self) -> None:
        pass