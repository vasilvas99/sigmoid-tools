from script_configurator import SIGMOID_CONFIG
import argparse
import pathlib
import numpy as np
from scipy.optimize import minimize_scalar

FINDER_CONFIG = SIGMOID_CONFIG["time_offset_finder_proprs"]

method = FINDER_CONFIG["fit_procedure"].lower()

if "nlsq" == method:
    from parameter_finder import fit_data, read_data_csv, r2_calc
elif "uniform" == method:
    from parameter_finder_uniform import fit_data, read_data_csv, r2_calc
else:
    raise ValueError("Unkown fitting procedure")

def calculate_cost(t_offset, t_d, y_d):
    print(t_offset)
    t_new = np.copy(t_d) - t_offset
    offset_data = np.array(list(zip(t_new,y_d)))
    _, d, g, mu = fit_data(offset_data)
    r2 = r2_calc(d, g, mu, offset_data)
    return np.abs((1-r2))*1e6

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", type=pathlib.Path)
    p = parser.parse_args()

    if not p.file_path.exists():
        raise FileNotFoundError("Input File not found!")
    print(f"Running finder with config: \n{FINDER_CONFIG}")
    
    data = read_data_csv(p.file_path)
    t_d = data[:, 0]
    y_d = data[:, 1]
    t_offset_max = np.min(t_d)
    
    
    minimizer = minimize_scalar(calculate_cost, method='bounded', bounds=(0, t_offset_max), args=(t_d, y_d))
    print(minimizer)
    print(f'final r2:  {1-minimizer.fun/1e6}')
 

if __name__ == "__main__":
    main()


