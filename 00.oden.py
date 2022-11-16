import sys
import os
import glob
import numpy
#sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")
#sys.path.append("/isilon/BL32XU/BLsoft/PPPP/Libs")
from Libs import DirectoryProc # currently not used
from Libs import ComRefine
from Libs import ResolutionFromXscaleHKL # currently not used
from Libs import AnaXSCALE

###----------Setting----------###
# Sequence file
seq = "/isilon/BL32XU/BLsoft/PPPP/30.RD11/lys.pir"
# Model PDB
model="/isilon/BL32XU/BLsoft/PPPP/30.RD11/lys_model.pdb"

# path_string
path_string = 'cluster_*/run_*/xscale.hkl'

print(path_string)

# Default parameters for SHELX C/D/E
prefix = "shihoya"
symm = "C2"
dmax = 25
dmin = 2.90 # set default dmin value
n_shelxd = 1000
n_site = 25
anom_atom = "I"
solcon = 0.50
n_dm = 50
n_residue = 430
ncycle_automodel = 5

# Directory name
SAD_dir = "00.SAD"


###---------------------------------###


# NOTE: AnaXSCALE sometimes output message below
#       "resolution limit would be beyond the max resolution in this XSCALE.LP"
#       therefore, cell info will be read from 'XSCALE.LP' and dmin from 'xds2mtz.log'
# TODO?: read dmin from 'XSCALE.LP' or 'cluster_summary.dat'???


### util ###
def read_resol_from_xds2mtzLog(xds2mtzLog):

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
 

### 

class ODEN():
# 1. Make oden_proc.lst
    def prep_proc_lst(self):
        lst = glob.glob(path_string)
        lst = sorted(lst)
        fo = open('oden_proc.lst', 'w')
        tmp_str = ''
        for path in lst:
            tmp_str += '%s\n' % path
        fo.write(tmp_str)
        fo.close()

# 2. read cell & dmin info 

    def run_proc_from_lst(self):
        # read 'oden_proc.lst' (output from prep_proc_lst())
        oden_proc_lst = 'oden_proc.lst'
        xscale_path_lst = []
        proc_path_lst = []

        lines = open(oden_proc_lst, 'r').readlines()
        for xscale_path in lines:
            proc_path = '/'.join(xscale_path.split('/')[:-1])
            proc_path_lst.append(proc_path)
    
            xscale_path_lst.append(xscale_path)
    
        xscale_path_lst = sorted(xscale_path_lst)
        proc_path_lst = sorted(proc_path_lst)


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

            # SAD process
            sad_proc_path = os.path.join(proc_path, SAD_dir)
            if not os.path.exists(sad_proc_path):
                os.makedirs(sad_proc_path)
                
            xscale_hkl_path = proc_path + '/xscale.hkl'
            xscale_hkl_rel_path = os.path.relpath(xscale_hkl_path, sad_proc_path)
            comf = ComRefine.ComRefine(sad_proc_path)
            comname = comf.solve_sad(symm, prefix, dmax, n_shelxd, n_site, anom_atom, solcon, n_dm, n_residue, xscale_hkl_rel_path, dmin, seq, ncycle_automodel, cells)
            os.system("chmod a+x %s" % comname)
            os.system("qsub %s" % comname)
            

if __name__ == '__main__':
    oden = ODEN()
    oden.prep_proc_lst()
    oden.run_proc_from_lst()
