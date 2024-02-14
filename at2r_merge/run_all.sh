#!/bin/bash
ROOTDIR=/media/kuntaro/KBU-004/180522-180628_AsadaAT2R/merge_dials/merge_auto/merge_ccc_3.0S_at2r/cc_3.18A_final

SYMM="C2221"
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
envsubst < refine_template.com | bash &

# ccp4_pathに .resol がないか、サイズが0
else
    echo "Skip $xscale_file"
    continue
fi

# 8つのジョブが終了するまで待つ
echo $count
if ((count % 48 == 0)); then
    wait
fi

done
