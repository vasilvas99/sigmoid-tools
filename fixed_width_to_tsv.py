#!/usr/bin/env python3

"""
An executable script that converts fixed-width (Fortran) format files to the more predictable
and thus easier to parse tab-separated values (TSV) format.
Provides an ArgParse Cli.
"""
import csv
from typing import List
from pathlib import Path
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor


parser = ArgumentParser(
    description="Converts fixed-width (Fortran) format files to tab-separated (TSV) format."
)
parser.add_argument(
    "input_file",
    help="Input file in fixed-width format",
    metavar="INPUT_PATH",
)
parser.add_argument("-o", dest="output_path", help="Output file path.")
parser.add_argument(
    "-s",
    "--skip",
    help="Number of header lines to skip. [Default: 0]",
    type=int,
    default=0,
)
args = parser.parse_args()

# Setup input-output paths
input_path = Path(args.input_file).resolve(strict=True)
if args.output_path is not None:
    output_path = Path(args.output_path)
else:
    base_name = input_path.stem
    output_path = Path(base_name).with_suffix(".tsv")


def parse_line(line: str) -> List[float]:
    """Parse a single line of whitespace separated values to a list of float

    Args:
        line (str): Line string

    Returns:
        List[float]: Output list of floats.
    """
    return [float(number) for number in line.strip().split()]


with open(input_path, encoding="utf-8") as f:
    for _ in range(args.skip):
        # skip the first args.skip lines (header)
        next(f)
    with ThreadPoolExecutor() as executor:
        parsed_list = list(executor.map(parse_line, f))

with open(output_path, mode="w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerows(parsed_list)
