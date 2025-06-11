import os,sys
import time

# run_?? directory
# rootdir: the path for xscale.hkl from KAMO merge
rootdir=sys.argv[1]
symstr=sys.argv[2]
resol=float(sys.argv[3])

# absolute path
abspath=os.path.abspath(rootdir)

# ccp4 directory
ccp4_path=os.path.join(abspath,"ccp4")

# anode path
anode_path=os.path.join(abspath,"anode")

# make anode_path directory
if os.path.exists(anode_path)==False:
    os.makedirs(anode_path)

# XSCALE.INP
xscaleinp_path=os.path.join(abspath,"XSCALE.INP")

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
export ANOD=$ROOT/anode/
#SBATCH -o $ANOD/output.%a.out # STDOUT
#SBATCH -o $ANOD/error.%a.out # STDOUT

cd $ANOD/

ln -s $ROOT/xscale.hkl ./xscale.hkl

~/shelx/shelxc sad <<EOF > ./shelxc.log
SAD ./xscale.hkl
MAXM 2000000000
CELL {cellstr}
SHEL 999 {resol}
SPAG {symstr}
FIND 9
NTRY 1000
EOF

sleep 5

# ANODE
# copy a model as sad.pdb
cp {ccp4_path}/refine_001.pdb ./sad.pdb

/opt/xtal/ccp4-7.1/bin/anode sad > anode.log

""" 

    ofile=open(comfile,"w").write("%s"%comstr)

writeCom(f"{anode_path}/phase.sh")
time.sleep(10.0)
os.system(f"chmod 744 {anode_path}/phase.sh")
os.system(f"sbatch {anode_path}/phase.sh")
