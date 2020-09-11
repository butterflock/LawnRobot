import datetime
from os import mkdir
from queue import Queue
from threading import Thread
from typing import Dict

import numpy as np
from PIL import Image
from processor.Processor import Processor


class StoreFileProcessor(Processor):
    def __init__(self, output_folder="img"):
        folder = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        self.output_folder = output_folder + "/" + folder
        mkdir(self.output_folder)
        print(self.output_folder)

        self.queue = Queue()
        self.running = True

        self.meta_file = open(self.output_folder + "/meta1.txt", "w")

        def store_file_loop():
            while self.running or not self.queue.all_tasks_done:
                update = self.queue.get()
                Image.fromarray(update["rgb"]).save(self.output_folder + f"/{update['meta']}.jpg")
                Image.fromarray(update["seg"].astype(np.uint8)).save(self.output_folder + f"/{update['meta']}.png")
                self.meta_file.write(f"{update['meta']};{update['distance']};{update['heading']}\n")
                self.meta_file.flush()
                self.queue.task_done()
            self.meta_file.close()

        thread = Thread(target=store_file_loop)
        thread.start()

    def process(self, update: Dict):
        self.queue.put(update)

    def shutdown(self):
        self.running = False
