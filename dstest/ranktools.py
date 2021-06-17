import re
import argparse
import os
from collections import OrderedDict, defaultdict
from accuracy import accplot

parser = argparse.ArgumentParser()

parser.add_argument('-t', '--txt2hpo', help='The txt2hpo output folder', default='txt2hpo/out')
parser.add_argument('-c', '--clamp', help='The directory for clamp output', default='clamp/out')
parser.add_argument('-k', '--ctakes', help = 'The directory for cTakes output', default='ctakes/out')
parser.add_argument('-m', '--metamap', help='The directory for metamap output', default='metamap/out')
parser.add_argument('-e', '--expert', help='The directory for manual expert output', default='expert/out')
parser.add_argument('-p', '--probe', help='The file for the probe genes', default='probe_info')

args = parser.parse_args()

patients = OrderedDict()
originals = OrderedDict()
with open(args.probe, "r") as f:
    for line in f:
        fields = line.strip().split("\t")
        order, original, gene = fields[0], fields[1], fields[-1]
        originals[original]=gene # order is important
        patients[order]=gene # order is important
ds=[args.ctakes,args.clamp,args.txt2hpo,args.metamap,args.expert]
names=['cTakes', 'CLAMP', 'txt2hpo', 'MetaMap', 'Expert']
dictinit=OrderedDict({name:0.0 for name in names})
values = defaultdict(lambda: OrderedDict({"Top 10": 0.0, "Top 50": 0.0, "Top 100": 0.0, "Top 1000": 0.0}))
top10, top50, top100, top250 = dictinit.copy(), dictinit.copy(), dictinit.copy(), dictinit.copy()
for d, name in zip(ds, names):
    filelist = [os.path.join(d, path) for path in sorted(os.listdir(d))] # sort by number, may not be right order based on results though
    count = 0.0
    for filen in filelist:
        patient = filen.split("/")[-1].split(".")[0].split("_minus")[0]
        if patient in patients.keys() or patient in originals.keys():
            count+=1.0
            for line in open(filen, 'r'):
                try:
                    gene = patients[patient]
                except KeyError:
                    gene = originals[patient]
                except Exception as e:
                    print (e)
                    break
                if re.search("\t"+gene+"\t", line):
                    fields = line.strip().split("\t")
                    rank = int(fields[0])
                    # print (patient, name, gene, rank)
                    if rank <= 10:
                        # Top 10[name] +=1
                        values[name]["Top 10"] +=1
                    if rank <= 50:
                        # Top 50[name] +=1
                        values[name]["Top 50"] +=1
                    if rank <= 100:
                        # Top 100[name] +=1
                        values[name]["Top 100"] +=1
                    if rank <= 1000:
                        # Top 1000[name] +=1
                        values[name]["Top 1000"] +=1
    values[name]["Top 10"] = values[name]["Top 10"]*100/count
    values[name]["Top 50"] = values[name]["Top 50"]*100/count
    values[name]["Top 100"] = values[name]["Top 100"]*100/count
    values[name]["Top 1000"] = values[name]["Top 1000"]*100/count
    # Top 10[name] = Top 10[name]*100/count
    # Top 50[name] = Top 50[name]*100/count
    # Top 100[name] = Top 100[name]*100/count
    # Top 1000[name] = Top 1000[name]*100/count

accplot(values, names, "CUaccuracy")
# print("10:", Top 10)
# print("50:", Top 50)
# print("100:", Top 100)
# print("1000:", top250)
