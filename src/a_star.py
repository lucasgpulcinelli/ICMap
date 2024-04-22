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
    
    def stairs_in_floor(floor):
        with open("res/stairs.json") as f:
            stairs = json.load(f)
            #remove floor from coordinates
            return [(x, y) for f, x, y in stairs if f == floor]

    def distance_from_point_to_points(point, points):
        dist = [(p, utils.euclidean_distance(point, p)) for p in points]
        dist.sort(key=lambda x: x[1])
        return dist

    def add_floor_to_coordinates(floor, coordinates):
        return [[(floor, x, y) for x, y in step] if step is not None else None for step in coordinates]

    def astar_2d(start, destiny):
        paths, borders = astar(maze[start[0]], (start[1], start[2]), destiny, diagonal_level)

        paths = add_floor_to_coordinates(start[0], paths)
        borders = add_floor_to_coordinates(start[0], borders)    
        return paths, borders
    
    def process_stair(current_stair, paths_from_this_end, paths_from_other_end, is_reversed):
        paths, borders = astar_2d(start if not is_reversed else end, current_stair)
        path_step.extend(paths)
        border_step.extend(borders)
        last_path = paths[-1]
        
        if last_path is None:
            return False
        paths_from_this_end[current_stair] = last_path
        
        matching_path = paths_from_other_end.get(current_stair)
        if matching_path is None:
            return False
        
        combined_path = []
        if is_reversed:
            last_path.reverse()
            combined_path = matching_path + last_path
        else:
            matching_path.reverse()
            combined_path = last_path + matching_path
        path_step.append(combined_path)
        border_step.append(None)
        return True

    start_to_stairs = distance_from_point_to_points(start, stairs_in_floor(start[0]))
    end_to_stairs = distance_from_point_to_points(end, stairs_in_floor(end[0]))

    stairs_in_start_floor = len(start_to_stairs)
    stairs_in_end_floor = len(end_to_stairs)

    path_step, border_step = [], []

    paths_from_start = {}
    paths_from_end = {}
    i = 0 
    while i < stairs_in_start_floor or i < stairs_in_end_floor:
        if i < stairs_in_start_floor and process_stair(start_to_stairs[i][0], paths_from_start, paths_from_end, False):
            return path_step, border_step
        if i < stairs_in_end_floor and process_stair(end_to_stairs[i][0], paths_from_end, paths_from_start, True):
            return path_step, border_step
        i += 1

    path_step.append(None)
    border_step.append(None)
    return path_step, border_step

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
    diagonal_level = max(1, min(dimension, diagonal_level))
    
    if len(start) != dimension or len(end) != dimension:
        raise ValueError("Start and end must have the same dimension as the maze")

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
            
            child.g = current_node.g + child.euclidean_distance(current_node)
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