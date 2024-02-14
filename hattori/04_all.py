import os,sys
import time

# run_?? directory
rootdir=sys.argv[1]
symstr=sys.argv[2]
resol=float(sys.argv[3])

# absolute path
abspath=os.path.abspath(rootdir)

# ccp4 directory
ccp4_path=os.path.join(abspath,"ccp4")

# phasing path
phase_path=os.path.join(abspath,"phase")

# make phase_path directory
if os.path.exists(phase_path)==False:
    os.makedirs(phase_path)

# XSCALE.INP
xscaleinp_path=os.path.join(abspath,"XSCALE.INP")

print(ccp4_path)
print(phase_path)
print(xscaleinp_path)

lines=open(xscaleinp_path,"r").readlines()

for line in lines:
    if "UNIT_CELL" in line:
        cols=line.split()
        cellstr="%8s %8s %8s %8s %8s %8s"% (cols[1],cols[2],cols[3],cols[4],cols[5],cols[6])

def writeCom(comfile):
    #rootdir="staff/bl32xu/Staff/kuntaro/181010-hattori/_kamoproc/merge_ccc_2.0S_Se/cc_2.31A_final/cluster_1323/run_03.re"
    #cellstr="'57.44    83.29    98.62  90.000  90.000  90.000'"
    #symstr="C222"
    
    comstr= f"""#!/bin/bash
export ROOT={abspath}
export PHAD=$ROOT/phase/
#SBATCH -o $PHAD/output.%a.out # STDOUT
#SBATCH -o $PHAD/error.%a.out # STDOUT

cd $PHAD/

ln -s $ROOT/xscale.hkl ./xscale.hkl

~/shelx/shelxc sad <<EOF > ./shelxc.log
SAD ./xscale.hkl
CELL {cellstr}
SHEL 999 {resol}
SPAG {symstr}
FIND 9
NTRY 1000
EOF

~/shelx/shelxd sad_fa > ./shelxd.log
~/shelx/shelxe sad sad_fa -h -s0.6 -m200 -a3 >  ./shelxe.log
~/shelx/shelxe sad sad_fa -h -s0.6 -m200 -i -a3 > ./shelxe_i.log

sleep 5

# phs2mtz 
# original
f2mtz hklin ./sad.phs hklout ./phs.mtz > ./f2mtz.log << END
symmetry {symstr}
CELL {cellstr}
labout H K L FP FOM PHIB SIGFP
CTYPOUT H H H F W P Q
END

# inverse
f2mtz hklin ./sad_i.phs hklout ./phs_i.mtz > ./f2mtz_i.log << END
symmetry {symstr}
CELL {cellstr}
labout H K L FP FOM PHIB SIGFP
CTYPOUT H H H F W P Q
END

# Map CC
# original
phenix.get_cc_mtz_pdb ./phs.mtz {ccp4_path}/refine_001.pdb | tee ./cc_orig.log
# inverse
phenix.get_cc_mtz_pdb ./phs_i.mtz {ccp4_path}/refine_001.pdb | tee ./cc_inv.log
""" 

    ofile=open(comfile,"w").write("%s"%comstr)

writeCom(f"{phase_path}/phase.sh")
time.sleep(10.0)
os.system(f"chmod 744 {phase_path}/phase.sh")
os.system(f"sbatch {phase_path}/phase.sh")
