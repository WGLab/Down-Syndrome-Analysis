import json
import sys
import os

os.makedirs(os.path.dirname(sys.argv[2]), exist_ok=True) # make directory

def hpohash(): 
    hpofile = open(sys.argv[3], 'r') # umlshpo.json needed for conversion of UMLS to HPO quickly
    hpo = json.load(hpofile) 
    hpofile.close() 
    return hpo

umlshpo = hpohash()
# will work for umls terms formatted cui\tname as with clamp, ctakes, metamap
hpolist = [] # tf-idf needs all
with open(sys.argv[1], "r") as f, open(sys.argv[2], "w") as o:
    for line in f:
        fields = line.strip().split("\t")
        cui, name = fields[0], fields[1]
        try:
            for term in umlshpo[cui]:
                hpolist.append(term)
        except KeyError:
            pass
    for term in hpolist:
        print(term, file=o)
