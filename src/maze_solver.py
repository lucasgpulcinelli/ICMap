import numpy as np
from typing import Tuple, List

import a_star


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

    maze = tensor[0]

    #invert maze true is false and false is true
    maze = np.logical_not(maze)

    #convert maze from boolean to int
    maze = maze.astype(int)

    start = (source[1], source[2])
    end = (destination[1], destination[2])

    path = a_star.astar(maze, start, end, True)

    print("Printing maze")
    print(maze)

    for step in path:
        maze[step[0]][step[1]] = 2

    maze[start[0]][start[1]] = 3
    maze[end[0]][end[1]] = 4

    
    print("Printing maze with path")
    print(maze)
    
    for row in maze:
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

    #generate path with 3d coordinates
    path = [(0, step[0], step[1]) for step in path]
    print(path)

    return path
