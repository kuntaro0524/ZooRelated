#!/bin/bash
PHENIX_OVERWRITE_ALL=true

# 必要な環境変数
#ORIMTZ=/media/kuntaro/KBU-004/180522-180628_AsadaAT2R/merge_dials/merge_auto/merge_ccc_3.0S_at2r/cc_3.18A_final/cluster_2748/run_01/ccp4/xscale.mtz
#PROCPATH=/isilon/users/target/target/AutoUsers/180621/abe/_kamoproc/blend_A3-2/blend_1.50A_final/cluster_0190/run_03/ccp4/
#SYMM="C2221"
#REFMTZ=/isilon/users/target/target/AutoUsers/180621/abe/_kamoproc/blend_A3-2/blend_1.50A_final/cluster_0190/run_03/ccp4/free.mtz
#FREEMTZ=/isilon/users/target/target/AutoUsers/180621/abe/_kamoproc/blend_A3-2/blend_1.50A_final/cluster_0190/run_03/ccp4/free_common.mtz
#MODELPDB=/isilon/users/target/target/AutoUsers/180621/abe/_kamoproc/blend_A3-2/blend_1.50A_final/cluster_0190/run_03/ccp4/jelly.pdb
#RESOL=1.8

reindex hklin $ORIMTZ hklout $PROCPATH/reindex.mtz <<EOF > $PROCPATH/reindex.log 
symm $SYMM
end
EOF

ls -latr $PROCPATH/reindex.mtz

copy_free_R_flag.py -r $REFMTZ $PROCPATH/reindex.mtz -o $FREEMTZ

# MOLREP: molecular replacement
molrep HKLIN $FREEMTZ \
       MODEL $MODEL_PDB \
       PATH_OUT $PROCPATH <<stop > $PROCPATH/molrep.log
NMON   1
NP     3
NPT    10
_END
stop

# Wait for generation of molrep.pdb
sleep 5.0

echo "Starting REFMAC5"
refmac5 \
hklin $FREEMTZ \
hklout $PROCPATH/refmac.mtz \
xyzin $PROCPATH/molrep.pdb \
xyzout $PROCPATH/jelly.pdb << eof> $PROCPATH/refmac.log
resol 25 $RESOL
refi     type REST     resi MLKF     meth CGMAT     bref ISOT 
ncyc 50
scal     type SIMP     LSSC     ANISO     EXPE
solvent YES
weight     AUTO
LABIN FP=F SIGFP=SIGF FREE=FreeR_flag
RIDG DIST SIGM 0.02
END
eof

phenix.refine $FREEMTZ $PROCPATH/jelly.pdb  \
xray_data.labels="IMEAN,SIGIMEAN"\
xray_data.low_resolution=25.0 xray_data.high_resolution=$RESOL \
output.prefix=$PROCPATH/refine_ 