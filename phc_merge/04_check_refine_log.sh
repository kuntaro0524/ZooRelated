#!/bin/bash

dirs=`find . -name 'xscale.hkl'`

for dir in $dirs; do
dpath="${dir%/*}/"
cpath=$dpath/ccp4/
if [ -e $cpath/refine_001.log ]; then
	echo $cpath OK
else
	echo $cpath NG
	cat $cpath/.resol
fi
done
