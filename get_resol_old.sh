#!/bin/bash
xscale_files=`find . -name 'xscale.hkl'`

for xscale_file in $xscale_files; do
existing_path="${xscale_file%/*}/"
echo $existing_path

# yamtbxの分解能判定スクリプトを走らせる
line=`yamtbx.python /opt/dials/dials-v1-14-13/modules/yamtbx/yamtbx/dataproc/auto/command_line/decide_resolution_cutoff.py $xscale_file | grep "Suggested cutoff="` 

if [ -z "$line" ]; then
    echo -999.999 > $existing_path/.resol
else
    value=$(echo $line | grep -oP 'cutoff= \K[0-9.]+')
    if [ -z "$value" ]; then
        echo "数値が見つかりませんでした。"
    else
        echo $value > $existing_path/.resol
    fi
fi

done
