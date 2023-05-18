#!/usr/bin/env python
"""
Calculations related to the analysis
of sunspots across multiply days
"""

import argparse
import numpy as np

from modules import helper
from modules import rotational_rate


def parse_data(spot: int):
    """
    Parse spot_n.txt into a dictionary
    which contains the key as the Julian date
    and value as a list of values.

    Each list contains a list of the same variable
    """
    helper.check_file(f"./dataset/spot_{spot}.txt")
    with open(f"./dataset/spot_{spot}.txt", "r", encoding="utf-8") as file:
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
    column_key = {"long": 0, "long_err": 1, "lat": 2, "lat_err": 3}
    avg_data = {key: np.zeros(4, dtype="float64") for key in data.keys()}
    for key, value in data.items():
        avg_data[key][column_key["long"]] = helper.find_average(value[0])
        avg_data[key][column_key["long_err"]] = max(
            helper.find_std(value[0]), helper.find_average(value[1])
        )
        avg_data[key][column_key["lat"]] = helper.find_average(value[2])
        avg_data[key][column_key["lat_err"]] = max(
            helper.find_std(value[2]), helper.find_average(value[1])
        )
    return avg_data


def write_to_file(data: dict, spot: int):
    """
    Write the data to final_n.txt
    """
    helper.check_file(f"./dataset/final_{spot}.txt")
    data_to_write = []
    for key, value in data.items():
        values = " ".join(list(map(str, value)))
        data_to_write.append(f"{str(key)} {values}\n")
    with open(f"./dataset/final_{spot}.txt", "w", encoding="utf-8") as new_file:
        new_file.writelines(data_to_write)


def main():
    """
    Driver code
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("spot", help="The ID of the spot to be analysed")
    parser.add_argument("-a", "--nasa", help="Using SDO trend", action="store_true")
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-s", "--stats", help="Find average and std", action="store_true"
    )
    group.add_argument(
        "-e", "--expect", help="Calculate expected rate and save plots", action="store_true"
    )
    args = parser.parse_args()
    if args.spot:
        if args.stats:
            data = parse_data(args.spot)
            avg_data = compute_values(data)
            write_to_file(avg_data, args.spot)
        if args.expect:
            rotational_rate.driver(args.spot, args.nasa)
    else:
        print("Program needs an argument. Run -h for help.")


if __name__ == "__main__":
    main()
