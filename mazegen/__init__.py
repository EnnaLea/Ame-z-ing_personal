from constants import N, E, S, W, ALL_WALLS
from graph import Graph
from maze_graph import MazeGraph
from backtracking_generator import MazeGenerator
from kruskal_generator import KruskalMazeGenerator, DisjoinSet
from solver import solve, path_to_string

# Pattern facade: clean and stable API that hides
# implementation details.
# who'll use the package doesn't need to know the internal
# structure of the maze code


__all__ = [
    "MazeGenerator", "KruskalMazeGenerator",
    "DisjoinSet", "Graph", "MazeGraph",
    "solve", "path_to_string",
    "N", "E", "S", "W", "ALL_WALLS"
]

__version__ = "1.0.0"
