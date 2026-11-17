from __future__ import annotations
from typing import TypeAlias
from constants import (
    ALL_WALLS, N, S, E, W, DIRX, DIRY, OPPOSITE)
from graph import Graph


Cell: TypeAlias = tuple[int, int]


class MazeGraph(Graph[Cell]):
    """Graph representation of a maze.

    The maze is modeled as an undirected graph:
        - Nodes: non-reserved cells ``(x, y)``.
        - Edges: open passages between
                 adjacent cells.
    """

    def __init__(self, width: int, height: int,
                 reserved: set[Cell]) -> None:
        super().__init__(directed=False)
        self.width = width
        self.height = height
        self._reserved: set[Cell] = reserved or set()
        self._build_nodes()

    def _build_nodes(self) -> None:
        """Add every non-reserved cell as
           an isoleted node.
        """
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) not in self._reserved:
                    self.add_node((x, y))

    def full_edge_list(self) -> list[tuple[Cell, Cell,
                                           int, int]]:
        """All possible edges as
           (cell_a, cell_b, dir_a_to_b, dir_b_to_a).
           Uses only E and Sto avoid duplicates in
           undirected graph.

        Returns:
            list[tuple[Cell, Cell, int, int]]: list
            of tuple with 4 elements.
        """
        result: list[tuple[Cell, Cell, int, int]] = []
        for (x, y) in self.nodes():
            for d in (E, S):
                nx, ny = x + DIRX[d], y + DIRY[d]
                # control if the node is in the graph
                if (nx, ny) in self:
                    result.append(((x, y), (nx, ny), d, OPPOSITE[d]))
        return result

    def direction_between(self, a: Cell, b: Cell) -> int:
        """Return the direction bit to go from a to b.

        Args:
            a (Cell): starting cell
            b (Cell): arriving cell

        Returns:
            int: direction bit, one of (N, E, S, W)
        """
        # horizontal difference
        dx = b[0] - a[0]
        # vertical difference
        dy = b[1] - a[1]
        for d in (N, E, S, W):
            if DIRX[d] == dx and DIRY[d] == dy:
                return d
        raise ValueError(f"Cell {a} and {b} are not adjacent.")

    def to_wall_grid(self) -> list[list[int]]:
        """Convert the graph back to bitmask grid
           for display.

        - Reserved cells: ALL_WALLS (isolated "42").
        - Cells with no edges: ALL_WALLS (isolated by spec).
        - Cells with edges: walls removed for each open passage.

        Returns:
            list[list[int]]: bitmask grid.
        """
        grid: list[list[int]] = [
            # nested list comprehension
            # internal loop: create columns
            [ALL_WALLS for _ in range(self.width)]
            # external loop: create rows
            for _ in range(self.height)
        ]
        for cell in self.nodes():
            x, y = cell
            for nb in self.neighbors(cell):
                d = self.direction_between(cell, nb)
                # open the wall
                # ~d: complement bit to bits of d.
                # it means not d(take the opposite of d)
                # &=: AND bit a bit with assignment.
                # grid[y][x] = grid[y][x] & (~d).
                grid[y][x] &= ~d
        return grid

    def cell_count(self) -> int:
        """sums all cells.

        Returns:
            int: total of cells.
        """
        return len(self)

    def edge_count(self) -> int:
        """sums all edges.

        Returns:
            int: total of edeges.
        """
        return len(self.edeges())
