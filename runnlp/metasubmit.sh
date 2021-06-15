#! /bin/bash
#
#SBATCH --export=ALL
#SBATCH --ntasks=1
#SBATCH --mem=4G
#SBATCH --time=12:00:00
#SBATCH -o slurmnew/slurm-%j.out
#--array=1-10000%1000
#-o slurm/slurm-%A_%a.out
set -x
START=$1
END=$2
NOTEDIR=$3
NAME=$4
#STOP=$(bc <<< "$END+1")

DSDIR=/mnt/isilon/wang_lab/jim/Down-Syndrome-Clustering
#for FILE in $DSDIR/28-pts-notes-20180821-rechecked-wkc/*; do
cd $NOTEDIR

for i in $(seq $START 1 $END); do
    #FILE=$(sed -n "$i"p $DSDIR/dspaths)
    FILE=$(sed -n "$i"p $DSDIR/notepaths)
    #FILE=$(sed -n "$SLURM_ARRAY_TASK_ID"p <(sed -n ''"$START"','"$END"'p;'"$STOP"'q' $DSDIR/notepaths))
    #FILE=$(sed -n "$SLURM_ARRAY_TASK_ID"p <(sed -n '10000,10100p;10101q' $DSDIR/notepaths))
    echo "$FILE"
    #srun -N1 -n1 -c1 --exclusive bash $DSDIR/runnlp/metamapparse.sh $NOTEDIR "$FILE" $DSDIR
    bash $DSDIR/runnlp/metamapparse.sh $NOTEDIR "$FILE" $DSDIR $NAME
done
#done
#wait
