#!/bin/bash
export KPATH=~/Staff/kuntaro/kundev/

CPU_COUNT=48
count=0

xscale_files=`find . -name 'xscale.hkl'`

for xscale_file in $xscale_files; do
# file existing path
existing_path="${xscale_file%/*}/"
echo $existing_path
ccp4_path=${existing_path}/ccp4/
echo $ccp4_path

# ccp4_pathに .resol がないか、サイズが0でない場合のみ実行
if [ ! -s $ccp4_path/.resol ]; then
    echo "Run $xscale_file"

$KPATH/k3python $KPATH/command_lines/decide_resolution.py $existing_path/XSCALE.LP $ccp4_path  &

((count=count+1))

else
    echo "Skip $xscale_file"
    continue
fi

echo $count
if ((count % CPU_COUNT == 0)); then
        wait # 48つのジョブが終了するまで待つ
fi

done
