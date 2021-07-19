DSDIR=/mnt/isilon/wang_lab/jim/Down-Syndrome-Clustering
python notehash.py -p $DSDIR/controldata/hpo -d $DSDIR/../patientnotes.tsv -o $DSDIR/controlages.tsv
python notehash.py -p $DSDIR/dsdata/hpo -d $DSDIR/../patientnotes.tsv -o $DSDIR/dsages.tsv
python notehash.py -p $DSDIR/dsfilterdata/hpo -d $DSDIR/../patientnotes.tsv -o $DSDIR/dsfilterages.tsv
python calc.py -d $DSDIR/controldata/hpo -o $DSDIR/control -a $DSDIR/controlages.tsv
python calc.py -d $DSDIR/dsdata/hpo -o $DSDIR/ds -f $DSDIR/control.tsv -a $DSDIR/dsages.tsv
python calc.py -d $DSDIR/dsfilterdata/hpo -o $DSDIR/dsfilter -f $DSDIR/control.tsv -a $DSDIR/dsfilterages.tsv
python plots.py -t $DSDIR/ds.tsv $DSDIR/control.tsv -a $DSDIR/dstermage.tsv -n 4094 7845 -o $DSDIR/dsodds $DSDIR/dsages
python plots.py -t $DSDIR/dsprop.tsv $DSDIR/control.tsv -a $DSDIR/dsproptermage.tsv -n 4094 7845 -o $DSDIR/dspropodds $DSDIR/dspropages
python plots.py -t $DSDIR/dsfilter.tsv $DSDIR/control.tsv -a $DSDIR/dsfiltertermage.tsv -n 3553 7845 -o $DSDIR/dsfilterodds $DSDIR/dsfilterages
