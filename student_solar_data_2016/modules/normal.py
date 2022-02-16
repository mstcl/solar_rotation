#!/usr/bin/env python
"""Find the normal given a set of x,y values"""

from os.path import exists as file_exists
import numpy as np


def get_gradient(x_arr: np.ndarray, y_arr: np.ndarray):
    """Interpolate to first degree and return gradient"""
    return np.polyfit(x_arr, y_arr, 1)[0]


def write_data(x_arr: np.ndarray, y_arr: np.ndarray, sequence: str):
    """
    Write to data.txt the normal
    """
    if not file_exists(f"./{sequence}/data.txt"):
        raise FileNotFoundError(
            "The file data.txt was not found in this sequence. Run init.sh first."
        )
    with open(f"./{sequence}/data.txt", "r", encoding="utf-8") as old_file:
        data = old_file.readlines()
    normal = f"N {-1 / get_gradient(x_arr, y_arr)}"
    if len(data) > 6:
        data[6] = normal
    else:
        data.append(normal)
    with open(f"./{sequence}/data.txt", "w", encoding="utf-8") as new_file:
        new_file.writelines(data)
    return True


def parse_data(files_num: int, sequence: str):
    """
    Go through each file and appends centre coordinate
    """
    x_arr, y_arr = np.zeros(files_num, dtype="float64"), np.zeros(
        files_num, dtype="float64"
    )
    radii = np.array(x_arr)
    for file in range(files_num):
        if not file_exists(f"./{sequence}/sun_disc_{file+1}.reg"):
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
    return x_arr, y_arr, radii


if __name__ == "__main__":
    print("This file is not supposed to be executed directly")
