#!/bin/bash
WD=$PWD
n_done=`grep "=========================== phenix.refine: finished ===========================" $WD/merge*/01.MR/mr_001.log | wc -l`
echo $n_done
