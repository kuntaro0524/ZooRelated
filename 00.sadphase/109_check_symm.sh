#!/bin/bash

sad_list="00.SAD 02.SAD_DM20"

while read filepath
do

WD=$filepath

for PHASE_DIR in $sad_list; do
n_wrong=`grep C2221 $WD/merge*/$PHASE_DIR/phs2mtz.com | wc -l`
n_good=`grep P43212 $WD/merge*/$PHASE_DIR/phs2mtz.com | wc -l`
echo $WD/$PHASE_DIR/ "GOOD=" $n_good "NG=" $n_wrong
done


done < $1
