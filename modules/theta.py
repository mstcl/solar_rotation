#!/usr/bin/env python
"""
Find the angle between celestial north and sunspot
"""

import numpy as np


def get_angle(r_x:float, r_y:float, normal:float):
    """
    Determine theta from the sign of r_y and normal
    """
    angle = (
        np.arccos(
            (((r_x**2 + r_y**2) * (normal**2 + 1)) ** (-0.5))
            * (r_x + (r_y * normal))
        )
        * 180
        / np.pi
    )
    if angle > 180:
        angle = angle - 180

    if r_y > 0:
        return angle if normal > 0 else (360 - angle)
    return (360 - angle) if normal > 0 else angle


if __name__ == "__main__":
    print("This file is not supposed to be executed directly")
