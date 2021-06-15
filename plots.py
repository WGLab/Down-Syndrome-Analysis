import urllib.request
import shutil
import os
import pandas as pd
import numpy as np
import networkx
import obonet
from matplotlib import pyplot as plt
import argparse
import csv
import seaborn as sns

parser = argparse.ArgumentParser(description='Make plots for frequency and age data')
parser.add_argument('-t', '--termdata', nargs=2, help='Frequency data for HPO terms')
parser.add_argument('-a', '--ages', help='Age data for cases and controls')
parser.add_argument('-n', '--numbers', nargs=2, help='Patient counts for cases and controls')
parser.add_argument('-o', '--output', nargs=2, help='Output file names')
args = parser.parse_args()

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

def age_parse(agefile, id_to_name, bins):
    agedict = {}
    with open(agefile, "r") as f:
        for line in f:
            term, ages = line.strip().split("\t")
            term = id_to_name[term]
            inds = np.digitize(np.array(ages.split(",")).astype(float), bins, right=True)
            agedict[term] = sorted(bins[inds])
    return agedict

bins = np.arange(0, 120, .25)
agedict = age_parse(args.ages, id_to_name, bins)
caseterms = pd.read_csv(args.termdata[0], sep='\t', header=0, index_col=0)
top100 = caseterms.head(100).index
controlterms = pd.read_csv(args.termdata[1], sep='\t', header=0, index_col=0)
# 4209 - 115(22q) = 4094 DS patients, 7845 control patients (or could get patient inputs from -n if you want)
case_n = 4094
control_n = 7845
if args.numbers:
    case_n = int(args.numbers[0])
    control_n = int(args.numbers[1])

# OR = DeHn/DnHe
# Case PC = de; Control PC = he; dn = case_n - de; hn = control_n - he
de = caseterms['PC']
he = controlterms['PC']
dn = case_n - de
hn = control_n - he
odds = de.mul(hn, fill_value=0)/dn.mul(he, fill_value=1) # in case denom is 0
odds.sort_values(axis=0, inplace=True, ascending=False)

# if args.filter:
    # controlset = set()
    # with open(args.filter, 'r') as f:
        # f.readline()
        # for line in f:
            # fields = line.strip().split("\t")
            # if float(fields[-1]) >= .05: # Patient Frequency of term
                # controlset.add(fields[0]) # index, HPO term name
    # df = df.loc[df.index.difference(controlset)]

# odds ratio of terms plot
fig, ax = plt.subplots()
sns.set_style('ticks')
sns.despine(right=True,top=True)
odds.head(20).plot(kind='bar')
ax.set_ylabel('Odds Ratio, Patient Frequency')
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
plt.savefig(args.output[0]+'.png', bbox_inches='tight')
plt.close()

# individual term age plots
odds.to_csv(args.output[0]+'.tsv', sep='\t')
fig, ax = plt.subplots()
# fig, ax = plt.subplots(3,2)
term = 'Abnormal ear physiology'
# ax.hist(agedict[term], bins, histtype='stepfilled')
sns.histplot(agedict[term], bins=bins)
# use top 100 odds ratio terms, plot age dists, heatmap line by line
ticks=sorted(set(agedict[term]))
ax.set_xticks(ticks)
ax.set_xticklabels(map("{:.0f}".format, ticks))
ax.set_xlim(0,max(ticks))
for i, t in enumerate(ax.get_xticklabels()):
    if (i % 16) != 0:
        t.set_visible(False)
plt.xlabel('Age')
plt.ylabel('Count of Visits')
plt.title(term)
print(ticks)

topkeys = odds.head(100).index
topage = { key: agedict[key] for key in top100 }

# ax[0, 0].plot(agedict['Zonular cataract'])
sns.set_style('ticks')
sns.despine(right=True,top=True)
# for a in ax.flat:
    # a.set(xlabel='Age', ylabel='Count of Visits')
plt.savefig(args.output[1]+'.png', bbox_inches='tight')
plt.close()
# heatmap of top 100 HPO terms by age
f, ax = plt.subplots(figsize=(15, 15))
# df = pd.DataFrame.from_dict(agedict,orient='index').transpose()
df = pd.concat({k: pd.Series(v).value_counts() for k, v in topage.items()}, axis=1).transpose()
print(df)
ax = sns.heatmap(df, mask=df.isnull(), cmap="icefire", yticklabels=True, cbar_kws={'label': 'Number of Visits'})#, xticklabels=True)
ax.set_ylabel("HPO terms", fontsize=16)
ax.set_xlabel("Age in Years", fontsize=16)
ax.figure.axes[-1].yaxis.label.set_size(16)
plt.savefig(args.output[1]+'top100.png', bbox_inches='tight')
plt.close()
