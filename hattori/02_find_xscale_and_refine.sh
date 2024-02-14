#!/bin/bash
source ~/phenix/phenix-1.21-5207/phenix_env.sh 
ROOTDIR=/staff/bl32xu/Staff/kuntaro/181010-hattori/_kamoproc/merge_ccc_2.0S_Se/cc_2.31A_final/
SCRIPTS=$ROOTDIR/scripts/

SYMM="C222"
MODEL_PDB=$ROOTDIR/Models/model.pdb
REFMTZ=$ROOTDIR/Models/free.mtz

count=0

# $PROCPATHに存在する
xscale_files=`find $ROOTDIR -name 'xscale.hkl'`

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

# 環境変数を引き継ぎつつ、refine_template.comを実行
# backgroundで実行し、48つのジョブが終了するまで待つ
export ORIMTZ PROCPATH SYMM FREEMTZ MODEL_PDB REFMTZ RESOL
#envsubst < $SCRIPTS/02_refine_template.com | bash &
envsubst < $SCRIPTS/03_rerefine.com | bash &

# ccp4_pathに .resol がないか、サイズが0
else
    echo "Skip $xscale_file"
    continue
fi

# 8つのジョブが終了するまで待つ
echo $count
if ((count % 128 == 0)); then
    wait
fi

done
