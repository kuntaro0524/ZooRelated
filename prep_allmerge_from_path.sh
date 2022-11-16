#!/bin/bash

echo "/oys/xtal/cctbx/snapshots/upstream/build/bin/yamtbx.python /oys/xtal/cctbx/snapshots/upstream/modules/yamtbx/dataproc/auto/command_line/multi_prep_merging.py \\" > prep.com
echo "workdir=merge_all01 \\" >> prep.com

path1='/isilon/users/target/target/yonekura/220210/_kamo_30deg/'
path2='../../../220125/_kamo_30deg/'

xds_list1=`find $path1 -name 'XDS_ASCII.HKL'`
xds_list2=`find $path2 -name 'XDS_ASCII.HKL'`

for xds_file1 in $xds_list1;
do
pathname=`echo $xds_file1 | sed -e 's/XDS_ASCII.HKL//g'` 
echo "xdsdir=$pathname \\" >> prep.com
done

for xds_file2 in $xds_list2;
do
pathname=`echo $xds_file2 | sed -e 's/XDS_ASCII.HKL//g'` >> prep.com
echo "xdsdir=$pathname \\" >> prep.com
done
