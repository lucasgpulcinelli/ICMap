import random
from typing import List, Tuple
from warnings import warn
import heapq
import numpy as np
import json

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

def return_path(current_node):
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    return path[::-1]  # Return reversed path

def add_floor_to_steps(steps, floor):
    new_steps = []
    for step in steps:
        if step is not None:
            new_step = [(floor, x, y) for x, y in step]
            new_steps.append(new_step)
        else:
            new_steps.append(None)
    return new_steps

def astar_partitioned(
    maze: np.ndarray,
    start: Tuple[int, int, int],
    end: Tuple[int, int, int],
    allow_diagonal_movement: bool = False
) -> Tuple[List[List[Tuple[int, int, int]]], List[List[Tuple[int, int, int]]]]:
    if start[0] == end[0]:
        path_step, border_step = astar_euclidean(maze, start, end, allow_diagonal_movement)
        return path_step, border_step
    
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
            paths, borders = astar_2d(maze[start[0]], start_2d, destiny, allow_diagonal_movement)

            paths = add_floor_to_steps(paths, start[0])
            borders = add_floor_to_steps(borders, start[0])

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
            paths, borders = astar_2d(maze[end[0]], end_2d, destiny, allow_diagonal_movement)
            paths = add_floor_to_steps(paths, end[0])
            borders = add_floor_to_steps(borders, end[0])
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

