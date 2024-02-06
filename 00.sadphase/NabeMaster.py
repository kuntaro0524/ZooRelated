# NabeMaster
# 2020/12/08

import sys
import os
import glob
import numpy

from yamtbx.dataproc import eiger
from yamtbx.dataproc import cbf
from yamtbx.dataproc.XIO.plugins import eiger_hdf5_interpreter
from libtbx import easy_mp

#sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")
#sys.path.append("/isilon/BL32XU/BLsoft/PPPP/Libs")
#sys.path.append("/isilon/users/target/target/Staff/mat/dev/")
#sys.path.append("/isilon/users/target/target/Staff/mat/dev/Libs")
#sys.path.append("/isilon/users/target/target/Staff/mat/nabe/oden")
sys.path.append("/isilon/users/target/target/Staff/rooms/kuntaro/Libs")
import ComRefine
import ResolutionFromXscaleHKL 
import MyException
import DirectoryProc # currently not used
import ODEN
#import AnaXSCALE
###----------Setting----------###
# dataset with lower resolution than dmin_threshold will not processed
dmin_threshold = 120 

###---------------------------------###

### util ###
def read_resol_from_xds2mtzLog(xds2mtzLog):
    """ read dmin from 'xds2mtz.log' (not used in current oden) """ 

    lines = open(xds2mtzLog, 'r').readlines()
    key_i = 0
    isFlag = None
    resol = 0

    for line in lines:   
        if isFlag:
            if key_i > 2:
                isFlag = None
                break
         
            if key_i == 1:   
                resol = float(line.strip().split()[-3])
                key_i += 1
                continue
            
            key_i += 1
        
        
        if line.count('Resolution Range'):
            isFlag = True 
    return resol

def read_cellparams_from_gxparm(gxparm):
    """ read cell const from 'GXPARM.XDS' """
    cell_params = ""
    with open(gxparm, "r") as f:
        line = f.readlines()[3].strip()
        cell_params = " ".join(line.split()[1:])

    return cell_params 

def read_cellparams_from_xscalelp(xscalelp):
    """ read cell const from 'XSCALE.LP' """
    cell_params = ""
    with open(xscalelp, "r") as f:
        lines = f.readlines()
        for line in reversed(lines):
            if "UNIT_CELL_CONSTANTS" in line:
                cell_params = " ".join(line.split()[1:])
    return cell_params

def read_dmin_from_xscalelp(xscalelp):
    """ read dmin from 'XSCALE.LP' """
    with open(xscalelp, "r") as f:
        lines = f.readlines()
        for line in lines:
            if "RESOLUTION_SHELLS" in line:
                dmin = float(line.split()[-1].rstrip())
    return dmin


def read_dmin_from_decisionLog(decision_log):
    """ read dmin from 'decision.log' """
    dmin = 99.9999
    with open(decision_log, "r") as f:
        lines = f.readlines()
        for line in lines:
            if "Re-scale at" in line:
                dmin = float(line.split()[-2])

    return dmin


def exec_cmd(cmd):
    return subprocess.Popen(
        cmd, stdout=subprocess.PIPE,
        shell=True).communicate()[0]


def calc_resol_limit(xscalelp):
    cmd = "yamtbx.python /oys/xtal/yamtbx/yamtbx/dataproc/auto/command_line/decide_resolution_cufoff.py %s" % xscalelp
    print "command = %s" % cmd
    logs = exec_cmd(cmd)
    lines = logs.split('\n')

    for line in lines:
        if line.rfind("Suggested cutoff") != -1:
            try:
                resolution = float(line.split()[2])
                print "Suggested cutoff= %f" % resolution
                return resolution
            except:
                return  99.99 

### 

