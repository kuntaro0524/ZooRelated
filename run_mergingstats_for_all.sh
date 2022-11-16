#!/bin/sh

files=`find . -name xscale.hkl`
pwd=`pwd`

for xscale_path in $files;do
echo "XSCALE_PATH",$xscale_path
proc_dir=`echo $xscale_path | sed -e 's/xscale.hkl//'`
echo "PROC_PATH", $proc_dir

cd $proc_dir
echo "Processing $xscale_path"

qsub -pe par 4-8 -j y -cwd -S /bin/bash -V -N phenix_merging_stats <<+
LANG=C date
echo "Host=\$HOSTNAME"
phenix.merging_statistics xscale.hkl > merging_stats.log
+

cd $pwd/

done

