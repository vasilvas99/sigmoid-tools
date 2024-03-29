import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate as integrate
from script_configurator import SIGMOID_CONFIG

NTAYLOR = SIGMOID_CONFIG["n_terms_taylor"]

def rhs(t, y, d, g, mu):
    taylor_sum = 0
    for n in range(1, NTAYLOR+1, 1):
        taylor_sum += np.power(y,n)/n

    return (
        2
        * d
        * mu
        * np.power((1 - y), g)
        * np.power(taylor_sum, (1 - (1 / d)))
    )
    # return 2 * d * ((1 - y) ** g) * (y ** (1 - (1 / d)))


def get_sigmoid(d, g, mu=1):
    sol = integrate.solve_ivp(
        rhs,
        [SIGMOID_CONFIG["t0"], SIGMOID_CONFIG["t_final"]],
        [SIGMOID_CONFIG["initial_alpha"]],
        args=(d, g, mu),
        dense_output=True,
        method="DOP853",
        atol=1e-7,
    )
    if sol.status != 0:
        raise RuntimeError("Sigmoid integration failed!")
    return sol.sol


def main():
    t = np.linspace(SIGMOID_CONFIG["t0"], SIGMOID_CONFIG["t_final"], 1000)
    sigmoid = get_sigmoid(2, 1, 0.2)
    y = sigmoid(t)
    plt.plot(t, y.T)
    plt.show()


if __name__ == "__main__":
    main()
