#!/bin/bash
SCRIPT="/isilon/users/admin45/admin45/2020B/staff_data/S-SAD_merge/Scripts/"

#sad_list="00.SAD 02.SAD_DM20"
sad_list="02.SAD_DM20"

while read filepath
do

echo "FILEPATH=" $filepath
cd $filepath/
cwd=$PWD

cd $filepath/ 

for PHASE_DIR in $sad_list; do

qsub -pe par 1 -j y -cwd -S /bin/bash -V -N "make_sulfer_pd" <<+
LANG=C date
yamtbx.python $SCRIPT/make_sulfer_anomalous.py $PHASE_DIR
+

done
echo "Up to " $cwd
cd $cwd/

done < $1
