import os
import cv2

import image_reader


def generate_video(solution, scale=10):
    '''
    generate_video generates an avi video in "res/path.avi" showing the 
    discovery of a solution to find a path using a search algorithm.

    the video first draws the discovery of the solution process: it creates a 
    frame with the path at every iteration coloring the path being tested blue,
    the already visited nodes red, and the border (nodes to be visited at some
    point in the future) cyan. After that, the full found path is shown from 
    beginning to end.
    '''

    imgs = image_reader.getImgs(os.path.join("res", "map"))

    videodims = imgs[0].shape[1]*scale, imgs[0].shape[0]*scale

    # create the video writer with 20 fps
    fourcc = cv2.VideoWriter_fourcc(*'MPEG')
    video = cv2.VideoWriter(os.path.join(
        "res", "path.avi"), fourcc, 20, videodims)

    # the path at the previous iteration is needed to color the pixels back
    # from blue to red
    last_path = []

    red = (255, 0, 0, 255)
    cyan = (0, 255, 255, 255)
    blue = (0, 0, 255, 255)

    # for every step
    for path, border in zip(*solution):
        # color the pixels from the last path back to red (these necessarely
        # have already been visited)
        for f, x, y in last_path:
            imgs[f][x, y] = red

        # color the border of new nodes to be traveled
        if border is not None:
            for f, x, y in border:
                imgs[f][x, y] = cyan

        # color the path being explored now
        for f, x, y in path:
            imgs[f][x, y] = blue
        floor = path[-1][0]

        last_path = path

        # and send the frame to the video using the floor of the node being
        # visited now
        frame = cv2.cvtColor(imgs[floor], cv2.COLOR_RGBA2BGR)
        resized = cv2.resize(frame, videodims,
                             interpolation=cv2.INTER_NEAREST_EXACT)

        video.write(resized)

    # now, show the full found path

    # reload all images
    imgs = image_reader.getImgs(os.path.join("res", "map"))

    # for every step in the final path
    for f, x, y in solution[0][-1]:
        # color it
        imgs[f][x, y] = blue

        # and draw the frame 6 times in order to slow the path creation
        frame = cv2.cvtColor(imgs[f], cv2.COLOR_RGBA2BGR)
        resized = cv2.resize(frame, videodims,
                             interpolation=cv2.INTER_NEAREST_EXACT)

        for _ in range(6):
            video.write(resized)

    video.release()
