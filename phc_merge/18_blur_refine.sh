#!/bin/bash
kpython /staff/Common/kunpy-dev/command_lines/clustering_analysis/b_blur_comfiles.py Matome/2410251100.csv

files=`find . -name 'blur*.com'`

for file in $files; do
chmod 744 $file
sbatch $file
done
