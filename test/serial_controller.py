import serial

speed = 0.0
direction = 'f'
enable = False

with serial.Serial('/dev/cu.usbmodem14401', 19200, timeout=1) as ser:
    while True:
        key = input()

        if key == ' ':
            enable = not enable
        elif key == 'd':
            if direction == 'f':
                direction = 'b'
            else:
                direction = 'f'
        elif key == 'f':
            speed = min(1.0, speed + 0.1)
        elif key == 's':
            speed = max(0.0, speed - 0.1)
        else:
            print(f"unknown key {key}")

        if enable:
            command = f'd{direction}{(int(speed * 255)):03d}\n'.encode('utf-8')
            print(f"Send command {command}")
            ser.write(command)
        else:
            ser.write('s\n'.encode('utf-8'))

        print(ser.read_until('\n').decode("utf-8"))
