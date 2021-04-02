#! /bin/bash
#
#SBATCH --ntasks=100
#SBATCH --export=ALL
#SBATCH --mem=100G
#SBATCH --time=24:00:00
set -x

NOTEDIR=/mnt/isilon/wang_lab/mengge/project/DownSymdrome/ds_notes
#UMLSDIR=/mnt/isilon/wang_lab/jim/Down-Syndrome-Clustering/ds_cui
#HPODIR=/mnt/isilon/wang_lab/jim/Down-Syndrome-Clustering/ds_hpo
DSDIR=/mnt/isilon/wang_lab/jim/Down-Syndrome-Clustering
#for i in {1..1000}
#do
   #srun -N1 -n1 -c1 --exclusive ./myprog $i &
#done
#for FILE in $DSDIR/28-pts-notes-20180821-rechecked-wkc/*; do
# for FILE in */*; do echo $FILE; done
cd $NOTEDIR
for FILE in $(python $DSDIR/runnlp/pathwalk.py $NOTEDIR); do
    srun -N1 -n1 -c1 --exclusive bash $DSDIR/runnlp/parseterms.sh $NOTEDIR $FILE $DSDIR &
done
wait
