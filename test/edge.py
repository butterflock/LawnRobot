# Lint as: python3
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
r"""Example using TF Lite to classify a given image using an Edge TPU.
   To run this code, you must attach an Edge TPU attached to the host and
   install the Edge TPU runtime (`libedgetpu.so`) and `tflite_runtime`. For
   device setup instructions, see g.co/coral/setup.
   Example usage (use `install_requirements.sh` to get these files):
   ```
   python3 classify_image.py \
     --model models/mobilenet_v2_1.0_224_inat_bird_quant_edgetpu.tflite  \
     --labels models/inat_bird_labels.txt \
     --input images/parrot.jpg
   ```
"""

import argparse
import time

from PIL import Image

import classify
import tflite_runtime.interpreter as tflite
import platform

from vis import vis_segmentation

EDGETPU_SHARED_LIB = {
    'Linux': 'libedgetpu.so.1',
    'Darwin': 'libedgetpu.1.dylib',
    'Windows': 'edgetpu.dll'
}[platform.system()]


def load_labels(path, encoding='utf-8'):
    """Loads labels from file (with or without index numbers).
  Args:
    path: path to label file.
    encoding: label file encoding.
  Returns:
    Dictionary mapping indices to labels.
  """
    with open(path, 'r', encoding=encoding) as f:
        lines = f.readlines()
        if not lines:
            return {}

        if lines[0].split(' ', maxsplit=1)[0].isdigit():
            pairs = [line.split(' ', maxsplit=1) for line in lines]
            return {int(index): label.strip() for index, label in pairs}
        else:
            return {index: line.strip() for index, line in enumerate(lines)}


def make_interpreter(model_file, edge):
    model_file, *device = model_file.split('@')
    if edge:
        return tflite.Interpreter(
            model_path=model_file,
            experimental_delegates=[tflite.load_delegate(EDGETPU_SHARED_LIB, {'device': device[0]} if device else {})]
        )
    else:
        return tflite.Interpreter(model_path=model_file)


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-m', '--model', required=True, help='File path of .tflite file.')
    parser.add_argument(
        '-i', '--input', required=True, help='Image to be classified.')
    parser.add_argument(
        '-l', '--labels', help='File path of labels file.')
    parser.add_argument(
        '-c', '--count', type=int, default=5,
        help='Number of times to run inference')
    parser.add_argument(
        '-e', '--edge', action="store_true", help='set for edge tpu'
    )
    parser.add_argument(
        '-o', '--output', type=str, default=None,
        help="Saves the inferred to the given folder"
    )
    args = parser.parse_args()

    interpreter = make_interpreter(args.model, args.edge)
    interpreter.allocate_tensors()

    size = classify.input_size(interpreter)
    print(f"Size: {size}")
    image = Image.open(args.input).convert('RGB').resize(size, Image.ANTIALIAS)
    classify.set_input(interpreter, image)

    print('----INFERENCE TIME----')
    print('Note: The first inference on Edge TPU is slow because it includes',
          'loading the model into Edge TPU memory.')
    for _ in range(args.count):
        start = time.perf_counter()
        interpreter.invoke()
        inference_time = time.perf_counter() - start
        seg = classify.get_output(interpreter)

        print('%.1fms' % (inference_time * 1000))

    if args.output is not None:
        vis_segmentation(image, seg, out=args.output)


if __name__ == '__main__':
    main()
