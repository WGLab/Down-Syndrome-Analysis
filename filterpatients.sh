# filter ids on
mkdir -p filters
ls /mnt/isilon/wang_lab/mengge/project/DownSymdrome/control_heart_pat > filters/heartpats
ls /mnt/isilon/wang_lab/shared/datasets/DownSyndromeData/pat_22q > filters/22qpats
ls /mnt/isilon/wang_lab/shared/datasets/DownSyndromeData/ds_selected_hpo_data > filters/dspats
# mengge's control patients for asd
ls /mnt/isilon/wang_lab/mengge/project/autism_notes/nonpsy_nonasd_notes | grep -v -f filters/dspats -f filters/22qpats -f filters/heartpats > /mnt/isilon/wang_lab/jim/Down-Syndrome-Clustering/controls
cat filters/dspats | grep -v -f $DSDIR/filters/22qpats -f $DSDIR/controls > tmp; mv tmp filters/dspats
find dsdata/hpo/ -size 0 -type f -exec rm {} +
find controldata/hpo/ -size 0 -type f -exec rm {} +
