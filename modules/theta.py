#!/usr/bin/env python
"""
Find the angle between celestial north and sunspot
"""

import numpy as np
from . import helper


def get_angle(r_x: np.ndarray, r_y: np.ndarray, normal: float):
    """
    Determine theta from the sign of r_y and normal
    """
    angles = []
    for component in zip(r_x, r_y):
        angle = (
            np.arccos(
                (((component[0]**2 + component[1]**2) * (normal**2 + 1)) ** (-0.5))
                * (component[0] + (component[1] * normal))
            )
            * 180
            / np.pi
        )
        if angle > 180:
            angle = angle - 180
        if (component[1] > 0 and normal > 0) or (component[1] < 0 and normal < 0):
            angles.append(angle)
        else:
            angles.append(360 - angle)
    return np.array(angles)


if __name__ == "__main__":
    helper.warn_module()
