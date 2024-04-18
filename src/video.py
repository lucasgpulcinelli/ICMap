import numpy as np
from PIL import Image
import cv2


def generate_video(path):
    imgs = []
    for i in range(5):
        imgs.append(Image.open(f"res/map/{i}.png"))

    videodims = imgs[0].size[0]*10, imgs[0].size[1]*10

    for i in range(5):
        imgs[i] = np.array(
            imgs[i].resize(videodims, Image.NEAREST))

    fourcc = cv2.VideoWriter_fourcc(*'MPEG')    
    video = cv2.VideoWriter("res/path.avi",fourcc, 1,videodims)

    for point in path:
        img = imgs[point[0]]

        for i in range(10):
            for j in range(10):
                img[point[1]*10+i, point[2]*10+j] = (255, 0, 0, 255)

        video.write(cv2.cvtColor(img, cv2.COLOR_RGBA2BGR))
    
    video.release()

generate_video([(0, 0, 0), (1, 0, 0), (1, 0, 1), (1, 0, 2), (1, 1, 2)])