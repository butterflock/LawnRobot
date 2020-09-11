from threading import Lock

from control.DriveController import DriveController


class ArduinoDriveController(DriveController):

    def __init__(self):
        from serial import Serial
        self.ser = Serial('/dev/ttyUSB0', 19200)
        self.last_command = ""
        self.lock = Lock()

        self.m1 = 0
        self.m2 = 0

    def stop(self):
        self.send_command("s")
        self.last_command = ""
        distance = ((self.m1 + self.m2) / 2) / 2069
        print(f"Driven Distance: {distance}")

    def turn_right(self):
        self.send_drive_command('tr')

    def turn_left(self):
        self.send_drive_command('tl')

    def straight(self, speed):
        speed_command = int(round(speed, 1) * 255)
        command = f'df{speed_command :03d}'
        self.send_drive_command(command)

    def backwards(self, speed):
        speed_command = int(round(speed, 1) * 255)
        command = f'db{speed_command :03d}'
        self.send_drive_command(command)

    def send_drive_command(self, command):
        if self.last_command != command:
            self.last_command = command
            self.send_command(command)

    def send_command(self, command):
        print(f"Send command {command}")
        command = (command + "\n").encode('utf-8')
        self.lock.acquire()
        self.ser.write(command)
        message = self.ser.read_until()
        self.lock.release()
        return message

    async def get_info(self):
        message = self.send_command("i")
        m1, m2, heading = message.decode('utf-8')[1:].strip().split(";")

        distance = ((int(m1) + int(m2)) / 2) / 2069
        print(f"Status ${message}, Distance: {distance}")

        return distance, float(heading)
