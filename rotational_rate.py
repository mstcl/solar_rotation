#!/usr/bin/env python
"""
Calculate the rotational rate and period from data
"""
import numpy as np
from modules import helper


def get_rotational_frequency(latitude: float, constants: dict):
    """
    Return the rotational frequency
    """
    latitude = latitude * np.pi / 180
    return (
        constants["A"][0]
        + constants["B"][0] * (np.sin(latitude)) ** 2
        + constants["C"][0] * (np.sin(latitude)) ** 4
    )


def get_period(frequency: float):
    """
    Return the rotational period expected
    """
    return 360 / frequency


def get_frequency_error(latitude: float, latitude_error: float, constants: dict):
    """
    Return the error of rotational frequency
    """
    latitude = latitude * np.pi / 180
    in_a = float(constants["A"][1]) ** 2
    in_b = (np.sin(latitude) ** 2) * float(constants["B"][1]) ** 2
    in_c = (np.sin(latitude) ** 4) * float(constants["C"][1]) ** 2
    in_l = (
        (
            float(constants["B"][0])
            + 2 * float(constants["C"][0]) * (np.sin(latitude) ** 2)
        )
        * latitude_error
        * (np.sin(2 * latitude)) ** 2
    )
    return (in_a**2 + in_b**2 + in_c**2 + in_l**2) ** (1 / 2)


def get_period_error(frequency: float, frequency_error: float):
    """
    Return the error of period
    """
    return frequency_error / frequency**2


def driver():
    """
    Fetch all quantities
    """
    latitudes = np.array([22, 23, 26, 27])
    latitude = float(helper.find_average(latitudes))
    latitude_error = helper.find_std(latitudes, len(latitudes))
    constants = {
        "A": (14.713, 0.0491),
        "B": (-2.396, 0.188),
        "C": (-1.787, 0.253),
    }
    sidereal_correction = 360 / 365.25
    frequency = get_rotational_frequency(latitude, constants)
    frequency_error = get_frequency_error(latitude, latitude_error, constants)
    period = get_period(frequency) - sidereal_correction
    period_error = get_period_error(frequency, frequency_error)
    print(f"freq:{frequency} +/- {frequency_error*frequency}")
    print(f"period:{period} +/- {period_error*period}")


if __name__ == "__main__":
    driver()
