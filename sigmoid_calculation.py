import json

import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate as integrate
from script_configurator import *


def rhs(t, y, d, g):
    return 2 * d * np.power((1 - y), g) * np.power(y, (1 - (1 / d)))
    # return 2 * d * ((1 - y) ** g) * (y ** (1 - (1 / d)))


def get_sigmoid(d, g):
    sol = integrate.solve_ivp(rhs, [SIGMOID_CONFIG["t0"], SIGMOID_CONFIG["t_final"]], [SIGMOID_CONFIG["initial_alpha"]],
                              args=(d, g),
                              dense_output=True,
                              method="DOP853",
                              atol=1e-15
                              )
    if sol.status != 0:
        raise RuntimeError("Sigmoid integration failed!")
    return sol.sol


def main():
    t = np.linspace(SIGMOID_CONFIG["t0"], SIGMOID_CONFIG["t_final"], 1000)
    sigmoid = get_sigmoid(2, 1)
    y = sigmoid(t)
    plt.plot(t, y.T)
    plt.show()


if __name__ == "__main__":
    main()
