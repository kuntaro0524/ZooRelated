#!/bin/bash
while read filepath
do
WD=$filepath sh /isilon/users/admin45/admin45/2020B/staff_data/S-SAD_merge/Scripts/do_protocol.sh
done < $1
