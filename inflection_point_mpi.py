"""
MPI backend for the inflection point calculator to allow generation of stats in massively parallel
environments
"""
from mpi4py.futures import MPIPoolExecutor as Pool
import numpy as np
from inflection_point import map_func
from pathlib import Path
import csv
from script_configurator import SIGMOID_CONFIG
import argparse

def get_dg_pairs(d_range, g_range):
    dims = np.arange(d_range[0], d_range[1], d_range[2])
    gs = np.arange(g_range[0], g_range[1], g_range[2])
    dims2D, gs2D = np.meshgrid(dims, gs)
    return np.column_stack((dims2D.ravel(), gs2D.ravel()))


def map_func_wrapper(dg_pair):
    return map_func(*dg_pair)

def save_as_csv(pairs, computation_result, file_path):
    with open(file_path, "w") as f:
        writer = csv.writer(f, delimiter=SIGMOID_CONFIG["csv_delimiter"])
        writer.writerow(["g", "d", "inflection"])
        for pair, result in zip(pairs, computation_result):
            writer.writerow([pair[1], pair[0], result])

def cli():
    parser = argparse.ArgumentParser(
        description="Inflection point finder for SM models. MPI aware. Finds the inflection point for a whole range of d and g values")
    parser.add_argument("dstart", type=float, default=1.1)
    parser.add_argument("dend", type=float, default=3)
    parser.add_argument("dstep", type=float, default=0.1)
    parser.add_argument("gstart", type=float, default=1)
    parser.add_argument("gend", type=float, default=2)
    parser.add_argument("gstep", type=float, default=0.1)
    parser.add_argument("output_file", type=Path, default=Path("./output.csv"))
    args = parser.parse_args()

    return args

def main():
    args = cli()
    d_range = (args.dstart, args.dend+args.dstep, args.dstep)
    g_range = (args.gstart, args.gend+args.dstep, args.gstep)
    pairs = get_dg_pairs(d_range, g_range)
    print(f'\nRunning with config: \n {args} \n {d_range=}, {g_range=}')

    with Pool() as p:
        res = p.map(map_func_wrapper, pairs)
        res = np.squeeze(np.array(list(res)))
        save_as_csv(pairs, res, args.output_file)


if __name__ == "__main__":
    main()
