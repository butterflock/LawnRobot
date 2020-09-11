import base64
from typing import Dict

import cv2

from processor.Processor import Processor, get_colored_seg


class NetworkProcessor(Processor):
    def __init__(self, safety_controller, update_callback):
        super(NetworkProcessor, self).__init__()
        self.safety_controller = safety_controller
        self.update_callback = update_callback

    def process(self, update: Dict):
        client_update = {
            "rgb": self.img_as_jpeg(self.add_drive_area(update["rgb"], update)),
            "seg": self.img_as_jpeg(self.add_drive_area(get_colored_seg(update["seg"]), update)),
            "fps": update["fps"],
            "distance": update["distance"],
            "heading": update["heading"],
            "automatic_drive_enabled": update["automatic_drive_enabled"],
            "automatic_drive_message": update["automatic_drive_message"],
            "is_safe_to_drive": self.safety_controller.is_safe_to_drive() if self.safety_controller is not None else True
        }
        self.update_callback(client_update)

    @staticmethod
    def add_drive_area(image, update: Dict):
        if "automatic_drive_area_corners" in update.keys():
            return cv2.polylines(image, [update["automatic_drive_area_corners"]], isClosed=True, color=(0, 0, 0),
                                 thickness=1)
        else:
            return image

    @staticmethod
    def img_as_jpeg(img):
        return base64.b64encode(cv2.imencode('.jpg', cv2.cvtColor(img, cv2.COLOR_RGB2BGR))[1]).decode('UTF-8')
