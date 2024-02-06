#!/bin/bash
mapccn=`ls $WD/merge*/00.SAD/mapcc.dat | wc -l`
pdbn=`ls $WD/merge*/01.MR/mr_001.pdb | wc -l`
xdsn=`ls $WD/merge*/xscale.hkl | wc -l`
mtzn=`find $WD/merge* -name 'xscale.mtz' | wc -l`
resn=`find $WD/merge* -name '.resol_dat'|wc -l`
shelxn=`ls $WD/merge*/00.SAD/shelxe_i.log | wc -l`
csvn=`ls $WD/merge*/00.SAD/*csv | wc -l`
resol_failed=`grep FAIL $WD/merge*/.resol_dat |wc -l`

echo "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
echo $WD
echo XDS:$xdsn MTZ:$mtzn RESOL:$resn REFINE:$pdbn SHELXE:$shelxn MAPCC:$mapccn PHASE_CSV:$csvn FAILED_RESOL:$resol_failed

paths=`find $WD/merge*/ -name '01.MR'`

for path in $paths; do
check_file=$path/mr_001.pdb
if [ ! -e $check_file ]; then
echo "#############"
grep "failed" $path/jelly.log
grep HOST $path/refine.com.o*
#echo $path
fi
done
