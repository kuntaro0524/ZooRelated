#!/bin/bash
KPATH=/home/kuntaro/kundev/kunpy/
export KPATH
CPU_COUNT=48
count=0
xscale_files=`find . -name 'xscale.hkl' | grep -v 'anode'`

for xscale_file in $xscale_files; do
# file existing path
existing_path="${xscale_file%/*}/"
ccp4_path=${existing_path}/ccp4/

# ccp4 dicretoryがあるかどうか
# パスが存在しない
if [ ! -d $ccp4_path ]; then
	echo "EEEEEEEEEEEEEEEEEEEEEEEEEE"
	echo "CCP4 path cannot be found"
	echo $ccp4_path
	echo "EEEEEEEEEEEEEEEEEEEEEEEEEE"
#xds2mtz.py $xscale_file &

# あるとき
else

# ファイルが存在するか
if [ -f $ccp4_path/refine_001.pdb ]; then
	continue
else 
	echo "REFINE_NG: $ccp4_path"
fi

if
[ -f $ccp4_path/water_001.pdb ]; then
        continue
else
	echo "water NG!: $ccp4_path"
fi
fi

done
