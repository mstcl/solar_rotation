#!/usr/bin/env python
"""Main driver code for all operations"""

import argparse

import numpy as np
from modules import normal
from modules import plot


def main():
    """
    Driver code to parse arguments and options
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("number", help="Number of files")
    parser.add_argument("sequence", help="Date and sequence")
    parser.add_argument(
        "-p", "--plot", help="Plot and save a graph", action="store_true"
    )
    parser.add_argument(
        "-v", "--verbose", help="Show more information", action="store_true"
    )
    args = parser.parse_args()
    if args.number and args.sequence:
        is_plot_saved, is_normal_saved = False, False
        files_num = int(args.number)
        sequence = args.sequence
        x_arr, y_arr, radii = normal.parse_data(files_num, sequence)
        is_normal_saved = normal.write_data(x_arr, y_arr, sequence)
        if args.plot:
            is_plot_saved = plot.plot_equator(x_arr, y_arr, sequence)
        if args.verbose:
            print_output(x_arr, y_arr, is_plot_saved, is_normal_saved, sequence)
    else:
        print("Program needs some data to parse! Run with -h for help")


def print_output(
    x_arr: np.ndarray,
    y_arr: np.ndarray,
    is_plot_saved: bool,
    is_normal_saved: bool,
    sequence: str,
):
    """
    CLI output
    """
    print(f"X values: {x_arr}\nY values: {y_arr}")
    print(f"Gradient: {normal.get_gradient(x_arr, y_arr)}")
    print(f"Normal: {-1/normal.get_gradient(x_arr, y_arr)}")
    if is_plot_saved:
        print(f"Plot saved as ./{sequence}/equatorial_plane.png")
    if is_normal_saved:
        print(f"Update ./{sequence}/data.txt with value of the normal")


if __name__ == "__main__":
    main()
