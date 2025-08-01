#!/bin/bash
ROOTDIR=/staff/bl32xu/Staff/kuntaro/171101-PH/_kamoproc_dials/merge_scripts/merge_10deg_re/ccc_1.1A_framecc_b+B/
SCRIPT_DIR=$ROOTDIR/scripts/

SYMM="I23"

count=0

# $PROCPATHに存在する
#xscale_files=`find $ROOTDIR -name 'xscale.hkl'`
xscale_files=`find . -name 'xscale.hkl' | grep -v anode`

for xscale_file in $xscale_files; do

# file existing path -> PROCPATH
data_path="${xscale_file%/*}/"
PROCPATH=${data_path}/ccp4/
ORIMTZ=$PROCPATH/xscale.mtz
FREEMTZ=$PROCPATH/free_common.mtz

# ccp4_pathに .resol があり or サイズが0より大きい場合のみ実行
if [ ! -s $ccp4_path/.resol ]; then
    echo "Run $xscale_file"
fi

# RESOLUTIONを数値として取得
RESOL=1.33
echo "RESOL=$RESOL"

# 環境変数を引き継ぎつつ、refine_template.comを実行
# backgroundで実行し、48つのジョブが終了するまで待つ
export ORIMTZ PROCPATH SYMM FREEMTZ MODEL_PDB REFMTZ RESOL
sbatch $SCRIPT_DIR/17_refine_template_fixed.com 

done
