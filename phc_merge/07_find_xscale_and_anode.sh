#!/bin/bash
source ~/phenix/phenix-1.21-5207/phenix_env.sh 
ROOTDIR=/staff/bl32xu/Staff/kuntaro/171101-PH/_kamoproc_dials/merge_scripts/merge_10deg_re/ccc_1.1A_framecc_b+B/
SCRIPTS=$ROOTDIR/scripts/

SYMM="I23"

# $PROCPATHに存在する
xscale_files=`find . -name 'xscale.hkl'`

for xscale_file in $xscale_files; do

# file existing path -> PROCPATH
data_path="${xscale_file%/*}/"
PROCPATH=${data_path}/ccp4/

# ccp4_path?~A? .resol ?~A~L?~A~B?~B~J or ?~B??~B??~B??~A~L0?~B~H?~B~J大?~A~M?~A~D?| ??~P~H?~A??~A??~_?~L
if [ -s $PROCPATH/.resol ]; then
# RESOLUTION?~B~R?~U??~@??~A??~A~W?~A??~O~V?~W
RESOL=`cat $PROCPATH/.resol`

# 環境変数を引き継ぎつつ、refine_template.comを実行
# backgroundで実行し、48つのジョブが終了するまで待つ

python $SCRIPTS/07_anode_all.py $data_path $SYMM $RESOL

fi


done
