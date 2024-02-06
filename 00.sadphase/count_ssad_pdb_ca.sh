#!/bin/bash

sad_dir='00.SAD'

dlist=`ls $WD | grep merge100`

#echo $dlist
#merge_10A_01MGy/merge_blend_1.04S_10A_1MGy/*final/cluster_0484/run_03/merge*/02.SAD_DM20/

for d in $dlist; do

testfile="$WD/$d/$sad_dir/ssad.pdb"

if [ -e $testfile ]; then
oscore=`grep CA $WD/$d/02.*/ssad.pdb | wc -l`
fi

testfile="$WD/$d/02.SAD_DM20/ssad_i.pdb"
if [ -e $testfile ]; then
iscore=`grep CA $WD/$d/02.*/ssad_i.pdb | wc -l`
fi

echo $WD $oscore $iscore

done
