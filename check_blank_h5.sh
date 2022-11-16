#!/bin/bash
datadirs=`find . -name 'data0?' -maxdepth 2`

for dd in $datadirs; do

master_files=`find $dd -name '*master.h5'`

for master_file in $master_files; do
yamtbx.python ~/Staff/rooms/kuntaro/h5/ManH5.py $master_file >> check_blank_h5.log
done

done
