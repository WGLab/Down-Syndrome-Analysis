import json
import sys

def hpohash(): 
    hpofile = open('umlshpo.json', 'r')      
    hpo = json.load(hpofile) 
    hpofile.close() 
    return hpo

umlshpo = hpohash()
# will work for umls terms formatted cui\tname as with clamp, ctakes, metamap
hposet = set()
with open(sys.argv[1], "r") as f, open(sys.argv[2], "w") as o:
    for line in f:
        fields = line.strip().split("\t")
        cui, name = fields[0], fields[1]
        try:
            for term in umlshpo[cui]:
                hposet.add(term)
        except KeyError:
            pass
    for term in hposet:
        print(term, file=o)
