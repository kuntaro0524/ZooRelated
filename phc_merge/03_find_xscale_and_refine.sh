#!/bin/bash
ROOTDIR=/staff/bl32xu/Staff/kuntaro/171101-PH/_kamoproc_dials/merge_scripts/merge_10deg_re/ccc_1.1A_framecc_b+B/
SCRIPT_DIR=$ROOTDIR/scripts/

SYMM="I23"
MODEL_PDB=$ROOTDIR/Models/model.pdb
REFMTZ=$ROOTDIR/Models/free.mtz

count=0

# $PROCPATHに存在する
#xscale_files=`find $ROOTDIR -name 'xscale.hkl'`
xscale_files=`find . -name 'xscale.hkl'`

for xscale_file in $xscale_files; do

# file existing path -> PROCPATH
data_path="${xscale_file%/*}/"
PROCPATH=${data_path}/ccp4/
ORIMTZ=$PROCPATH/xscale.mtz
FREEMTZ=$PROCPATH/free_common.mtz

# ccp4_pathに .resol があり or サイズが0より大きい場合のみ実行
if [ ! -s $ccp4_path/.resol ]; then
    echo "Run $xscale_file"

((count=count+1))

# RESOLUTIONを数値として取得
RESOL=`cat $PROCPATH/.resol`
echo "RESOL=$RESOL"

# 環境変数を引き継ぎつつ、refine_template.comを実行
# backgroundで実行し、48つのジョブが終了するまで待つ
export ORIMTZ PROCPATH SYMM FREEMTZ MODEL_PDB REFMTZ RESOL
envsubst < $SCRIPT_DIR/03_refine_template.com | bash &

# ccp4_pathに .resol がないか、サイズが0
else
    echo "Skip $xscale_file"
    continue
fi

# 8つのジョブが終了するまで待つ
echo $count
if ((count % 100 == 0)); then
    wait
fi

done
