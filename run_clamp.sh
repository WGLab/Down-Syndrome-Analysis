cd /mnt/isilon/wang_lab/shared/apps/ClampCmd_1.6.4
mkdir -p $2 mkdir -p $3
python clamp_slurm_starter.py -i $1 -o $2 -l $3 > $3/clamp.log 
