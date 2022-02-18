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


def write_data(radius_disc: float, sequence: str):
    """
    Write to data.txt the radii of the sunspots
    """
    if not file_exists(f"./{sequence}/data.txt"):
        raise FileNotFoundError(
            f"./{sequence}/data.txt was not found in this sequence. Run init.sh first."
        )
    with open(f"./{sequence}/data.txt", "r", encoding="utf-8") as old_file:
        data = old_file.readlines()

    changed = False
    for i, line in enumerate(data):
        if line[0] == "r":
            data[i] = f"r {radius_disc}\n"
            changed = True
            break
    if not changed:
        data.append(f"r {radius_disc}\n")
    with open(f"./{sequence}/data.txt", "w", encoding="utf-8") as new_file:
        new_file.writelines(data)
    return True


if __name__ == "__main__":
    print("This file is not supposed to be executed directly")
