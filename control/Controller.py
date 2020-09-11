from abc import ABC

from control.DriveController import DriveController


class Controller(ABC):

    def __init__(self, drive_controller: DriveController):
        self.drive_controller = drive_controller
