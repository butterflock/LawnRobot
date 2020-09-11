import cv2
import numpy as np

from vis import vis_segmentation
import matplotlib.pyplot as plt


def check_for_obstacle(drive_area):
    return np.any((drive_area != 4) & (drive_area != 255))


# original image
# -1 loads as-is so if it will be 3 or 4 channel as the original
image = cv2.imread('img/20200708-213521.jpg', -1)
seg = cv2.imread('seg/20200708-213521.png', -1)

# image = cv2.imread('img/1_20200708-213601.jpg', -1)
# seg = cv2.imread('img/1_20200708-213601.png', -1)

# mask defaulting to black for 3-channel and transparent for 4-channel
# (of course replace corners with yours)
image = image[224:, :]
seg = seg[224:, :]
mask = np.ones(seg.shape, dtype=np.uint8)
roi_corners = np.array([[(0, 196), (0, 66), (74, 0), (487, 16), (513, 46), (513, 196)]], dtype=np.int32)
cv2.fillConvexPoly(mask, roi_corners, (0,))

mask = mask.astype(dtype=bool)

drive_area = np.copy(seg)
drive_area[mask] = 255

if check_for_obstacle(drive_area):
    print("Obstacle Detected")

vis_segmentation(image, drive_area)
