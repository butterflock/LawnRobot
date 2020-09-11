import time
from threading import Thread


class ConnectionValidator:
    def __init__(self, disconnect_callback):
        self.alive_thread = None
        self.alive_signal = time.time()
        self.disconnect_callback = disconnect_callback

    def on_connect(self):
        self.on_alive_signal()
        self.alive_thread = Thread(target=self.poll_alive)
        self.alive_thread.start()

    def disconnect(self):
        self.disconnect_callback()

    def poll_alive(self):
        while True:
            time.sleep(1)

            if self.alive_signal + 2 < time.time():
                print(f"Client sent no life signal for {time.time() - self.alive_signal}")
                self.disconnect()
                break

    def on_alive_signal(self):
        self.alive_signal = time.time()
