#!/usr/bin/env python3

import image_reader
import maze_solver

if __name__ == "__main__":
    tensor = image_reader.dirToWalkTensor('res/map')

    print(maze_solver.solveBFS(tensor, (0, 2, 2), (0, 29, 29)))
