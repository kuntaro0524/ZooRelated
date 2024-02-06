#!/bin/bash

SCRIPT="/isilon/users/admin45/admin45/2020B/staff_data/S-SAD_merge/Scripts/"
sad_list="00.SAD 02.SAD_DM20"
cwd=$PWD

while read filepath
do

for PHASE_DIR in $sad_list; do

cd $filepath/

yamtbx.python $SCRIPT/11_run_anode.py $PHASE_DIR
sleep 10
done

cd $cwd/

done < $1
