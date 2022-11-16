#!/bin/bash
echo $1
each_file=`cat $1`

echo "" > all_cell.dat

for file in $each_file; do
grep "!UNIT_CELL_CONSTANTS=" $file >>  all_cell.dat
done
