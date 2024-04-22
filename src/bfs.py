from collections import deque
import numpy as np
 
def isValid(vis, floor, row, col):
    #Cell out of bounds
    if floor > (len(vis) - 1) or floor < 0 or row > (len(vis[len(vis)-1]) -1) or row < 0 or col > (len(vis[len(vis)-1][0]) -1) or col < 0:
        return False
    #Cell already visited
    if (vis[floor][row][col] == True):
        return False 
    # Otherwise
    return True

def bfs(grid, start, end):
    vis = np.zeros_like(grid, dtype=bool)
    queue = deque()
    queue.append(start)
    vis[start] = True

    path_steps = []
    border_steps = []


    parent = {}
    while queue:
        border = []
        curr = queue.popleft()
        path_steps.append(reconstructPath(parent, start, curr))
        if curr == end:
            break
        # Check adjacent cells
        for dr, dc, dz in [(-1, 0, 0), (1, 0, 0), (0, 0, -1), (0, 0, 1), (0, -1, 0), (0, 1, 0),
                            (0, -1, -1), (0, -1, 1), (0, 1, -1), (0, 1, 1)]:
            newr, newc, newz = curr[0] + dr, curr[1] + dc, curr[2] + dz
            if isValid(vis,newr, newc, newz) and grid[newr][newc][newz]:
                queue.append((newr, newc, newz))
                vis[newr][newc][newz] = True
                parent[(newr, newc, newz)] = curr
                border.append((newr, newc, newz))
        border_steps.append(border)

    # Reconstruct path
    #ERROR IF PATH DOES NOT EXIST!
    path_steps.append(reconstructPath(parent, start, end))
    border_steps.append(None)
    return path_steps, border_steps


def reconstructPath(parent, start, end):
    path = []
    curr = end
    while curr != start:
        path.append(curr)
        curr = parent.get(curr)
        if curr is None:
            return None
    path.append(start)
    path.reverse()
    return path

