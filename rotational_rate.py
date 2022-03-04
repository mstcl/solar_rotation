#!/usr/bin/env python3

import numpy as np

def get_rotational_frequency(latitude: float, constants: dict):
    """
    Return the rotational frequency
    """
    latitude = latitude * np.pi / 180
    return (
            constants["A"][0] +
            constants["B"][0]*(np.sin(latitude))**2 +
            constants["C"][0]*(np.sin(latitude))**4
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
    return (
            constants["A"][1]**2 +
            (np.sin(latitude)**2) * constants["B"][1]**2 +
            (np.sin(latitude)**4) * constants["C"][1]**2 +
            (constants["B"][0] + 2*constants["C"]*(np.sin(latitude)**2)) * (np.sin(2*latitude))**2 * latitude_error
    ) ** (1/2)

def get_period_error(frequency: float, frequency_error: float):
    """
    Return the error of period
    """
    return frequency_error / frequency**2

def driver():
    latitude = 0
    latitude = 1
    constants = {
            "A": (14.713, 0.0491),
            "B": (-2.396, 0.188),
            "C": (-1.787, 0.253),
    }
    sidereal_correction = 360 / 365.25
    frequency = get_rotational_frequency(latitude, constants)
    frequency_error = get_frequency_error(latitude, latitude_error, constants)
    period = get_period(frequency) * sidereal_correction
    get_period_error = get_period_error(frequency, frequency_error)

if __name__ == "__main__":
    driver()
