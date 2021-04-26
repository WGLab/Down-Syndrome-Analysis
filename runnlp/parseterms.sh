set -x
NOTEDIR=$1
FILE=$2
DSDIR=$3
#FILEN=$(echo "$FILE" | sed "s/.*\///")
DIR=$(echo "$FILE" | sed 's:/[^/]*$::')
cd $NOTEDIR
#cat /etc/hostname >&2
mkdir -p $DSDIR/dsdata/raw/$DIR
mkdir -p $DSDIR/dsdata/terms/$DIR
mkdir -p $DSDIR/dsdata/hpo/$DIR
python $DSDIR/runnlp/metarepeat.py $DSDIR/dsdata/raw/$FILE $DSDIR/dsdata/terms/$FILE
python $DSDIR/runnlp/hporepeat.py $DSDIR/dsdata/terms/$FILE $DSDIR/dsdata/hpo/$FILE $DSDIR/umlshpo.json
