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

if len(sys.argv) == 2:
    sad_dir=sys.argv[1]
else:
    sad_dir="00.SAD"

phs_log=".PHASING"

n_file=0
for index, col in df.iterrows():
    filepath=col['hkl_file']
    # Root directory for data analysis
    procpath=filepath[:filepath.rfind("/")]
    # SAD analysis directory
    sadpath=os.path.join(procpath,sad_dir)
    target_file=os.path.join(sadpath, phs_log)

    # Phasing results from SHELX C/D/E
    csv_file=os.path.join(sadpath,"phasing_results.csv")
    if os.path.exists(csv_file):
        tmpdf=pd.read_csv(csv_file)
        tmpdf['path']=filepath

    # results from mapcc
    mapcc_file=os.path.join(sadpath,"mapcc.dat")
    if os.path.exists(mapcc_file):
        lines=open(mapcc_file,"r").readlines()
        for line in lines:
            if "overall CC:" in line:
                overall_cc=float(line.split()[2])
            if "local CC:" in line:
                local_cc=float(line.split()[2])
        tmpdf['overall_cc']=overall_cc
        tmpdf['local_cc']=local_cc
    else:
        tmpdf['overall_cc']=-9999.9999
        tmpdf['local_cc']=-9999.9999

    if n_file==0:
        final_df=tmpdf
    else:
        final_df=pd.concat([final_df,tmpdf])

    n_file+=1

# Solved selection
solved_selection=final_df['nres_o']>0

solved_df=final_df[solved_selection]
solved_df.to_csv("phasing_summary.csv", index=None)
