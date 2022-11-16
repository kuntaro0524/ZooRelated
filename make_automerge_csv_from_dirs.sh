#!/bin/bash
curr_path=$PWD
name=$1
anomalous=$2

echo "topdir,name,anomalous" > merge.csv

#echo $curr_path
ls_list=`find $curr_path -name 'XDS_ASCII.HKL'`

for dir in $ls_list; do
proc_path=${dir%/*} 
#echo $proc_path
printf "%s,%s,%s\n" $proc_path $name $anomalous >> merge.csv
done
