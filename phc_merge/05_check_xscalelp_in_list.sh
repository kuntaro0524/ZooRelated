#!/bin/bash
KPATH=~/Staff/kuntaro/kundev/
export PYTHONPATH=~/Staff/kuntaro/kundev/Libs/
export KPATH

while read dir
do
ccpd=$dir/ccp4/
xscalelp_path=$dir/XSCALE.LP

#echo "Processing $line"
#$KPATH/k3python $KPATH/command_lines/decide_resolution.py $xscalelp_path $ccpd
echo "####### $xscalelp_path #######"
$KPATH/k3python ./scripts/get_xscale_summary.py $xscalelp_path


# $1 = a list file including 'worse' data path
# ex) one line like this
# ./cluster_11258/run_01/
done < $1
