#!/usr/bin/env python
# coding: utf-8
import sys
import pandas as pd
import numpy as np
pd.set_option('display.max_colwidth', 150)
pd.get_option("display.max_colwidth")

df = pd.read_csv(sys.argv[1])
print("Number of data=", len(df))

n_final=0
n_merge = 0
new_array=[]

for index, col in df.iterrows():
    if "run_03" in col['hkl_file']:
        filepath=col['hkl_file']
        dose_path = filepath[:filepath.rfind('blend')]
        col['dose_path']=dose_path
        
        pppp = filepath[:filepath.rfind('run_03')]
        cluster_index = int(pppp[pppp.rfind("_"):].replace("/","").replace("_",""))
        col['cluster_index']=cluster_index
    
        new_array.append(col)
        n_merge+=1


na = pd.DataFrame(new_array)

print(len(na))
# Grouping 'dose_path'
target_group = na.groupby(['dose_path'])
n_groups = len(target_group)
print(n_groups)

aaa=[]
for dose_path, tmpdf in target_group: 
    max_index=tmpdf['cluster_index'].idxmax()
    aaa.append(tmpdf.loc[max_index])

final_df = pd.DataFrame(aaa)
final_df.to_csv("test.csv", index=False)
