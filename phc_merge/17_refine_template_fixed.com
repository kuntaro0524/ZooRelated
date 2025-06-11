#!/bin/bash
source ~/phenix/phenix-1.21-5207/phenix_env.sh 
PHENIX_OVERWRITE_ALL=true

phenix.refine $FREEMTZ $PROCPATH/refine_001.pdb  \
xray_data.labels="IMEAN,SIGIMEAN"\
xray_data.low_resolution=25.0 xray_data.high_resolution=$RESOL \
output.prefix=$PROCPATH/fixed_resol ordered_solvent=true > $PROCPATH/phenix_fixed_resol.log
