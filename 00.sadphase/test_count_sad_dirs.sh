#!/bin/bash
cycle_100=`ls $WD/merge*/00.SAD/anode.log  | wc -l`
cycle_020=`ls $WD/merge*/02.SAD_DM20/anode.log  | wc -l`

echo $WD "CYCLE100=" $cycle_100 "CYCLE20=" $cycle_020
