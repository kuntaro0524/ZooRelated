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

n_phased=`grep "f2mtz:  Normal termination" merge*/00.SAD/f2mtz.log | wc -l`

SCRIPT=/isilon/users/admin45/admin45/2020B/staff_data/S-SAD_merge/Scripts/
yamtbx.python $SCRIPT/06_mapcc.py 

# Wait for end of file convertion
# Normally it waits for increment of finished processes over 60
# But this is not robust for waiting. Then limit is set to 'number of cycles'
# 5 mins for maximum: 5*60 = 300 sec -> 30 times
n_cycle=0
while [ 1 ]
do
n_finished=`find ./merge* -name 'mapcc.dat' | wc -l`
echo "finished " $n_finished
if [ $n_finished -ge $n_phased ] ; then
break
else
    echo "waiting: $n_cycle"
    let n_cycle++
    if [ $n_cycle -gt 30 ]; then
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
