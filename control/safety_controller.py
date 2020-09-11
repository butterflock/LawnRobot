from control.DriveController import DriveController
from gpiozero import Button, Buzzer


class SafetyController(DriveController):

    def __init__(self, drive_controller, buzzer: Buzzer):
        self.buzzer = buzzer
        self.drive_controller = drive_controller
        self.button = Button(26)
        self.button.when_deactivated = self.on_safety_switch_is_triggered
        self.button.when_activated = self.on_safety_switch_is_untriggered

    def on_safety_switch_is_triggered(self):
        print("Safety switch was triggered")
        self.drive_controller.stop()
        self.buzzer.beep(n=1)

    @staticmethod
    def on_safety_switch_is_untriggered():
        print("Safety switch was closed. It is safe to drive again")

    def is_safe_to_drive(self):
        return self.button.is_active

    def turn_right(self):
        if self.is_safe_to_drive():
            self.drive_controller.turn_right()
        else:
            print("It is not safe to drive")
            self.drive_controller.stop()

    def turn_left(self):
        if self.is_safe_to_drive():
            self.drive_controller.turn_left()
        else:
            print("It is not safe to drive")
            self.drive_controller.stop()

    def straight(self, speed):
        if self.is_safe_to_drive():
            self.drive_controller.straight(speed)
        else:
            print("It is not safe to drive")
            self.drive_controller.stop()

    def backwards(self, speed):
        if self.is_safe_to_drive():
            self.drive_controller.backwards(speed)
        else:
            print("It is not safe to drive")
            self.drive_controller.stop()

    def stop(self):
        self.drive_controller.stop()

    async def get_info(self):
        return await self.drive_controller.get_info()
