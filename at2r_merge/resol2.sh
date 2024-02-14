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

# $ccp4_path/resol.log　が存在しない、もしくはあるけどサイズが０の場合はcontinue
if [ ! -s $ccp4_path/resol.log ]; then
    echo "Run $xscale_file"
fi

# $ccp4_path/resol.log から最終的な分解能を取得する
# 抜き出す行はこれ
# Suggested cutoff= 3.53 A (CC1/2= 0.5134)
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

done