import os
import time
from os.path import basename, splitext

import numpy as np
from PIL import Image
from camera.Camera import Camera


class FileCamera(Camera):

    def __init__(self, input):
        self.input = input
        self.image_paths = os.listdir(input)
        self.i = 0

    def get_frame(self):
        time.sleep(5)
        self.i = self.i % len(self.image_paths)
        img_name = self.image_paths[self.i]
        img = np.array(Image.open(self.input + "/" + img_name))
        self.i = self.i + 1
        return img, splitext(basename(img_name))[0]
