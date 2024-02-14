#!/bin/bash

while true; do
log=`date`
log2=`squeue  | wc -l`
echo $log $log2
sleep 60
done

