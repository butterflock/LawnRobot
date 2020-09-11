import time
from collections import deque
from threading import Thread
from typing import List

from processor.Processor import Processor
from util.common import make_interpreter, set_input, get_output


class Perception:
    def __init__(self, camera: str, model: str):

        self.camera = create_camera(camera)

        if model.endswith("edgetpu.tflite"):
            edge = True
        else:
            edge = False
        self.interpreter = create_interpreter(model, edge)

    async def get_update(self):
        frame, meta = self.camera.get_frame()

        if frame is None:
            print(f"Frame is None!")
            return None

        set_input(self.interpreter, frame)
        self.interpreter.invoke()
        seg = get_output(self.interpreter)

        update = {
            "rgb": frame,
            "seg": seg,
            "meta": meta
        }

        return update

    def shutdown(self):
        print("Shutdown perception")
        self.camera.release()


def create_camera(camera: str):
    if camera == 'pi':
        from camera.PiCamera import PiCamera
        return PiCamera()
    elif camera == 'opencv':
        from camera.OpenCvCamera import OpenCvCamera
        return OpenCvCamera()
    elif camera == 'img':
        assert input is not None
        from camera.FileCamera import FileCamera
        return FileCamera(input)
    elif camera == 'none':
        from camera.EmptyCamera import EmptyCamera
        return EmptyCamera()
    else:
        raise AttributeError("Invalid value for camera")


def create_interpreter(model, edge):
    interpreter = make_interpreter(model, edge=edge)
    interpreter.allocate_tensors()
    return interpreter
