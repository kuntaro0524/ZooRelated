# 2021/01/05
import os, sys, glob
import sys
import pandas as pd
import subprocess as sp
sys.path.append('/isilon/users/target/target/Staff/rooms/kuntaro/Libs')
import ComRefine

# Read CSV file
model="/isilon/BL32XU/BLsoft/PPPP/30.RD11/lys_model.pdb"

df = pd.read_csv("./oden_prep.csv")
print("Number of data=", len(df))

find_file="XSCALE.INP"

def count_datasets(xscale_inp):
    n_count=0
    for line in open(xscale_inp,"r").readlines():
        if "INPUT_FILE=" in line:
            n_count+=1
    return n_count

for index, col in df.iterrows():
    filepath=col['hkl_file']
    procpath=filepath[:filepath.rfind("/")]
    # target_file
    target_file=os.path.join(procpath, find_file)
    if os.path.exists(target_file):
        n_merged=count_datasets(target_file)
        print(procpath, n_merged)

    procpath=filepath[:filepath.rfind("/")]
