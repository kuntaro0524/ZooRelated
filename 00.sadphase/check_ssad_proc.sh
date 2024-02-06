#!/bin/bash
while [ 1 ]
do
n_proc=`qstat | grep shelx.com | wc -l`
if [ $n_proc -eq 0 ] ; then
break
else
    echo "MADA"
fi
done
