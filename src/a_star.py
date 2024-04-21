import random
from typing import List, Tuple
from warnings import warn
import heapq
import numpy as np
import json
import utils

class Node:
    """
    A node class for A* Pathfinding
    """

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position
    
    def __repr__(self):
      return f"{self.position} - g: {self.g} h: {self.h} f: {self.f}"

    # defining less than for purposes of heap queue
    def __lt__(self, other):
      return self.f < other.f
    
    # defining greater than for purposes of heap queue
    def __gt__(self, other):
      return self.f > other.f

    def return_path(self):
        path = []
        current = self
        while current is not None:
            path.append(current.position)
            current = current.parent
        return path[::-1]  # Return reversed path
    
    def euclidean_distance(self, other):
        return round(sum([(self.position[i] - other.position[i])**2 for i in range(len(self.position))]) ** 0.5, 3)

    def is_outside(self, maze):
        def check_dimension(dim_maze, position, dim=0):
            if dim >= len(position):
                return False
            
            if position[dim] < 0 or position[dim] >= len(dim_maze):
                return True
            
            return check_dimension(dim_maze[position[dim]], position, dim + 1)
        
        return check_dimension(maze, self.position)

    def is_wall(self, maze):
        def navigate_dimension(dim_maze, position, dim=0):
            if dim == len(position) - 1:
                return dim_maze[position[dim]] == 0
            
            return navigate_dimension(dim_maze[position[dim]], position, dim + 1)
        
        return navigate_dimension(maze, self.position)

def astar_partitioned(
    maze: np.ndarray,
    start: Tuple[int, int, int],
    end: Tuple[int, int, int],
    diagonal_level: int = 1
) -> Tuple[List[List[Tuple[int, int, int]]], List[List[Tuple[int, int, int]]]]:
    if start[0] == end[0]:
        return astar(maze, start, end, diagonal_level)
    
    f = open("res/stairs.json")
    stairs = json.load(f)
    f.close()

    start_euclidean_distances = []
    end_euclidean_distances = []

    start_2d = (start[1], start[2])
    end_2d = (end[1], end[2])

    for f, x, y in stairs:
        if f == start[0]:
            distance = np.sqrt((x - start[1]) ** 2 + (y - start[2]) ** 2)
            coordinates = (x, y)
            start_euclidean_distances.append((coordinates, distance))
        elif f == end[0]:
            distance = np.sqrt((x - end[1]) ** 2 + (y - end[2]) ** 2)
            coordinates = (x, y)
            end_euclidean_distances.append((coordinates, distance))

    start_euclidean_distances.sort(key=lambda x: x[1])
    end_euclidean_distances.sort(key=lambda x: x[1])

    paths_in_start_floor = []
    paths_in_end_floor = []

    path_step = []
    border_step = []

    i = 0
    stop = 2
    while 1:
        if i < len(start_euclidean_distances):
            destiny = start_euclidean_distances[i][0]
            paths, borders = astar(maze[start[0]], start_2d, destiny, diagonal_level)

            paths = [[(start[0], x, y) for x, y in step] if step is not None else None for step in paths] #adds floor back to coordinates
            borders = [[(start[0], x, y) for x, y in step] if step is not None else None for step in borders]

            path_step += paths
            border_step += borders
            path = paths[-1]
            if path is not None:
                end_calculated_destinations = [x[0] for x in paths_in_end_floor]
                if destiny in end_calculated_destinations:
                    end_path = paths_in_end_floor[end_calculated_destinations.index(destiny)][1]
                    end_path.reverse()
                    path_step.append(path + end_path)
                    border_step.append(None)
                    return path_step, border_step

                paths_in_start_floor.append((destiny, path))
        else:
            stop -= 1
            if stop == 0:
                break

        if i < len(end_euclidean_distances):
            destiny = end_euclidean_distances[i][0]
            paths, borders = astar(maze[end[0]], end_2d, destiny, diagonal_level)

            paths = [[(end[0], x, y) for x, y in step] if step is not None else None for step in paths]
            borders = [[(end[0], x, y) for x, y in step] if step is not None else None for step in borders]

            path_step += paths
            border_step += borders
            path = paths[-1]
            if path is not None:
                start_calculated_destinations = [x[0] for x in paths_in_start_floor]
                if destiny in start_calculated_destinations:
                    start_path = paths_in_start_floor[start_calculated_destinations.index(destiny)][1]
                    path.reverse()
                    path_step.append(start_path + path)
                    border_step.append(None)
                    return path_step, border_step
                paths_in_end_floor.append((destiny, path))
        else:
            stop -= 1
            if stop == 0:
                break

        i += 1
    return None

def astar(
    maze: np.ndarray,
    start,
    end,
    diagonal_level: int = 1
) -> Tuple[List[List], List[List]]:
    """
    Returns a list of tuples as a path from the given start to the given end in the given maze
    :param maze:
    :param start:
    :param end:
    :param diagonal_level: how many planes should consider diagonals (keep between 1 and maze_dimension)
    :return path, visited, border:
    """
    dimension = len(maze.shape)
    if diagonal_level < 1 or diagonal_level > dimension:
        raise ValueError("Diagonal level cannot be less than 1 or greater than the number of dimensions")
    
    if len(start) != dimension or len(end) != dimension:
        raise ValueError("Start and end must have the same number of dimensions as the maze")

    #list of lists with the path at each step

    # Create start and end node
    start_node = Node(None, start)
    end_node = Node(None, end)

    #list with a list of nodes for every iteration of the algorithm
    path_step = []
    border_step = []

    closed_list = []
    open_list = []
    heapq.heapify(open_list) #create priority queue for open list
    heapq.heappush(open_list, start_node)

    # Adding a stop condition
    outer_iterations = 0
    max_iterations = (maze.size // 2)

    adjacent_squares = utils.generate_adjacent_squares(dimension, diagonal_level)

    # Loop until you find the end
    while len(open_list) > 0:
        outer_iterations += 1

        new_border = []
        if outer_iterations > max_iterations:
            # if we cannot find searching for half the maze, we give up
            warn("giving up on pathfinding. too many iterations")
            return path_step, border_step    
        
        # Get the current node
        current_node = heapq.heappop(open_list)
        closed_list.append(current_node)

        if current_node == end_node and open_list[0].f >= current_node.f:
            #! we are done
            border_step.append(None)
            path_step.append(current_node.return_path())
            return path_step, border_step   

        for new_position in adjacent_squares:
            # Get node position
            node_position = tuple([current_node.position[i] + new_position[i] for i in range(dimension)])
            new_node = Node(current_node, node_position)

            if new_node.is_outside(maze):
                continue

            if new_node.is_wall(maze):
                continue

            if new_node in closed_list:
                continue

            child = new_node #the new node is a valid child of the current_node
            #calculate the heuristic
            child.g = current_node.g + utils.euclidean_distance(dimension, current_node.position, child.position)
            child.h = child.euclidean_distance(end_node)
            child.f = child.g + child.h

            #add or update the child to the open list
            if child in open_list: 
                i = open_list.index(child) 
                if child.g < open_list[i].g:
                    # update the node in the open list
                    open_list.pop(i)
                    heapq.heappush(open_list, child)
            else:
                heapq.heappush(open_list, child)

            # update the border for this step
            new_border.append(child.position)

        border_step.append(new_border)
        path_step.append(current_node.return_path())

    warn("Couldn't get a path to destination")
    path_step.append(None)
    return path_step, border_step   