from threading import Thread
from time import sleep
import picamera
import numpy as np

from camera.Camera import Camera


class PiCamera(Camera):

    def __init__(self):
        self.thread = Thread(target=self._thread)
        self.thread.start()
        self.frame = None
        self.release_camera = False

        while self.get_frame() is None:
            sleep(1)

    def _thread(self):
        """Camera background thread."""
        print('Starting camera thread.')
        frames_iterator = self.frames()
        for frame in frames_iterator:
            self.frame = frame
            sleep(0)

    def frames(self):
        with picamera.PiCamera() as camera:
            camera.resolution = (544, 432)
            camera.rotation = 180

            # let camera warm up
            sleep(2)
            w, h = camera.resolution
            output = np.empty((w * h * 3,), dtype=np.uint8)

            for _ in camera.capture_continuous(output, 'rgb', use_video_port=True):
                if self.release_camera:
                    break
                yield output.reshape((h, w, 3))[h - 420:, (w - 513) // 2:-(w - 513) // 2, :]

    def get_frame(self):
        return self.frame, self.get_timestamp()

    def release(self):
        self.release_camera = True
