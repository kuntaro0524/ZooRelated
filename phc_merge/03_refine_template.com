#!/bin/bash
source ~/phenix/phenix-1.21-5207/phenix_env.sh 
PHENIX_OVERWRITE_ALL=true

reindex hklin $ORIMTZ hklout $PROCPATH/reindex.mtz <<EOF > $PROCPATH/reindex.log 
symm $SYMM
end
EOF

sleep 5.0

#copy_free_R_flag.py -r $REFMTZ $PROCPATH/reindex.mtz -o $FREEMTZ
/opt/dials/dials-v1-14-13/modules/yamtbx/yamtbx/dataproc/command_line/copy_free_R_flag.py -r $REFMTZ $PROCPATH/reindex.mtz -o $FREEMTZ


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
output.prefix=$PROCPATH/refine
