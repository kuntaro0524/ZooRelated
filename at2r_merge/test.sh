#!/bin/bash
ROOTDIR=/media/kuntaro/KBU-004/180522-180628_AsadaAT2R/merge_dials/merge_auto/merge_ccc_3.0S_at2r/cc_3.18A_final
PROCPATH=$ROOTDIR/cluster_3196/run_03/ccp4.test/
ORIMTZ=$PROCPATH/xscale.mtz
SYMM="C2221"
FREEMTZ=$PROCPATH/free_common.mtz
MODEL_PDB=$ROOTDIR/Models/model.pdb
REFMTZ=$ROOTDIR/Models/free.mtz

# $PROCPATH/.resolが存在しない場合には処理をしない
if [ ! -s $PROCPATH/.resol ]; then
    echo "No resol.log"
    exit 1
else
RESOL=`cat $PROCPATH/.resol`
fi
echo $RESOL

# 環境変数を引き継ぎつつ、refine_template.comを実行
export ORIMTZ PROCPATH SYMM FREEMTZ MODEL_PDB REFMTZ RESOL
envsubst < refine_template.com | bash