# before running metamap (may have to replace with your OWN metamap servers)
#/mnt/isilon/wang_lab/jim/public_mm/bin/skrmedpostctl start
#/mnt/isilon/wang_lab/jim/public_mm/bin/wsdserverctl start
DSDIR=/mnt/isilon/wang_lab/jim/Down-Syndrome-Clustering
#NOTEDIR=/mnt/isilon/wang_lab/mengge/project/DownSymdrome/ds_notes
NOTEDIR=/mnt/isilon/wang_lab/jim/Down-Syndrome-Clustering/filternotes
cd $NOTEDIR
# make sure 22q and controls are filtered
python $DSDIR/runnlp/pathwalk.py $NOTEDIR | grep -v -f $DSDIR/filters/22qpats -f $DSDIR/controls > $DSDIR/notepaths
cd -
#len=$(wc -l $DSDIR/dspaths | cut -f 1 -d " ")
len=$(wc -l $DSDIR/notepaths | cut -f 1 -d " ")
for i in $(seq 1001 1000 $len); do
    a=$len-i+1; b=1000
    ((++ct))
    j=$(( a < b ? a : b ))
    j=$(bc <<< "$i + $j - 1")
    echo $i $j
    sbatch runnlp/metasubmit.sh $i $j $NOTEDIR "dsfilter" # can run sbatch --wait
done
