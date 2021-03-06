"""
Find the coordinate of sunspots
"""

import numpy as np
from numpy.lib.function_base import average
from . import helper


def parse_data(
    criteria: int, arr: np.ndarray, files_num: list, spot: int, sequence: str
):
    """
    Parse coordinates for all images
    """
    key_coord = {0: "y", 1: "x"}
    data = np.zeros(max(files_num))
    for file in files_num:
        helper.check_file(
            f"./{sequence}/regions/{key_coord.get(criteria)}_const_{file}.reg"
        )
        with open(
            f"./{sequence}/regions/{key_coord.get(criteria)}_const_{file}.reg",
            "r",
            encoding="utf-8",
        ) as projection_file:
            projection_origin = list(
                map(
                    float,
                    projection_file.readlines()[3].split(" ")[0][11:-2].split(","),
                )
            )[criteria]
            helper.check_file(
                f"./{sequence}/sunspot_data/{key_coord.get(criteria)}_constant_{file}_{spot}.txt"
            )
            with open(
                f"./{sequence}/sunspot_data/{key_coord.get(criteria)}_constant_{file}_{spot}.txt",
                "r",
                encoding="utf-8",
            ) as sunspot_file:
                data[file - 1] = (
                    average(
                        [
                            float(line.strip("\n").split(" ")[0])
                            for line in sunspot_file.readlines()
                        ]
                    )
                    + projection_origin
                ) - arr[file - 1]
    missing_indices = [
        n - 1 for n in range(max(files_num)) if n not in files_num and n != 0
    ]
    return np.delete(data, missing_indices)


def get_radius(r_x: np.ndarray, r_y: np.ndarray):
    """
    Return the magnitude of the radius for all images
    """
    radii = []
    for component in zip(r_x, r_y):
        radii.append((component[0] ** 2 + component[1] ** 2) ** (1 / 2))
    return np.array(radii)


if __name__ == "__main__":
    helper.warn_module()
