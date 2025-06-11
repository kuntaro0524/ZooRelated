#!/bin/bash
#source ~/phenix/phenix-1.21-5207/phenix_env.sh 
ROOTDIR=/media/kuntaro/KBU-004/240115-PH_matome/_kamoproc_dials/merge_scripts/merge_10deg_re/ccc_1.1A_framecc_b+B/
SCRIPTS=$ROOTDIR/scripts/

SYMM="I23"
MODEL_PDB=$ROOTDIR/Models/model.pdb
REFMTZ=$ROOTDIR/Models/free.mtz
NRESIDUES=250

count=0

# $PROCPATHに存在する
xscale_files=`find $ROOTDIR -name 'xscale.hkl'`

for xscale_file in $xscale_files; do

# file existing path -> PROCPATH
data_path="${xscale_file%/*}/"
PROCPATH=${data_path}/ccp4/
ORIMTZ=$PROCPATH/xscale.mtz

# RESOLUTIONを数値として取得
RESOL=`cat $PROCPATH/.resol`

echo "#################"
echo $PROCPATH
echo "#################"

# wilson plot
wilson  hklin $ORIMTZ << EOF-wil > $PROCPATH/wilson_re.log
resolution 40.0 $RESOL
# original scaling
#rscale 4.0 $RESOL
rscale 6.0 $RESOL
wilson observed
nresidues   $NRESIDUES
LABIN  FP=F SIGFP=SIGF
EOF-wil

done
