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
        self._visited: set[tuple[int, int]] = set()
        self._ranum = random.Random(seed)
        self._grid: list[list[int]] = [
            [ALL_WALLS for _ in range(width)] for _ in range(height)
        ]
        self._reserved: set[tuple[int, int]] = set()
        if draw_42:
            self.place_42()

    def place_42(self) -> None:
        """Center '42' pattern if the maze is big enough"""
        pattern_h = len(PATTERN_42)
        pattern_w = len(PATTERN_42[0])
        # create a 1 cell margin around the pattern
        if (self.width < (pattern_w + 2)
            or self.height < (pattern_h + 2)):
            print("[Warning!] Maze too small to draw '42', skipping.")
            return
        offset_x = (self.width - pattern_w) // 2
        offset_y = (self.height - pattern_h) // 2
        for j, row in enumerate(PATTERN_42):
            for i, cell in enumerate(row):
                if cell:
                    x, y = offset_x + i, offset_y + j
                    self._reserved.add((x, y))
                    # all walls closed
                    self._grid[y][x]= ALL_WALLS

    def generate(self) -> list[list[int]]:
        """Execute recursive backtracking
        from (0, 0) and print the grid
        """
        start_x, start_y = self._start_cell()
        self._carve(start_x, start_y)
        if not self.perfect:
            self._add_loops(extra=0.1)
        return self._grid

    def _start_cell(self) -> tuple[int, int]:
        """Find a not reserved cell
           as a start point
        """
        for y in range(self.height):
            for x in range(self.width):
                if (x, y )not in self._reserved:
                    return x, y
        raise RuntimeError("All cells reserved: maze impossible")

    def _carve(self, carve_x: int, carve_y: int) -> None:
        """Recursive backtracking: carve a path from cell.

        Args:
            carve_x (int): horizontal point
            carve_y (int): vertical point
        """
        self._visited.add((carve_x, carve_y))
        directions = [N, S, E, W]
        self._ranum.shuffle(directions)
        for d in directions:
            new_x, new_y = carve_x + DIR_X[d], carve_y + DIR_Y[d]
            if not(0 <= new_x < self.width and 0 <= new_y < self.height):
                continue
            if ((new_x, new_y) in self._reserved or
                (new_x, new_y) in self._visited):
                    continue
            if self._grid[new_y][new_x] == ALL_WALLS and (new_x, new_y) not in self._reserved:
                # open walls from both directions
                # &= bit to bit with assignement operator
                # ~ bit to bit negation
                # we negate bit d and leave the othersas they are -> open wall
                self._grid[carve_y][carve_x] &= ~d
                self._grid[new_y][new_x] &= ~OPPOSITE[d]
                self._carve(new_x, new_y)

    def _add_loops(self, extra: float) -> None:
        """Break the perfection by adding more loops(more open walls)

        Args:
            extra (float): how much percentage of walls will be opened
            es.(extra=0.1 -> 10% of walls to be opened)
        """
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in self._reserved:
                    continue
                for d in (E, S):
                    new_x, new_y = x + DIR_X[d], y + DIR_Y[d]
                    if not (0 <= new_x < self.width and 0 <= new_y < self.height):
                        continue
                    if (new_x, new_y) in self._reserved:
                        continue
                    # & d -> isolating bit of direction d
                    if self._grid[new_y][new_x] & d and self._ranum.random() < extra:
                        self._grid[y][x] &= ~d
                        self._grid[new_y][new_x] &= ~OPPOSITE[d]

    def to_hex_lines(self) -> list[str]:
        """ an esadecimal character per cell.

        Returns:
            list[str]: string of esadecimal character
        """
        return [
            "".join(format(self._grid[y][x], "X") for x in range(self.width))
            for y in range(self.height)
        ]   