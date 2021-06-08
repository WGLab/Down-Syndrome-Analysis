import time
from datetime import timedelta
import urllib.request
import shutil
import sys
import os
from collections import Counter, defaultdict
import pandas as pd
import networkx
import obonet
import numpy as np
from matplotlib import pyplot as plt
import argparse
import csv

parser = argparse.ArgumentParser(description='Calculate TF, PF, DF, TF-IDF, generate tables and plots')
parser.add_argument('-d', '--directory', help='directory where all patient notes are stored by patient folder')
parser.add_argument('-o', '--output', help='output file name for png and tsv')
parser.add_argument('-f', '--filter', help='control file to filter cases')
parser.add_argument('-a', '--ages', help='age data for cases or controls')
args = parser.parse_args()

def age_parse(agefile):
    agedict = {}
    with open(agefile,'r') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for d in reader:
            agedict[(d['patient'], d['note'])] = d['age']
    return agedict

def print_time(message, start):
    elapsed = time.time() - start
    print (message+":", str(timedelta(seconds=elapsed)), file=sys.stderr)

t = time.time()
# Read the ontology
try:
    graph = obonet.read_obo("hp.obo")
except FileNotFoundError:
    url = 'https://raw.githubusercontent.com/obophenotype/human-phenotype-ontology/master/hp.obo'
    # Download the file from "url" and save it locally under "hp.obo":
    with urllib.request.urlopen(url) as response, open("hp.obo", 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    graph = obonet.read_obo("hp.obo")

# Mapping from term ID to name
id_to_name = {id_: data.get('name') for id_, data in graph.nodes(data=True)}
# id_to_name['HP:0000118']  # HP:0001626 is cardiac abnormality, HP:0000118 is phenotypic

# no useless terms
phenotype_terms=networkx.ancestors(graph, 'HP:0000118')

print_time("Ontology Section", t)

t = time.time()

agedict = age_parse(args.ages)

print_time("Age File Parsing", t)

# set of documents
def patient_calculation(directory, agedict, term_ages):
    filecounts=Counter()
    doccounts=Counter()
    n_docs=0

    def tokenizer(s):
        return s.split()

    files,filenames=[],[]
    for file in os.listdir(directory):
        files.append(os.path.abspath(os.path.join(directory, file)))
        filenames.append(file)

    for file in files:
        patient, note = directory.rsplit('/', 1)[-1], file.rsplit('/', 1)[-1].rstrip(".txt")
        try:
            age = agedict[(patient, note)]
            with open(file, "r") as f:
                hpos = []
                for line in f:
                    hpos.append(line.strip())
                filecounts += Counter(hpos)
                doccounts += Counter({key:1 for key in Counter(hpos).keys()})
                for hp in set(hpos):
                    term_ages[hp].append(age)
                n_docs +=1
        except KeyError:
            print ("Patient, note: " + patient + ", " + note + ", not in table")
            pass
        except Exception as e:
            print(file)
            print(e)
            pass

    patientcounts = Counter({key:1 for key in doccounts.keys()})

    # print ('patient', directory)
    # print ('filecounts', filecounts)
    # print ('doccounts', doccounts)
    # print ('patientcounts', patientcounts)
    # print ('n_docs', n_docs)
    return filecounts, doccounts, patientcounts, n_docs, term_ages


# folder="dsdata/hpo"
t = time.time()
directory=args.directory

n_docs_total = 0
total_df = pd.DataFrame()
filecounts=Counter()
doccounts=Counter()
patientcounts=Counter()
term_ages = defaultdict(list)
for i, dir in enumerate(os.listdir(directory)):
    # if i == 50:
        # break
    patient_dir = os.path.abspath(os.path.join(directory, dir))
    fc, dc, pc, n_docs, term_ages = patient_calculation(patient_dir, agedict, term_ages)
    filecounts += fc
    doccounts += dc
    patientcounts += pc
    n_docs_total += n_docs

n_patients = i + 1

print_time("I/O, Counting Terms by Note, Age by Term and Patient", t)

def entries_to_keep(entries, the_dict):
    for key in list(the_dict.keys()):
        if key not in entries:
            del the_dict[key]

t = time.time()
entries_to_keep(phenotype_terms, filecounts)
entries_to_keep(phenotype_terms, doccounts)
entries_to_keep(phenotype_terms, patientcounts)
entries_to_keep(phenotype_terms, term_ages)
print_time("Filtering", t)

t = time.time()
df = pd.DataFrame({'TC': filecounts, 'DC': doccounts, 'PC': patientcounts})
df['IDF'] = np.log10(n_docs_total/df['DC'])
df['TF-IDF'] = df['TC']*df['IDF']
df['PF'] = df['PC']/n_patients
names = []
for x in df.index:
    try:
        names.append(id_to_name[x])
    except KeyError:
        names.append(x)
df.index = names
if args.filter:
    controlset = set()
    with open(args.filter, 'r') as f:
        f.readline()
        for line in f:
            fields = line.strip().split("\t")
            if float(fields[-1]) >= .05: # Patient Frequency of term
                controlset.add(fields[0]) # index, HPO term name
    df = df.loc[df.index.difference(controlset)]

df.sort_values('PF', inplace=True, ascending=False)
df.index.name = 'Term'
df.to_csv(args.output+'.tsv', sep = '\t')
with open(args.output+'termage.tsv', 'w') as f:
    for key in term_ages:
        ages = sorted(term_ages[key])
        print("\t".join([key, ",".join(ages)]), file=f)
print_time("Output", t)
print ('Number of Notes:', n_docs_total)
print ('Number of Patients:', n_patients)
ax = df['PF'].head(20).plot(kind='bar')
ax.set_ylabel("Patient Frequency")
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

plt.savefig(args.output+'.png', bbox_inches='tight')
