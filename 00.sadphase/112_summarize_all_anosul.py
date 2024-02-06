import sys,os
import pandas as pd
import glob

sys.path.append("/isilon/users/target/target/Staff/rooms/kuntaro/Libs")
sys.path.append("/isilon/users/target/target/Staff/rooms/kuntaro/summarize_stats/")

import AnaXSCALE
import PhenixMergingStats

phs_log=".PHASING"

n_file=0
"""
/isilon/users/admin45/admin45/2020B/staff_data/S-SAD_merge/merge_14A_05MGy/merge_blend_1.41S_14A_5MGy/blend_1.41A_final/cluster_0453/run_03/merge200_index03/02.SAD_DM20/cysmet.csv
CYS_mean_dist,CYS_mean_height,CYS_n_data,MET_mean_dist,MET_mean_height,MET_n_data
0.8428749999999999,8.30875,8,0.5775,7.59,2

"""

def ana_sulfer_info(procpath, subdir="02.SAD_DM20"):
    sadpath=os.path.join(procpath,subdir)
    new_dics={}

    cols=procpath.split("/")
    wavelength=float(cols[8].split("_")[1].replace("A",""))/10.0
    dose=float(cols[8].split("_")[2].replace("MGy",""))
    n_merged=int(cols[-1].split("_")[0].replace("merge",""))
    merge_index=int(cols[-1].split("_")[1].replace("index",""))

    print(wavelength,dose,n_merged,merge_index)

    # Reading CSV file of 'anode' analysis
    csv_file=os.path.join(sadpath,"cysmet.csv")
    if os.path.exists(csv_file):
        df=pd.read_csv(csv_file)
    else:
        # Empty data frame -> add some 'dummy' information
        dummy_dict={}
        df=pd.DataFrame(dummy_dict)

    # Storing information
    cys_flag=False
    if 'CYS_mean_dist' not in df.columns:
        df['CYS_mean_dist']=999.999
        df['CYS_mean_height']=-999.999
        df['CYS_n_data']=0
    else:
        cys_flag=True

    met_flag=False
    if 'MET_mean_dist' not in df.columns:
        df['MET_mean_dist']=999.999
        df['MET_mean_height']=-999.999
        df['MET_n_data']=0
    else:
        met_flag=True

    # Adding required information from 'proc_path'
    df['procpath']=procpath
    df['wavelength']=wavelength
    df['dose']=dose
    df['n_merged']=n_merged
    df['merge_index']=merge_index

    # Analysis flag
    df['cys_flag']=cys_flag
    df['met_flag']=met_flag

    return df

# Data frame of 'proc_path'
df = pd.read_csv(sys.argv[1])

n_file=0
for index, col in df.iterrows():
    filepath=col['procpath']
    dirlist=glob.glob("%s/*"%filepath)
    print(filepath)
    # For 'merging directories'
    for di in dirlist:
        if "merge" in di and "index" in di:
            # DM 20 cycle data frame
            sul_df=ana_sulfer_info(di, "02.SAD_DM20")

            if n_file==0:
                final_df=sul_df
            else:
                final_df=pd.concat([final_df, sul_df])
 
            # Number of data directories
            n_file+=1

final_df.to_csv(sys.argv[2], index=None)
