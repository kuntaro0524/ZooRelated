#!/bin/bash

files=`find . -name 'XSCALE.LP'`
pwd=`pwd`

for file in $files;do
proc_dir=`echo $file | sed -e 's/XSCALE.LP//'`
echo "Processing directory:" $proc_dir

cd $proc_dir/
/isilon/kunpy/kpython /isilon/kunpy/summarize_stats/make_xscale_stats_csv.py XSCALE.LP xscale.csv
cd $pwd/

done
