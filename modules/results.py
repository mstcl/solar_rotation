#!/usr/bin/env python
"""
Find and return the final results, B and I of all the
sunspots in the sequence
"""

from os.path import exists as file_exists
import numpy as np
from . import helper


def parse_data(sequence: str, spots: int):
    """
    Parse all the variables into a table
    """
    if not file_exists(f"./{sequence}/data.txt"):
        raise FileNotFoundError(
            f"./{sequence}/data.txt was not found in this sequence. Run init.sh first."
        )
    with open(f"./{sequence}/data.txt", "r", encoding="utf-8") as file:
        data = [line.strip("\n").split(" ") for line in file.readlines()]
    assert (
        len(data) >= 8 + 2 * spots
    ), "The database is not populated correctly, please run all the other commands first"
    return data


def get_radius_ratio(radius_disc: float, radius_sunspot: float):
    """
    Returns the angle alpha/S
    alpha is rho_1, renamed for easier distinction
    """
    return radius_sunspot / radius_disc


def get_rho(radius_ratio: float, S: float):
    """
    Returns the angle rho
    """
    return np.arcsin(radius_ratio) - ((radius_ratio) * S)


def get_chi(P: float, angle: float):
    """
    Returns the angle chi
    """
    return P - angle


def get_lat(chi: float, B: float, rho: float):
    """
    Returns the latitude of the sunspot
    """
    return np.arcsin(np.sin(B) * np.cos(rho) + np.cos(B) * np.sin(rho) * np.cos(chi))


def get_long_i(lat: float, rho: float, chi: float):
    """
    Returns the difference between longitude of the sunspot and centre of disc
    """
    return np.arcsin(np.sin(rho) * np.sin(chi) / np.cos(lat))


def sort_data(data: list):
    """
    Sort data into dictionary and get results
    """
    values = {}
    for entry in data:
        if entry[0] not in {"D", "T"}:
            values[entry[0]] = float(entry[1])
    return values


def get_results(values: dict, spot):
    """
    Calculate the values and return final results
    Also converts all angles into radians
    Output in degrees
    """
    radius_ratio = get_radius_ratio(values["r"], values[f"R{spot+1}"])
    rho = get_rho(radius_ratio, (values["S"] * np.pi / 180) / 7200)
    chi = get_chi(values["P"] * np.pi / 180, values[f"A{spot+1}"] * np.pi / 180)
    lat = get_lat(chi, values["B"] * np.pi / 180, rho)
    I = get_long_i(lat, rho, chi)
    return I * 180 / np.pi


def driver(sequence: str, spots: int):
    """
    Putting everything together
    """
    values = sort_data(parse_data(sequence, spots))
    all_i = np.zeros(spots, dtype="float64")
    for spot in range(spots):
        all_i[spot] = get_results(values, spot)
    return all_i


if __name__ == "__main__":
    helper.warn_module()
