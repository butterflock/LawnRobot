import time

import adafruit_bno055
import board
import busio

# Use these lines for I2C
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055_I2C(i2c)

sensor.mode = adafruit_bno055.NDOF_MODE

# User these lines for UART
# uart = busio.UART(board.TX, board.RX)
# sensor = adafruit_bno055.BNO055_UART(uart)

while True:
    # print("Temperature: {} degrees C".format(sensor.temperature))
    # print("Accelerometer (m/s^2): {}".format(sensor.acceleration))
    # print("Magnetometer (microteslas): {}".format(sensor.magnetic))
    # print("Gyroscope (rad/sec): {}".format(sensor.gyro))
    # print("Euler angle: {}".format(sensor.euler))
    # print("Quaternion: {}".format(sensor.quaternion))
    # print("Linear acceleration (m/s^2): {}".format(sensor.linear_acceleration))
    # print("Gravity (m/s^2): {}".format(sensor.gravity))
    # print()

    print(f"Calibrated: {sensor.calibration_status}")

    # mag_x, mag_y, mag_z = sensor.magnetic
    # heading = atan2(mag_y, mag_x) * 180/3.14159
    # print(f"Heading: {heading}")

    print(f"Mode: {sensor.mode}")
    print("Euler angle: {}".format(sensor.euler))

    time.sleep(1)
