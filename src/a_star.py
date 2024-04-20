import random
from warnings import warn
import heapq
import numpy as np

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


def astar(maze, start, end, allow_diagonal_movement = False):
    """
    Returns a list of tuples as a path from the given start to the given end in the given maze
    :param maze:
    :param start:
    :param end:
    :return:
    """

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

    adjacent_squares = ((-1, 0, 0), (1, 0, 0), (0, 0, -1), (0, 0, 1), (0, -1, 0), (0, 1, 0))
    direction_cost= (1.0, 1.0, 1.0, 1.0, 1.0, 1.0)
    adjacent_square_pick_index = [0, 1, 2, 3, 4, 5]

    # what squares do we search
    if allow_diagonal_movement:
        adjacent_squares = ((-1, 0, 0), (1, 0, 0), (0, 0, -1), (0, 0, 1), (0, -1, 0), (0, 1, 0),
                            (0, -1, -1), (0, -1, 1), (0, 1, -1), (0, 1, 1))
        direction_cost = (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.4, 1.4, 1.4, 1.4)
        adjacent_square_pick_index = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    # Loop until you find the end
    while len(open_list) > 0:
        #Randomize the order of the adjacent_squares_pick_index to avoid a decision making bias
        random.shuffle(adjacent_square_pick_index)
        outer_iterations += 1

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
            return return_path(current_node)

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
            if len([open_node for open_node in open_list if child.position == open_node.position and child.g > open_node.g]) > 0:
                continue

            # Add the child to the open list
            heapq.heappush(open_list, child)

    warn("Couldn't get a path to destination")
    return None