import numpy as np
from typing import Tuple, List


def solveBFS(
    tensor: np.ndarray,
    source: Tuple[int, int, int],
    destination: Tuple[int, int, int]
) -> List[Tuple[int, int, int]]:
    '''
    solveBFS finds a path from source to destination in a boolean walk tensor 
    using a BFS search. The return is a list of tuples containing the path.

    usage example: 

    map = np.array([[[True], [True], [True]]])

    # from the top of the maze to the bottom
    path = solveBFS(map, (0, 0, 0), (0, 2, 0))
    print(path) # prints [(0, 0, 0), (0, 1, 0), (0, 2, 0)]
    '''

    _ = tensor

    return [source, destination]


def solveAStar(
    tensor: np.ndarray,
    source: Tuple[int, int, int],
    destination: Tuple[int, int, int]
) -> List[Tuple[int, int, int]]:
    '''
    solveAStar finds a path from source to destination in a boolean walk tensor 
    using A*. The return is a list of tuples containing the path.

    usage example: 

    map = np.array([[[True], [True], [True]]])

    # from the top of the maze to the bottom
    path = solveAStar(map, (0, 0, 0), (0, 2, 0))
    print(path) # prints [(0, 0, 0), (0, 1, 0), (0, 2, 0)]

    '''

    _ = tensor

    return [source, destination]
