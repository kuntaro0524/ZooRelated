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
	echo $ccp4_path
else

if [ -f $ccp4_path/molrep.pdb ]; then

if [ -f $ccp4_path/refine_001.pdb ]; then
	continue
else
	echo "SOMETHING WRONG: $ccp4_path"
fi
fi
fi

done
