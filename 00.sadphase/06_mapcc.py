# 2021/01/05
import pandas as pd
import glob
import os
import sys
import subprocess as sp
sys.path.append('/isilon/users/target/target/Staff/rooms/kuntaro/Libs/')
import ComRefine

def read_final_contrast(fin):
    """ read contrast value in final column"""
    contrast = 0.0 
    lines = open(fin, 'r').readlines()
    # reversed (search contrast value from the end of the log file to get final contrast)
    for line in reversed(lines):
        if "Contrast" in line:
            contrast = float(line.split(',')[1].split()[-1])
            break

    return contrast

def count_CA(pdb):
    """ count CA atoms in PDB file"""
    #count = 0
    cmd = "cat %s | grep CA | wc -l" % pdb
    res = sp.Popen(cmd, shell=True, stdout=sp.PIPE)
    stdout, stderr = res.communicate()
    count = stdout.strip()

    return count

def write_status(outpath,judge):
    ofile=open(os.path.join(outpath, ".mapcc"),"w")
    ofile.write("%s\n"%judge)
    ofile.close()

if __name__ == "__main__":
    df = pd.read_csv("./oden_prep.csv")
    print("Number of data=", len(df))
    prefix="ssad"

    if len(sys.argv)==2:
        sad_dir=sys.argv[1]
    else:
        sad_dir="00.SAD"
    
    for index, col in df.iterrows():
        filepath=col['hkl_file']
        procpath=filepath[:filepath.rfind("/")]
        sad_proc_path=os.path.join(procpath, sad_dir)

        # MTZ file names
        mtz_o = "%s.mtz" % prefix
        mtz_i = "%s_i.mtz" % prefix
        
        # read contrast from log file (if not available constrast = 0.0)
        if os.path.exists(os.path.join(sad_proc_path, mtz_o)):
            prefix = 'ssad'
        elif os.path.exists(os.path.join(sad_proc_path, mtz_i)):
            prefix = 'ssad_i'
        else:
            write_status(sad_proc_path, "failed")
            continue
    
        # phenix.map_cc_mtz_pdb 
        mtzin = '%s.mtz' % prefix
        mtzin_path = '%s/%s.mtz' % (sad_proc_path, prefix)
        mr_proc_path = os.path.join(procpath,'01.MR')
        print("MR=",mr_proc_path)

        model_pdb = '%s/mr_001.pdb' % mr_proc_path
        model_pdb_rel_path = os.path.relpath(model_pdb, sad_proc_path)
        print(model_pdb_rel_path)
        #print model_pdb, model_pdb_rel_path
        if os.path.exists(mtzin_path) and os.path.exists(model_pdb):
            comf = ComRefine.ComRefine(sad_proc_path,qhost_selection_flag=False)
            comname = comf.map_cc(mtzin, model_pdb_rel_path)
            os.system("chmod a+x %s" % comname)
            os.system("qsub %s" % comname)
            write_status(sad_proc_path, "success")
