from time import sleep

import numpy as np

from camera.Camera import Camera


class EmptyCamera(Camera):

    def get_frame(self):
        return np.zeros((420, 513, 3), dtype=np.uint8), self.get_timestamp()

    def release(self):
        pass
