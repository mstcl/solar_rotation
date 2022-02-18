#!/usr/bin/env python
"""Find the equation of the line given a set of x,y values"""

from os.path import exists as file_exists
import numpy as np


def get_line(x_arr: np.ndarray, y_arr: np.ndarray):
    """Interpolate to first degree and return gradient"""
    return tuple(np.polyfit(x_arr, y_arr, 1))


def write_data(x_arr: np.ndarray, y_arr: np.ndarray, sequence: str):
    """
    Write to data.txt the normal
    """
    if not file_exists(f"./{sequence}/data.txt"):
        raise FileNotFoundError(
            f"./{sequence}/data.txt was not found in this sequence. Run init.sh first."
        )
    with open(f"./{sequence}/data.txt", "r", encoding="utf-8") as old_file:
        data = old_file.readlines()
    normal = f"N {-1 / get_line(x_arr, y_arr)[0]}\n"
    changed = False
    for i,line in enumerate(data):
        if line[0] == "N":
            data[i] = normal
            changed = True
            break
    if not changed:
        data.append(normal)
    with open(f"./{sequence}/data.txt", "w", encoding="utf-8") as new_file:
        new_file.writelines(data)
    return True


if __name__ == "__main__":
    print("This file is not supposed to be executed directly")
