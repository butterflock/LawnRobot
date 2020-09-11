import os
import sys

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib import gridspec


def create_lawn_label_colormap():
    colormap = np.zeros((256, 3), dtype=int)

    colormap[0] = (120, 120, 120)  # 0 - wall
    colormap[1] = (140, 140, 140)  # 1 - road
    colormap[2] = (4, 200, 3)  # 2 - vegetation
    colormap[3] = (204, 5, 255)  # 3 - object
    colormap[4] = (4, 250, 7)  # 4 - grass
    colormap[5] = (150, 5, 61)  # 5 - creature
    colormap[6] = (120, 120, 70)  # 6 - earth
    colormap[7] = (61, 230, 250)  # 7 - water
    colormap[8] = (6, 230, 230)  # 8 - background
    colormap[255] = (0, 0, 0)  # void

    return colormap


LABEL_NAMES = np.asarray([
    'wall', 'road', 'vegetation', 'object', 'grass', 'creature',
    'earth', 'water', 'background'])

COLOR_MAP = create_lawn_label_colormap()
FULL_COLOR_MAP = COLOR_MAP[np.arange(len(LABEL_NAMES)).reshape(len(LABEL_NAMES), 1)]


def vis_segmentation(image, seg_map, out=None):
    seg_map = seg_map.astype(int)
    plt.figure(figsize=(15, 5))
    grid_spec = gridspec.GridSpec(1, 4, width_ratios=[6, 6, 6, 1])

    plt.subplot(grid_spec[0])
    plt.imshow(image)
    plt.axis('off')
    plt.title('input image')

    plt.subplot(grid_spec[1])
    seg_image = COLOR_MAP[seg_map]
    # seg_image = seg_map
    plt.imshow(seg_image)
    plt.axis('off')
    plt.title('segmentation map')

    plt.subplot(grid_spec[2])
    plt.imshow(image)
    plt.imshow(seg_image, alpha=0.7)
    plt.axis('off')
    plt.title('segmentation overlay')

    ax = plt.subplot(grid_spec[3])
    plt.imshow(FULL_COLOR_MAP.astype(np.uint8), interpolation='nearest')
    ax.yaxis.tick_right()
    plt.yticks(range(len(FULL_COLOR_MAP)), LABEL_NAMES[range(len(FULL_COLOR_MAP))])
    plt.xticks([], [])
    ax.tick_params(width=0)

    if out is None:
        plt.show()
    else:
        plt.savefig(out)
        plt.close()


if __name__ == '__main__':
    rgb_folder = sys.argv[1] + "/rgb/"
    seg_folder = rgb_folder.replace("rgb", "seg")
    out_folder = rgb_folder.replace('rgb', 'out')
    os.mkdir(out_folder)

    for jpg_file in os.listdir(rgb_folder):
        camera = np.array(Image.open(rgb_folder + "/" + jpg_file))
        seg = np.array(Image.open(seg_folder + "/" + jpg_file.replace("jpg", "png")))
        vis_segmentation(camera, seg, out=f"{out_folder}/vis_{jpg_file.replace('jpg', 'png')}")
