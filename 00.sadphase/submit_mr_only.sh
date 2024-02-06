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

# Remaking a 'oden_prep.csv' to rewrite resolution limit from .resol_dat 
yamtbx.python $MAT/prep_oden.py
# Save the file
cp -Rf oden_prep.csv oden_prep.csv_with_blank

# Add required information to oden_prep.csv for Lysozyme SSAD
yamtbx.python $SCRIPT/10_fill_odencsv.py ./oden_prep.csv_with_blank

# Re-run MR processes
SCRIPT=/isilon/users/admin45/admin45/2020B/staff_data/S-SAD_merge/Scripts/
yamtbx.python $SCRIPT/02_run_MR.py

cd $ODIR
