#!/usr/bin/env python
"""
Frequently used functions
"""

from os.path import exists as file_exists
import numpy as np

def write_data(heading:str, values, sequence:str):
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
    if isinstance(values, np.ndarray):
        for j, val in enumerate(values):
            for i, line in enumerate(data):
                if "".join(line[0:2]) == f"{heading}{j+1}":
                    data[i] = f"{heading}{j+1} {val}\n"
                    changed = True
                    break
        if not changed:
            for j, val in enumerate(values):
                data.append(f"R{j+1} {val}\n")
    else:
        for i, line in enumerate(data):
            if line[0] == heading:
                data[i] = f"{heading} {values}\n"
                changed = True
                break
        if not changed:
            data.append(f"{heading} {values}\n")

    with open(f"./{sequence}/data.txt", "w", encoding="utf-8") as new_file:
        new_file.writelines(data)
    return True


def warn_module():
    """
    Print a warning for modules that are not supposed to be executed
    """
    print("This file is not supposed to be executed directly")

if __name__ == "__main__":
    warn_module()
