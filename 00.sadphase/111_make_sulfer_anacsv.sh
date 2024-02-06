#!/bin/bash
SCRIPT="/isilon/users/admin45/admin45/2020B/staff_data/S-SAD_merge/Scripts/"

#sad_list="00.SAD 02.SAD_DM20"
sad_list="02.SAD_DM20"

while read filepath
do

echo "FILEPATH=" $filepath
cd $filepath/
cwd=$PWD

merge_dirs=`ls | grep merge`

for merge_dir in $merge_dirs; do
echo "Doing " $merge_dir
echo "PWD=" $PWD
cd $merge_dir/

for PHASE_DIR in $sad_list; do

tmppath="$filepath/$merge_dir"
is_okay=`grep success $PHASE_DIR/.ANODE | wc -l`

if [ $is_okay -ge 1 ];then
echo "Making anomalous data csv"
echo $PWD

qsub -pe par 1 -j y -cwd -S /bin/bash -V -N "make_sulfer_pd" <<+
LANG=C date
yamtbx.python $SCRIPT/make_sulfer_anomalous.py $PHASE_DIR
+

fi

done
echo "Up to " $cwd
cd $cwd/

# Wait for a bit
sleep 15.0

done


done < $1
