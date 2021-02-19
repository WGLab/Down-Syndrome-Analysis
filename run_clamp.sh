cd /mnt/isilon/wang_lab/shared/apps/ClampCmd_1.6.0

mkdir -p $3

python clamp_starter.py -i $1 -o $2 -l $3 > $3/qsub.log 

