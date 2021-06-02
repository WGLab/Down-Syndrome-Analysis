import time
from datetime import timedelta
import urllib.request
import shutil
import sys
import os
from collections import Counter
import pandas as pd
import networkx
import obonet
import numpy as np
from matplotlib import pyplot as plt
import argparse

parser = argparse.ArgumentParser(description='Calculate TF, PF, DF, TF-IDF, generate tables and plots')
parser.add_argument('-d', '--directory', help='directory where all patient notes are stored by patient folder')
parser.add_argument('-o', '--output', help='output file name for png and tsv')
parser.add_argument('-f', '--filter', help='string containing control file to filter cases')
args = parser.parse_args()

def print_time(message, start):
    elapsed = time.time() - start
    print (message+":", str(timedelta(seconds=elapsed)))

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

# set of documents
def patient_calculation(directory):
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
        try:
            with open(file, "r") as f:
                hpos = []
                for line in f:
                    hpos.append(line.strip())
                filecounts += Counter(hpos)
                doccounts += Counter({key:1 for key in Counter(hpos).keys()})
                n_docs +=1
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
    return filecounts, doccounts, patientcounts, n_docs


# folder="dsdata/hpo"
t = time.time()
directory=args.directory

n_docs_total = 0
total_df = pd.DataFrame()
filecounts=Counter()
doccounts=Counter()
patientcounts=Counter()
for i, dir in enumerate(os.listdir(directory)):
    if i == 100:
        break
    fc, dc, pc, n_docs = patient_calculation(os.path.abspath(os.path.join(directory, dir)))
    filecounts += fc
    doccounts += dc
    patientcounts += pc
    n_docs_total += n_docs

n_patients = i + 1

print_time("I/O and Counting Note by Note", t)

def entries_to_keep(entries, the_dict):
    for key in list(the_dict.keys()):
        if key not in entries:
            del the_dict[key]

def print_to_file(data, filename, mod):
    with open(filename, mod) as f:
        return print(data, file=f)

t = time.time()
entries_to_keep(phenotype_terms, filecounts)
entries_to_keep(phenotype_terms, doccounts)
entries_to_keep(phenotype_terms, patientcounts)
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
df.to_csv(args.output+'.tsv', sep = '\t')
# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    # print_to_file(df, args.output+'.tsv', 'w')
print_time("Output", t)
print ('Number of Notes:', n_docs_total)
print ('Number of Patients:', n_patients)
ax = df['PF'].head(20).plot(kind='bar')
ax.set_ylabel("Patient Frequency")
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

plt.savefig(args.output+'.png', bbox_inches='tight')
