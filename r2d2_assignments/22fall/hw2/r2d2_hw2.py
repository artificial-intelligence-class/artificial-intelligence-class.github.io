# CIS 521: R2D2 - Homework 2
from typing import List, Tuple, Set, Optional

import numpy as np
from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI

student_name = 'Type your full name here.'

Vertex = Tuple[int, int]
Edge = Tuple[Vertex, Vertex]


# Part 1: Compare Different Searching Algorithms
class Graph:
    """A directed Graph representation"""

    def __init__(self, vertices: Set[Vertex], edges: Set[Edge]):
        ...  # TODO

    def neighbors(self, u: Vertex) -> Set[Vertex]:
        """Return the neighbors of the given vertex u as a set"""
        ...  # TODO

    def bfs(self, start: Vertex, goal: Vertex) -> Tuple[Optional[List[Vertex]], Set[Vertex]]:
        """Use BFS algorithm to find the path from start to goal in the given graph.

        :return: a tuple (shortest_path, node_visited),
                 where shortest_path is a list of vertices that represents the path from start to goal, and None if
                 such a path does not exist; node_visited is a set of vertices that are visited during the search."""
        ...  # TODO

    def dfs(self, start: Vertex, goal: Vertex) -> Tuple[Optional[List[Vertex]], Set[Vertex]]:
        """Use BFS algorithm to find the path from start to goal in the given graph.

        :return: a tuple (valid_path, node_visited),
                 where valid_path is a list of vertices that represents the path from start to goal (no need to be shortest), and None if
                 such a path does not exist; node_visited is a set of vertices that are visited during the search."""
        ...  # TODO

    def a_star(self, start: Vertex, goal: Vertex) -> Tuple[Optional[List[Vertex]], Set[Vertex]]:
        """Use A* algorithm to find the path from start to goal in the given graph.

        :return: a tuple (shortest_path, node_visited),
                 where shortest_path is a list of vertices that represents the path from start to goal, and None if
                 such a path does not exist; node_visited is a set of vertices that are visited during the search."""

        ...  # TODO

    def tsp(self, start: Vertex, goals: Set[Vertex]) -> Tuple[Optional[List[Vertex]], Optional[List[Vertex]]]:
        """Use A* algorithm to find the path that begins at start and passes through all the goals in the given graph,
        in an order such that the path is the shortest.

        :return: a tuple (optimal_order, shortest_path),
                 where shortest_path is a list of vertices that represents the path from start that goes through all the
                 goals such that the path is the shortest; optimal_order is an ordering of goals that you visited in
                 order that results in the above shortest_path. Return (None, None) if no such path exists."""
        ...  # TODO


# Part 2: Let your R2-D2 rolling in Augment Reality (AR) Environment
def get_transformation(k: np.ndarray, r: np.ndarray, t: np.ndarray) -> np.ndarray:
    """Calculate the transformation matrix using the given equation P = K x (R | T)"""
    ...  # TODO


def convert_3d_to_2d(p: np.ndarray, points_3d: List[Tuple[float, float, float]]) -> List[Tuple[int, int]]:
    """Convert a list of 3D real world points to 2D image points in pixels given the transformation matrix,
       preserving the order of the points."""
    ...  # TODO


def convert_2d_to_relative(point_2d: Tuple[int, int], maze_in_2d: List[List[Tuple[int, int]]]) -> Optional[Vertex]:
    """Convert a 2D image point to maze coordinates using the given maze coordinates in 2D image.
       Return None if the 2D point isn't in the maze. Assume the coordinates are axis-aligned."""
    ...  # TODO


def path_to_moves(path: List[Vertex]) -> List[Tuple[int, int]]:
    """Taking a list of vertices and returns a list of droid actions (heading, steps)"""

    heading_mapping = {
        (0, 1): 90,
        (0, -1): 270,
        (1, 0): 180,
        (-1, 0): 0
    }

    ...  # TODO


def droid_roll(path: List[Vertex]):
    """Make your droid roll with the given path. You should decide speed and time of rolling each move."""
    moves = path_to_moves(path)
    with SpheroEduAPI(scanner.find_toy()) as droid:
        ...  # TODO
