#!/usr/bin/env python
"""Get the equation of equatorial plane, plot it, and find the normal vector"""

import argparse
import matplotlib.pyplot as plt
import numpy as np


def main():
    """Driver"""
    parser = argparse.ArgumentParser()
    parser.add_argument("number", help="Number of files")
    parser.add_argument("-p", "--Plot", help="Plot a graph", action="store_true")
    args = parser.parse_args()
    if args.number:
        files_num = int(args.number)
        x_arr, y_arr, radii = parse_data(files_num)
        print_output(x_arr, y_arr)
        if args.Plot:
            plot_equator(x_arr, y_arr)
    else:
        print("Program needs the number of files to parse! -h for help")


def print_output(x_arr, y_arr):
    """CLI output"""
    # print(f"X values: {x_arr}\nY values: {y_arr}")
    print(f"Gradient: {get_gradient(x_arr, y_arr)}")
    print(f"Normal: {-1/get_gradient(x_arr, y_arr)}")


def get_gradient(x_arr, y_arr):
    """Interpolate to first degree and return gradient"""
    return np.polyfit(x_arr, y_arr, 1)[0]


def parse_data(files_num):
    """Go through each file and appends centre coordinate"""
    x_arr, y_arr = np.zeros(files_num, dtype="float64"), np.zeros(
        files_num, dtype="float64"
    )
    radii = np.array(x_arr)
    for file in range(files_num):
        with open(f"./sun_disc_{file+1}.reg", "r") as regionfile:
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
    return x_arr, y_arr, radii


def plot_equator(x_arr, y_arr):
    """
    Plot using matplotlib
    """
    plt.plot(x_arr, y_arr, "-ob")
    plt.show()


if __name__ == "__main__":
    main()
