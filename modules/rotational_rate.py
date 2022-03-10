"""
Calculate the rotational period from latitude
This is a 'projection' or expected value
"""
import numpy as np
from numpy.ma.core import exp
from . import helper
from . import plot


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


def fetch_data(spot: int):
    """
    Fetch the data in final_n.txt to pass
    it onto a plotter
    """
    helper.check_file(f"./dataset/final_{spot}.txt")
    with open(f"./dataset/final_{spot}.txt", "r", encoding="utf-8") as file:
        data = [
            list(map(float, line.strip("\n").split(" "))) for line in file.readlines()
        ]
    return data


def driver(spot: int, is_nasa: bool):
    """
    Fetch all quantities
    Send to plot.py
    """
    column_key = {"date": 0, "long": 1, "long_err": 2, "lat": 3, "lat_err": 4}
    lats = [val[column_key["lat"]] for val in fetch_data(spot)]
    lats_err = [val[column_key["lat_err"]] for val in fetch_data(spot)]
    longs = [val[column_key["long"]] for val in fetch_data(spot)]
    longs_err = [val[column_key["long_err"]] for val in fetch_data(spot)]
    dates = [val[column_key["date"]] for val in fetch_data(spot)]
    constants = {
        "A": (14.713, 0.0491),
        "B": (-2.396, 0.188),
        "C": (-1.787, 0.253),
    }
    sidereal_correction = 360 / 365.25
    freqs, freqs_err = [], []
    periods, periods_err = [], []
    for i, latitude in enumerate(lats):
        freqs.append(get_rotational_frequency(latitude, constants))
        freqs_err.append(get_frequency_error(latitude, lats_err[i], constants))
        periods.append(get_period(freqs[i]) * sidereal_correction)
        periods_err.append(get_period_error(freqs[i], freqs_err[i]))
    plot.plot_long_against_jd(
        np.array(longs), np.array(dates), np.array(freqs), np.array(longs_err), spot, is_nasa
    )
    plot.plot_lat_against_jd(np.array(lats), np.array(dates), np.array(longs_err), spot)
    write_final_results(longs, dates, periods, periods_err, spot)


def write_final_results(longs, dates, periods, periods_err, spot: int):
    """
    Write to file
    """
    interpolated = helper.get_line(dates, longs)
    interp_period = 360 / abs(interpolated[0][0])
    if interpolated[1]:
        interp_period_err = abs(interpolated[1][0]) / (abs(interpolated[0][0]) ** 2)
    else:
        interp_period_err = 0
    exp_period = helper.find_average(periods)
    exp_period_err = max(
        helper.find_std(periods), helper.find_average(periods_err)
    )
    helper.write_data_final(f"P{spot}", [str(exp_period), str(exp_period_err)])
    helper.write_data_final(f"C{spot}", [str(interp_period), str(interp_period_err)])


if __name__ == "__main__":
    helper.warn_module()
