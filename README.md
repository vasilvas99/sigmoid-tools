# Sigmoid toolkit

This is a repo with the numerical scripts used in the study of the SM-dg family of curves.

## Installation and dependencies

### pip

These scripts depend on a few numerical python libraries like scipy and numpy. To install them you need the python module pip.

To obtain pip, please follow the guide at:

```
https://pip.pypa.io/en/stable/installation/
```

### Requirements

After obtaining a functional instance of pip, in the trunk of repo you will find a file named `requirements.txt`.

To install all the needed libraries to run these scripts open a terminal and run:

```bash
pip3 install -r requirements.txt
```

Wait for the installation of all libraries to finish. 


### Configuration

To configure the general behaiviour of all scripts that currently exist and might be developed in the future, please use the `config.toml` file available in the repo. It's general structure should look something like this:

```json
t0 = 0
t_final = 784035.0
initial_alpha = 1e-8
n_terms_taylor = 1
csv_delimiter = "\t"

[param_finder_props]
d_min = 2
g_min = 1
mu_min = 0

d_max = 2.0000000002
g_max = 1.00000002
mu_max = 5

g_ini = 1.000000001
d_ini = 2.0000000001
mu_ini = 1.3392259274139547e-06
shift_time = 0
plot_graphs_matplotlib = 0

[time_offset_finder_proprs]
fit_procedure = "nlsq"
```

`t0` и `t_final` set the integration interval for the numerical integrator.


## Scripts 

### Parameter finder

This script uses non-linear least squares to fit the best values for D and g for tab-separated dataset.

Usage

```bash
python3 parameter_finder.py <path_to_input_file.csv>
```

The first column in the tab-seperated list should be the values of the time coordinate and the second - the values for alpha.
