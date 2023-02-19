from sigmoid_calculation import get_sigmoid
from script_configurator import *
import numpy as np 
import csv

def generate_xi_data(alpha_range):
    t = np.linspace(SIGMOID_CONFIG["t0"], SIGMOID_CONFIG["t_final"], 1000)
    ys = []

    for alpha in np.arange(*alpha_range):
        sigmoid = get_sigmoid(alpha, 1, 1)
        ys.append(sigmoid(t))
    return t, np.squeeze(np.array(ys))


if __name__ == "__main__":
    alpha_ini = 2
    alpha_final = 3.1
    alpha_step = 0.1
    alpha_range = [alpha_ini, alpha_final, alpha_step]
    
    ts, ys = generate_xi_data(alpha_range)
    
    with open("alpha_d_1-models.dat", "w") as f:
        writer = csv.writer(f, delimiter="\t")
        alpha_labels = [f"alpha_{a:.2f}_{1}" for a in np.arange(*alpha_range)]
        writer.writerow(["t"] + alpha_labels)
      
        for idx, t in enumerate(ts):
            row = [t] + list(ys[:, idx])
            writer.writerow(row)