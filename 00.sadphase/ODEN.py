# ODEN (@BL32XU)
# 2020/12/08 HM

import sys
import os
import glob
import numpy
#sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")
#sys.path.append("/isilon/BL32XU/BLsoft/PPPP/Libs")
#sys.path.append("/isilon/users/target/target/Staff/mat/dev/")
#sys.path.append("/isilon/users/target/target/Staff/mat/dev/Libs")
#sys.path.append("/isilon/users/target/target/Staff/mat/nabe/oden")
sys.path.append("/isilon/users/target/target/Staff/rooms/kuntaro/Libs")

import DirectoryProc # currently not used
import ComRefine
import ResolutionFromXscaleHKL # currently not used
import NabeMaster
#import AnaXSCALE

###----------Setting----------###
# dataset with lower resolution than dmin_threshold will not processed
dmin_threshold = 6.0
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
        a = float(line.split()[1])
        b = float(line.split()[2])
        c = float(line.split()[3])
        alpha = float(line.split()[4])
        beta = float(line.split()[5])
        gamma = float(line.split()[6])
        cell_params = "%8.3f %8.3f %8.3f %8.3f %8.3f %8.3f" % (a, b, c, alpha, beta, gamma) 

    return cell_params 

def read_dmin_from_decisionLog(decision_log):
    """ read dmin from 'decision.log' """
    dmin = 99.9999
    with open(decision_log, "r") as f:
        lines = f.readlines()
        for line in lines:
            if "Re-scale at" in line:
                dmin = float(line.split()[-2])

    return dmin

### 


# ODEN class
class ODEN():
    def __init__(self, params):
        self.params = params

        self.prefix = params[0]
        self.hklin = params[1]
        self.cell_params = params[2] #Attention: cell_params (float list) will be given as string in shelx_sad func
        self.sg = params[3]
        self.anom_atom = params[4]
        self.n_anom = int(params[5])
        self.n_try = int(params[6])
        self.phase_dmax = float(params[7])
        self.solv_cnt = float(params[8])
        self.n_dm = int(params[9])
        self.build_cycle = int(params[10])
        self.dmin = float(params[11])

    def run_shelx(self, oden_wdir="00.SAD", batch="sge", thorough=False):
        # K.Hirata modified. 2020/12/17
        # TODO: 'os.system' should be replaced with 'subprocess.call(command, shell=True)'
        if "XDS_ASCII.HKL" in self.hklin:
            proc_dir = self.hklin.replace("/XDS_ASCII.HKL", "")
        elif "xscale.hkl" in self.hklin:
            proc_dir = self.hklin.replace("/xscale.hkl", "")

        oden_dir = "%s/%s" % (proc_dir, oden_wdir)
        if not os.path.exists(oden_dir):
            os.makedirs(oden_dir)

        hkl_rel_path = os.path.relpath(self.hklin, oden_dir)
        com = ComRefine.ComRefine(oden_dir)

        if thorough:
            comfile = com.shelx_sad_thorough(self.prefix, hkl_rel_path, self.cell_params, self.sg, self.anom_atom, self.n_anom, self.n_try, self.phase_dmax, self.solv_cnt, self.n_dm, self.build_cycle, self.dmin, batch)
        else:
            comfile = com.shelx_sad(self.prefix, hkl_rel_path, self.cell_params, self.sg, self.anom_atom, self.n_anom, self.n_try, self.phase_dmax, self.solv_cnt, self.n_dm, self.build_cycle, self.dmin, batch)

        os.system("chmod a+x %s" % comfile)
        if batch == "sge":
            os.system("qsub %s" % comfile) 
        elif batch == "slurm":
            os.system("sbatch %s" % comfile)

    def show_hklin(self):
        print self.hklin

    def show_prefix(self):
        print self.prefix

if __name__ == "__main__":
    nm = NabeMaster.NabeMaster()
    #nm.prep_oden_csv()
    nm.make_oden()

"""

        for proc_path in proc_path_lst:
            # read cell info from XSCALE.LP
            xscalelp_path = proc_path + '/XSCALE.LP'
            ac = AnaXSCALE.AnaXSCALE(xscalelp_path)
            cells = ac.getCellParm()
            #print xscalelp_path
            #print "cell info: ", cells
    
            # Read resolution from xsd2mtz.log
            xds2mtz_path = proc_path + '/ccp4/xds2mtz.log'
            dmin = read_resol_from_xds2mtzLog(xds2mtz_path)
            #print xds2mtz_path
            #print 'Resolution: ', dmin
            
            
            #comrefine=ComRefine.ComRefine(proc_path)
            #comname=comrefine.refine_normal(xscale_list,symm,dmin,model,prefix)
            #os.system("qsub %s" % comname)

            # SAD process
            sad_proc_path = os.path.join(proc_path, SAD_dir)
            if not os.path.exists(sad_proc_path):
                os.makedirs(sad_proc_path)
                
            xscale_hkl_path = proc_path + '/xscale.hkl'
            xscale_hkl_rel_path = os.path.relpath(xscale_hkl_path, sad_proc_path)
            comf = ComRefine.ComRefine(sad_proc_path)
            comname = comf.shelx_sad(symm, prefix, xscale_hkl_rel_path, cells, sg, anom_atom, n_anom, n_shelxd, phase_dmax, solv_cnt, n_dm, build_cycle, dmin)
            os.system("chmod a+x %s" % comname)
            os.system("qsub %s" % comname)

"""
