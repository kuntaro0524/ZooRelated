#!/bin/bash
dirs=`ls | grep cluster_`

for dir in $dirs; do
count_run=`ls $dir/run*/XSCALE.LP | wc -l`
if [ $count_run  -eq 3 ];then
	continue
else
	echo "$dir BAD"
fi

done
