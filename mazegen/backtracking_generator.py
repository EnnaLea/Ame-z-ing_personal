from __future__ import annotations
import random

from constants import PATTERN42
from maze_graph import MazeGraph, Cell


class MazeGenerator:
    """Generates a maze by DFS on MazeGraph.

       Alghoritm:
       - Build MazeGraph with all non reserved cell and no edges.
       - Use DFS to add an edge to each non visited neighbor from
         a starting cell.
       - If not perfect: add random edeges with loops.
       - Convert the graph to a bitmask grid.
    """

    def __init__(
                self,
                width: int,
                height: int,
                seed: int | None = None,
                perfect: bool = True,
                draw_42: bool = True) -> None:
        """Constructor of the maze

        Args:
            width (int): columns of the matrix
            height (int): rows of the matrix
            seed (int | None): numeber for looping
            random edeges
            perfect (bool, optional): Choice of the
            type of maze. Defaults to True.
            draw_42 (bool, optional): Reserved cell
            that draw "42". Defaults to True.
        """
        if width < 2 or height < 2:
            raise ValueError("Maze size must be at least 2x2")
        self.width = width
        self.height = height
        self.perfect = perfect
        self.draw42 = draw_42
        self._rng = random.Random(seed)
        self._reserved: set[Cell] = set()
        if draw_42:
            self._place_42()
        self._graph: MazeGraph | None = None

    def _place_42(self) -> None:
        """Reserve and isolate cells to form 42 pattern
        """
        ph = len(PATTERN42)
        pw = len(PATTERN42[0])

        if self.width < pw + 2 or self.height < ph + 2:
            print("[Warning]: Maze too small"
                  "to draw '42'pattern, skipping.")
            return
        # number of offset colums to
        # leave to the left to have the pattern centered
        # (total column of the maze minus total column of
        # the pattern ) // 2 (returns an integer)
        offset_x = (self.width - pw) // 2
        # number of offset rows to leave from the bottom
        # to have the pattern centered
        offset_y = (self.height - ph) // 2
        for j, row in enumerate(PATTERN42):
            for i, cell in enumerate(row):
                if cell:
                    self._reserved.add((offset_x + i,
                                        offset_y + j))

    def generate(self) -> list[list[int]]:
        """Generates the maze and return its bitmask grid.

        Returns:
            list[list[int]]: list of lists of int (bitmask).
        """
        self._graph = MazeGraph(self.width, self.height, self._reserved)
        start = self._start_cell()
        self._visited: set[Cell] = set()
        self._dfs(start)
        if not self.perfect:
            self._add_loops(extra=0.1)
        return self._graph.to_wall_grid()

    def _start_cell(self) -> Cell:
        """Fist non-reserved cell (top-left).

        Returns:
            Cell: starting cell.
        """
        for y in range(self.height):
            for x in range(self.width):
                if x not in self._reserved:
                    return (x, y)
        raise RuntimeError("All cells reserved: Maze impossible.")

    def _dfs(self, cell: Cell) -> None:
        """Recursive DFS that visit cell than each unvisited   neighbor.

        Args:
            cell (Cell): starting cell.
        """
        self._visited.add(cell)
        if self._graph is None:
            raise RuntimeError("generate() must be called first.")
        for neighbor in self._shuffled_neighbors(cell):
            if neighbor in self._visited:
                continue
            # assert self._graph is not None
            self._graph.add_edge(cell, neighbor)
            self._dfs(neighbor)

    def _shuffled_neighbors(self, cell: Cell) -> list[Cell]:
        """Return unvisited neighbors cells.

        Args:
            cell (Cell): starting cell.

        Returns:
            list[Cell]: list of unviseted nighbor cells.
        """
        if self._graph is None:
            raise RuntimeError("generate() must be called first.")
        neighbors = list(self._graph.neighbors(cell))
        self._rng.shuffle(neighbors)
        return neighbors

    def _add_loops(self, extra: float) -> None:
        """Add random extra edges(loops) with probability 'extra'.


        Args:
            extra (float): probability of adding an edge(0.0, 0.1)
        """
        if self._graph is None:
            raise RuntimeError("generate() must be called first.")
        candidates = self._graph.full_edge_list()
        self._rng.shuffle(candidates)
        # iterate each tuple then unpack in four variables.
        for (a, b, _, _) in candidates:
            if self._graph.has_edge(a, b):
                continue
            if self._rng.random() < extra:
                self._graph.add_edge(a, b)

    def to_hex_lines(self) -> list[str]:
        """Output format: one hex char per cell, row by row.

        Returns:
            list[str]: bitmask grid.
        """
        if self._graph is None:
            raise RuntimeError("generate() must be called first.")
        grid = self._graph.to_wall_grid()
        return [
            "".join(format(grid[y][x], "X") for x in range(self.width))
            for y in range(self.height)
        ]
