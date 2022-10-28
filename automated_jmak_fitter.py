from genericpath import isdir
from importlib.resources import path
import re
import subprocess
import pathlib
import glob, os
import sys
import csv

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

# fitter patterns
PATTERN = r"(?<={}\s=\s)[-+]?(?:\d*\.\d+|\d+)"
D = "d"
G = "g"
MU = "mu"
R2 = r"R\^2"
SCRIPT_DIR = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))

os.chdir(SCRIPT_DIR)

def get_float_value(string, key):
    matches = re.findall(PATTERN.format(key), string)
    return float(matches[0])
    
def run_nlsq(file_path: pathlib.Path):
    s = subprocess.run(["python3", SCRIPT_DIR/"parameter_finder.py", file_path.absolute()],
                       stdout=subprocess.PIPE,)
    stdout = s.stdout.decode("ascii","ignore")
    return stdout

def run_uniform(file_path: pathlib.Path):
    s = subprocess.run(["python3", SCRIPT_DIR/"parameter_finder_uniform.py", file_path.absolute()],
                       stdout=subprocess.PIPE,)
    stdout = s.stdout.decode("ascii","ignore")
    return stdout

def get_jmakn(filename):
    jmak_pattern = r"(?<=-{})\d+.\d+"
    n = float(re.findall(jmak_pattern.format("n"), filename)[0])
    return n

def get_filename(path: pathlib.Path):
    return os.path.basename(path.absolute())

def process_file(fit_procedure, data_file_path: pathlib.Path):
    print(f"Processing {data_file_path.absolute()}")
    jmak_n = get_jmakn(get_filename(data_file_path))
    stdout = fit_procedure(data_file_path)
    d_fit = get_float_value(stdout, D)
    g_fit = get_float_value(stdout, G)
    mu_fit = get_float_value(stdout, MU)
    R2_fit = get_float_value(stdout, R2)
    
    return [jmak_n, d_fit, g_fit, mu_fit, R2_fit]   

def get_jmak_file_paths(data_dir: pathlib.Path):
    os.chdir(data_dir.absolute())
    data_files = []
    for file in glob.glob("jmak-n*-tau*-tmin*-tmax*.tsv"):
        data_files.append(data_dir/file)
    os.chdir(SCRIPT_DIR)
    return data_files

def main():
    data_path = pathlib.Path("/home/vasko/Documents/sigmoid-tools/jmak_data")
    if not os.path.isdir(data_path.absolute()):
        eprint("Data path is not a valid directory")
        exit(-1)
    jmak_files = get_jmak_file_paths(pathlib.Path("/home/vasko/Documents/sigmoid-tools/jmak_data"))

    csv_rows = [["jmak-n", "d", "g", "c.f. SM->JMAK", "R^2", "procedure"]]
    for file in jmak_files:
        res = process_file(run_nlsq, file)
        res.append("NLSQ")
        csv_rows.append(res)
        
    csv_rows.append(["jmak-n", "d", "g", "c.f. SM->JMAK", "R^2", "procedure"])
    for file in jmak_files:
        res = process_file(run_uniform, file)
        res.append("UNIFORM")
        csv_rows.append(res)
        
    with open("jmak_fits.dat", "w") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerows(csv_rows)
    
if __name__ == "__main__":
    main()