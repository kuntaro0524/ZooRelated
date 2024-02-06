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

# Re-calculate .resol_dat for "failed cases"
# Before re-calculation
n_before=`grep FAILED merge*/.resol_dat | wc -l`
# Resolution calculation -> store infromation to .resol_dat in each processing directory
yamtbx.python $KDEV/rd11/calc_resol_from_xscale_mp.py xscale.hkl
# After re-calculation
n_after=`grep FAILED merge*/.resol_dat | wc -l`

# This process does not require 'waiting' because the process was already done in a command line.
# Then this is the suitable place to check the number of 'reflection files'
n_useful=`find $WD/merge* -name '.resol_dat' | wc -l`
echo "N_USEFUL= $n_useful"

paths=`find $WD/merge*/ -name '01.MR'`
for path in $paths; do
check_file=$path/mr_001.pdb
if [ ! -e $check_file ]; then
# This cannot re-write 'refine.com' then resolution limit cannot be changed!!
#qsub $path/refine.com
yamtbx.python $SCRIPT/02_run_MR.py
fi
done

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

# Additional waiting for the residuals
echo "Waiting for safety margin. 60 seconds"
sleep 60.0

# A maximum number of clusters
max_num_mapcc=`$WD/00.SAD/ssad*mtz | wc -l`

# Map cc calculation (from oden_prep.csv)
SCRIPT=/isilon/users/admin45/admin45/2020B/staff_data/S-SAD_merge/Scripts/
yamtbx.python $SCRIPT/06_mapcc.py 

# Wait for end of file convertion
# Normally it waits for increment of finished processes over 60
# But this is not robust for waiting. Then limit is set to 'number of cycles'
# 5 mins for maximum: 5*60 = 300 sec -> 30 times
n_cycle=0
while [ 1 ]
do
n_finished=`find . -name 'mapcc.dat' | wc -l`
echo "finished " $n_finished
if [ $n_finished -ge $max_num_mapcc ] ; then
break
else
    echo "waiting cycle=$n_cycle done=$n_finished/$n_useful"
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
