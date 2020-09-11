###  COPY ALL THE CODE INTO A JYPYTER NOTEBOOK  ###
###  THE JYPYTER NOTEBOOK NEEDS TO BE IN 'tensorflow\models\research\deeplab'  ###

## Imports

import os
import sys
import time

import numpy as np
import tensorflow as tf
from PIL import Image
from vis import vis_segmentation


class DeepLabModel(object):
    """Class to load deeplab model and run inference."""

    INPUT_TENSOR_NAME = 'ImageTensor:0'
    OUTPUT_TENSOR_NAME = 'SemanticPredictions:0'
    INPUT_SIZE = (420, 513)

    def __init__(self, frozen_graph_filename):
        """Creates and loads pretrained deeplab model."""
        self.graph = tf.Graph()

        with tf.gfile.GFile(frozen_graph_filename, "rb") as f:
            graph_def = tf.GraphDef.FromString(f.read())

        if graph_def is None:
            raise RuntimeError('Cannot find inference graph in tar archive.')

        with self.graph.as_default():
            tf.import_graph_def(graph_def, name='')

        self.sess = tf.Session(graph=self.graph)

    def run(self, image):
        """Runs inference on a single image.

        Args:
            image: A PIL.Image object, raw input image.

        Returns:
            resized_image: RGB image resized from original input image.
            seg_map: Segmentation map of `resized_image`.
        """
        batch_seg_map = self.sess.run(
            self.OUTPUT_TENSOR_NAME,
            feed_dict={self.INPUT_TENSOR_NAME: [np.asarray(image)]})
        seg_map = batch_seg_map[0]
        return image, seg_map


model = DeepLabModel(sys.argv[1])

## Run on sample images

# Note that we are using single scale inference in the demo for fast
# computation, so the results may slightly differ from the visualizations
# in README, which uses multi-scale and left-right flipped inputs.


def run_demo_image(image_dir):
    listdir = os.listdir(image_dir)
    print(f'running deeplab...')
    images = []
    for image_path in listdir:
        images.append(Image.open(os.path.join(image_dir, image_path)))

    start_time = time.process_time()
    for image in images:
        resized_im, seg_map = model.run(image)
    elapsed_time = time.process_time() - start_time
    print(f'Finished deeplab in {elapsed_time} ({elapsed_time / len(listdir)} per image).')
    vis_segmentation(resized_im, seg_map)


run_demo_image(sys.argv[2])
