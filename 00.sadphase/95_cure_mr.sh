#!/bin/bash
while read filepath
do
WD=$filepath sh /isilon/users/admin45/admin45/2020B/staff_data/S-SAD_merge/Scripts/work_cure_mr.sh
done < $1
