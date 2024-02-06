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

# ccp4_pathに resol.log がないか、サイズが0でない場合のみ実行
if [ ! -s $ccp4_path/resol.log ]; then
    echo "Run $xscale_file"

yamtbx.python /opt/dials/dials-v1-14-13/modules/yamtbx/yamtbx/dataproc/auto/command_line/decide_resolution_cutoff.py \
$xscale_file > $ccp4_path/resol.log &

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
