import numpy as np
from typing import Tuple, List

import a_star
import bfs


def solveBFS(
    tensor: np.ndarray,
    source: Tuple[int, int, int],
    destination: Tuple[int, int, int]
) -> Tuple[List[List[Tuple[int, int, int]]], List[List[Tuple[int, int, int]]], List[List[Tuple[int, int, int]]]]:
    '''
    solveBFS finds a path from source to destination in a boolean walk tensor 
    using a BFS search. The return is a list of tuples containing the path.

    usage example: 

    map = np.array([[[True], [True], [True]]])

    # from the top of the maze to the bottom
    path = solveBFS(map, (0, 0, 0), (0, 2, 0))
    print(path) # prints [(0, 0, 0), (0, 1, 0), (0, 2, 0)]
    '''

    path_step, border_step = bfs.bfs(tensor, source, destination)

    print(f"Steps for BFS: {len(path_step)}")

    return path_step, border_step


def solveAStarEuclidean(
    tensor: np.ndarray,
    source: Tuple[int, int, int],
    destination: Tuple[int, int, int]
) -> Tuple[List[List[Tuple[int, int, int]]], List[List[Tuple[int, int, int]]]]:
    '''
    solveAStar finds a path from source to destination in a boolean walk tensor 
    using A*. The return is a list of tuples containing the path.

    usage example: 

    map = np.array([[[True], [True], [True]]])

    # from the top of the maze to the bottom
    path = solveAStar(map, (0, 0, 0), (0, 2, 0))
    print(path) # prints [(0, 0, 0), (0, 1, 0), (0, 2, 0)]

    '''
    #maze = np.logical_not(tensor)
    maze = tensor.astype(int)

    path_step, border_step = a_star.astar(maze, source, destination, 2)
    
    print(f"Steps for euclidean A*: {len(path_step)}")

    return path_step, border_step

def solveAStarPartitioned(
    tensor: np.ndarray,
    source: Tuple[int, int, int],
    destination: Tuple[int, int, int]
) -> Tuple[List[List[Tuple[int, int, int]]], List[List[Tuple[int, int, int]]]]:
    maze = tensor.astype(int)
    path_step, border_step = a_star.astar_partitioned(
        maze, source, destination, True)
    
    print(f"Steps for partitioned A*: {len(path_step)}")

    return path_step, border_step

def print_maze(
    maze: np.ndarray,
    source: Tuple[int, int, int] = None,
    destination: Tuple[int, int, int] = None,
    path: List[Tuple[int, int, int]] = None
):
    if path is not None:
        for step in path:
            maze[step[0]][step[1]][step[2]] = 2

    if source is not None:
        maze[source[0]][source[1]][source[2]] = 3

    if destination is not None:
        maze[destination[0]][destination[1]][destination[2]] = 4

    for floor in maze:
        print(f"New floor\n")
        for row in floor:
            line = []
            for col in row:
                if col == 1:
                    line.append("\u2588")
                elif col == 0:
                    line.append(" ")
                elif col == 2:
                    line.append(".")
                elif col == 3:
                    line.append("S")
                elif col == 4:
                    line.append("E")
            print("".join(line))
