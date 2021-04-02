import json
import sys
import os

os.makedirs(os.path.dirname(sys.argv[2]), exist_ok=True) # make directory
# from downmeta folder of metamap 
patient = sys.argv[1].split("/")[-1].split(".")[0]
print(patient)
cuis=[] # tf-idf needs all terms
with open(sys.argv[1], "r") as f:
    data = json.load(f, strict=False)
    for document in data["AllDocuments"]:
        terms = document["Document"]["Utterances"]
        for i in terms:
            for j in i["Phrases"]:
                if j["Mappings"]:
                    for k in j["Mappings"]:
                        for l in k["MappingCandidates"]:
                            if l["Negated"] == '1':
                                continue
                            else:
                                cuis.append(l["CandidateCUI"]+"\t"+l["CandidateMatched"])
with open(sys.argv[2], "w") as f:
    for member in cuis:
        print(member, file=f)
