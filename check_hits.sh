#!/bin/bash
sch_files=`find . -name 'multi.sch'`

for file in $sch_files; do
nhits=`grep "gonio" $file | wc -l`
echo $file $nhits
done
