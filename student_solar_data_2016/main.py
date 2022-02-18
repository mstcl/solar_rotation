#!/usr/bin/env python
"""Main driver code for all operations"""

import argparse

import numpy as np
from modules import equator
from modules import centre
from modules import plot
from modules import sunspotting
from modules import theta
from modules import results


def resolve_args(args):
    """
    Execute child functions called by args
    """
    if args.number and args.sequence:
        is_plot_saved = is_normal_saved = is_sunspots_saved = is_result_saved = False
        files_num = int(args.number)
        sequence = args.sequence
        x_arr, y_arr, radius_disc = centre.parse_data(files_num, sequence)
        is_radius_saved = centre.write_data(float(radius_disc), sequence)
        if args.normal:
            is_normal_saved = equator.write_data(x_arr, y_arr, sequence)
        if args.plot:
            is_plot_saved = plot.plot_equator(
                x_arr, y_arr, sequence, equator.get_line(x_arr, y_arr)
            )
        if args.sunspot:
            is_sunspots_saved = resolve_sunspots(
                args, sequence, files_num, x_arr, y_arr
            )
        if args.result:
            resolve_results(args, sequence)
        if args.verbose:
            print_output(
                is_plot_saved,
                is_normal_saved,
                is_sunspots_saved,
                is_result_saved,
                is_radius_saved,
            )
    else:
        print("Program needs some data to parse! Run with -h for help")


def resolve_sunspots(
    args, sequence: str, files_num: int, x_arr: np.ndarray, y_arr: np.ndarray
):
    """
    Separate function to find and write sunspots information
    """
    spots = int(args.sunspot)
    radii_spots = np.zeros(spots, dtype="float64")
    angle_spots = np.zeros(spots, dtype="float64")
    for spot in range(spots):
        r_x = sunspotting.parse_data(0, x_arr, files_num, spot + 1, sequence)
        r_y = sunspotting.parse_data(1, y_arr, files_num, spot + 1, sequence)
        radii_spots[spot] = sunspotting.get_radius(float(r_x), float(r_y))
        angle_spots[spot] = theta.get_angle(
            float(r_x), float(r_y), -1 / equator.get_line(x_arr, y_arr)[0]
        )
    is_sunspots_saved = theta.write_data(angle_spots, sequence)
    is_sunspots_saved = sunspotting.write_data(radii_spots, sequence)
    return is_sunspots_saved


def resolve_results(args, sequence: str):
    """
    Separate function to fetch and write the final results
    """
    all_i = results.driver(sequence, int(args.result))
    is_result_saved = results.write_data(all_i, sequence)
    return is_result_saved


def main():
    """
    Driver code to parse arguments and options
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("number", help="Number of files")
    parser.add_argument("sequence", help="Date and sequence")
    parser.add_argument(
        "-v", "--verbose", help="Show more information", action="store_true"
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-p", "--plot", help="Plot and save a graph", action="store_true"
    )
    group.add_argument(
        "-n", "--normal", help="Calculate normal and write to data", action="store_true"
    )
    group.add_argument(
        "-s",
        "--sunspot",
        help="Find r_0 of {arg} number of sunspots and its angle and write to data",
    )
    group.add_argument(
        "-r",
        "--result",
        help="Get I of {arg} number of sunspot(s). Requires a populated data.txt.",
    )
    args = parser.parse_args()
    resolve_args(args)


def print_output(
    is_plot_saved: bool,
    is_normal_saved: bool,
    is_sunspots_saved: bool,
    is_result_saved: bool,
    is_radius_saved: bool,
):
    """
    CLI output
    """
    if is_plot_saved:
        print("Plot saved as equatorial_plane.png")
    if is_sunspots_saved:
        print("Update data.txt with sunspot(s) radius and theta")
    if is_normal_saved:
        print("Update data.txt with value of the normal")
    if is_result_saved:
        print("Update data.txt with values of I")
    if is_radius_saved:
        print("Update data.txt with the average disc radius")


if __name__ == "__main__":
    main()
