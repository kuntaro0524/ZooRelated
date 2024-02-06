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

find_file=sys.argv[1]

for index, col in df.iterrows():
    if "run_03" in col['hkl_file']:
        filepath=col['hkl_file']
        procpath=filepath[:filepath.rfind("/")]
        # target_file
        target_file=os.path.join(procpath, find_file)
        #print(target_file)
        if os.path.exists(target_file):
            print("FOUND",target_file)
