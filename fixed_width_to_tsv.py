#!/usr/bin/env python3
import os
import sys
import pandas as pd
from pathlib import Path

def help():
    print("Converts a file in fixed-width-format (.dat) to tab-separated values (.tsv)\n")
    print(f"Usage: {sys.argv[0]} [INPUT_FILE] [OUTPUT_DIRECTORY_PATH]\n\n"
          f"If [OUTPUT_DIRECTORY_PATH] is not specified the parent of [INPUT_PATH] is used.\n")
    print(f"{sys.argv[0]} -h or {sys.argv[0]} --help to show this help message")

if len(sys.argv) < 2:
    help()
    exit(1)
if sys.argv[1] == "-h" or sys.argv[1] == "--help":
    help()
    exit(0)

p = Path(sys.argv[1])
try:
    o = Path(sys.argv[2]).resolve()
    if not o.exists():
        os.makedirs(o)
    file_dir = o
except IndexError:
    file_dir = p.parent

if not p.exists() or not p.is_file():
    print(f"File {p} does not exist")
    sys.exit(2)


p  = p.resolve(strict=True)
new_file_name = p.stem + ".tsv"
data = pd.read_fwf(p, header=None)

data.to_csv(file_dir/new_file_name, sep = "\t", index=False, header=False)