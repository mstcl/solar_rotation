#!/usr/bin/env python
"""
Find the coordinate of sunspots
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter


def parse_data():
    """
    Parse data into tuples
    """
    with open(
        "../solar_2016-10-05_seq1/sunspot_data/y_constant_a_1.txt", "r", encoding="utf"
    ) as sunspot_file:
        x_data = [
            (
                float(line.strip("\n").split(" ")[0]),
                float(line.strip("\n").split(" ")[1]),
            )
            for line in sunspot_file.readlines()[:-1]
            if float(line.strip("\n").split(" ")[1]) > 200
        ]
    coord = np.array([val[0] for val in x_data])
    counts = np.array([val[1] for val in x_data])
    y = savgol_filter(counts,65,5)
    plt.plot(coord,y)
    plt.show()
    print(np.where(np.diff(np.diff(y)) > 0)[0])

if __name__ == "__main__":
    parse_data()
