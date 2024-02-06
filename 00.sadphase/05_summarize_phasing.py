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

#find_file=sys.argv[1]
phs_log=".PHASING"

n_file=0
for index, col in df.iterrows():
    filepath=col['hkl_file']
    procpath=filepath[:filepath.rfind("/")]
    sadpath=os.path.join(procpath,"00.SAD")
    target_file=os.path.join(sadpath, phs_log)

    #if os.path.exists(target_file):
        #lines=open(target_file,"r").readlines()
        #for line in lines:
            #if line.rfind("succe"):
    csv_file=os.path.join(sadpath,"phasing_results.csv")
    if os.path.exists(csv_file):
        tmpdf=pd.read_csv(csv_file)
        tmpdf['path']=filepath
        if n_file==0:
            final_df=tmpdf
        else:
            final_df=pd.concat([final_df,tmpdf])
        n_file+=1

# Solved selection
solved_selection=final_df['nres_o']>25

solved_df=final_df[solved_selection]
solved_df.to_csv("phasing_summary.csv", index=None)
