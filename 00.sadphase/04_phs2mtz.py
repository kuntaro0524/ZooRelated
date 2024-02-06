# 2021/01/05
import os, sys, glob
import sys
import pandas as pd
import subprocess as sp
sys.path.append('/isilon/users/target/target/Staff/rooms/kuntaro/Libs')
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

def read_cellConst_from_xscalelp(xscalelp):
    """ read cellConst from XSCALE.LP """
    lines = open(xscalelp, 'r').readlines()
    for line in lines:
        if 'UNIT_CELL_CONSTANTS=' in line:
            cellConstants = ' '.join(line.split()[1:])
            break

    return cellConstants

if __name__ == "__main__":
    # Read CSV file
    model="/isilon/BL32XU/BLsoft/PPPP/30.RD11/lys_model.pdb"
    # PREFIX of shelx C/D/E
    prefix="ssad"
    
    df = pd.read_csv("./oden_prep.csv")
    print("Number of data=", len(df))

    if len(sys.argv)==2:
        sad_dir=sys.argv[1]
    else:
        sad_dir="00.SAD"
    
    # SHELXE log/pdb file (original/invert)
    log_orig = 'shelxe_o.log'
    log_inv = 'shelxe_i.log'
    pdb_orig = 'lys.pdb'
    pdb_inv = 'lys_i.pdb'

    for index, col in df.iterrows():
        filepath=col['hkl_file']
        procpath=filepath[:filepath.rfind("/")]

        sad_proc_path=os.path.join(procpath,sad_dir)

        log_o = os.path.join(sad_proc_path, log_orig)
        log_i = os.path.join(sad_proc_path, log_inv)
    
        pdb_o = os.path.join(sad_proc_path, pdb_orig)
        pdb_i = os.path.join(sad_proc_path, pdb_inv)

        # read contrast from log file (if not available constrast = 0.0)
        if os.path.exists(log_o):
            con_o = read_final_contrast(log_o)
        else:
            con_o = -9999.9999

        if os.path.exists(log_i):
            con_i = read_final_contrast(log_i)
        else:
            con_i = -9999.9999

        if con_o!=-9999.9999 and con_i!=-9999.9999:
            delta = abs(con_o - con_i)
            print("Delta of contrast=", delta)
        else:
            delta = 99999999999

        count = '0'
        flag = None

        # Check if .phs files exist or not
        # original
        phs_o = os.path.join(sad_proc_path,"ssad.phs")
        pdb_o = os.path.join(sad_proc_path,"ssad.pdb")
        # inverse
        phs_i = os.path.join(sad_proc_path,"ssad_i.phs")
        pdb_i = os.path.join(sad_proc_path,"ssad_i.pdb")

        existsOriginals=False
        existsInverse=False

        if os.path.exists(phs_o) and os.path.exists(pdb_o):
            print("Original phase exists")
            existsOriginals=True

        if os.path.exists(phs_o) and os.path.exists(pdb_o):
            print("Inverse phase exists")
            existsInverse=True

        # pattern 1,2,3
        existsSolved=False
        # No solution
        if existsOriginals==False and existsInverse==False:
            existsSolved=False
        elif existsOriginals==True or existsInverse==True:
            existsSolved=True

        if existsSolved: print("Structure solved?")

        # Contrast check
        count_o=count_i=-9999
        if existsOriginals:
            count_o = count_CA(pdb_o)
        if existsInverse:
            count_i = count_CA(pdb_i)

        out_str = 'contrast_orig,contrast_inv,delta,nres_o,nres_i\n'
        out_str += '%f,%f,%f,%s,%s\n' % (con_o, con_i, delta, count_o, count_i)

        # write 'contrast.dat' (including contrast (original/invert), delta, number of residues)
        contrast_dat_path = os.path.join(sad_proc_path, 'phasing_results.csv')
        fo = open(contrast_dat_path, 'w')
        fo.write(out_str)
        fo.close()

        # Space group from 'oden_prep.csv'
        symm=col['space_group']

        # Choose the data for converting to MTZ files
        if existsSolved:
            if count_o >= count_i:
                target_phs = phs_o
            elif count_o < count_i:
                target_phs = phs_i
            # phs2mtz 
            xscale_path = os.path.join(procpath,'XSCALE.LP')
            cell_params = read_cellConst_from_xscalelp(xscale_path)
            comf = ComRefine.ComRefine(sad_proc_path,qhost_selection_flag=False)
            comname = comf.phs2mtz(prefix, cell_params,symm=symm)
            os.system("chmod a+x %s" % comname)
            os.system("qsub %s" % comname)
            # Generating phasing succeeded file.
            result_file=os.path.join(sad_proc_path, ".PHASING")
            of=open(result_file,"w")
            of.write("success")
            of.close()

        else:
            # Generating phasing failed file.
            result_file=os.path.join(sad_proc_path, ".PHASING")
            of=open(result_file,"w")
            of.write("failed")
            of.close()
