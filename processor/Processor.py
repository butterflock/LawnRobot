from abc import ABC, abstractmethod
from typing import Dict

import numpy as np

from test import vis

color_mapping = vis.create_lawn_label_colormap()


def get_colored_seg(seg):
    return color_mapping[seg].astype(np.dtype('uint8'))


class Processor(ABC):

    @abstractmethod
    def process(self, update: Dict):
        pass

    def shutdown(self):
        pass
