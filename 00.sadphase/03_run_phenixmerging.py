#!/usr/bin/env python
# coding: utf-8
import os,sys
import pandas as pd
import numpy as np

sys.path.append("/isilon/users/target/target/Staff/rooms/kuntaro/Libs/")
import DirectoryProc # currently not used
import ComRefine
import ResolutionFromXscaleHKL # currently not used
import AnaXSCALE

## Header information
model="/isilon/BL32XU/BLsoft/PPPP/30.RD11/lys_model.pdb"

df = pd.read_csv("./oden_prep.csv")
print("Number of data=", len(df))

n_final=0
n_merge = 0
new_array=[]

####
def run_MR(proc_path,symm,dmin,model,prefix):
    # MR directory
    mr_dir=os.path.join(procpath,"01.MR")
    # SAD process
    if not os.path.exists(mr_dir):
        os.makedirs(mr_dir)

    xscale_mtz_path = proc_path + '/ccp4/xscale.mtz'
    xscale_mtz_rel_path = os.path.relpath(xscale_mtz_path, mr_dir)
    comf = ComRefine.ComRefine(mr_dir)
    comf.unsetSelectQhost()
    comname = comf.simple_refine(xscale_mtz_rel_path, symm, dmin, model, prefix, hkl_sort="")
    os.system("chmod a+x %s" % comname)
    os.system("qsub %s" % comname)

def run_phenix_mergingstats(proc_path, hklin="xscale.hkl"):
    hkl_path = os.path.join(proc_path, hklin)
    hkl_rel_path = os.path.relpath(hkl_path, proc_path)

    # phenix.merging_statistics
    if os.path.exists(hkl_path):
        comf = ComRefine.ComRefine(proc_path)
        comf.unsetSelectQhost()
        comname = comf.phenix_merging_statistics(hkl_rel_path)
        os.system("chmod a+x %s" % comname)
        os.system("qsub %s" % comname)

####
# prefix,hkl_file,cell_params,space_group,anom_atom,n_anom,n_try,phase_dmax,solv_cnt,n_dm,build_cycle,dmin
####

for index, col in df.iterrows():
    filepath=col['hkl_file']
    procpath=filepath[:filepath.rfind("/")]
    # phenix.merging_stats
    logname = os.path.join(procpath, "merging_stats.log")
    if os.path.exists(logname):
        print("Already done")
        continue
    else:
        run_phenix_mergingstats(procpath)
