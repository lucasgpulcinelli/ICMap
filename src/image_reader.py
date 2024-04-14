from PIL import Image
import numpy as np
import os


def imgToWalkMatrix(filename: str) -> np.ndarray:
    '''
    imgToWalkMatrix reads a file containing an image and returns a boolean 
    matrix with the same size as the image such that all elements that are 
    considered "walkable" are valued True and the rest are valued as False.

    Pixels are considered walkable if any of the RGB components are bright 
    enough.
    '''

    pillow_img = Image.open(filename)

    matrix = np.asarray(pillow_img)
    pillow_img.close()

    return (matrix[:, :, 0:3] / 3).sum(axis=2) > 127


def dirToWalkTensor(dirName: str) -> np.ndarray:
    '''
    dirToTensor reads all files named 0.png, 1.png, 2.png, etc. in a directory 
    in order and creates a tensor with all walkable pixels. 

    It is assumed all images have the same size in the rest of the program.
    '''

    tensor = []
    try:
        i = 0
        while True:
            matrix = imgToWalkMatrix(os.path.join(dirName, f'{i}.png'))
            tensor.append(matrix)
            i += 1
    except FileNotFoundError:
        pass

    return np.array(tensor)
