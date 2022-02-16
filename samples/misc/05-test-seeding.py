__author__ = "R Devon Hjelm, Bogdan Mazoure, Florian Golemo"
__copyright__ = "Copyright (c) Microsoft Corporation and Mila - Quebec AI " \
                "Institute"
__license__ = "MIT"

import cv2
import gym
import numpy as np
import imageio

import segar

resolution = 64

env1 = gym.make(
    "Segar-empty-hard-rgb-v0",
    num_envs=1,
    num_levels=2,
    framestack=1,
    resolution=resolution,
    max_steps=200,
    seed=123,
)
env2 = gym.make(
    "Segar-tilesx1-hard-rgb-v0",
    num_envs=1,
    num_levels=2,
    framestack=1,
    resolution=resolution,
    max_steps=200,
    seed=123,
)
env3 = gym.make(
    "Segar-objectsx2-hard-rgb-v0",
    num_envs=1,
    num_levels=2,
    framestack=1,
    resolution=resolution,
    max_steps=200,
    seed=123,
)

SCALE_FACTOR = 4
coords = []


cv2.namedWindow("image")

img_buf = np.zeros((resolution, resolution * 3 + 2, 3), np.uint8)

images = []
GIF_frames = 500
while 1:
    obs1 = env1.reset()
    obs2 = env2.reset()
    obs3 = env3.reset()
    done = False
    while 1:
        img_buf[:, :resolution, :] = obs1
        img_buf[:, resolution+1: resolution*2 + 1, :] = obs2
        img_buf[:, (resolution+1) * 2:, :] = obs3
        img_buf_rescaled = cv2.resize(img_buf, (0, 0), fx=SCALE_FACTOR, fy=SCALE_FACTOR)
        if GIF_frames:
            images.append(img_buf_rescaled)
            GIF_frames -= 1
        cv2.imshow(
            "image",
            img_buf_rescaled
        )
        # k = cv2.waitKey(-1) & 0xFF
        cv2.waitKey(10)

        action = env1.action_space.sample()

        obs1, rew1, done1, _ = env1.step(action)
        obs2, rew2, done2, _ = env2.step(action)
        obs3, rew3, done3, _ = env3.step(action)

        if done1 or done2 or done3:
            break

        if not GIF_frames:
            imageio.mimsave('movie.gif', images)
            print('GIF saved!')