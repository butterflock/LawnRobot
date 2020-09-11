import asyncio
import random
import time
from collections import deque
from enum import Enum
from threading import Thread
from typing import Dict

import cv2
import numpy as np

from control.Controller import Controller
from control.DriveController import DriveController


class AutomaticController(Controller):

    def __init__(self, drive_controller: DriveController, processors):
        super().__init__(drive_controller)
        self.perception = None
        (self.mask, self.corners, self.drive_rect) = self.create_mask()

        self.processors = processors

        self.is_in_turn = False
        self.distance = 0

        self.automatic_drive_enabled = False
        self.running = False

    def start(self, perception):
        self.is_in_turn = False
        self.distance = 0

        self.perception = perception
        self.running = True
        thread = Thread(target=self.start_async)
        thread.start()

    def stop(self):
        self.disable_automatic_drive()
        self.perception.shutdown()
        [processor.shutdown() for processor in self.processors]
        self.running = False
        self.drive_controller.stop()

    def start_async(self):
        asyncio.run(self.run())

    async def run(self):
        print("Running...")
        fps = deque(maxlen=20)
        fps.append(time.time())

        # wait until first camera frame
        while await self.perception.get_update() is None:
            await asyncio.sleep(2)

        while self.running:
            update, info = await asyncio.gather(self.perception.get_update(), self.drive_controller.get_info())

            distance, heading = info

            if update is None:
                print(f"Perception is shutdown!")
                break

            fps.append(time.time())
            fps_ms = len(fps) / (fps[-1] - fps[0])

            self.distance += distance

            update["fps"] = fps_ms
            update["distance"] = self.distance
            update["heading"] = heading

            self.process(update)

    def update_processors(self, update, message):
        update["automatic_drive_enabled"] = self.automatic_drive_enabled
        update["automatic_drive_message"] = message
        if self.automatic_drive_enabled:
            update["automatic_drive_area_corners"] = self.corners
        [processor.process(update) for processor in self.processors]

    def enable_automatic_drive(self):
        self.automatic_drive_enabled = True
        self.is_in_turn = False

    def disable_automatic_drive(self):
        self.automatic_drive_enabled = False

    def process(self, update: Dict):
        if self.automatic_drive_enabled:
            seg = update["seg"]

            obstacle_detected = self.check_for_obstacle(seg)

            if obstacle_detected != Obstacle.NONE:
                if not self.is_in_turn:
                    self.is_in_turn = True

                    if obstacle_detected == Obstacle.LEFT:
                        self.drive_controller.turn_right()
                    elif obstacle_detected == Obstacle.RIGHT:
                        self.drive_controller.turn_left()
                    else:
                        if random.randint(0, 1) == 1:
                            self.drive_controller.turn_right()
                        else:
                            self.drive_controller.turn_left()
            else:
                self.is_in_turn = False
                self.drive_controller.straight(0.5)

            if obstacle_detected == Obstacle.NONE:
                message = ""
            elif obstacle_detected == Obstacle.NO_GRASS:
                message = "No grass detected!"
            elif obstacle_detected == Obstacle.RIGHT:
                message = "Obstacle detected (Right)!"
            elif obstacle_detected == Obstacle.LEFT:
                message = "Obstacle detected (Left)!"
            else:
                message = "Unknown error"
            self.update_processors(update, message)
        else:
            self.update_processors(update, "")

    def check_for_obstacle(self, seg):
        drive_area = np.copy(seg[self.drive_rect[1]:, :])
        drive_area[self.mask] = 255

        half_width = drive_area.shape[1] // 2

        pixel_rights = self.check_pixels(drive_area[:, half_width:])
        pixel_lefts = self.check_pixels(drive_area[:, :half_width])

        if pixel_lefts > 0 or pixel_rights > 0:
            if pixel_lefts > pixel_rights:
                print("Obstacle detected! (Left)")
                return Obstacle.LEFT
            else:
                print("Obstacle detected! (Right)")
                return Obstacle.RIGHT

        elif np.all(drive_area != 4):
            print("No grass detected")
            return Obstacle.NO_GRASS
        else:
            return Obstacle.NONE

    @staticmethod
    def check_pixels(image):
        obstacle_condition = (image == 0) | (image == 2) | (image == 3) | (image == 5) | (image == 7)
        return np.count_nonzero(obstacle_condition)

    @staticmethod
    def create_mask():
        corners = CameraConfigs.drive_area_waveshare

        drive_rect = np.min(corners, axis=1)[0]

        mask = np.zeros((420 - drive_rect[1], 513), dtype=np.uint8)
        roi_corners = corners - drive_rect

        cv2.fillConvexPoly(mask, roi_corners, (0,))

        mask = mask.astype(dtype=bool)

        return mask, corners, drive_rect


class Obstacle(Enum):
    NONE = 0
    RIGHT = 1
    LEFT = 2
    NO_GRASS = 3


class CameraConfigs:
    drive_area_old = np.array([[(0, 420), (0, 365), (87, 249), (442, 245), (513, 334), (513, 420)]], dtype=np.int32)
    drive_area_waveshare = np.array([[(76, 420), (146, 242), (385, 237), (462, 420)]], dtype=np.int32)
