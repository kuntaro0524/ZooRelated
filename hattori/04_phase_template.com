#!/bin/bash
export ROOT=/staff/bl32xu/Staff/kuntaro/181010-hattori/_kamoproc/merge_ccc_2.0S_Se/cc_2.31A_final/cluster_1323/run_03.re
export PHAD=$ROOT/phase/
#SBATCH -o $PHAD/output.%a.out # STDOUT
#SBATCH -o $PHAD/error.%a.out # STDOUT

CELL="57.44    83.29    98.62  90.000  90.000  90.000"
SYMM="C222"

cd $PHAD/

ln -s $ROOT/xscale.hkl ./xscale.hkl

~/shelx/shelxc sad <<EOF > ./shelxc.log
SAD ./xscale.hkl
CELL $CELL
SPAG $SYMM
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
symmetry $SYMM
CELL $CELL
labout H K L FP FOM PHIB SIGFP
CTYPOUT H H H F W P Q
END

# inverse
f2mtz hklin ./sad_i.phs hklout ./phs_i.mtz > ./f2mtz_i.log << END
symmetry $SYMM
CELL $CELL
labout H K L FP FOM PHIB SIGFP
CTYPOUT H H H F W P Q
END

# Map CC
# original
phenix.get_cc_mtz_pdb ./phs.mtz ./../ccp4/refine_001.pdb | tee ./cc_orig.log
# inverse
phenix.get_cc_mtz_pdb ./phs_i.mtz ./../ccp4/refine_001.pdb | tee ./cc_inv.log
