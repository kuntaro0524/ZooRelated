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

# This process does not require 'waiting' because the process was already done in a command line.
# Then this is the suitable place to check the number of 'reflection files'
n_useful=`find ./merge* -name '.resol_dat' | wc -l`

# Summarize results
SCRIPT=/isilon/users/admin45/admin45/2020B/staff_data/S-SAD_merge/Scripts/
yamtbx.python $SCRIPT/07_summarize_phasing.py

cd $ODIR/
