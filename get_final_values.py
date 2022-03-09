#!/usr/bin/env python
"""
Determine the average lat and long of sunpsots
I am dying and in pain as I try to rewrite this
from memory I wish I can sudo rm -rf my life rn
"""

import numpy as np
import argparse

from os.path import exists as file_exists
from modules import helper


def parse_data(spot: int):
    """
    Parse spot_n.txt into a dictionary
    which contains the key as the Julian date
    and value as a list of values.

    Each list contains a list of the same variable
    """
    if not file_exists(f"./spot_{spot}.txt"):
        raise FileNotFoundError(
            f"./spot_{spot} was not found. Generate it manually first."
        )
    with open(f"./spot_{spot}.txt", "r", encoding="utf-8") as file:
        data = [
            list(map(float, line.strip("\n").split(" "))) for line in file.readlines()
        ]
    unique_dates = set(line[0] for line in data)
    new_data = {date: [] for date in unique_dates}
    for line in data:
        new_data[line[0]].append(line[1:])
    for key, value in new_data.items():
        new_data[key] = np.array(value).T.tolist()
    return new_data


def compute_values(data: dict):
    """
    Compute the average values
    for all variables and errors
    """
    avg_data = {key: np.zeros(4, dtype="float64") for key in data.keys()}
    for key, value in data.items():
        avg_data[key][0] = helper.find_average(value[0])
        avg_data[key][1] = max(
            helper.find_std(value[0], len(value[0])), helper.find_average(value[1])
        )
        avg_data[key][2] = helper.find_average(value[2])
        avg_data[key][3] = max(
            helper.find_std(value[2], len(value[3])), helper.find_average(value[1])
        )
    return avg_data


def write_to_file(data: dict, spot: int):
    """
    Write the data to final_n.txt
    """
    if not file_exists(f"./final_{spot}.txt"):
        raise FileNotFoundError(
            f"./final_{spot} was not found. Generate it manually first."
        )
    data_to_write = []
    for key, value in data.items():
        values = " ".join(list(map(str, value)))
        data_to_write.append(f"{str(key)} {values}\n")
    with open(f"./final_{spot}.txt", "w", encoding="utf-8") as new_file:
        new_file.writelines(data_to_write)


def main():
    """
    Driver code I think
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("spot", help="The ID of the spot to be analysed")
    args = parser.parse_args()
    if args.spot:
        data = parse_data(args.spot)
        avg_data = compute_values(data)
        write_to_file(avg_data, args.spot)
    else:
        print("Program needs an argument. Run -h for help.")


if __name__ == "__main__":
    main()
