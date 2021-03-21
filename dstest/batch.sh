### SETUP ###

set -x
mkdir -p metamap/downmeta metamap/metaterms metamap/metahpo
mkdir -p clamp/downclamp clamp/clampterms clamp/clamplog clamp/clamphpo
mkdir -p ctakes/downctakes ctakes/ctakesterms ctakes/ctakeshpo
CDIR=/mnt/isilon/wang_lab/jim/Down-Syndrome-Clustering

### METAMAP ### 

# format files for metamap
for FILE in $CDIR/28-pts-notes-20180821-rechecked-wkc/*; do
    tr -cd '[:print:]\n\r' < $FILE | mysponge $FILE
done

# before running metamap (may have to replace with your OWN metamap servers)
/mnt/isilon/wang_lab/jim/public_mm/bin/skrmedpostctl start
/mnt/isilon/wang_lab/jim/public_mm/bin/wsdserverctl start

# metamap (instructions at https://metamap.nlm.nih.gov/Docs/MM_2016_Usage.pdf)
for FILE in $CDIR/28-pts-notes-20180821-rechecked-wkc/*; do
    FILE=$(echo "$FILE" | sed "s/.*\///")
    metamap -y -R HPO -V USAbase --JSONf 2 $CDIR/28-pts-notes-20180821-rechecked-wkc/$FILE $CDIR/metamap/downmeta/$FILE
done

for FILE in $CDIR/metamap/downmeta/*; do
    FILE=$(echo "$FILE" | sed "s/.*\///")
    python $CDIR/dstest/parsemeta.py $CDIR/metamap/downmeta/$FILE $CDIR/metamap/metaterms/$FILE
done

### CLAMP ###

# running clamp
bash $CDIR/dstest/run_clamp.sh $CDIR/28-pts-notes-20180821-rechecked-wkc $CDIR/clamp/downclamp $CDIR/clamp/clamplog
rm $CDIR/clamp/downclamp/*xmi

# formatting clamp output
# https://clamp.uth.edu/res/CLAMP_v1.1.3_README.pdf is useful for interpretation
for FILE in $CDIR/clamp/downclamp/*; do
    FILE=$(echo "$FILE" | sed "s/.*\///")
    python $CDIR/dstest/parseclamp.py $CDIR/clamp/downclamp/$FILE $CDIR/clamp/clampterms/$FILE
done

### cTakes ###

# when downloading ctakes, need to run "wget https://sourceforge.net/projects/ctakesresources/files/ctakes-resources-4.0-bin.zip" in the main folder, so you have all resources.
# may also have to go to YOUR ctakes script dir
# note: 'polarity="-1"' indicates negation for some reason. (https://cwiki.apache.org/confluence/display/CTAKES/cTAKES+4.0+-+Assertion)

UMLSAPI="57a79e7a-a7ef-4280-a188-0f6c815572b1"
# running ctakes
bash /mnt/isilon/wang_lab/jim/apache-ctakes-4.0.0.1/bin/runClinicalPipeline.sh -i $CDIR/28-pts-notes-20180821-rechecked-wkc --xmiOut $CDIR/ctakes/downctakes --key $UMLSAPI

# formatting ctakes output
for FILE in $CDIR/ctakes/downctakes/*; do
    FILE=$(echo "$FILE" | sed "s/.*\///")
    python $CDIR/dstest/parsectakes.py $CDIR/ctakes/downctakes/$FILE $CDIR/ctakes/ctakesterms/$FILE
done

### extracting hpo terms for clamp, metamap, ctakes ###

### txt2hpo ###

# running txt2hpo
