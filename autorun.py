#! /usr/bin/env python3

import tomlkit
import os
import sys
import numpy as np
import subprocess
from pathlib import Path
import re
import parameter_finder

basepath = Path(os.path.dirname(__file__)).resolve(True)
config_toml = basepath / Path("config.toml")
dataset_path = Path(sys.argv[1]).resolve(True)
dataset_dir = dataset_path.parent

try: 
    idx = int(sys.argv[2])
except Exception as _:
    idx = "-"

with open(config_toml, encoding="utf-8") as f:
    SIGMOID_CONFIG = tomlkit.load(f)

dataset = np.loadtxt(dataset_path, delimiter=SIGMOID_CONFIG["csv_delimiter"])
ts = dataset[:, 0]
max_t = ts.max()

SIGMOID_CONFIG["t_final"] = max_t * 1.05
SIGMOID_CONFIG["param_finder_props"]["mu_ini"] = 1 / max_t

print("Using config:")
print(tomlkit.dumps(SIGMOID_CONFIG))

with open(config_toml, "w", encoding="ascii") as f:
    tomlkit.dump(SIGMOID_CONFIG, f)

d_fit, g_fit, mu_fit, R2_fit = parameter_finder.main([dataset_path.as_posix()])

# if it looks like the parameters are fixed, rescale time and save
FINDER_CONF = SIGMOID_CONFIG["param_finder_props"]
if FINDER_CONF["d_max"] - FINDER_CONF["d_min"] < 1e-4 and FINDER_CONF["g_max"]- FINDER_CONF["g_min"] < 1e-4:
    print("D and g seem fixed. Will save rescaled version.")
    dataset[:, 0] = dataset[:,0]*mu_fit
    np.savetxt(dataset_dir / ("rescaled_" + dataset_path.name), dataset)
    
# Lazy tsv format
output = f"idx\tD\tg\ttau\tR^2\n{idx}\t{d_fit}\t{g_fit}\t{1/mu_fit}\t{R2_fit}"

print(f"{d_fit=}\n{g_fit=}\ntau_fit={1/mu_fit}\n{R2_fit=}")
with open(dataset_dir / Path(f"fit_output_{dataset_path.stem}.tsv"), "w", encoding="utf-8") as f:
    f.write(output)
