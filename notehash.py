from datetime import datetime, timedelta
import argparse
import os
import csv

parser = argparse.ArgumentParser(description='Get all relevant patient note dates, store to file')
parser.add_argument('-d', '--dates', help='input file where literally all CHOP patient note dates are stored by patient and note')
parser.add_argument('-p', '--patients', help='input file with relevant patients and notes')
parser.add_argument('-o', '--outfile', help='output file with age outputs')
args = parser.parse_args()

# example root = '$DSDIR/dsdata/hpo', where all down syndrome hpo terms are in files by note name, in folders by patient
noteset, relset = set(), set()
for root, dirs, files in os.walk(args.patients):
    for f in files:
        _, patient, note = os.path.relpath(os.path.join(root, f), '.').rsplit('/', 2)
        note = note.rstrip(".txt")
        noteset.add((patient,note))

print(len(noteset))
with open(args.dates, 'r') as f, open(args.outfile, 'w') as o:
    writer = csv.writer(o, delimiter='\t')
    writer.writerow(["patient", "note", "age", "birth", "admit"]) 
    for line in f:
        fields = line.strip().split("\t")
        patient, note, admission, birthdate = fields[0], fields[1], fields[2], fields[3]
        if (patient, note) in noteset and (patient, note) not in relset:
            relset.add((patient,note))
            birth = datetime.strptime(birthdate, '%Y%m%d')
            admit = datetime.strptime(admission, '%Y%m%d')
            age = (admit - birth).days/365.2425
            writer.writerow([patient, note, age, birth, admit]) 
print(len(relset))
