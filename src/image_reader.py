import typing
from PIL import Image
import numpy as np
import os


def getImgs(dirName: str) -> typing.List[Image.Image]:
    '''
    getImgs reads all images in a directory named 0.png, 1.png, 2.png etc.

    It is assumed all images have the same size in the rest of the program.
    '''

    imgs = []
    i = 0

    try:
        while True:
            imgs.append(Image.open(os.path.join(dirName, f"{i}.png")))
            i += 1
    except FileNotFoundError:
        pass

    for i, img in enumerate(imgs):
        npI = np.array(img)
        img.close()
        imgs[i] = npI

    return imgs


def dirToWalkTensor(dirName: str) -> np.ndarray:
    '''
    dirToTensor reads all files named 0.png, 1.png, 2.png, etc. in a directory
    in order and returns a boolean tensor with the same size as the images such
    that all elements that are considered "walkable" are valued True and the
    rest are valued as False.

    Pixels are considered walkable if any of the RGB components are bright
    enough.
    '''

    imgs = getImgs(dirName)

    npTensor = np.array(imgs)

    # for every coordinate, divide by three the rgb values and sum them, if
    # the sum is > 127 the coordinate is walkable (the division is needed
    # because just addind them would cause an integer overflow)
    boolTensor = (npTensor[:, :, :, 0:3] / 3).sum(axis=3) > 127

    return boolTensor
