import argparse
import csv
import pathlib

import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as optimize

from script_configurator import SIGMOID_CONFIG
from sigmoid_calculation import get_sigmoid


def filter_data(data):
    # filter data to stay within interpolation bounds
    data = data[data[:, 0] > SIGMOID_CONFIG["t0"]]
    data = data[data[:, 0] < SIGMOID_CONFIG["t_final"]]
    return data


def read_data_csv(path: pathlib.Path):
    with open(path) as f:
        reader = csv.reader(f, delimiter=SIGMOID_CONFIG["csv_delimiter"], quoting=csv.QUOTE_NONNUMERIC)
        data = [row for row in reader]
    return filter_data(np.array(data))


def calculate_resd_vector(trial_sol, data):
    t_vals = data[:, 0]
    s_vals = data[:, 1]

    f_vals = np.squeeze(trial_sol(t_vals))

    return 1000 * (s_vals - f_vals)


def lsq_cost(x, data):
    d, g = x
    s = get_sigmoid(d, g)
    return calculate_resd_vector(s, data)


def plot(d, g, data):
    t_d = data[:, 0]
    y_d = data[:, 1]

    s = get_sigmoid(d, g)
    t_calc = np.linspace(SIGMOID_CONFIG["t0"], SIGMOID_CONFIG["t_final"], 1000)
    y_calc = np.squeeze(s(t_calc))

    plt.plot(t_calc, y_calc)
    plt.plot(t_d, y_d, "ro")
    plt.show()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", type=pathlib.Path)
    p = parser.parse_args()

    if not p.file_path.exists():
        raise FileNotFoundError("Input File not found!")

    dat = read_data_csv(p.file_path)

    print("Data read successfully. Starting optimization.")
    print("============================================================================")
    fit = optimize.least_squares(lsq_cost, x0=[1, 1], args=(dat,), verbose=2, bounds=(1e-10, np.inf))
    d = fit.x[0]
    g = fit.x[1]
    print("\n\n============================================================================")
    print(fit)
    print("============================================================================")
    if fit.success:
        print(f"Least Squares Fit successfully completed. "
              f"Obtained d = {d}, g = {g}")
    else:
        print("!!!!!!!\nFit failed. Check the algorithm output above\n!!!!!!")
    print("============================================================================")

    plot(d, g, dat)


if __name__ == "__main__":
    main()
