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

# Re-run job whenever or not
if len(sys.argv)==2:
    force_to_rerun = True
else:
    force_to_rerun = False

n_final=0
n_merge = 0
new_array=[]

####
def run_MR(proc_path,symm,dmin,model,prefix):
    # MR directory
    mr_dir=os.path.join(procpath,"01.MR")
    # Check directory existence
    if not os.path.exists(mr_dir):
        os.makedirs(mr_dir)
    # Check if already done or not.
    check_file = os.path.join(mr_dir,"mr_001.pdb")
    print("Checking if %s exists..." % check_file)
    if os.path.exists(check_file):
        if force_to_rerun == False:
            print("Already done.")
            return True
        else:
            print("Forced to redo refinement.")
    # File paths
    xscale_mtz_path = proc_path + '/ccp4/xscale.mtz'
    xscale_mtz_rel_path = os.path.relpath(xscale_mtz_path, mr_dir)
    comf = ComRefine.ComRefine(mr_dir,qhost_selection_flag=False)
    comname = comf.simple_refine(xscale_mtz_rel_path, symm, dmin, model, prefix, hkl_sort="")

    os.system("chmod a+x %s" % comname)
    os.system("qsub %s" % comname)
    return True

####
# prefix,hkl_file,cell_params,space_group,anom_atom,n_anom,n_try,phase_dmax,solv_cnt,n_dm,build_cycle,dmin
####

for index, col in df.iterrows():
    filepath=col['hkl_file']
    procpath=filepath[:filepath.rfind("/")]
    print(procpath)
    # RD11 process
    symm=col['space_group']
    dmin=col['dmin']
    run_MR(procpath,symm,dmin,model,prefix="mr")
