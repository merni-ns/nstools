#RMB Archiving script by Merni
#Version 4.1
#If the script fails, send me a TG.
#Automatically ratelimited to 100 msgs (1 req) every 1.5s, i.e. 20 reqs / 30s
#Some code using urllib taken from stackoverflow.
 
import urllib.request
import xml.etree.ElementTree as ET
from copy import copy
from datetime import datetime
import time
import argparse

def dictify(r,root=True):
    #This function by Erik Aronesty at stackoverflow
    if root:
        return {r.tag : dictify(r, False)}
    d=copy(r.attrib)
    if r.text:
        d["_text"] = r.text
    for x in r.findall("./*"):
        if x.tag not in d:
            d[x.tag] = []
        d[x.tag].append(dictify(x,False))
    return d

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--useragent", help="NS API user agent")
parser.add_argument("-r", "--region", help="Region name")
parser.add_argument("-o", "--file", help="File to output the result (with path if required)")
parser.add_argument("-i", "--startid", help="Starting Post ID")
parser.add_argument("-s", "--startno", help="Starting serial number")
args = parser.parse_args()

if None in (args.region, args.useragent, args.file):
    print('Your useragent should have your email/NS name, as well as the purpose of this program (RMB archiving). The mods need this info.')
    useragent = input('Enter your useragent : ')
    regionname = input('Enter your region name : ')
    print('You must enter the full path of the text file, including extension. If the file is in your Python directory, you can enter the filename and extension only. If the file does not exist it will be created.')
    filename = input('Enter path/name of text file : ')
    adv = input('Advanced options? Y/N : ').casefold()
    if adv =='y':
        print('>>>If you want to start from the first post, press Enter for the next two prompts.<<<')
        print('The archive assigns a serial number 1,2,3... to each post. If you are starting from a later post,you may want to change the first serial number. Otherwise press Enter.')
        sid = input('Enter starting post ID : ')
        sn = input('Enter starting serial number : ')
    else: sid = sn = ''
else:
    useragent = args.useragent
    regionname = args.region
    filename = args.file
    sid = '' if args.startid is None else args.startid
    sn = '' if args.startno is None else args.startno


regionnamef = regionname.casefold().replace(' ','_')


 
nt = datetime.utcnow().strftime('%Y-%m-%d at %H:%M:%S UTC')
init = 1 if sn=='' else int(sn)
n = init
f = open(filename,mode = 'a+',errors = 'replace')
out = '_text'
url = 'https://www.nationstates.net/cgi-bin/api.cgi?region='+regionnamef+'&q=messages&fromid='+sid
pid = '1' if sid=='' else sid
start = '\nArchive starts from Post ID '+pid+' as Post '+str(n)+'\n'+'='*80 if pid!='1' or n!=1 else '' # Adds archive start info to heading
f.write('='*80+'\n'+regionname+' NationStates RMB Archive\non '+nt+'\n'+'='*80+'\nPython script by Merni\n'+'='*80+start)
 
while True:
    time.sleep(1.5)
    url = 'https://www.nationstates.net/cgi-bin/api.cgi?region='+regionnamef+'&q=messages&limit=100&fromid='+pid
    req = urllib.request.Request(url,headers={'User-Agent':useragent})
    s = urllib.request.urlopen(req).read()
    t = ET.fromstring(s)
    dc = dictify(t)
 
    if 'POST' in dc['REGION']['MESSAGES'][0]:
        msgs = dc['REGION']['MESSAGES'][0]['POST']
    else:
        print('No more posts found. Check text file to ensure all posts are archived.')
        break
 
    for i in msgs:
        pid = i['id']
        t = int(i['TIMESTAMP'][0][out])
        dt = datetime.utcfromtimestamp(t).strftime('%Y-%m-%d at %H:%M:%S UTC') #by rkachach at stackoverflow
        poster = i['NATION'][0][out]
        likes = int(i['LIKES'][0][out])
        status = int(i['STATUS'][0][out])
        mess = str(i['MESSAGE'][0][out])
        if likes!=0:
            likers = i['LIKERS'][0][out]
        else:
            likers=''
        if status==1:
            stat = 'suppressed by '
            supp = i['SUPPRESSOR'][0][out]
        elif status==2:
            stat = 'self-deleted'
            supp = ''
        elif status==9:
            stat = 'moderator deleted'
            supp = ''
        else:
            stat = supp = ''
 
        f.write('\n'+('-'*80)+'\n'+pid+': Post '+str(n)+' by '+poster+' on '+dt+'\nLikes: '+str(likes)+'('+likers+')'+'\n'+stat+supp+'\n'+mess)
 
        n += 1
 
    print(n-init)
    pid = str(int(pid)+1)
 
f.close()
