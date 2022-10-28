"""A script that generates a bunch of
tab-separated data for jmak with pre-set n and tau

"""

from genericpath import isdir
import numpy as np
import argparse
import pathlib
import csv
import os
import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def jmak_n_tau(t, n, tau):
    return 1 - np.exp(-((2 * t / tau) ** n))


def cli():
    parser = argparse.ArgumentParser(
        description="Generates tab-separated values for\
                                     the JMAK model that can be used later"
    )
    parser.add_argument("n", type=float, help='The "dimension" of the JMAK model')
    parser.add_argument("tau", type=float, help="The timescale of the Model")
    parser.add_argument(
        "tmin", type=float, help="The starting time value for calculation"
    )
    parser.add_argument("tmax", type=float, help="The final time value for calculation")
    parser.add_argument(
        "tstep",
        nargs="?",
        type=float,
        default=0.01,
        help="The timestep for data generation. Default = 0.01",
    )
    parser.add_argument("outputdir", type=pathlib.Path, help ="Output file location")
    return parser.parse_args()

def main():
    args = cli()
    
    if not os.path.isdir(args.outputdir):
        eprint("outputdir is not a valid directory!")
        exit(-1)
    
    # generate data
    t = np.arange(args.tmin, args.tmax, args.tstep)
    alpha = jmak_n_tau(t, args.n, args.tau)
    
    # save to csv
    with open(args.outputdir/f"jmak-n{args.n}-tau{args.tau}-tmin{args.tmin}-tmax{args.tmax}.tsv", "w") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerows(zip(t, alpha))
        
if __name__ == "__main__":
    main()
    
    