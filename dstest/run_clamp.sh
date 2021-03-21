#!/bin/bash

set -x
cd /mnt/isilon/wang_lab/shared/apps/ClampCmd_1.6.4

umlsAPI="57a79e7a-a7ef-4280-a188-0f6c815572b1"

input=$1
output=$2
mkdir -p $output

clampbin="bin/clamp-nlp-1.6.4-jar-with-dependencies.jar"
pipeline="pipeline/clamp-ner.pipeline.jar"
#pipeline="pipeline/nerattr/clamp-ner-attribute.pipeline"
umlsIndex="resource/umls_index/"

java -DCLAMPLicenceFile="CLAMP.LICENSE" -Xmx3g -cp $clampbin edu.uth.clamp.nlp.main.PipelineMain \
    -i $input \
    -o $output \
    -p $pipeline \
    -A $umlsAPI \
    -I $umlsIndex
