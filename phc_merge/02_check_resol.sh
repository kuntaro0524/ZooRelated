#!/bin/bash
KPATH=/staff/bl32xu/Staff/kuntaro/171101-PH/_kamoproc_dials/merge_scripts/merge_10deg_re/ccc_1.1A_framecc_b+B/scripts/

while read -r xscale_file; do

# file existing path
existing_path="${xscale_file%/*}/"
#echo $existing_path
ccp4_path=${existing_path}/ccp4/
#echo $ccp4_path
python $KPATH/02_check_resol.py $ccp4_path/.resol
done < <(find . -name 'XSCALE.LP')