class NabeMaster():
    def __init__(self):
        pass

    def prep_oden_csv(self, csvout="oden_prep.csv", outdir="."):
        """ make 'oden_prep.csv' """

        # Original
        #hkl_list = glob.glob('_kamoproc/*/data*/*/XDS_ASCII.HKL')
        #hkl_list = glob.glob("*/merge*/blend*/cluster*/run_03/xscale.hkl")
        hkl_list = glob.glob("*/xscale.hkl") # for Hirata Script (lysozyme data analysis)
        #hkl_list = glob.glob("xscale.hkl") # for Hirata Script (Tsukazaki data analysis)
        #hkl_list += glob.glob('_kamoproc/CPS1276-??/data*/*/XDS_ASCII.HKL')

        hkl_list = sorted(hkl_list)

        # write oden_prep.csv with some default value
        oden_prep_csv = "%s/%s" % (outdir, csvout)

        with open(oden_prep_csv, "w") as fo:
            tmp_str = "prefix,hkl_file,cell_params,space_group,anom_atom,n_anom,n_try,phase_dmax,solv_cnt,n_dm,build_cycle,dmin\n"
            fo.write(tmp_str)

            for hklfile in hkl_list:
                print "HKL file: %s" % hklfile
                if hklfile.split("/")[-1] == "XDS_ASCII.HKL":
                    # read cell info from 'GXPARM.XDS'
                    gxparm = hklfile.replace("XDS_ASCII.HKL", "GXPARM.XDS")
                    if os.path.exists(gxparm):
                        cell_params = read_cellparams_from_gxparm(gxparm)
                    else:
                        cell_params=""
                    
                    print "Cell Const: %s" % cell_params 

                    xscalelp = hklfile.replace("XDS_ASCII.HKL", "XSCALE.LP")
                    # calc resolution from "XSCALE.LP"
                    resol_calculator = ResolutionFromXscaleHKL.ResolutionFromXscaleHKL(hklfile)
                    dmin = resol_calculator.get_resolution()
                    print "dmin: %f" % dmin
                    

                elif hklfile.split("/")[-1] == "xscale.hkl":
                    # read cell info from 'XSCALE.LP'
                    xscalelp = hklfile.replace("xscale.hkl", "XSCALE.LP")
                    if os.path.exists(xscalelp):
                        cell_params = read_cellparams_from_xscalelp(xscalelp)
                    else:
                        cell_params=""
                
                    print cell_params 

                    
                    # calc resolution from "XSCALE.LP"
                    #dmin = read_dmin_from_xscalelp(xscalelp)
                    try:
                        resol_calculator = ResolutionFromXscaleHKL.ResolutionFromXscaleHKL(hklfile)
                        dmin = resol_calculator.get_resolution()
                    except:
                        dmin = 99.99
                        resol_dat = hklfile.replace("xscale.hkl", ".resol_dat")
                        if os.path.exists(resol_dat):
                            dmin = float(open(resol_dat, "r").readline().strip())
                    print dmin
                """    
                # read dmin from 'decision.log'
                decision_log = hklfile.replace("XDS_ASCII.HKL", "decision.log")
                if os.path.exists(decision_log):
                    dmin = read_dmin_from_decisionLog(decision_log)
                else:
                    dmin = 99.9999
                """


                if dmin < dmin_threshold:
                    hkl_abs_path = os.path.abspath(hklfile)
                    tmp_str = ",%s,%s,,,,1000,25,,50,5,%.2f\n" % (hkl_abs_path, cell_params, dmin)

                    fo.write(tmp_str)


    def make_oden(self, csvin="oden_prep.csv",oden_dir="00.SAD", batch="sge", thorough=False):
        """ read 'oden_prep.csv' and make oden """
        oden_csv = csvin
        with open(oden_csv, "r") as f:
            params_lines = f.readlines()[1:]

            for params_line in params_lines:
                params = list(params_line.split(","))
                oden = ODEN.ODEN(params) 
                if thorough:
                    oden.run_shelx(oden_dir, batch, thorough=True)
                else:
                    oden.run_shelx(oden_dir, batch)
                
if __name__ == "__main__":
    nm = NabeMaster()
    #nm.prep_oden_csv()
    #nm.make_oden()
