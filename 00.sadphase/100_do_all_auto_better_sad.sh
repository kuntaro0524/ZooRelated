#!/bin/bash
while read filepath
do
WD=$filepath sh /isilon/users/admin45/admin45/2020B/staff_data/S-SAD_merge/Scripts/do_phase_only_better.sh
done < $1
