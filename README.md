# Solar rotation

Python scripts to determine the rate of rotation of the Sun on its axis (data files included).

## Requirements

- python3
- `numpy`
- `matplotlib`
- Shell scripts are written for POSIX-compliant systems.

## Download

```
$ git clone https://github.com/mstcl/solar_rotation
$ cd solar_rotation
```

Or straight from the browser: `Code` then `Download ZIP`.

## Installation & Usage

There is no installation, this is portable.

```
$ cd solar_rotation
$ ./sunspot_analysis.py -h
```

There is no documentation. Run `./sunspot_analysis.py -h` for descriptions of
what to do. The data needs to be structured in a specific hierarchy and also
specifically named. The file `./rotational_rate_analysis.py` contains the
calculations to obtain rotational periods.

Shell scripts provided can automate certain file operations, and can be run as

```
$ ./script.sh arg1 arg2 arg3 …
```

Check source code for details on what they do and the arguments required.

## Things to do

- [x] Parse all and analyse data
  - [x] Variables
  - [x] Results
- [x] Include error calculations
- [x] Produce final plots

## LICENSE

The experimental data is (free to use?) provided by the University.

The codebase is licensed under GNU General Public License v3.
