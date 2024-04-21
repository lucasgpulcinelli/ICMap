from itertools import product

def euclidean_distance(n, p1, p2):
    return round(sum([(p1[i] - p2[i])**2 for i in range(n)]) ** 0.5, 3)

# enumerator for diagonal level: full diagonals, n-1 diagonals, n-2 diagonals, etc.
def generate_adjacent_squares(n, diagonal_level):
    if diagonal_level > n:
        raise ValueError("Diagonal level cannot be greater than the number of dimensions")
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

    center = tuple([0 for _ in range(n)])
    adjacent_coordinates = []
    for x in coordinates:
        distance = euclidean_distance(n, x, center)
        adjacent_coordinates.append((distance, x))
    return adjacent_coordinates
