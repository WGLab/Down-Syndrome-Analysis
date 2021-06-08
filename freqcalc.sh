DSDIR=/mnt/isilon/wang_lab/jim/Down-Syndrome-Clustering
python notehash.py -p $DSDIR/dsdata/hpo -d $DSDIR/../patientnotes.tsv -o $DSDIR/dsages.tsv
python calc.py -d $DSDIR/controldata/hpo -o $DSDIR/control -a $DSDIR/controlages.tsv
python calc.py -d $DSDIR/dsdata/hpo -o $DSDIR/ds -f $DSDIR/control.tsv -a $DSDIR/dsages.tsv
python plots.py -t $DSDIR/ds.tsv $DSDIR/control.tsv -a $DSDIR/dstermage.tsv -n 4209 7845 -o $DSDIR/dsodds $DSDIR/dsages
