#!/bin/bash
#WD=/isilon/users/admin45/admin45/2020B/staff_data/S-SAD_merge/merge_14A_01MGy/merge_blend_1.41S_14A_1MGy/blend_1.41A_final/cluster_0400/test_dir
#WD=$PWD
KDEV=/isilon/users/target/target/Staff/rooms/kuntaro/
SCRIPT=/isilon/users/admin45/admin45/2020B/staff_data/S-SAD_merge/Scripts/
MAT=/isilon/users/target/target/Staff/mat/nabe/oden/

# Original directory
ODIR=`pwd`

# Go to the processing directory
cd $WD/
echo "processing $WD"

# This process does not require 'waiting' because the process was already done in a command line.
# Then this is the suitable place to check the number of 'reflection files'
n_useful=`find $WD/merge* -name '.resol_dat' | wc -l`
echo "N_USEFUL= $n_useful"

# Re-run MR processes
SCRIPT=/isilon/users/admin45/admin45/2020B/staff_data/S-SAD_merge/Scripts/
yamtbx.python $SCRIPT/02_run_MR.py force_to_run

# Wait for end of file convertion
# Normally it waits for increment of finished processes over 60
# But this is not robust for waiting. Then limit is set to 'number of cycles'
# 15 mins for maximum: 15*60 = 900 sec -> 90 times
n_cycle=0
while [ 1 ]
do
n_finished=`grep "=========================== phenix.refine: finished ===========================" merge*/01.MR/mr_001.log | wc -l`
echo "finished " $n_finished
if [ $n_finished -ge $n_useful ] ; then
break
else
    echo "waiting cycle=$n_cycle done=$n_finished/$n_useful"
    let n_cycle++
    if [ $n_cycle -ge 90 ]; then
        echo "Limitation"
        break
    fi
    sleep 10.0
fi
done

