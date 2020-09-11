import cv2

from camera.Camera import Camera


class OpenCvCamera(Camera):

    def __init__(self):
        self.cap = cv2.VideoCapture(0)

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 513)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 420)

    def get_frame(self):
        _, frame = self.cap.read()
        if frame is not None:
            h, w, _ = frame.shape
            dif_w = (w - 513) // 2
            cv2_im = frame[h - 420:h, dif_w: w - dif_w - 1]
            cv2_im_rgb = cv2.cvtColor(cv2_im, cv2.COLOR_BGR2RGB)
            return cv2_im_rgb, self.get_timestamp()
        else:
            return None, None

    def release(self):
        self.cap.release()
