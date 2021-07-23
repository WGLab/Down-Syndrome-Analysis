# gives min, max, median, mean age of earliest correct diagnosis with ICD-10, with filtering on unknown values, and incorrect birthdates
cut -f 4 demographics.tsv | sed '1d' | grep -v "Unknown" | grep -v "-" | ./mmmm.r
# sex statistics
cut -f 2 demographics.tsv | sort | uniq -c
# self-reported ethnicity statistics
cut -f 3 demographics.tsv | sort | uniq -c
