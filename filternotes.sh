#! /bin/bash
#SBATCH --export=ALL
#SBATCH --ntasks=1
#SBATCH --mem=4G
#SBATCH --time=12:00:00
#SBATCH -o slurmfilter/slurm-%j.out
set -x
START=$1
END=$2
DSDIR=$3
FILTERDIR=$4

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
