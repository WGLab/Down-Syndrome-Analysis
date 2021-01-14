import os, argparse

parser = argparse.ArgumentParser(description='Parse CLAMP output.')
parser.add_argument('-f', '--folder')
parser.add_argument('-c', '--cui_output')
parser.add_argument('-n', '--noncui_output')
args = parser.parse_args()


# In the outputs, if one line startswith 'NamedEntity', this line shows the NER info
NER = 'NamedEntity'

# store NER info into these dictionaries
ner_dict = dict()

# NERs with no CUI
ne_no_cui = dict()


for n in os.listdir('{}'.format(args.folder)):

    for line in open(r'{}/{}'.format(args.folder, n)):
        if(not line.startswith(NER)): continue


        data = line.rstrip('\n').split('\t')

        semantic = ''
        assertion = ''
        cui = ''
        ne = ''

        # Parse the NER info
        for d in data:
            ddata = d.split('=')

            if(ddata[0] == 'semantic'): semantic = ddata[1]
            if(ddata[0] == 'assertion'): assertion = ddata[1]
            if(ddata[0] == 'cui'): cui = ddata[1].split(',')[0]


            if(ddata[0] == 'ne'): ne = ddata[1]

        if(cui == '' or cui[0] != 'C'): cui = ''

        if(ne== ''):
            #print(line)
            continue

        

        if(cui != ''):
            if(ner_dict.get(cui) == None): ner_dict[cui] = {'pos':0, 'neg':0,'other':0}
            if(assertion == 'present'): ner_dict[cui]['pos']+=1
            elif(assertion == 'absent'): ner_dict[cui]['neg']+=1
            else: ner_dict[cui]['other']+=1

            

        else:
            if(ne_no_cui.get(ne) == None): ne_no_cui[ne] =0
            ne_no_cui[ne] += 1

            
with open(args.cui_output, 'w+') as fw:
    fw.write('CUI\tpos\tneg\tother\n')
    for ner in ner_dict.keys():
        fw.write('{}\t{}\t{}\t{}\n'.format(ner, str(ner_dict[ner]['pos']), str(ner_dict[ner]['neg']), str(ner_dict[ner]['other'])  ) )
        
with open(args.noncui_output, 'w+') as fw:     
    fw.write('ner\tnum\n')
    for ner in ne_no_cui.keys():
        fw.write('{}\t{}\n'.format(ner, str(ne_no_cui[ner])))
 

