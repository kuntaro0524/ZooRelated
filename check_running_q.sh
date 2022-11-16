#!/bin/bash

while [ true ]
do 
nqstat=`qstat | wc -l`

echo "NUMBER OF QUE=" $nqstat

sleep 1.0

if [ $nqstat == 0 ];then 
 break
fi
done
