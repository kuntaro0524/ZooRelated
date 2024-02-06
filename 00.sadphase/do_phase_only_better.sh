#!/bin/bash
#WD=/isilon/users/admin45/admin45/2020B/staff_data/S-SAD_merge/merge_14A_01MGy/merge_blend_1.41S_14A_1MGy/blend_1.41A_final/cluster_0400/test_dir
KDEV=/isilon/users/target/target/Staff/rooms/kuntaro/
SCRIPT=/isilon/users/admin45/admin45/2020B/staff_data/S-SAD_merge/Scripts/
MAT=/isilon/users/target/target/Staff/mat/nabe/oden/

# Original directory
ODIR=`pwd`

# SAD directory setting & DM cycle
sad_dir="03.SAD_honki"
dm_cycle=20

# Go to the processing directory
cd $WD/

echo "processing $WD"

# This process does not require 'waiting' because the process was already done in a command line.
# Then this is the suitable place to check the number of 'reflection files'
n_useful=`find ./merge* -name '.resol_dat' | wc -l`

cp -Rf oden_prep.csv oden_prep.csv.save

# Preparing the NABE (generate oden_prep.csv)
yamtbx.python $SCRIPT/prep_oden.py
# Save the file
cp -Rf oden_prep.csv oden_prep.csv_with_blank
# Add required information to oden_prep.csv for Lysozyme SSAD
build_cycle=3
yamtbx.python $SCRIPT/10_fill_odencsv.py ./oden_prep.csv_with_blank $dm_cycle $build_cycle

# Run ODEN  (SHELX C/D/E) (from oden_prep.csv)
# Processing directory name : 03.SAD_honki for 100 DM cycle
# 
yamtbx.python $SCRIPT/make_oden.py $sad_dir thorough_dm

# Wait for end of SHELXE
# Normally it waits for increment of finished processes over 60
# But this is not robust for waiting. Then limit is set to 'number of cycles'
# 20 mins for maximum: 20*60 = 1200 sec -> 120 times
n_cycle=0
while [ 1 ]
do
n_finished=`grep "SHELXE finished" merge*/$sad_dir/shelxe_i.log | wc -l`
echo "finished " $n_finished
if [ $n_finished -ge $n_useful ] ; then
break
else
    echo "waiting cycle=$n_cycle done=$n_finished"
    let n_cycle++
    if [ $n_cycle -ge 120 ]; then
        echo "Limitation"
        break
    fi
    sleep 10.0
fi
done

# phs2mtz for mapcc calculation (from oden_prep.csv)
SCRIPT=/isilon/users/admin45/admin45/2020B/staff_data/S-SAD_merge/Scripts/
yamtbx.python $SCRIPT/04_phs2mtz.py $sad_dir

# Wait for end of file convertion
# Normally it waits for increment of finished processes over 60
# But this is not robust for waiting. Then limit is set to 'number of cycles'
# 5 mins for maximum: 4*60 = 200 sec -> 30 times
n_cycle=0
while [ 1 ]
do
n_finished=`grep "f2mtz:  Normal termination" merge*/$sad_dir/f2mtz.log | wc -l`
echo "finished " $n_finished
if [ $n_finished -ge $n_useful ] ; then
break
else
    echo "waiting cycle=$n_cycle done=$n_finished"
    let n_cycle++
    if [ $n_cycle -gt 20 ]; then
        echo "Limitation"
        n_phased=$n_finished
        break
    fi
    sleep 10.0
fi
done

# Map cc calculation (from oden_prep.csv)
SCRIPT=/isilon/users/admin45/admin45/2020B/staff_data/S-SAD_merge/Scripts/
yamtbx.python $SCRIPT/06_mapcc.py $sad_dir

# Wait for end of file convertion
# Normally it waits for increment of finished processes over 60
# But this is not robust for waiting. Then limit is set to 'number of cycles'
n_cycle=0
while [ 1 ]
do
n_finished=`ls merge*/$sad_dir/mapcc.dat | wc -l`
echo "finished " $n_finished
if [ $n_finished -ge $n_phased ] ; then
break
else
    echo "waiting cycle=$n_cycle done=$n_finished"
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
yamtbx.python $SCRIPT/07_summarize_phasing.py $sad_dir

cd $ODIR/
