from control.DriveController import DriveController


class TestDriveController(DriveController):

    def turn_right(self):
        print("Turn right")

    def turn_left(self):
        print("Turn left")

    def straight(self, speed):
        print("Drive straight")

    def backwards(self, speed):
        print("Drive backwards")

    def stop(self):
        print("Stop!")

    async def get_info(self):
        print("Get Distance")
        return 1, 0.0
