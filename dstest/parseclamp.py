import json
import sys

# from downclamp folder of clamp
patient = sys.argv[1].split("/")[-1].split(".")[0]
print(patient)
cuis=set()
with open(sys.argv[1], "r") as f:
    for line in f:
        if line.startswith("NamedEntity") and "cui=" in line:
            fields = line.strip().split("\t")
            ## NamedEntity   83       104     semantic=problem        assertion=present       cui=C3662068    ne=static encephalopathy
            negation=fields[4]
            cui=fields[5].split("=")[-1]
            name=fields[6].split("=")[-1]
            if negation == "assertion=absent":
                continue
            cuis.add(cui+"\t"+name)
with open(sys.argv[2], "w") as f:
    for member in cuis:
        print(member, file=f)
