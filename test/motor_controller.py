from gpiozero import DigitalOutputDevice, PWMOutputDevice, SmoothedInputDevice

# motor_enable = DigitalOutputDevice(22)
# direction = DigitalOutputDevice(27)
#
# speed_control = PWMOutputDevice(17, frequency=1000)

motor_enable = DigitalOutputDevice(13)
direction = DigitalOutputDevice(6)

speed_control = PWMOutputDevice(5, frequency=1000)

speed_control.value = 0.0

# speed = SmoothedInputDevice(18)

while True:
    key = input()

    if key == ' ':
        motor_enable.toggle()
    elif key == 'd':
        direction.toggle()
    elif key == 'f':
        speed_control.value = min(1, speed_control.value + 0.1)
    elif key == 's':
        speed_control.value = max(0, speed_control.value - 0.1)
    else:
        print(f"unknown key {key}")

    print(f"Enabled: {motor_enable.is_active}, Forward: {direction.is_active}, Speed Set: {speed_control.value}")
