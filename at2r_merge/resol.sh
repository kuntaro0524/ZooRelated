#!/bin/bash
CPU_COUNT=48
count=0

xscale_files=`find . -name 'xscale.hkl'`

for xscale_file in $xscale_files; do
# file existing path
existing_path="${xscale_file%/*}/"
echo $existing_path
ccp4_path=${existing_path}/ccp4/
echo $ccp4_path
(
yamtbx.python /opt/dials/dials-v1-14-13/modules/yamtbx/yamtbx/dataproc/auto/command_line/decide_resolution_cutoff.py $xscale_file > $ccp4_path/resol.log

line=`grep "Suggested cutoff=" $ccp4_path/resol.log`

if [ -z "$line" ]; then
    echo 10.0 > $ccp4_path/.resol
else
    value=$(echo $line | grep -oP 'cutoff= \K[0-9.]+')
    if [ -z "$value" ]; then
        echo 10.0 > $ccp4_path/.resol
    else
        echo $value > $ccp4_path/.resol
    fi
fi

    echo "$file"

    ((count=count+1))
) &
echo "Processing $xscale_file"


echo $count
if ((count % CPU_COUNT == 0)); then
        wait # 8つのジョブが終了するまで待つ
    fi

done
