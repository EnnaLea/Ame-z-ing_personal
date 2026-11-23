from __future__ import annotations
from collections import deque
from constants import N, E, S, W
from maze_graph import MazeGraph, Cell


""" BFS(Breath First Search):
    solve the maze with the shortest path
    on MazeGraph.
"""

DIR_TO_LETTER: dict[int, str] = {N: "N", E: "E", S: "S", W: "W"}


def solve(
        graph: MazeGraph,
        entry: Cell,
        exit_: Cell,
           ) -> list[int]:
    """Return the direction of the shortest path
       from entry to exit in bits.
       Uses BFS.

    Args:
        graph (MazeGraph): the generated maze
        entry (Cell): entry coordinates.
        exit_ (Cell): exit coordinates.

    Returns:
        list[int]: list of bits that represent the
                    shortest path to exit the maze.
                    Return [] if no path exist.
    """
    if entry == exit_:
        return []
    # deque: double-ended queue from the module collections.
    # Inserting and removing elements from both side
    # are done efficiently:
    # - append(x) → add to the tail, O(1).
    # - appendleft(x) → add to the head, O(1).
    # - pop() → remove from the tail, O(1).
    # - popleft() → remove from the head, O(1).
    queue: deque[Cell] = deque([entry])
    parent: dict[Cell, tuple[Cell, int] | None] = {entry: None}
    while queue:
        curr = queue.popleft()
        # explore neighbor cells
        for nb in graph.neighbors(curr):
            if nb in parent:
                continue
            d = graph.direction_between(curr, nb)
            parent[nb] = (curr, d)
            if nb == exit_:
                queue.clear()
                break
            queue.append(nb)
    if exit_ not in parent:
        return []
    # reconstruction of the path from exti_ to entry
    path: list[int] = []
    curr = exit_
    while parent[curr] is not None:
        prev, d = parent[curr]  # type: ignore[misc]
        path.append(d)
        curr = prev
    path.reverse()
    return path


def path_to_string(path: list[int]) -> str:
    """Convert direction bits to 'NESW...' string

    Args:
        path (list[int]): list of bits representing the path

    Returns:
        str: path converted in string
    """
    return "".join(DIR_TO_LETTER[d] for d in path)
