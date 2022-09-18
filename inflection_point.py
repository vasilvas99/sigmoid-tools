import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as optimize

from sigmoid_calculation import get_sigmoid

DELTA_DER = 5e-5


def equation(t, sigmoid):
    dt = DELTA_DER
    return ((sigmoid(t + dt) - 2 * sigmoid(t) + sigmoid(t - dt)) / (dt ** 2))[0]


def find_inflection(sigmoid):
    # run a global optimizer to find a fitting initial cond
    anneal = optimize.dual_annealing(lambda x, sigmoid: equation(x, sigmoid) ** 2,
                                     args=(sigmoid,),
                                     # bounds=((sigmoid.t_min + 1 * DELTA_DER, sigmoid.t_max - DELTA_DER),)
                                     bounds=((sigmoid.t_min + 1 * DELTA_DER, (sigmoid.t_max - sigmoid.t_min) / 2),)
                                     )
    return optimize.root(equation, anneal.x, args=sigmoid)


def main():
    print("Inflection point calculator")
    print("============================================================================")

    dims = float(input("Enter the number of dimensions d = "))
    iteract = float(input("Enter the regime exponent g = "))
    s = get_sigmoid(dims, iteract)
    solution = find_inflection(s)

    print("============================================================================")
    print(solution)
    print("============================================================================")
    if solution.success:
        if np.abs(s(solution.x)-1) < 0.05:
            print("!!!!!!!\n"
                  "It seems that the sigmoid at the solution is too close to 1.0. This might be due to numerical"
                  " errors from the second derivative that make the root finding procedure unstable. Try lowering t_max"
                  " in the config.json file and rerun this script."
                  "\n!!!!!!!!!\n")
        print(f'Obtained solution for inflection point x0 = {solution.x[0]}, '
              f'with sigmoid value f(x0)={s(solution.x[0])[0]}')
    else:
        print("!!!!!!!!!! There was a problem during the optimization. Be careful with the results!")

    # plotting functions, probably should be in their own function ...
    t = np.linspace(s.t_min + DELTA_DER, s.t_max - DELTA_DER, 1000)
    second_der = equation(t, s)
    sigmoid_data = s(t)
    (fig, (ax1, ax2)) = plt.subplots(1, 2)

    ax1.set_title(f"SM {dims}-{iteract}")
    ax1.plot(t, sigmoid_data.T)
    ax1.plot(solution.x, s(solution.x), "ro")

    ax2.set_title(f"Second derivative")
    ax2.plot(t, second_der.T)
    ax2.plot(solution.x, solution.fun, "ro")
    plt.show()


if __name__ == "__main__":
    main()
