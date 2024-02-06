#!/bin/bash

testfunc() {
n_cycle=1
while [ 1 ]
do
n_finished=`grep "f2mtz:  Normal termination" merge*/00.SAD/f2mtz.log | wc -l`
echo "finished " $n_finished
if [ $n_finished -gt 60 ] ; then
break
else
    echo "waiting"
    sleep 5.0
    let n_cycle++
    if [ $n_cycle -gt 5 ]; then
        echo "Limitation"
        break
    fi
fi
done

}

LIMIT=30

testfunc
