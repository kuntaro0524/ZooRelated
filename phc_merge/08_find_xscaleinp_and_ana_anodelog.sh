#!/bin/bash
ROOTPATH=/staff/bl32xu/Staff/kuntaro/171101-PH/_kamoproc_dials/merge_scripts/merge_10deg_re/ccc_1.1A_framecc_b+B
SCPATH=$ROOTPATH/scripts/

xscale_files=`find . -name 'XSCALE.INP'`

for xscale_file in $xscale_files; do

# file existing path -> PROCPATH
data_path="${xscale_file%/*}/"
PROCPATH=${data_path}/anode/

# Check if the anode.log exists
if [ -s $PROCPATH/anode.log ]; then
python $SCPATH/08_ana_anodelog.py $PROCPATH/anode.log
else
	echo "No file"
fi

done
