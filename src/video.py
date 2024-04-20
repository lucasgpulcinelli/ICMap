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
    video = cv2.VideoWriter("res/path.avi", fourcc, 20, videodims)

    last_path = []

    for path, border in zip(*solution):
        for f, x, y in last_path:
            imgs[f][x, y] = (255, 0, 0, 255)

        if border is not None:
            for f, x, y in border:
                imgs[f][x, y] = (0, 255, 255, 255)

        for f, x, y in path:
            imgs[f][x, y] = (0, 0, 255, 255)

        floor = path[-1][0]

        last_path = path

        frame = cv2.cvtColor(imgs[floor], cv2.COLOR_RGBA2BGR)
        resized = cv2.resize(frame, videodims,
                             interpolation=cv2.INTER_NEAREST_EXACT)

        video.write(resized)

    video.release()
