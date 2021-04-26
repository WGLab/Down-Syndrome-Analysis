DSDIR=/mnt/isilon/wang_lab/jim/Down-Syndrome-Clustering
NOTEDIR=/mnt/isilon/wang_lab/mengge/project/autism_notes/nonpsy_nonasd_notes
bash $DSDIR/filterpatients.sh
cd $NOTEDIR
python $DSDIR/runnlp/pathwalk.py $NOTEDIR | grep -f $DSDIR/controls > $DSDIR/notepaths
cd -
len=$(wc -l $DSDIR/notepaths | cut -f 1 -d " ")
for i in $(seq 1001 1000 $len); do
    a=$len-i+1; b=1000
    ((++ct))
    j=$(( a < b ? a : b ))
    j=$(bc <<< "$i + $j - 1")
    echo $i $j
    sbatch runnlp/metasubmit.sh $i $j $NOTEDIR "control" # can run sbatch --wait
done
