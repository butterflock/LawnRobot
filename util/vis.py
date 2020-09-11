import numpy as np


def create_lawn_label_colormap():
    return np.asarray([
        (120, 120, 120),    # 0 - wall
        (140, 140, 140),    # 1 - road
        (4, 200, 3),        # 2 - vegetation
        (204, 5, 255),      # 3 - object
        (4, 250, 7),        # 4 - grass
        (150, 5, 61),       # 5 - creature
        (120, 120, 70),     # 6 - earth
        (61, 230, 250),     # 7 - water
        (6, 230, 230),      # 8 - background
    ])
