#!/bin/bash
KPATH=/home/kuntaro/kundev/kunpy/
export KPATH
CPU_COUNT=48
count=0
xscale_files=`find . -name 'xscale.hkl'`

for xscale_file in $xscale_files; do
# file existing path
existing_path="${xscale_file%/*}/"
echo $existing_path
ccp4_path=${existing_path}/ccp4/
echo $ccp4_path

# ccp4 dicretoryがあるかどうか
# パスが存在しない
if [ ! -d $ccp4_path ]; then
	echo "CCP4 path cannot be found"
#xds2mtz.py $xscale_file &

# あるとき
else
# ファイルが存在するか
if [ -f $ccp4_path/xscale.mtz ]; then
	echo "xscale.mtz cannot be found"
#xds2mtz.py $xscale_file &
else
echo "Skipping!"
fi
fi

((count=count+1))

echo $count
if ((count % CPU_COUNT == 0)); then
        wait # 48つのジョブが終了するまで待つ
fi

done
