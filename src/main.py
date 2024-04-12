#!/usr/bin/env python3

from PIL import Image
import numpy as np


def imgToMatrix(filename: str) -> np.ndarray:
    pillow_img = Image.open(filename)

    matrix = np.asarray(pillow_img)
    pillow_img.close()

    return matrix


if __name__ == "__main__":
    matrix = imgToMatrix('res/map.png')

    print(matrix.shape, '\n')

    red = matrix[:, :, 0]
    green = matrix[:, :, 1]
    blue = matrix[:, :, 2]

    is_walkable = matrix.sum(axis=2) > 0

    print(red, '\n')
    print(green, '\n')
    print(blue, '\n')
    print(is_walkable, '\n')
