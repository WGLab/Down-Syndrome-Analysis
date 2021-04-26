#! /bin/bash
#
#SBATCH --export=ALL
#SBATCH --time=24:00:00
#SBATCH --array=1-100%1
#SBATCH -o slurm/slurm-%A_%a.out
set -x

NOTEDIR=/mnt/isilon/wang_lab/mengge/project/DownSymdrome/ds_notes
DSDIR=/mnt/isilon/wang_lab/jim/Down-Syndrome-Clustering
#for FILE in $DSDIR/28-pts-notes-20180821-rechecked-wkc/*; do
#python $DSDIR/runnlp/pathwalk.py $NOTEDIR > $DSDIR/notepaths
#while read FILE; do
cd $NOTEDIR
# for FILE in $(python $DSDIR/runnlp/pathwalk.py $NOTEDIR); do
# there are 1136012 lines, but slurm MaxArraySize is 1000000:
# scontrol show config | grep -E 'MaxArraySize|MaxJobCount'
FILE=$(sed -n "$SLURM_ARRAY_TASK_ID"p <(head -100 $DSDIR/notepaths))
echo "$FILE"
srun -N1 -n1 -c1 --exclusive bash $DSDIR/runnlp/parseterms.sh $NOTEDIR "$FILE" $DSDIR
#done
#wait
