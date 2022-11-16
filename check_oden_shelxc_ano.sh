#!/bin/bash

shelxc_logs=`find . -name 'shelxc.log'`

for logfile in $shelxc_logs; do
value=`grep "d..sig" $logfile | grep -v "zero"`
echo $logfile $value
done
