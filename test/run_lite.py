import os
import sys
import time

import numpy as np
import tflite_runtime.interpreter as tflite
from PIL import Image
from vis import vis_segmentation

# Load TFLite model and allocate tensors.
interpreter = tflite.Interpreter(model_path=sys.argv[1])
interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

input_shape = input_details[0]['shape']

def run(images):
    output_data = []
    for i in range(images.shape[0]):
        input = images[i: i+1]
        interpreter.set_tensor(input_details[0]['index'], input)

        interpreter.invoke()

        # The function `get_tensor()` returns a copy of the tensor data.
        # Use `tensor()` in order to get a pointer to the tensor.
        output_data.append(interpreter.get_tensor(output_details[0]['index']))
    return output_data

def run_demo_image(image_dir):
    listdir = os.listdir(image_dir)[:10]
    print(f'running deeplab...')
    images = np.zeros((len(listdir), 420, 513, 3), dtype=np.uint8)
    for i, image_path in enumerate(listdir):
        images[i, :, :, :] = np.asarray(Image.open(os.path.join(image_dir, image_path)))

    start_time = time.process_time()
    # for image in images:
    #     seg_map = run(image)
    seg_map = run(images)
    elapsed_time = time.process_time() - start_time
    print(f'Finished deeplab in {elapsed_time} ({elapsed_time / len(listdir)} per image).')
    vis_segmentation(images[0], np.squeeze(seg_map[0]))


run_demo_image(sys.argv[2])
