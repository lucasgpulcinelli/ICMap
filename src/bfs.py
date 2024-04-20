from collections import deque
import numpy as np
 
def isValid(vis, floor, row, col):
    #Cell out of bounds
    if (row < 0 or col < 0 or row >= 70 or col >= 102 or floor < 0 or floor >= 5):
        return False
    #Cell already visited
    if (vis[floor][row][col] == True):
        return False 
    # Otherwise
    return True

def bfs(grid, start, end):
    # Initialize a boolean array to keep track of visited cells
    vis = np.zeros_like(grid, dtype=bool)
    # Initialize a queue for BFS traversal
    queue = deque()
    # Add the start cell to the queue and mark it as visited
    queue.append(start)
    vis[start] = True
    # Initialize a dictionary to store the parent of each cell
    parent = {}
    # Perform BFS traversal
    while queue:
        curr = queue.popleft()
        if curr == end:
            break
        # Check adjacent cells
        for dr, dc, dz in [(0, 1, 0), (1, 0, 0), (0, -1, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1)]:
            newr, newc, newz = curr[0] + dr, curr[1] + dc, curr[2] + dz
            if isValid(vis,newr, newc, newz) and grid[newr][newc][newz]:
                queue.append((newr, newc, newz))
                vis[newr][newc][newz] = True
                parent[(newr, newc, newz)] = curr

    # Reconstruct path
    #ERROR IF PATH DOES NOT EXIST!
    path = []
    curr = end
    while curr != start:
        path.append(curr)
        curr = parent[curr]
    path.append(start)
    path.reverse()
    return path

