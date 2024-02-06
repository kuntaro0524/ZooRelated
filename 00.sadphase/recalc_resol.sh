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

# Before re-calculation
n_before=`grep FAILED merge*/.resol_dat | wc -l`

# Resolution calculation -> store infromation to .resol_dat in each processing directory
yamtbx.python $KDEV/rd11/calc_resol_from_xscale_mp.py xscale.hkl

# After re-calculation
n_after=`grep FAILED merge*/.resol_dat | wc -l`

echo "BEFORE: $n_before AFTER: $n_after"

cd $ODIR/
