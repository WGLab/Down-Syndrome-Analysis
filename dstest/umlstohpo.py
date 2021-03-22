import simplejson as json
# need the MRCONSO.RRF UMLS file! #
MRCONSO = '/mnt/isilon/wang_lab/shared/datasets/UMLS_unzipped/2019AB-full/UMLS_lib/2019AB/META/MRCONSO.RRF'
cui_hpo = dict()
cnt = 0
for line in open(MRCONSO, 'r'):
    fields = line.strip().split('|')
    cui, sid, source = fields[0], fields[10], fields[11]
    if('HPO' in source):
        if(cui_hpo.get(cui) == None):
            cui_hpo[cui] = set()
        cui_hpo[cui].add(sid)
# pickle the set, it takes forever to use otherwise

with open('umlshpo.json', 'w') as hpofile:
    json.dump(cui_hpo, hpofile, iterable_as_array=True)
    hpofile.close()
