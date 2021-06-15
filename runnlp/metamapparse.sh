set -x
NOTEDIR=$1
FILE=$2
DSDIR=$3
NAME=$4
FILEN=$(echo "$FILE" | sed "s/.*\///")
DIR=$(echo "$FILE" | sed 's:/[^/]*$::')
mkdir -p $DSDIR/"$NAME"notes_ascii/$DIR
mkdir -p $DSDIR/"$NAME"data/raw/$DIR
mkdir -p $DSDIR/"$NAME"data/terms/$DIR
mkdir -p $DSDIR/"$NAME"data/hpo/$DIR
chmod -R 774 $DSDIR/"$NAME"notes_ascii/$DIR
chmod -R 774 $DSDIR/"$NAME"data/raw/$DIR
chmod -R 774 $DSDIR/"$NAME"data/terms/$DIR
chmod -R 774 $DSDIR/"$NAME"data/hpo/$DIR
#mkdir -p $DSDIR/dsnotes_ascii/$DIR
#mkdir -p $DSDIR/dsdata/raw/$DIR
#mkdir -p $DSDIR/dsdata/terms/$DIR
#mkdir -p $DSDIR/dsdata/hpo/$DIR
#chmod -R 774 $DSDIR/dsnotes_ascii/$DIR
#chmod -R 774 $DSDIR/dsdata/raw/$DIR
#chmod -R 774 $DSDIR/dsdata/terms/$DIR
#chmod -R 774 $DSDIR/dsdata/hpo/$DIR
#cat /etc/hostname >&2
cd $NOTEDIR
java -jar /mnt/isilon/wang_lab/jim/replace_utf8.jar $FILE > $DSDIR/"$NAME"notes_ascii/$DIR/$FILEN
metamap -y -@ reslnvvhpc062.research.chop.edu -S reslnvvhpc062.research.chop.edu -R HPO -V USAbase --JSONf 2 $DSDIR/"$NAME"notes_ascii/$DIR/$FILEN $DSDIR/"$NAME"data/raw/$DIR/$FILEN
python $DSDIR/runnlp/metarepeat.py $DSDIR/"$NAME"data/raw/$DIR/$FILEN $DSDIR/"$NAME"data/terms/$DIR/$FILEN
python $DSDIR/runnlp/hporepeat.py $DSDIR/"$NAME"data/terms/$DIR/$FILEN $DSDIR/"$NAME"data/hpo/$DIR/$FILEN $DSDIR/umlshpo.json
