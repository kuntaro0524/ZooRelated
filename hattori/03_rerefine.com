#!/bin/bash
export PHENIX_OVERWRITE_ALL=true
phenix.refine $FREEMTZ $PROCPATH/jelly.pdb  \
miller_array.labels.name="IMEAN" \
xray_data.low_resolution=25.0 xray_data.high_resolution=$RESOL \
output.prefix=$PROCPATH/refine 
