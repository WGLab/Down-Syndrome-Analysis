import xml.etree.ElementTree as ET
import sys

# from downctakes folder of ctakes
patient = sys.argv[1].split("/")[-1].split(".")[0]
print(patient)
tree = ET.parse(sys.argv[1])
root = tree.getroot()
ns = {'textsem': 'http:///org/apache/ctakes/typesystem/type/textsem.ecore',
      'xmi': '{http://www.omg.org/XMI}',
      'umls': 'http:///org/apache/ctakes/typesystem/type/refsem.ecore'}
#texts=["RomanNumeralAnnotation","FractionAnnotation","MedicationMention","DiseaseDisorderMention","SignSymptomMention","ProcedureMention","AnatomicalSiteMention","ConllDependencyNode","Predicate","SemanticArgument","SemanticRoleRelation"]
texts=["MedicationMention","DiseaseDisorderMention","SignSymptomMention","ProcedureMention","AnatomicalSiteMention"]
negids={}
termset=set()
for text in texts:
    for child in root.findall('textsem:'+text, namespaces=ns):
        child=child.attrib
        for xmid in child["ontologyConceptArr"].split():
            negids[xmid]=child["polarity"]
    for child in root.findall("umls:UmlsConcept", namespaces=ns):
        child=child.attrib
        try:
            if negids[child[ns["xmi"]+"id"]] == "-1":
                continue
        except KeyError:
            continue
        termset.add(child["cui"]+"\t"+child["preferredText"])

with open(sys.argv[2], "w") as f:
    for t in termset:
        print(t, file=f)
