## Down syndrome case study

This repository contains the code used to get the data and generate plots for the Down syndrome case study paper.

## Citation

Havrilla, J.M.; Zhao, M.; Liu, C.; Weng, C.; Helbig, I.; Bhoj, E.; Wang, K. Clinical Phenotypic Spectrum of 4,095 Individuals with Down Syndrome from Text Mining of Electronic Health Records. Genes 2021, 12, xx. https://doi.org/10.3390/xxxxx

## Description

`Baseline_cohort.ipynb`: Grab the baseline cohort

`Query_ICD_codes.ipynb`: Query the ICD code of the Down Syndrome Patients

`DS_Parsing.ipynb`: Query the gender, age, ethnicity data of the notes

`pipeline.sh`: This is the script that tells you what to run to do basically everything to generate the NLP-derived HPO terms, filter notes, and generate tables, OR calcs, TF-IDF, PF, and all plots.

Inside of `pipeline.sh` we run:

`filterpatients.sh` is used to filter out 22q patients from Down syndrome patients

`filternotes.sh` to filters out those patients from the notes and removes low quality notes

`runbaseline.sh` to generates all baseline notes, uses the `runnlp` folder, and runs `filterpatients.sh`

`runbatches.sh` to generate all Down syndrome notes and uses the `runnlp` folder

`freqcalc.sh` is the script that we run to get frequencies and tf-idf calculations, OR and p-values, and plots; data not otherwise obtained in `DS_parsing.ipynb`
