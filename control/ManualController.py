from control.Controller import Controller
from control.DriveController import DriveController


class ManualController(Controller):

    def __init__(self, drive_controller: DriveController):
        super().__init__(drive_controller)
        self.speed_multiplier = 0.5

    def exec_command_steer(self, angle):
        if -45 < angle < 45:
            self.drive_controller.straight(self.speed_multiplier)
        elif 45 < angle < 135:
            self.drive_controller.turn_right()
        elif -45 > angle > -135:
            self.drive_controller.turn_left()
        elif angle > 135 or angle < -135:
            self.drive_controller.backwards(self.speed_multiplier)

    def exec_command_speed(self, speed):
        print(f"Speed multiplier {speed}")
        self.speed_multiplier = speed

    def exec_command_active(self, active):
        print(f"Active {active}")
        if active is False:
            self.drive_controller.stop()
