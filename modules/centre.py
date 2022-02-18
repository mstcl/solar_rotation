#!/usr/bin/env python
"""Fetch the centres of the sun discs"""

from os.path import exists as file_exists
import numpy as np


def parse_data(files_num: int, sequence: str):
    """
    Go through each file and appends centre coordinate
    """
    x_arr, y_arr = np.zeros(files_num, dtype="float64"), np.zeros(
        files_num, dtype="float64"
    )
    radii = np.array(x_arr)
    for file in range(files_num):
        if not file_exists(f"./{sequence}/regions/sun_disc_{file+1}.reg"):
            raise FileNotFoundError(
                "Check name format, sequence name, and number of files and try again.\n"
            )
        with open(
            f"./{sequence}/regions/sun_disc_{file+1}.reg", "r", encoding="utf-8"
        ) as regionfile:
            data = np.array(
                list(
                    map(
                        float,
                        regionfile.readlines()[3].split(" ")[0][7:-1].split(","),
                    )
                )
            )
        x_arr[file] = data[0]
        y_arr[file] = data[1]
        radii[file] = data[2]
    return x_arr, y_arr, np.average(radii)


if __name__ == "__main__":
    print("This file is not supposed to be executed directly")
