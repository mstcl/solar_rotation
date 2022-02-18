#!/usr/bin/env python
"""
Find the coordinate of sunspots
"""

from os.path import exists as file_exists
import numpy as np
from numpy.lib.function_base import average


def parse_data(
    criteria: int, arr: np.ndarray, files_num: int, spot: int, sequence: str
):
    """
    Parse coordinates for all images
    """
    key_coord = {0: "y", 1: "x"}
    data = np.zeros(files_num)
    for file in range(files_num):
        if not file_exists(
            f"./{sequence}/regions/{key_coord.get(criteria)}_const_{file+1}.reg"
        ):
            raise FileNotFoundError(
                f"Can't find ./{sequence}/regions/{key_coord.get(criteria)}_const_{file+1}.reg\n"
            )
        with open(
            f"./{sequence}/regions/{key_coord.get(criteria)}_const_{file+1}.reg",
            "r",
            encoding="utf-8",
        ) as projection_file:
            projection_origin = list(
                map(
                    float,
                    projection_file.readlines()[3].split(" ")[0][11:-1].split(","),
                )
            )[criteria]
            if not file_exists(
                f"./{sequence}/sunspot_data/{key_coord.get(criteria)}_constant_{file+1}_{spot}.txt"
            ):
                raise FileNotFoundError(
                    f"Can't find ./{sequence}/sunspot_data/{key_coord.get(criteria)}_constant_{file+1}_{spot}.txt\n"
                )
            with open(
                f"./{sequence}/sunspot_data/{key_coord.get(criteria)}_constant_{file+1}_{spot}.txt",
                "r",
                encoding="utf-8",
            ) as sunspot_file:
                # TODO: error
                data[file] = (
                    average(
                        [
                            float(line.strip("\n").split(" ")[0])
                            for line in sunspot_file.readlines()
                        ]
                    )
                    + projection_origin
                ) - arr[file]
    return average(data)


def get_radius(r_x: float, r_y: float):
    """
    Return the magnitude of the radius
    """
    return (r_x**2 + r_y**2) ** (1 / 2)


def write_data(radii: np.ndarray, sequence: str):
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
    for j, radius in enumerate(radii):
        for i, line in enumerate(data):
            if "".join(line[0:2]) == f"R{j+1}":
                data[i] = f"R{j+1} {radius}\n"
                changed = True
                break
    if not changed:
        for j, radius in enumerate(radii):
            data.append(f"R{j+1} {radius}\n")

    with open(f"./{sequence}/data.txt", "w", encoding="utf-8") as new_file:
        new_file.writelines(data)
    return True


if __name__ == "__main__":
    print("This file is not supposed to be executed directly")
