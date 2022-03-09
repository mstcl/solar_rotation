"""
Frequently used functions
"""

from os.path import exists as file_exists
from numpy.lib.function_base import average
import numpy as np


def get_value(sequence: str, target: str):
    """
    Return the normal
    """
    if not file_exists(f"./{sequence}/data.txt"):
        raise FileNotFoundError(
            f"./{sequence}/data.txt was not found in this sequence. Run init.sh first."
        )
    with open(f"./{sequence}/data.txt", "r", encoding="utf-8") as file:
        data = {
            line.split(" ")[0]: " ".join(line.split(" ")[1:])
            for line in file.readlines()
        }
    value = data.get(target, None)
    assert (
        value is not None
    ), f"This value {target} was not found. Make sure to run the required functions first."
    return float(value)

def find_std(data: np.ndarray, num: int):
    """
    Find the standard deviation on the mean of a sample
    """
    num = len(data)
    sample_var = 0
    avg = find_average(data)
    for var in data:
        sample_var += (var - avg) ** 2
    sample_var = (sample_var / num) ** (1 / 2)
    return sample_var / (num - 1) ** (1 / 2)


def find_average(data: np.ndarray):
    """
    Return the average of an array
    """
    return average(data)


def write_data(heading: str, values, sequence: str):
    """
    Write to data.txt the radii of the sunspots
    """
    if not file_exists(f"./{sequence}/data.txt"):
        raise FileNotFoundError(
            f"./{sequence}/data.txt was not found in this sequence. Run init.sh first."
        )
    with open(f"./{sequence}/data.txt", "r", encoding="utf-8") as old_file:
        data = {
            line.split(" ")[0]: " ".join(line.split(" ")[1:])
            for line in old_file.readlines()
        }
    if isinstance(values, np.ndarray):
        for j, val in enumerate(values):
            data[f"{heading}{j+1}"] = f"{val}\n"
    else:
        data[f"{heading}"] = f"{values}\n"
    with open(f"./{sequence}/data.txt", "w", encoding="utf-8") as new_file:
        new_file.writelines([" ".join(line) for line in data.items()])
    return True


def warn_module():
    """
    Print a warning for modules that are not supposed to be executed
    """
    print("This file is not supposed to be executed directly")


if __name__ == "__main__":
    warn_module()
