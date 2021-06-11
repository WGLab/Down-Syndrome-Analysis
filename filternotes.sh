DSDIR=/mnt/isilon/wang_lab/jim/Down-Syndrome-Clustering
NOTEDIR=/mnt/isilon/wang_lab/jim/Down-Syndrome-Clustering/dsnotes_ascii
FILTERDIR=/mnt/isilon/wang_lab/jim/Down-Syndrome-Clustering/filternotes
mkdir -p $FILTERDIR
#python $DSDIR/runnlp/pathwalk.py $NOTEDIR > $DSDIR/dspaths
len=$(wc -l $DSDIR/dspaths | cut -f 1 -d " ")
START=1; END=$len
for i in $(seq $START 1 $END); do
    FILE=$(sed -n "$i"p $DSDIR/dspaths)
    DIR=$(echo "$FILE" | sed 's:/[^/]*$::' | sed 's/[^/]*\///g')
    FILTERFILE=$(echo "$FILE" | sed 's/[^/]*\///g')
    if grep -q "MRN" $FILE; then
        x=$(wc -c $FILE | awk '$1 >=3000')
        if [ ! -z "${x}" ]; then
            mkdir $FILTERDIR/$DIR
            cp $FILE "$FILTERDIR/$DIR/$FILTERFILE"
        fi
    fi
done
