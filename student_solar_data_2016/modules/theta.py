#!/usr/bin/env python
"""
Find the angle between celestial north and sunspot
"""

from os.path import exists as file_exists
import numpy as np


def get_angle(r_x:float, r_y:float, normal:float):
    """
    Determine theta from the sign of r_y and normal
    """
    angle = (
        np.arccos(
            (((r_x**2 + r_y**2) * (normal**2 + 1)) ** (-0.5))
            * (r_x + (r_y * normal))
        )
        * 180
        / np.pi
    )
    if angle > 180:
        angle = angle - 180

    if r_y > 0:
        return angle if normal > 0 else (360 - angle)
    return (360 - angle) if normal > 0 else angle


def write_data(angles:np.ndarray, sequence: str):
    """
    Write to data.txt the angle theta
    """
    if not file_exists(f"./{sequence}/data.txt"):
        raise FileNotFoundError(
            f"./{sequence}/data.txt was not found in this sequence. Run init.sh first."
        )
    with open(f"./{sequence}/data.txt", "r", encoding="utf-8") as old_file:
        data = old_file.readlines()
    changed = False
    for j, val in enumerate(angles):
        for i, line in enumerate(data):
            if "".join(line[0:2]) == f"A{j+1}":
                data[i] = f"A{j+1} {val}\n"
                changed = True
                break
    if not changed:
        for j, val in enumerate(angles):
            data.append(f"A{j+1} {val}\n")
    with open(f"./{sequence}/data.txt", "w", encoding="utf-8") as new_file:
        new_file.writelines(data)
    return True


if __name__ == "__main__":
    print("This file is not supposed to be executed directly")
