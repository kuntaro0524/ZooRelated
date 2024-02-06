#!/bin/bash

#sad_list="00.SAD 02.SAD_DM20"
sad_list="03.SAD_honki"

while read filepath
do

for PHASE_DIR in $sad_list; do
PHASE_DIR=$PHASE_DIR WD=$filepath sh /isilon/users/admin45/admin45/2020B/staff_data/S-SAD_merge/Scripts/recalc_phase.sh
done

done < $1
