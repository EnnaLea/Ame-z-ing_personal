from __future__ import annotations

import random

from constants import PATTERN42
from maze_graph import MazeGraph, Cell


class DsjoinSet:
    """Union-Find with path compression and union by rank.
    """

    def __init__(self, n: int) -> None:
        """Constructor of the class.

        Args:
            n (int): number of nodes to manage.
        """
        # self._parent: instance attribute that stores the parent of each node.
        # At first, each node is root of itself, hence _parent[i] = i for each i.
        # This represents a separate sets, each containing only one node.
        self._parent = list(range(n))
        # The rank is an estimate of the height of the shaft rooted in i. It is used for the optimization union by rank: when you join two trees, you attach the one with a smaller rank under the one with a greater rank, keeping the trees as "low" and therefore efficient as possible.
        self._rank = [0] * n

    def find(self, x: int) -> int:
        """Recursively find the parent of the node x.

        Args:
            x (int): a node

        Returns:
            int: the parent of the node.
        """
        if self._parent[x] != x:
            self._parent[x] = self.find(self._parent[x])
        return self._parent[x]

    def union(self, a: int, b: int) -> bool:
        """Apply union between two node.

        Args:
            a (int): a node (or cell)
            b (int): a node (or cell)

        Returns:
            bool: returns True if union is succefully applied, False otherwise.
        """
        # finding the root of a and b
        # in the Union-Find, each set is represented by its root. To know if a and b are in the same set, just compare their roots. If ra == rb, they are in the same set; otherwise, they are in different sets.
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self._rank[ra] < self._rank[rb]:
            ra, rb = rb, ra
        self._parent[rb] = ra
        if self._rank[ra] == self._rank[rb]:
            self._rank[ra] += 1
        return True



class KruskalMazeGenerator:
    """Generate a maze by Kruskal algorhitm on MazeGraph.
    """

    def __init__(
                self,
                width: int,
                height: int,
                seed: int | None = None,
                perfect: bool = True,
                draw_42: bool = True
                 ) -> None:
        if width < 2 or height < 2:
            raise ValueError("Maze size must be at least 2 x 2")
        self.width = width
        self.height = height
        self.perfect = perfect
        self.draw_42 = draw_42
        self._rng = random.Random(seed)
        self._reserved: set[Cell] = set()
        if draw_42:
            self._place_42()
        self._graph: MazeGraph | None = None

    def _place_42(self) -> None:
        ph = len(PATTERN42)
        pw = len(PATTERN42[0])
        if self.width < pw + 2 or self.height < ph + 2:
            print("[Warning] Maze too small to draw '42', skipping.")
            return
        offset_x = (self.width - pw) // 2
        offset_y = (self.height - ph) // 2
        for j, row in enumerate(PATTERN42):
            for i, cell in enumerate(row):
                if cell:
                    self._reserved.add((offset_x + i, offset_y + j))

    def generate(self) -> list[list[int]]:
        """Generates the maze and return it's bitmask grid.

        Returns:
            list[list[int]]: list of lists of bit.
        """
        # Build all possible edges
        assert self._graph is not None
        candidates = self._graph.full_edge_list()
        self._rng.shuffle(candidates)

        # Use Union_Find on all nodes
        nodes = self._graph.nodes()
        index: dict[Cell, int] = {cell: i for i, cell in enumerate(nodes)}
        ds = DsjoinSet(len(nodes))

        # Process edges in random order
        for (a, b, _, _) in candidates:
            if ds.union(index[a], index[b]):
                self._graph.add_edge(a, b)

        # Add optional loop
        if not self.perfect:
            self._add_loops(extra=0.1)

        return self._graph.to_wall_grid()

    def _add_loops(self, extra: float) -> None:
        """Add random extra edges(loops) with probability 'extra'.

        Args:
            extra (float): probability of adding an edge(0.0, 0.1)
        """
        assert self._graph is not None
        candidates = self._graph.full_edge_list()
        self._rng.shuffle(candidates)
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
            "".join(format([y][x], "X") for x in range(self.width))
			for y in range(self.height)
		]