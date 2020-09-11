import cv2
import numpy as np
from dynarray import DynamicArray
from imutils import rotate_bound


class Map:
    def __init__(self):
        self.map = DynamicArray((None, None))
        self.position = (0, 0, 0)  # x, y, heading

        src = np.float32([[100, 255], [429, 255], [0, 0], [513, 0]])
        dst = np.float32([[202, 255], [328, 255], [0, 0], [513, 0]])
        self.warp_matrix = cv2.getPerspectiveTransform(src, dst)

    def update(self, x, y, r, image):
        self_x, self_y, self_r = self.position

        new_x = x + self_x
        new_y = y + self_y
        new_r = (r + self_r) % 360

        rotated_image = rotate_bound(image, new_r)

    def warp_image(self, img):
        return cv2.warpPerspective(img, self.warp_matrix, (513, 255))

    def rotate(self, image, heading):
        # grab the dimensions of the image and then determine the
        # center
        (h, w) = image.shape[:2]
        (cX, cY) = (w / 2, h / 2)

        # grab the rotation matrix (applying the negative of the
        # angle to rotate clockwise), then grab the sine and cosine
        # (i.e., the rotation components of the matrix)
        M = cv2.getRotationMatrix2D((cX, cY), -heading, 1.0)
        cos = np.abs(M[0, 0])
        sin = np.abs(M[0, 1])

        # compute the new bounding dimensions of the image
        nW = int((h * sin) + (w * cos))
        nH = int((h * cos) + (w * sin))

        # adjust the rotation matrix to take into account translation
        M[0, 2] += (nW / 2) - cX
        M[1, 2] += (nH / 2) - cY

        center = (M.dot(np.array([h, w / 2, 1]).T))
        center[0] = round(max(0, min(nH, center[0])))
        center[1] = round(max(0, min(nW, center[1])))
        center = center.astype(int)

        # perform the actual rotation and return the image
        return cv2.warpAffine(image, M, (nW, nH)), center
