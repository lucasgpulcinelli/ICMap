import numpy as np
from PIL import Image
import cv2


def getImgs():
    imgs = []
    for i in range(5):
        imgs.append(Image.open(f"res/map/{i}.png"))

    for i in range(5):
        imgs[i] = np.array(imgs[i])

    return imgs


def generate_video(solution, scale=10):
    imgs = getImgs()

    videodims = imgs[0].shape[1]*scale, imgs[0].shape[0]*scale

    fourcc = cv2.VideoWriter_fourcc(*'MPEG')
    video = cv2.VideoWriter("res/path.avi", fourcc, 20, videodims)

    last_path = []

    red = (255, 0, 0, 255)
    cyan = (0, 255, 255, 255)
    blue = (0, 0, 255, 255)

    for path, border in zip(*solution):
        for f, x, y in last_path:
            imgs[f][x, y] = red

        if border is not None:
            for f, x, y in border:
                imgs[f][x, y] = cyan

        for f, x, y in path:
            imgs[f][x, y] = blue
        floor = path[-1][0]

        last_path = path

        frame = cv2.cvtColor(imgs[floor], cv2.COLOR_RGBA2BGR)
        resized = cv2.resize(frame, videodims,
                             interpolation=cv2.INTER_NEAREST_EXACT)

        video.write(resized)

    imgs = getImgs()

    for f, x, y in solution[0][-1]:
        imgs[f][x, y] = blue

        frame = cv2.cvtColor(imgs[f], cv2.COLOR_RGBA2BGR)
        resized = cv2.resize(frame, videodims,
                             interpolation=cv2.INTER_NEAREST_EXACT)

        for i in range(6):
            video.write(resized)

    video.release()