def astar_2d(
    maze: np.ndarray,
    start: Tuple[int, int],
    end: Tuple[int, int],
    allow_diagonal_movement: bool = False
) -> Tuple[List[List[Tuple[int, int]]], List[List[Tuple[int, int]]]]:
    """
    Returns a list of tuples as a path from the given start to the given end in the given maze
    :param maze:
    :param start:
    :param end:
    :return:
    """

    #list of lists with the path at each step
    path_step = []
    border_step = []

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Heapify the open_list and Add the start node
    heapq.heapify(open_list) 
    heapq.heappush(open_list, start_node)

    # Adding a stop condition
    outer_iterations = 0
    max_iterations = (len(maze[0]) * len(maze) // 2)

    diagonal_cost = 3.5
    horizontal_cost = 1.0

    adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0))
    direction_cost= (horizontal_cost, horizontal_cost, horizontal_cost, horizontal_cost)
    adjacent_square_pick_index = [0, 1, 2, 3]

    # what squares do we search
    if allow_diagonal_movement:
        adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1))
        direction_cost = (horizontal_cost, horizontal_cost, horizontal_cost, horizontal_cost, diagonal_cost, diagonal_cost, diagonal_cost, diagonal_cost)
        adjacent_square_pick_index = [0, 1, 2, 3, 4, 5, 6, 7]

    # Loop until you find the end
    while len(open_list) > 0:
        #Randomize the order of the adjacent_squares_pick_index to avoid a decision making bias
        random.shuffle(adjacent_square_pick_index)
        outer_iterations += 1

        new_border = []

        if outer_iterations > max_iterations:
          # if we hit this point return the path such as it is
          # it will not contain the destination
          warn("giving up on pathfinding too many iterations")
          return return_path(current_node)       
        
        # Get the current node
        current_node = heapq.heappop(open_list)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            border_step.append(None)
            path_step.append(return_path(current_node))
            return path_step, border_step   

        # Generate children
        children = []
        cost_factor = []
        
        for pick_index in adjacent_square_pick_index:
            new_position = adjacent_squares[pick_index]
            direction_cost_factor = direction_cost[pick_index]

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)
            cost_factor.append(direction_cost_factor)

        # Loop through children
        for child, cost in zip(children, cost_factor):
            # Child is on the closed list
            if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + cost 
            child.h = np.sqrt(((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2))
            child.f = child.g + child.h

            # Child is already in the open list
            if child in open_list: 
                idx = open_list.index(child) 
                if child.g < open_list[idx].g:
                    # update the node in the open list
                    open_list[idx].g = child.g
                    open_list[idx].f = child.f
                    open_list[idx].h = child.h
            else:
                heapq.heappush(open_list, child)

            new_border.append(child.position)

        border_step.append(new_border)
        path_step.append(return_path(current_node))

    warn("Couldn't get a path to destination")
    path_step.append(None)
    return path_step, border_step  

def astar_euclidean(
    maze: np.ndarray,
    start: Tuple[int, int, int],
    end: Tuple[int, int, int],
    allow_diagonal_movement: bool = False
) -> Tuple[List[List[Tuple[int, int, int]]], List[List[Tuple[int, int, int]]]]:
    """
    Returns a list of tuples as a path from the given start to the given end in the given maze
    :param maze:
    :param start:
    :param end:
    :return path, visited, border:
    """

    #list of lists with the path at each step
    path_step = []
    border_step = []

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Heapify the open_list and Add the start node
    heapq.heapify(open_list) 
    heapq.heappush(open_list, start_node)

    # Adding a stop condition
    outer_iterations = 0
    max_iterations = (len(maze[0][0]) * len(maze[0]) * len(maze) // 4)

    diagonal_cost = 3.5
    vertical_cost = 1.0
    horizontal_cost = 1.0

    adjacent_squares = ((-1, 0, 0), (1, 0, 0), (0, 0, -1), (0, 0, 1), (0, -1, 0), (0, 1, 0))
    direction_cost= (vertical_cost, vertical_cost, horizontal_cost, horizontal_cost, horizontal_cost, horizontal_cost)
    adjacent_square_pick_index = [0, 1, 2, 3, 4, 5]

    # what squares do we search
    if allow_diagonal_movement:
        adjacent_squares = ((-1, 0, 0), (1, 0, 0), (0, 0, -1), (0, 0, 1), (0, -1, 0), (0, 1, 0),
                            (0, -1, -1), (0, -1, 1), (0, 1, -1), (0, 1, 1))
        direction_cost = (vertical_cost, vertical_cost, horizontal_cost, horizontal_cost, horizontal_cost, horizontal_cost, diagonal_cost, diagonal_cost, diagonal_cost, diagonal_cost)
        adjacent_square_pick_index = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    # Loop until you find the end
    while len(open_list) > 0:
        #Randomize the order of the adjacent_squares_pick_index to avoid a decision making bias
        random.shuffle(adjacent_square_pick_index)
        outer_iterations += 1

        new_border = []

        if outer_iterations > max_iterations:
            # if we hit this point return the path such as it is
            # it will not contain the destination
            warn("giving up on pathfinding too many iterations")
            return path_step, border_step    
        
        # Get the current node
        current_node = heapq.heappop(open_list)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            border_step.append(None)
            path_step.append(return_path(current_node))
            return path_step, border_step   

        # Generate children
        children = []
        cost_factor = []
        
        for pick_index in adjacent_square_pick_index:
            new_position = adjacent_squares[pick_index]
            direction_cost_factor = direction_cost[pick_index]

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1], current_node.position[2] + new_position[2])

            # make sure within range for a 3d array
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0 or node_position[2] > (len(maze[len(maze)-1][0]) -1) or node_position[2] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]][node_position[2]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)
            cost_factor.append(direction_cost_factor)

        # Loop through children
        for child, cost in zip(children, cost_factor):
            # Child is on the closed list
            if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + cost 
            #we could do this without the sqrt, but this would make COST have almost no effect
            child.h = np.sqrt(((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2) + ((child.position[2] - end_node.position[2]) ** 2))
            child.f = child.g + child.h

            # Child is already in the open list
            if child in open_list: 
                idx = open_list.index(child) 
                if child.g < open_list[idx].g:
                    # update the node in the open list
                    open_list[idx].g = child.g
                    open_list[idx].f = child.f
                    open_list[idx].h = child.h
            else:
                heapq.heappush(open_list, child)

            new_border.append(child.position)

        border_step.append(new_border)
        path_step.append(return_path(current_node))

    warn("Couldn't get a path to destination")
    path_step.append(None)
    return path_step, border_step   