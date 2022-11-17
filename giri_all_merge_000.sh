
#!/bin/sh
# 2 dmin values should be evaluated.
# Merging process will be applied to datasets with better thresholds
# of completeness/redundancy.
# When a "wrongly" shorter dmin(higher resolution) is set here, 
# completeness value becomes very low for bad datasets and this 
# process does not reach to merging/scaling stages.
dmin_start_1=1.31

# dmin for CC calculation
# this should be set for each dmin values
# Very simple calculation (modify 'cc_margin' if you need)
# cc_dmin = dmin_start + cc_margin
cc_dmin=2.81

# Minimum normal/anomalous completeness
# Normal completeness
min_cmpl=10
# Anomalous completeness
min_acmpl=10

# Minimum anomalous redundancy
min_aredun=2.0

# Maximum number of cluster
max_clusters=10

# Memory disk
use_ramdisk=true

# Number of cores
nproc=8

kamo.auto_multi_merge   filtering.choice=cell filtering.cell_iqr_scale=2.5   csv="/isilon/users/target/target/AutoUsers/221108/nakayama/merge_inputs/giri_all_merge_000.csv"   workdir=/isilon/users/target/target/AutoUsers/221108/nakayama/_kamo_30deg/   prefix=merge_blend_${dmin_start_1}S_   cell_method=reindex   reject_method=framecc+lpstats   rejection.lpstats.stats=em.b+bfactor   merge.max_clusters=${max_clusters}   merge.d_min_start=$dmin_start_1   merge.clustering=blend   merge.blend.min_cmpl=$min_cmpl   merge.blend.min_acmpl=$min_acmpl   merge.blend.min_aredun=$min_aredun   xscale.degrees_per_batch=1.0   xscale.reference=bmin   batch.engine=sge   merge.batch.engine=sge   merge.batch.par_run=merging   merge.nproc=$nproc   merge.batch.nproc_each=$nproc   xscale.use_tmpdir_if_available=${use_ramdisk}   batch.sge_pe_name=all &

kamo.auto_multi_merge   filtering.choice=cell filtering.cell_iqr_scale=2.5   csv="/isilon/users/target/target/AutoUsers/221108/nakayama/merge_inputs/giri_all_merge_000.csv"   workdir=/isilon/users/target/target/AutoUsers/221108/nakayama/_kamo_30deg/   prefix=merge_ccc_${dmin_start_1}S_   cell_method=reindex   reject_method=framecc+lpstats   rejection.lpstats.stats=em.b+bfactor   merge.max_clusters=${max_clusters}   xscale.reference=bmin   merge.d_min_start=$dmin_start_1   merge.clustering=cc   merge.cc_clustering.d_min=${cc_dmin}   merge.cc_clustering.min_cmpl=$min_cmpl   merge.cc_clustering.min_acmpl=$min_acmpl   merge.cc_clustering.min_aredun=$min_aredun   xscale.degrees_per_batch=1.0   batch.engine=sge   merge.batch.engine=sge   merge.batch.par_run=merging   merge.nproc=$nproc   merge.batch.nproc_each=$nproc   xscale.use_tmpdir_if_available=${use_ramdisk}   batch.sge_pe_name=all &