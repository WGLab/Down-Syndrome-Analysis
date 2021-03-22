import re
import sys
import glob
from operator import itemgetter
import argparse
import os
from collections import defaultdict

parser = argparse.ArgumentParser()

parser.add_argument('-t', '--txt2hpo', help='The txt2hpo output folder', default='txt2hpo/out')
parser.add_argument('-c', '--clamp', help='The directory for clamp output', default='clamp/out')
parser.add_argument('-k', '--ctakes', help = 'The directory for cTakes output', default='ctakes/out')
parser.add_argument('-m', '--metamap', help='The directory for metamap output', default='metamap/out')
parser.add_argument('-p', '--probe', help='The file for the probe genes', default='probe_info')

args = parser.parse_args()

genes = []
with open(args.probe, "r") as f:
    for line in f:
        if line.startswith("Columbia"):
            fields = line.strip().split("\t")
            order, gene = fields[1], fields[-1]
            genes.append([order, gene]) # order is important
# genes.sort(key=itemgetter(0))
# print(genes)
genes = [gene[1] for gene in genes]
# print(genes)
ds=[args.ctakes,args.clamp,args.txt2hpo,args.metamap]
names=['cTakes', 'CLAMP', 'txt2hpo', 'MetaMap']
top10, top50, top100, top250 = defaultdict(float), defaultdict(int), defaultdict(int), defaultdict(int)
for d, name in zip(ds, names):
    filelist = [os.path.join(d, path) for path in sorted(os.listdir(d))] # sort by number, may not be right order based on results though
    for file, gene in zip(filelist, genes):
        for line in open(file, 'r'):
            if re.search(gene+"\t", line):
                fields = line.strip().split("\t")
                rank = int(fields[0])
                if rank <= 10:
                    top10[name] +=100/28.0
                if rank <= 50:
                    top50[name] +=100/28.0
                if rank <= 100:
                    top100[name] +=100/28.0
                if rank <= 250:
                    top250[name] +=100/28.0

print("10:", top10)
print("50:", top50)
print("100:", top100)
print("250:", top250)
