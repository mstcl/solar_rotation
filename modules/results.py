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
        data = [
            [line.strip("\n").split(" ")[0], " ".join(line.split(" ")[1:])]
            for line in file.readlines()
        ]
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


def get_long(lat: float, rho: float, chi: float):
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
        if entry[0][0] not in {"d", "T", "E", "M"}:
            values[entry[0]] = float(entry[1])
    return values


def get_results(values: dict, spot):
    """
    Calculate the values and return final results
    Also converts all angles into radians
    Output in radians
    """
    radius_ratio = get_radius_ratio(values["r"], values[f"R{spot+1}"])
    rho = get_rho(radius_ratio, (values["S"] * np.pi / 180) / 7200)
    chi = get_chi(values["P"] * np.pi / 180, values[f"A{spot+1}"] * np.pi / 180)
    lat = get_lat(chi, values["B"] * np.pi / 180, rho)
    long = get_long(lat, rho, chi)
    return (
        long,
        lat,
        chi,
        rho,
        radius_ratio,
    )


def driver(sequence: str, spots: int):
    """
    Putting everything together
    Return results and errors in degrees
    """
    values = sort_data(parse_data(sequence, spots))
    results = {
        variable: np.zeros(spots, dtype="float64")
        for variable in ["long", "lat", "chi", "rho", "ratio"]
    }
    errors = {
        variable: np.zeros(spots, dtype=object)
        for variable in ["long", "lat", "errors"]
    }
    other_data = np.zeros(spots, dtype=object)
    rad_to_deg = 180 / np.pi
    for spot in range(spots):
        (
            results["long"][spot],
            results["lat"][spot],
            results["chi"][spot],
            results["rho"][spot],
            results["ratio"][spot],
        ) = get_results(values, spot)
        other_data[
            spot
        ] = f"RATIO {results['ratio'][spot]} RHO {results['rho'][spot]*rad_to_deg} CHI {results['chi'][spot]*rad_to_deg}"
    for spot in range(spots):
        errors["long"][spot], errors["lat"][spot], errors["errors"][spot] = get_errors(
            values, spot, results
        )
    return (
        (results["long"] * rad_to_deg, errors["long"]),
        (
            results["lat"] * rad_to_deg,
            errors["lat"],
        ),
        errors["errors"],
        other_data,
    )


def get_errors(values: dict, spot: int, results: dict):
    """
    Calculate the errors for all variables
    Output in degrees
    """
    radius_ratio_error = get_radius_ratio_error(values, spot)
    rho_error = get_rho_error(radius_ratio_error, values, results["ratio"][spot])
    chi_error = get_chi_error(values[f"DA{spot+1}"])
    lat_error = get_lat_error(values, rho_error, chi_error, results, spot)
    long_error = get_long_error(results, lat_error, chi_error, rho_error, spot)
    rad_to_deg = 180 / np.pi
    other_errors = (
        f"DRAT {radius_ratio_error*rad_to_deg} DRHO {rho_error*rad_to_deg} DCHI {chi_error*rad_to_deg}"
    )
    return str(long_error * rad_to_deg), str(lat_error * rad_to_deg), other_errors


def get_radius_ratio_error(values: dict, spot: int):
    """
    Return the error for r/r_0
    """
    return (
        (values[f"DR{spot+1}"] ** 2 / values["r"] ** 2)
        + (values[f"R{spot+1}"] ** 2 * values["Dr"] ** 2 / values["r"] ** 4)
    ) ** (1 / 2)


def get_rho_error(radius_ratio_error: float, values: dict, radius_ratio: float):
    """
    Return the error for rho
    """
    return radius_ratio_error * (
        (1 - radius_ratio**2) ** (-1 / 2) - ((values["S"] * np.pi / 180) / 7200)
    )


def get_chi_error(angle_error: float):
    """
    Return the error for chi
    """
    return angle_error


def get_lat_error(
    values: dict, rho_error: float, chi_error: float, results: dict, spot: int
):
    """
    Return the error for lat
    """
    B = values["B"] * np.pi / 180
    rho = results["rho"][spot]
    chi = results["chi"][spot]
    lat = results["lat"][spot]
    return (
        (
            (np.cos(B) * np.cos(rho) * np.cos(chi) - np.sin(B) * np.sin(rho)) ** 2
            * rho_error**2
            + (np.cos(B) * np.sin(rho) * np.sin(chi)) ** 2 * chi_error**2
        )
        / np.cos(lat)**2
    ) ** (1 / 2)


def get_long_error(
    results: dict,
    lat_error: float,
    chi_error: float,
    rho_error: float,
    spot: int,
):
    """
    Return the error for I
    """
    rho = results["rho"][spot]
    chi = results["chi"][spot]
    lat = results["lat"][spot]
    long_i = results["long"][spot]
    return (
        (
            (np.cos(rho) * np.sin(chi) / np.cos(lat)) ** 2 * rho_error**2
            + (np.sin(rho) * np.cos(chi) / np.cos(lat)) ** 2 * chi_error**2
            + (np.sin(rho) * np.sin(chi) * np.tan(lat) / np.cos(lat)) ** 2
            * lat_error**2
        )
        / np.cos(long_i)**2
    ) ** (1 / 2)


if __name__ == "__main__":
    helper.warn_module()
