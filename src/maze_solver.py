import time
import numpy as np
from typing import Tuple, List

import a_star
import bfs
import utils


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
    paths_step, border_diff_step = solveBFS(map, (0, 0, 0), (0, 2, 0))
    print(paths_step[-1]) # prints [(0, 0, 0), (0, 1, 0), (0, 2, 0)]
    '''

    #calculate execution time
    start = time.time()
    #find path
    path_step, border_step = bfs.bfs(tensor, source, destination)
    delta = time.time() - start

    distance = utils.path_cost(path_step[-1]) if path_step[-1] is not None else None
    print(f"BFS: Steps: {len(path_step)} | Execution time: {delta} | Path cost: {distance}")


    return path_step, border_step


def solveAStarEuclidean(
    tensor: np.ndarray,
    source: Tuple[int, int, int],
    destination: Tuple[int, int, int]
) -> Tuple[List[List[Tuple[int, int, int]]], List[List[Tuple[int, int, int]]]]:
    '''
    solveAStar finds a path from source to destination in a boolean walk tensor 
    using A*. The return is a list of list of tuples of the path at each iteration and
    a list of lists of tuples of the nodes that can be explored at the next step.

    usage example: 

    map = np.array([[[True], [True], [True]]])

    # from the top of the maze to the bottom
    paths_step, border_diff_step = solveAStar(map, (0, 0, 0), (0, 2, 0))
    print(paths_step[-1]) # prints [(0, 0, 0), (0, 1, 0), (0, 2, 0)]
    '''
    maze = tensor.astype(int)

    start = time.time()
    path_step, border_step = a_star.astar(maze, source, destination, 2)
    delta = time.time() - start

    print(f"A*: Steps: {len(path_step)} | Execution time: {delta} | Path cost: {utils.path_cost(path_step[-1])}")

    return path_step, border_step

def solveAStarPartitioned(
    tensor: np.ndarray,
    source: Tuple[int, int, int],
    destination: Tuple[int, int, int]
) -> Tuple[List[List[Tuple[int, int, int]]], List[List[Tuple[int, int, int]]]]:
    '''
    solveAStar finds a path from source to destination in a boolean walk tensor 
    using a type of partitioned A*. The return is a list of list of tuples of the 
    path at each iteration and a list of lists of tuples of the nodes that can 
    be explored at the next step.

    usage example: 

    map = np.array([[[True], [True], [True]]])

    # from the top of the maze to the bottom
    paths_step, border_diff_step = solveAStarPartitioned(map, (0, 0, 0), (0, 2, 0))
    print(paths_step[-1]) # prints [(0, 0, 0), (0, 1, 0), (0, 2, 0)]
    '''
    maze = tensor.astype(int)

    start = time.time()
    path_step, border_step = a_star.astar_partitioned(
        maze, source, destination, 2)
    delta = time.time() - start

    print(f"Partitioned A*: Steps: {len(path_step)} | Execution time: {delta} | Path cost: {utils.path_cost(path_step[-1])}")

    return path_step, border_step
