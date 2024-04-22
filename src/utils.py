from itertools import product

def euclidean_distance(p1, p2):
    dim = max(len(p1), len(p2))
    p1_extended = [0] * (dim - len(p1)) + list(p1)
    p2_extended = [0] * (dim - len(p2)) + list(p2)
    return round(sum([(p1_extended[i] - p2_extended[i])**2 for i in range(dim)]) ** 0.5, 3)

def path_cost(path):
    return round(sum([euclidean_distance(path[i], path[i+1]) for i in range(len(path)-1)]), 2)

# enumerator for diagonal level: full diagonals, n-1 diagonals, n-2 diagonals, etc.
def generate_adjacent_squares(n, diagonal_level):
    coordinates = []
    for c in product((-1, 0, 1), repeat=n):
        full_sum = sum([abs(x) for x in c])
        undesired_planes_diagonal_sum = 0
        # sum of the first n-diagonal_level coordinates removes the undesired planes
        for i in range(n-diagonal_level):
            undesired_planes_diagonal_sum += abs(c[i])

        if full_sum <= diagonal_level and full_sum > 0:
            if undesired_planes_diagonal_sum == 0:
                coordinates.append(c)
            elif full_sum == undesired_planes_diagonal_sum:
                coordinates.append(c)

    return coordinates

def print_maze(maze, source, destination, path):
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
