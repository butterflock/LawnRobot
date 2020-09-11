from time import sleep

from gpiozero import Buzzer, Button

buzzer = Buzzer(18)

button = Button(4)

while True:
    print(f"Hall is active: {button.is_active}")
    if button.is_active:
        buzzer.on()
    sleep(0.5)
    buzzer.off()
