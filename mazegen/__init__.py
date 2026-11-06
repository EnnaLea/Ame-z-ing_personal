from backtracking_generator import MazeGenerator, N, E, S, W, ALL_WALLS
from solver import solve, path_to_string

# Pattern facade: clean and stable API that hides
# implementation details.
# who'll use the package doesn't need to know the internal
# structure of the maze code


__all__ = [
    "MazeGenerator", "solve", "path_to_string",
    "N", "E", "S", "W", "ALL_WALLS"
]

__version__ = "1.0.0"
