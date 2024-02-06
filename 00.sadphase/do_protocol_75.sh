#!/bin/bash
#WD=$PWD
KDEV=/isilon/users/target/target/Staff/rooms/kuntaro/
SCRIPT=/isilon/users/admin45/admin45/2020B/staff_data/S-SAD_merge/Scripts/
MAT=/isilon/users/target/target/Staff/mat/nabe/oden/

# Original directory
ODIR=`pwd`

# Go to the processing directory
cd $WD/

echo "processing $WD"

# Run XDS by using XDS.INP 
yamtbx.python $KDEV/rd11/random_xscale_from_xscaleinp_75.py XSCALE.INP

# Wait for 5 minutes in maximum
n_cycle=0
while [ 1 ]
do
n_finished=`ls merge075*/ | grep ccp4 | wc -l`
echo "finished " $n_finished
if [ $n_finished -ge 10 ] ; then
break
else
    echo "waiting cycle=$n_cycle done=$n_finished"
    let n_cycle++
    if [ $n_cycle -ge 30 ]; then
        echo "Limitation"
        break
    fi
    sleep 10.0
fi
done

# Resolution calculation -> store infromation to .resol_dat in each processing directory
yamtbx.python $KDEV/rd11/calc_resol_from_xscale_mp.py xscale.hkl

# This process does not require 'waiting' because the process was already done in a command line.
# Then this is the suitable place to check the number of 'reflection files'
n_useful=`ls ./merge075*/.resol_dat | wc -l`

cp -Rf oden_prep.csv oden_prep.csv.bak

# Preparing the NABE (generate oden_prep.csv)
yamtbx.python $SCRIPT/prep_oden.py
# Save the file
cp -Rf oden_prep.csv oden_prep.csv_with_blank
# Add required information to oden_prep.csv for Lysozyme SSAD
yamtbx.python $SCRIPT/10_fill_odencsv.py ./oden_prep.csv_with_blank

# Run ODEN  (SHELX C/D/E) (from oden_prep.csv)
yamtbx.python $SCRIPT/make_oden.py

# Wait for end of SHELXE
# Normally it waits for increment of finished processes over 60
# But this is not robust for waiting. Then limit is set to 'number of cycles'
# 10 mins for maximum: 10*60 = 600 sec -> 60 times
n_cycle=0
while [ 1 ]
do
n_finished=`grep "SHELXE finished" merge075*/00.SAD/shelxe_i.log | wc -l`
echo "finished " $n_finished
if [ $n_finished -ge $n_useful ] ; then
break
else
    echo "waiting cycle=$n_cycle done=$n_finished"
    let n_cycle++
    if [ $n_cycle -ge 60 ]; then
        echo "Limitation"
        break
    fi
    sleep 10.0
fi
done

# Molecular replacement for all  (from oden_prep.csv)
SCRIPT=/isilon/users/admin45/admin45/2020B/staff_data/S-SAD_merge/Scripts/
yamtbx.python $SCRIPT/02_run_MR.py 

# Run phenix.merging_statistics (from oden_prep.csv)
SCRIPT=/isilon/users/admin45/admin45/2020B/staff_data/S-SAD_merge/Scripts/
yamtbx.python $SCRIPT/03_run_phenixmerging.py

# Wait for end of file convertion
# Normally it waits for increment of finished processes over 60
# But this is not robust for waiting. Then limit is set to 'number of cycles'
# 20 mins for maximum: 20*60 = 1200 sec -> 120 times
n_cycle=0
while [ 1 ]
do
n_finished=`grep "=========================== phenix.refine: finished ===========================" merge075*/01.MR/mr_001.log | wc -l`
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

# Additional waiting for the residuals
sleep 60.0

# phs2mtz for mapcc calculation (from oden_prep.csv)
SCRIPT=/isilon/users/admin45/admin45/2020B/staff_data/S-SAD_merge/Scripts/
yamtbx.python $SCRIPT/04_phs2mtz.py

# Wait for end of file convertion
# Normally it waits for increment of finished processes over 60
# But this is not robust for waiting. Then limit is set to 'number of cycles'
# 5 mins for maximum: 5*60 = 300 sec -> 30 times
n_cycle=0
while [ 1 ]
do
n_finished=`grep "f2mtz:  Normal termination" merge075*/00.SAD/f2mtz.log | wc -l`
echo "finished " $n_finished
if [ $n_finished -ge $n_useful ] ; then
break
else
    echo "waiting cycle=$n_cycle done=$n_finished"
    let n_cycle++
    if [ $n_cycle -gt 30 ]; then
        echo "Limitation"
        n_phased=$n_finished
        break
    fi
    sleep 10.0
fi
done

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
n_finished=`ls merge075*/00.SAD/mapcc.dat | wc -l`
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
yamtbx.python $SCRIPT/07_summarize_phasing.py

cd $ODIR/
