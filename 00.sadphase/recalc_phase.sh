#!/bin/bash
#WD=/isilon/users/admin45/admin45/2020B/staff_data/S-SAD_merge/merge_14A_01MGy/merge_blend_1.41S_14A_1MGy/blend_1.41A_final/cluster_0400/test_dir
KDEV=/isilon/users/target/target/Staff/rooms/kuntaro/
SCRIPT=/isilon/users/admin45/admin45/2020B/staff_data/S-SAD_merge/Scripts/
MAT=/isilon/users/target/target/Staff/mat/nabe/oden/

# Original directory
ODIR=`pwd`

# Go to the processing directory
cd $WD/

echo "processing $WD"

# number of good datsets to be anlyzed.
# This process does not require 'waiting' because the process was already done in a command line.
# Then this is the suitable place to check the number of 'reflection files'
n_useful=`ls ./merge*/.resol_dat | wc -l`

# Cleaning previous logs.
\rm -Rf merge*/$PHASE_DIR/f2mtz.log

# phs2mtz for mapcc calculation (from oden_prep.csv)
SCRIPT=/isilon/users/admin45/admin45/2020B/staff_data/S-SAD_merge/Scripts/
yamtbx.python $SCRIPT/04_phs2mtz.py $PHASE_DIR

# Wait for end of file convertion
# Normally it waits for increment of finished processes over 60
# But this is not robust for waiting. Then limit is set to 'number of cycles'
# 5 mins for maximum: 5*60 = 300 sec -> 30 times
n_cycle=0
while [ 1 ]
do
n_finished=`grep "f2mtz:  Normal termination" merge*/$PHASE_DIR/f2mtz.log | wc -l`
echo "finished " $n_finished
if [ $n_finished -ge $n_useful ] ; then
break
else
    echo "waiting cycle=$n_cycle done=$n_finished"
    let n_cycle++
    if [ $n_cycle -gt 18 ]; then
        echo "Limitation"
        n_phased=$n_finished
        break
    fi
    sleep 10.0
fi
done


# Clear the previous runs
\rm -Rf merge*/$PHASE_DIR/mapcc.dat

# Map cc calculation (from oden_prep.csv)
SCRIPT=/isilon/users/admin45/admin45/2020B/staff_data/S-SAD_merge/Scripts/
yamtbx.python $SCRIPT/06_mapcc.py $PHASE_DIR

# Wait for end of file convertion
# Normally it waits for increment of finished processes over 60
# But this is not robust for waiting. Then limit is set to 'number of cycles'
# 5 mins for maximum: 5*60 = 300 sec -> 30 times
n_cycle=0
while [ 1 ]
do
n_finished=`ls merge*/$PHASE_DIR/mapcc.dat | wc -l`
echo "finished " $n_finished
if [ $n_finished -ge $n_phased ] ; then
break
else
    echo "waiting cycle=$n_cycle done=$n_finished"
    let n_cycle++
    if [ $n_cycle -gt 20 ]; then
        echo "Limitation"
        break
    fi
    sleep 10.0
fi
done

# Summarize results
SCRIPT=/isilon/users/admin45/admin45/2020B/staff_data/S-SAD_merge/Scripts/
yamtbx.python $SCRIPT/07_summarize_phasing.py

cd $ODIR/
