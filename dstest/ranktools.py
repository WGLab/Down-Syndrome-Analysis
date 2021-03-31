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
values = defaultdict(lambda: OrderedDict({"top10": 0.0, "top50": 0.0, "top100": 0.0, "top1000": 0.0}))
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
                        # top10[name] +=1
                        values[name]["top10"] +=1
                    if rank <= 50:
                        # top50[name] +=1
                        values[name]["top50"] +=1
                    if rank <= 100:
                        # top100[name] +=1
                        values[name]["top100"] +=1
                    if rank <= 1000:
                        # top1000[name] +=1
                        values[name]["top1000"] +=1
    values[name]["top10"] = values[name]["top10"]*100/count
    values[name]["top50"] = values[name]["top50"]*100/count
    values[name]["top100"] = values[name]["top100"]*100/count
    values[name]["top1000"] = values[name]["top1000"]*100/count
    # top10[name] = top10[name]*100/count
    # top50[name] = top50[name]*100/count
    # top100[name] = top100[name]*100/count
    # top1000[name] = top1000[name]*100/count

accplot(values, names, "CUaccuracy")
# print("10:", top10)
# print("50:", top50)
# print("100:", top100)
# print("1000:", top250)
