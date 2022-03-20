import math
import random
import datetime

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FFMpegWriter
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
from celluloid import Camera


def calculate_circle_coords():
    theta = random.random() * 2 * math.pi
    radius = random.random()
    x_rand = radius * math.cos(theta)
    y_rand = radius * math.sin(theta)
    return x_rand, y_rand


def calculate_obs(ob_count):
    x_obs = []
    y_obs = []
    for i in range(ob_count):
        x, y = calculate_circle_coords()
        x_obs.append(x)
        y_obs.append(y)
    return x_obs, y_obs


def animate_all(
        interval, total_steps, spadoc_ob_count, others_ob_count, x_spadoc,
        y_spadoc, x_others, y_others
):
    fig, ax = plt.subplots(figsize=[128, 128], dpi=100)
    fig.subplots_adjust(
        left=0, bottom=0, right=1, top=1, wspace=None, hspace=None
    )
    ax.patch.set_facecolor('black')

    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(
        bottom=False, labelbottom=False,
        left=False, labelleft=False
    )
    camera = Camera(fig)

    for frame in range(total_steps):
        curr_index_spadoc = (int(frame / total_steps * spadoc_ob_count))
        curr_index_others = (int(frame / total_steps * others_ob_count))
        x_spa = x_spadoc[0:curr_index_spadoc]
        y_spa = y_spadoc[0:curr_index_spadoc]
        x_oth = x_others[0:curr_index_others]
        y_oth = y_others[0:curr_index_others]
        plt.scatter(x_spa, y_spa, c='c')
        plt.scatter(x_oth, y_oth, c='m')
        camera.snap()

    return camera.animate(
        blit=True, interval=interval, repeat=False, repeat_delay=60 * 1000
    )


def animate_all_plt(frames, x_spadoc, y_spadoc, x_others, y_others):
    fig, ax = plt.subplots(figsize=[128, 128], dpi=100)
    fig.subplots_adjust(
        left=0, bottom=0, right=1, top=1, wspace=None, hspace=None
    )
    ax.patch.set_facecolor('black')

    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(
        bottom=False, labelbottom=False,
        left=False, labelleft=False
    )

    def animate_plt(frame):
        curr_index_spadoc = int(frame / frames * len(x_spadoc))
        curr_index_others = int(frame / frames * len(x_others))
        x_spa = x_spadoc[0:curr_index_spadoc]
        y_spa = y_spadoc[0:curr_index_spadoc]
        x_oth = x_others[0:curr_index_others]
        y_oth = y_others[0:curr_index_others]
        plt.scatter(x_spa, y_spa, c='c')
        plt.scatter(x_oth, y_oth, c='m')

    return animation.FuncAnimation(fig, animate_plt, frames=frames)


def main():
    # setup vars
    seconds = 18
    milliseconds = seconds * 1000
    interval = 100
    total_steps = int(milliseconds / interval)

    fps = 4
    frames = fps * seconds

    total_obs = 100000
    spadoc_ob_count = 8333
    others_ob_count = total_obs - spadoc_ob_count

    # calc points for spadoc and atlas
    x_spadoc, y_spadoc = calculate_obs(spadoc_ob_count)
    x_others, y_others = calculate_obs(others_ob_count)

    # animate
    # anim_all = animate_all(
    #     interval, total_steps, spadoc_ob_count, others_ob_count,
    #     x_spadoc, y_spadoc, x_others, y_others
    # )
    anim_all_plt = animate_all_plt(
        frames, x_spadoc, y_spadoc, x_others, y_others
    )
    # save
    # plt.rcParams['animation.ffmpeg_path'] = '/Users/engineer/opt/anaconda3/bin/ffmpeg'
    writer = animation.FFMpegWriter(fps=4)
    f = r"/Users/engineer/Desktop/spadoc_" + f"{datetime.datetime.now()}" + ".mp4"
    anim_all_plt.save(f, writer)


if __name__ == '__main__':
    main()
