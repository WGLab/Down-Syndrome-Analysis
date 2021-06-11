`Control cohort.ipynb`: Select the Control cohort
`OddsRatio.ipynb`: Calculate Odds Ratio and p-value for 1. Down Syndrome Patients vs. Control 2. Clusters of the Down Syndrome Patient

`DownSyndrome_pipeline.ipynb`: Query Down syndrome Notes, process the notes using CLAMP, get the HPO terms from the UMLS NERs; turn the HPO terms to vectors and turn Patients data to vector; Run TSNE to cluster the patients.
`parse_clamp_output.py`: qsub a parsing job in `DownSyndrome_pipeline.ipynb`

`Query ICD.ipynb`: Query the ICD code of the DownSyndrome Patient

