from __future__ import annotations
from collections import deque
from .backtracking_generator import N, E, S, W, DIR_X, DIR_Y


""" BFS(Breath First Search):
    solve the maze with the shortest path
"""

DIR_TO_LETTER: dict[int, str] = {N: "N", E: "E", S: "S", W: "W"}


def solve(
        grid: list[list[int]], width: int,
        height: int, entry: tuple[int, int],
        # exit_: since exit is a built-in function I added
        # a final undescore to avoid overriding it
        # it's a PEP8 convention
        exit_: tuple[int, int]) -> list[int]:
    """Return a list of directions (N/E/S/W as bit) from entry to exit.

    Args:
        grid (list[list[int]]): maze grid or maztrix
        width (int): total columns of the grid
        height (int): total rows of the grid
        entry (tuple[int, int]): entry coordinates cell
        exit_ (tuple[int, int]): exit coordinates cell

    Returns:
        list[int]: list of directions
    """
    if entry == exit_:
        return []
    # double-ended queue from the module collections
    # initialized with the entry cell
    # I use deque because the cost is O(1)
    # with popleft() method always used from BFS
    # it's especially useful for big mazes
    queue: deque[tuple[int, int]] = deque([entry])
    parent: dict[tuple[int, int],
                 tuple[tuple[int, int], int] | None] = {
        entry: None
    }
    while queue:
        # implement FIFO
        x, y = queue.popleft()
        for d in (N, E, S, W):
            # in case of closed wall
            if grid[y][x] & d:
                continue
            new_x, new_y = x + DIR_X[d], y + DIR_Y[d]
            # border control
            if not (0 <= new_x < width and 0 <= new_y < height):
                continue
            # control already visited
            if (new_x, new_y) in parent:
                continue
            # save previous cell and the directon from wich we came
            parent[(new_x, new_y)] = ((x, y), d)
            # when we found the exit
            if (new_x, new_y) == exit_:
                queue.clear()
                break
            queue.append((new_x, new_y))
    # case: maze disconnected
    if exit_ not in parent:
        return []
    # inverse recontruction of the path
    path: list[int] = []
    curr: tuple[int, int] = exit_
    while parent[curr] is not None:
        prev, d = parent[curr]  # type: ignore[misc]
        # form exit to entry
        path.append(d)
        curr = prev
    # from entry to exit
    path.reverse()
    return path


def path_to_string(path: list[int]) -> str:
    """Convert the direction-bit list in string

    Args:
        path (list[str]): list of directions in bit

    Returns:
        str: directions converted in one string
    """
    return "".join(DIR_TO_LETTER[d] for d in path)
