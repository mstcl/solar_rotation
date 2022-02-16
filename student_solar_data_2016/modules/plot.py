#!/usr/bin/env python
"""Plot the movement of the images and save it"""

import matplotlib.pyplot as plt
import numpy as np


def plot_equator(x_arr: np.ndarray, y_arr: np.ndarray, sequence: str):
    """
    Plot using matplotlib and save to directory
    """
    plt.plot(x_arr, y_arr, "-ob")
    plt.savefig(f"./{sequence}/equatorial_plane.png", format="png", dpi=150)
    return True


if __name__ == "__main__":
    print("This file is not supposed to be executed directly")
