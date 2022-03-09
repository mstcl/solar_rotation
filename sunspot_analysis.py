#!/usr/bin/env python
"""Main driver code for all operations"""

import argparse

import numpy as np
from modules import helper
from modules import centre
from modules import plot
from modules import sunspotting
from modules import theta
from modules import results


def get_files_num(files_arg):
    """
    Return the files number that are to be
    processed as a list
    """
    files_num = []
    for val in "".join(files_arg.split()).split(","):
        if "-" in val:
            for j in range(int(val.split("-")[0]), int(val.split("-")[1]) + 1):
                files_num.append(j)
        else:
            files_num.append(int(val))
    return list(set(files_num))


def resolve_args(args):
    """
    Execute child functions called by args
    """
    if args.number and args.sequence:
        is_plot_saved = (
            is_radius_saved
        ) = is_normal_saved = is_sunspots_saved = is_result_saved = False
        files_num = get_files_num(args.number)
        sequence = args.sequence
        x_arr, y_arr, radii_disc = centre.parse_data(files_num, sequence, False)
        if args.radius:
            is_radius_saved = helper.write_data(
                "r", helper.find_average(radii_disc), sequence
            )
            resolve_radius_errors(radii_disc, sequence, len(files_num))
        if args.normal:
            normal = -1 / helper.get_line(x_arr, y_arr)[0][0]
            is_normal_saved = helper.write_data("N", normal, sequence)
        if args.plot:
            is_plot_saved = plot.plot_equator(
                x_arr, y_arr, sequence, tuple(helper.get_line(x_arr, y_arr)[0])
            )
        if args.sunspot:
            is_sunspots_saved = resolve_sunspots(args, sequence, files_num)
        if args.result:
            is_result_saved = resolve_results(args, sequence)
        if args.verbose:
            print_output(
                is_plot_saved,
                is_normal_saved,
                is_sunspots_saved,
                is_result_saved,
                is_radius_saved,
            )
    else:
        print("Program needs some data to parse! Run with -h for help.")


def resolve_radius_errors(radii_pop: np.ndarray, sequence: str, size: int):
    """
    Separate function to find and write sun disc radii
    """
    radii_std = helper.find_std(radii_pop, size)
    _ = helper.write_data("Dr", radii_std, sequence)


def resolve_sunspots(args, sequence: str, files_num: list):
    """
    Separate function to find and write sunspots information
    """
    spots = int(args.sunspot)
    radii_spots = np.zeros(spots, dtype="float64")
    angle_spots = np.zeros(spots, dtype="float64")
    radii_pop = np.zeros(spots, dtype="float64")
    angle_pop = np.zeros(spots, dtype="float64")
    x_arr, y_arr, _ = centre.parse_data(files_num, sequence, True)
    for spot in range(spots):
        r_x = sunspotting.parse_data(0, x_arr, files_num, spot + 1, sequence)
        r_y = sunspotting.parse_data(1, y_arr, files_num, spot + 1, sequence)
        radii_pop = sunspotting.get_radius(r_x, r_y)
        radii_spots[spot] = helper.find_average(radii_pop)
        angle_pop = theta.get_angle(r_x, r_y, helper.get_value(sequence, "N"))
        angle_spots[spot] = helper.find_average(angle_pop)
        resolve_sunspots_errors(
            radii_pop,
            angle_pop,
            len(files_num),
            sequence,
            spot
        )
    _ = helper.write_data("A", angle_spots, sequence)
    is_sunspots_saved = helper.write_data("R", radii_spots, sequence)
    return is_sunspots_saved


def resolve_sunspots_errors(
    radii_pop: np.ndarray,
    angle_pop: np.ndarray,
    size: int,
    sequence: str,
    spot: int
):
    """
    Separate function for sunspot errors
    """
    radii_std = helper.find_std(radii_pop, size)
    angle_std = helper.find_std(angle_pop, size)
    _ = helper.write_data(f"DR{spot+1}", radii_std, sequence)
    _ = helper.write_data(f"DA{spot+1}", angle_std, sequence)


def resolve_results(args, sequence: str):
    """
    Separate function to fetch and write the final results
    """
    long_data, lat_data, other_errors, other_data = results.driver(sequence, int(args.result))
    _ = helper.write_data("I", long_data[0], sequence)
    _ = helper.write_data("DI", long_data[1], sequence)
    _ = helper.write_data("K", lat_data[0], sequence)
    _ = helper.write_data("DK", lat_data[1], sequence)
    _ = helper.write_data("E", other_errors, sequence)
    is_result_saved = helper.write_data("M", other_data, sequence)
    return is_result_saved


def main():
    """
    Driver code to parse arguments and options
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("number", help="Files to parse, e.g. 1-2,5-12")
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
        "-r",
        "--radius",
        help="Find the average radius of the sun disc and write to data",
        action="store_true",
    )
    group.add_argument(
        "-s",
        "--sunspot",
        help="Find r_0 of {arg} number of sunspots and its angle and write to data",
    )
    group.add_argument(
        "-l",
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
        print("Update data.txt with sunspot(s) radius and theta.")
    if is_normal_saved:
        print("Update data.txt with value of the normal.")
    if is_result_saved:
        print("Update data.txt with values of I and B.")
    if is_radius_saved:
        print("Update data.txt with the average disc radius.")


if __name__ == "__main__":
    main()
