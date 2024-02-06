#!/usr/bin/env python
# coding: utf-8
import sys,os
import pandas as pd
import numpy as np
pd.set_option('display.max_colwidth', 150)
pd.get_option("display.max_colwidth")

df = pd.read_csv(sys.argv[1])
print("Number of data=", len(df))

n_final=0
n_row = 0
new_array=[]

def count_datasets(xscale_inp):
    n_count=0
    for line in open(xscale_inp,"r").readlines():
        if "INPUT_FILE=" in line:
            n_count+=1
    return n_count

for index, col in df.iterrows():
    filepath=col['hkl_file']
    # Paths setting
    dose_path = filepath[:filepath.rfind('blend')]
    procpath=filepath[:filepath.rfind("/")]
    col['dose_path']=dose_path
    
    pppp = filepath[:filepath.rfind('run_03')]
    cluster_index = int(pppp[pppp.rfind("_"):].replace("/","").replace("_",""))
    col['cluster_index']=cluster_index

    # XSCALE.INP path
    xscaleinp = os.path.join(procpath,"XSCALE.INP")
    n_merged = count_datasets(xscaleinp)
    col['n_merged']=n_merged

    print(col['dose_path'],col['n_merged'])

    new_array.append(col)
    n_row+=1

na = pd.DataFrame(new_array)

# Grouping 'dose_path'
target_group = na.groupby('dose_path')
n_groups = len(target_group)

aaa=[]
for dose_path, tmpdf in target_group: 
    filepath=col['hkl_file']
    max_index=tmpdf['cluster_index'].idxmax()
    aaa.append(tmpdf.loc[max_index])

final_df = pd.DataFrame(aaa)
final_df.to_csv("test.csv", index=False)
