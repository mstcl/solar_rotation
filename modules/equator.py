#!/usr/bin/env python
"""Find the equation of the line given a set of x,y values"""

import numpy as np


def get_line(x_arr: np.ndarray, y_arr: np.ndarray):
    """Interpolate to first degree and return gradient"""
    return tuple(np.polyfit(x_arr, y_arr, 1))


if __name__ == "__main__":
    print("This file is not supposed to be executed directly")
