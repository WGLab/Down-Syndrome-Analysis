import os, argparse
import sqlite3
parser = argparse.ArgumentParser(description='Query notes')
parser.add_argument('-db', '--database')
parser.add_argument('-i','--idx', type=int)
parser.add_argument('-n','--num', type=int)
parser.add_argument('-l','--list')
parser.add_argument('-o','--outputfolder')
parser.add_argument('-a','--add', action='store_true', help='add new data')


args = parser.parse_args()

pats = [line.rstrip('\n') for line in open(args.list, 'r')]


con = sqlite3.connect(args.database)
cur = con.cursor()

os.system('mkdir -p {}'.format(args.outputfolder))


for i in range(len(pats)):
    if(i % args.num != args.idx): continue

    if(args.add):
        if(os.path.exists('{}/{}'.format(args.outputfolder, pats[i]))): 
            print('{} has been already in {}'.format(pats[i], args.outputfolder))
            continue

    cmd = "select note_id, note_text from note_text where pat_id = '{}'"
    cur.execute(cmd.format(pats[i]))
    os.system('mkdir -p {}/{}'.format(args.outputfolder, pats[i]))
    data  = cur.fetchone()
    while(data ):
        note_id = data[0]
        note_text = data[1].replace('?', '')
        with open('{}/{}/{}'.format(args.outputfolder, pats[i],note_id), 'w+') as fw:
            fw.write(note_text)
        data  = cur.fetchone()
    print('processed {}'.format(pats[i]))


        
cur.close()
con.close()
