from __future__ import annotations
import typing

# TypeVar("T") can be anything in this case
# it will be used for graph
T = typing.TypeVar("T")


class Graph(typing.Generic[T]):
    """Graph with hashable nodes.
       Supports both directed and undirected modes.
       Generic wheighted graph using adjacency lists because
       the graph is generic so reusable and not big so using
       adjacency matrix will be a waste of memory.
    """

    def __init__(self, directed: bool = False) -> None:
        """Constructor.

        Args:
            directed (bool, optional): choice to be directed
            or not. Defaults to False.
        """
        self._directed = directed
        self._adj: dict[T, dict[T, float]] = {}

    # methods for nodes
    def add_node(self, node: T) -> None:
        """Add node without connecting it.

        Args:
            node (T): node of a generic type.
        """
        if node not in self._adj:
            self._adj[node] = {}

    def nodes(self) -> list[T]:
        return list(self._adj.keys())

    # methods for edges
    def add_edge(self, a: T, b: T,
                 weight: float = 1.0) -> None:
        """Add edge and, only if missing, a node.

        Args:
            a (T): node a
            b (T): node b
            weight (float, optional): distance from a to b.
            Defaults to 1.0.
        """
        self.add_node(a)
        self.add_node(b)
        self._adj[a][b] = weight
        if not self._directed:
            self._adj[b][a] = weight

    def remove_edge(self, a: T, b: T) -> None:
        """Remove an edge

        Args:
            a (T): node a
            b (T): node b
        """
        self._adj[a].pop(b, None)
        if not self._directed:
            self._adj[b].pop(a, None)

    def has_edge(self, a: T, b: T) -> bool:
        """Control if an edge is present

        Args:
            a (T): node a
            b (T): node b

        Returns:
            bool: True if b is in the adjacenncy list
        """
        return b in self._adj.get(a, {})

    # movements methods
    def neighbors(self, node: T) -> list[T]:
        """Find neighbors nodes.

        Args:
            node (T): starting node

        Returns:
            list[T]: list of neighbors nodes
        """
        return list(self._adj.get(node, {}))

    def edeges(self) -> list[tuple[T, T, float]]:
        """Return unique edeges (tuple of three elements
           for Kruskal alghoritm).
           Deduplicates for undirected graphs because:
           frozenset(a, b) = forzenset(b, a).

        Returns:
            list[tuple[T, T, float]]: list of unique edges.
        """
        result: list[tuple[T, T, float]] = []
        # added edges
        seen: set[frozenset[T]] = set()
        for a, neigh in self._adj.items():
            for b, w in neigh.items():
                if self._directed:
                    result.append((a, b, w))
                else:
                    key = frozenset((a, b))
                    if not seen:
                        seen.add(key)
                        result.append((a, b, w))
        return result

    def degree(self, node: T) -> int:
        """Calculate numbers of
           neighbors nodes of a node.

        Args:
            node (T): starting node.

        Returns:
            int: total of neighbors nodes.
        """
        return len(list(self._adj.get(node, {})))

    def __len__(self) -> int:
        """Calculate numbers of nodes.

        Returns:
            int: total nodes in the graph.
        """
        return len(self._adj)

    def __contains__(self, node: object) -> bool:
        """Verify if a node exist

        Args:
            node (object): node in the graph

        Returns:
            bool: True if a node exixt False
                  otherwise.
        """
        return node in self._adj
