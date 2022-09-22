import argparse
import csv
import pathlib
from tarfile import TarInfo

import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as optimize

from script_configurator import SIGMOID_CONFIG
from sigmoid_calculation import get_sigmoid

FINDER_CONFIG = SIGMOID_CONFIG["param_finder_props"]


def filter_data(data):
    # filter data to stay within interpolation bounds
    data = data[data[:, 0] > SIGMOID_CONFIG["t0"]]
    data = data[data[:, 0] < SIGMOID_CONFIG["t_final"]]
    return data


def read_data_csv(path: pathlib.Path):
    with open(path) as f:
        reader = csv.reader(
            f, delimiter=SIGMOID_CONFIG["csv_delimiter"], quoting=csv.QUOTE_NONNUMERIC
        )
        data = [row for row in reader]
    return filter_data(np.array(data))


def calculate_resd_vector(trial_sol, data):
    t_vals = data[:, 0]
    s_vals = data[:, 1]

    f_vals = np.squeeze(trial_sol(t_vals))

    return 1000 * (s_vals - f_vals)


def lsq_cost(x, data):
    d, g, tau_sm = x
    s = get_sigmoid(d, g, tau_sm)
    return calculate_resd_vector(s, data)


def plot(d, g, tau_sm, data):
    t_d = data[:, 0]
    y_d = data[:, 1]

    s = get_sigmoid(d, g, tau_sm)
    t_calc = np.linspace(SIGMOID_CONFIG["t0"], SIGMOID_CONFIG["t_final"], 1000)
    y_calc = np.squeeze(s(t_calc))

    plt.plot(t_calc, y_calc)
    plt.plot(t_d, y_d, "ro")
    plt.show()


def r2_calc(d, g, tau_sm, data):
    t_d = data[:, 0]
    y_d = data[:, 1]
    y_davg = np.average(y_d)

    s = get_sigmoid(d, g, tau_sm)
    y_calc = np.squeeze(s(t_d))

    ss_tot = np.sum((y_d-y_davg)**2)
    ss_res = np.sum((y_d-y_calc)**2)
    return 1 - (ss_res/ss_tot)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", type=pathlib.Path)
    p = parser.parse_args()

    if not p.file_path.exists():
        raise FileNotFoundError("Input File not found!")
    print(f"Running optimization with config: \n{FINDER_CONFIG}")
    dat = read_data_csv(p.file_path)

    print("Data read successfully. Starting optimization.")
    print(
        "============================================================================"
    )
    fit = optimize.least_squares(
        lsq_cost,
        x0=[
            FINDER_CONFIG["d_ini"],
            FINDER_CONFIG["g_ini"],
            FINDER_CONFIG["tau_sm_ini"],
        ],
        args=(dat,),
        verbose=2,
        bounds=(
            (
                FINDER_CONFIG["d_min"],
                FINDER_CONFIG["g_min"],
                FINDER_CONFIG["tau_sm_min"],
            ),
            (
                FINDER_CONFIG["d_max"],
                FINDER_CONFIG["g_max"],
                FINDER_CONFIG["tau_sm_max"],
            ),
        ),
    )
    d = fit.x[0]
    g = fit.x[1]
    tau_sm = fit.x[2]
    print(
        "\n\n============================================================================"
    )
    print(fit)
    print(
        "============================================================================"
    )
    if fit.success:
        print(
            f"Least Squares Fit successfully completed. "
            f"Obtained d = {d}, g = {g}, tau_sm = {tau_sm}"
        )
    else:
        print("!!!!!!!\nFit failed. Check the algorithm output above\n!!!!!!")
    print(
        "============================================================================"
    )

    print(f"R^2: {r2_calc(d, g, tau_sm, dat)*100}%")
    plot(d, g, tau_sm, dat)


if __name__ == "__main__":
    main()
