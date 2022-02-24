#!/usr/bin/env python
"""Plot the movement of the images and save it"""

import matplotlib.pyplot as plt
import numpy as np
from . import helper


def plot_equator(x_arr: np.ndarray, y_arr: np.ndarray, sequence: str, line: tuple):
    """
    Plot using matplotlib and save to directory
    """
    y_int = line[0] * x_arr + line[1]
    plt.plot(x_arr, y_arr, "xb", label="data points")
    plt.plot(
        x_arr, y_int, "r-", label="interpolated"
    )
    plt.ylabel(r"Y-coordinate of centre", fontsize=15)
    plt.xlabel(r"X-coordinate of centre", fontsize=15)
    plt.title("Heliocentric drift of the Earth due to the apparent movement of the Sun")
    plt.legend(loc="upper right")
    plt.errorbar(x_arr, y_arr, yerr=5, xerr=5, fmt="x", capsize=2)
    plt.savefig(f"./{sequence}/equatorial_plane.png", format="png", dpi=150)
    return True


if __name__ == "__main__":
    helper.warn_module()
