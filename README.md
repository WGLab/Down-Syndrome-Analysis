## Down syndrome case study

This repository contains the code used to get the data and generate plots for the Down syndrome case study paper.

## Citation

Havrilla, J.M.; Zhao, M.; Liu, C.; Weng, C.; Helbig, I.; Bhoj, E.; Wang, K. Clinical Phenotypic Spectrum of 4,095 Individuals with Down Syndrome from Text Mining of Electronic Health Records. Genes 2021, 12, xx. https://doi.org/10.3390/xxxxx

## Description

So in order, the general workflow goes like this.

`DownSyndrome_pipeline.ipynb`: Mengge Zhao used some of the code in here to download all of the notes from Epic Clarity, and some of our initial filters and PCA/Clustering plots are in here as well.

`Baseline_cohort.ipynb`: This will help find the IDs to grab from the baseline cohort, which comes from random patients from 2012 with no heart problems, DS, or q22 deletion from the ASD-NER paper (unpublished).  This is used later to filter patients.

`DS_Parsing.ipynb`: Query the gender, age, ethnicity data of the notes.  You will need to manually extrapolate race and ethnicity as they come from multiple tables, values do not agree, and some don't exist from table to table.

`pipeline.sh`: This is the script that tells you what to run to do basically everything to generate the NLP-derived HPO terms, filter notes, and generate tables, OR calcs, TF-IDF, PF, and all plots.

Inside of `pipeline.sh` we run:

`filterpatients.sh` is used to filter out 22q patients from Down syndrome patients

`filternotes.sh` to filters out those patients from the notes and removes low quality notes

`runbaseline.sh` to generates all baseline notes, uses the `runnlp` folder, and runs `filterpatients.sh`

`runbatches.sh` to generate all Down syndrome notes and uses the `runnlp` folder

`freqcalc.sh` is the script that we run to get frequencies and tf-idf calculations, OR and p-values, and plots; data not otherwise obtained in `DS_parsing.ipynb`
