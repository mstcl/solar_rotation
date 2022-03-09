"""
Fetch the centres of the sun discs
"""

import numpy as np
from . import helper


def parse_data(files_num: list, sequence: str, full: bool):
    """
    Go through each file and appends centre coordinate
    """
    x_arr, y_arr = np.zeros(max(files_num), dtype="float64"), np.zeros(
        max(files_num), dtype="float64"
    )
    radii = np.array(x_arr)
    for file in files_num:
        helper.check_file(f"./{sequence}/regions/sun_disc_{file}.reg")
        with open(
            f"./{sequence}/regions/sun_disc_{file}.reg", "r", encoding="utf-8"
        ) as regionfile:
            data = np.array(
                list(
                    map(
                        float,
                        regionfile.readlines()[3].split(" ")[0][7:-1].split(","),
                    )
                )
            )
        x_arr[file - 1] = data[0]
        y_arr[file - 1] = data[1]
        radii[file - 1] = data[2]
    missing_indices = [
        n - 1 for n in range(max(files_num)) if n not in files_num and n != 0
    ]
    if full:
        return (
            x_arr,
            y_arr,
            np.array(0),
        )
    return (
        np.delete(x_arr, missing_indices),
        np.delete(y_arr, missing_indices),
        np.delete(radii, missing_indices),
    )


if __name__ == "__main__":
    helper.warn_module()
