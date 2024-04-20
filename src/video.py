import numpy as np
from PIL import Image
import cv2


def generate_video(solution, scale=10):
    imgs = []
    for i in range(5):
        imgs.append(Image.open(f"res/map/{i}.png"))

    videodims = imgs[0].size[0]*scale, imgs[0].size[1]*scale

    for i in range(5):
        imgs[i] = np.array(imgs[i])

    fourcc = cv2.VideoWriter_fourcc(*'MPEG')
    video = cv2.VideoWriter("res/path.avi", fourcc, 24, videodims)

    last_floor = -1

    f, x, y = solution[0][0][0]
    imgs[f][x, y] = (255, 0, 0, 255)

    for path, visited, border in zip(*solution):

        for f, x, y in border:
            imgs[f][x, y] = (255, 0, 0, 255)

        floor = path[-1][0]
        repeats = 1 if floor == last_floor else 12
        last_floor = floor

        frame = cv2.cvtColor(imgs[floor], cv2.COLOR_RGBA2BGR)
        resized = cv2.resize(frame, videodims,
                             interpolation=cv2.INTER_NEAREST_EXACT)

        for i in range(repeats):
            video.write(resized)

    video.release()
