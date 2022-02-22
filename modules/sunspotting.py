#!/usr/bin/env python
"""
Find the coordinate of sunspots
"""

from os.path import exists as file_exists
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
        if not file_exists(
            f"./{sequence}/regions/{key_coord.get(criteria)}_const_{file}.reg"
        ):
            raise FileNotFoundError(
                f"Can't find ./{sequence}/regions/{key_coord.get(criteria)}_const_{file}.reg\n"
            )
        with open(
            f"./{sequence}/regions/{key_coord.get(criteria)}_const_{file}.reg",
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
                f"./{sequence}/sunspot_data/{key_coord.get(criteria)}_constant_{file}_{spot}.txt"
            ):
                raise FileNotFoundError(
                    f"Can't find ./{sequence}/sunspot_data/{key_coord.get(criteria)}_constant_{file}_{spot}.txt\n"
                )
            with open(
                f"./{sequence}/sunspot_data/{key_coord.get(criteria)}_constant_{file}_{spot}.txt",
                "r",
                encoding="utf-8",
            ) as sunspot_file:
                # TODO: error
                data[file - 1] = (
                    average(
                        [
                            float(line.strip("\n").split(" ")[0])
                            for line in sunspot_file.readlines()
                        ]
                    )
                    + projection_origin
                ) - arr[file - 1]
    return average(data)


def get_radius(r_x: float, r_y: float):
    """
    Return the magnitude of the radius
    """
    return (r_x**2 + r_y**2) ** (1 / 2)


if __name__ == "__main__":
    helper.warn_module()
