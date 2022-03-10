"""
Plot a dataset and save it
"""

import matplotlib.pyplot as plt
import numpy as np
from . import helper


def plot_equator(x_arr: np.ndarray, y_arr: np.ndarray, sequence: str, line: tuple):
    """
    Plot equator movement and save to directory
    """
    y_int = line[0] * x_arr + line[1]
    plt.plot(x_arr, y_int, "r--", label="interpolated")
    plt.ylabel(r"Y-coordinate of centre / pixel", fontsize=15)
    plt.xlabel(r"X-coordinate of centre / pixel", fontsize=15)
    plt.title("Apparent movement of the Sun due to Earth's rotation")
    # plt.legend(loc="upper right") # Uncomment for legend
    plt.errorbar(x_arr, y_arr, yerr=5, xerr=5, fmt="xb", capsize=2)
    plt.savefig(f"./{sequence}/equatorial_plane.png", format="png", dpi=150)
    return True


def plot_long_against_jd(
    longs: np.ndarray,
    dates: np.ndarray,
    freqs: np.ndarray,
    longs_err: np.ndarray,
    spot: int,
    is_nasa: bool
):
    """
    Plot longitude of a feature against JD
    """
    factor = 1
    if is_nasa:
        factor = -1
    plt.clf()
    intercept_max = longs[0] + factor*max(freqs) * dates[0]
    intercept_min = longs[0] + factor*min(freqs) * dates[0]
    y_pred_max = -factor*max(freqs) * dates + intercept_max
    y_pred_min = -factor*min(freqs) * dates + intercept_min
    plt.plot(dates, y_pred_max, "g:", label="longitude max")
    plt.plot(dates, y_pred_min, "b:", label="longitude min")
    plt.ylabel(r"$L$ - $L_0$ / $\circ$", fontsize=15)
    plt.xlabel(r"Julian day / days", fontsize=15)
    plt.title(f"Displacement of feature {spot} due to solar rotation", fontsize=15)
    if is_nasa:
        plt.legend(loc="upper left")
    else:
        plt.legend(loc="upper right")
    plt.errorbar(dates, longs, yerr=longs_err, xerr=0, fmt="xk", capsize=2)
    plt.savefig(f"./dataset/long_{spot}.png", format="png", dpi=150)


def plot_lat_against_jd(
    lats: np.ndarray,
    dates: np.ndarray,
    lats_err: np.ndarray,
    spot: int,
):
    """
    Plot latitude of a feature against JD
    """
    plt.clf()
    # int_line = helper.get_line(dates, longs)
    # y_int = int_line[0] * dates + int_line[1]
    plt.ylabel(r"$B$ / $\circ$", fontsize=15)
    plt.xlabel(r"Julian day / days", fontsize=15)
    plt.title(f"Latitude of feature {spot} over time", fontsize=15)
    plt.errorbar(dates, lats, yerr=lats_err, xerr=0, fmt="xk", capsize=2)
    plt.savefig(f"./dataset/lat_{spot}.png", format="png", dpi=150)



if __name__ == "__main__":
    helper.warn_module()
