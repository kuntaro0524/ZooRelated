#!/bin/bash
while read filepath
do
WD=$filepath
yamtbx.python /isilon/users/target/target/Staff/rooms/kuntaro/summarize_stats/make_xscale_pms_summary.py $WD
done < $1
