#WA Delegate endorsement check by Merni, v1
#Some code taken from stackoverflow
 
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
parser.add_argument("-r","--region", help="Region name", type=str)
parser.add_argument("-u","--useragent", help="User agent", type=str)
parser.add_argument("-8","--line8",help="Output nation names only, 8 per line",action="store_true")

args = parser.parse_args()
full = args.line8

if args.region == None or args.useragent == None:
    print('Your useragent should have your email/NS name, as well as the purpose of this program (endo check). The mods need this info.')
    useragent = input('Enter your useragent : ')
    regionname = input('Enter your region name : ')  
else:
    useragent = args.useragent
    regionname = args.region
 
regionnamef = regionname.casefold().replace(' ','_')    
nt = datetime.utcnow().strftime('%Y-%m-%d at %H:%M:%S UTC') #rkachach, stackoverflow
out = '_text'
 
if not full: print("Querying nations in region...")
reg_url = 'https://www.nationstates.net/cgi-bin/api.cgi?region='+regionnamef+'&q=nations'
reg_req = urllib.request.Request(reg_url,headers={'User-Agent':useragent})
reg_req1 = urllib.request.urlopen(reg_req).read()
reg_req2 = ET.fromstring(reg_req1)
reg_d = dictify(reg_req2)
reg_stl = reg_d['REGION']['NATIONS'][0][out]
reg_l = reg_stl.split(':')
reg_set = set(reg_l)
 
time.sleep(1)
 
if not full: print("Querying WA members...")
wa_url = "http://www.nationstates.net/cgi-bin/api.cgi?wa=1&q=members"
wa_req = urllib.request.Request(wa_url,headers={'User-Agent':useragent})
wa_req1 = urllib.request.urlopen(wa_req).read()
wa_req2 = ET.fromstring(wa_req1)
wa_d = dictify(wa_req2)
wa_stl = wa_d['WA']['MEMBERS'][0][out]
wa_l = wa_stl.split(',')
wa_set = set(wa_l)
 
if not full: print("Finding intersection...")
reg_wa_set = reg_set.intersection(wa_set)
 
time.sleep(1)
 
if not full: print("Querying delegate...")
del_url = 'https://www.nationstates.net/cgi-bin/api.cgi?region='+regionnamef+'&q=delegate'
del_req = urllib.request.Request(del_url,headers={'User-Agent':useragent})
del_req1 = urllib.request.urlopen(del_req).read()
del_req2 = ET.fromstring(del_req1)
del_d = dictify(del_req2)
wadel = del_d['REGION']['DELEGATE'][0][out]
 
time.sleep(1)

if not full: print("Querying delegate endorsements...")
den_url = 'https://www.nationstates.net/cgi-bin/api.cgi?nation='+wadel+'&q=endorsements'
den_req = urllib.request.Request(den_url,headers={'User-Agent':useragent})
den_req1 = urllib.request.urlopen(den_req).read()
den_req2 = ET.fromstring(den_req1)
den_d = dictify(den_req2)
den_stl = den_d['NATION']['ENDORSEMENTS'][0][out]
den_l = den_stl.split(',')
den_set = set(den_l)
 
if not full: print("Finding difference...")
not_end = reg_wa_set.difference(den_set)
not_end = not_end.difference({wadel}) # to remove WAD from non-endorsers
nat = len(reg_set)
wan = len(reg_wa_set)
en = len(den_set)
nen = len(not_end)
perc = (en / wan) * 100
nperc = (nen / wan) * 100

if not full:
	print('\n\n\n')
	print("===============WA Delegate endorsement report===============")
	print("Generated (begin) on:\t\t",nt)
	print("Region:\t\t\t\t",regionname)
	print("WA Delegate:\t\t\t",wadel)
	print("Nations:\t\t\t",nat)
	print("WA nations:\t\t\t",wan)
	print("WA Delegate endorsements:\t",en)
	print("WA nations not endorsing:\t",nen)
	print("% of WA nations endorsing:\t",perc)
	print("% of WA nations not endorsing:\t",nperc)
	print("Note: WA delegate not included in calculations")
	print("============================List============================")
	n=1
	for i in not_end:
	    print(n,i,sep='\t')
	    n += 1
	input("Press Enter to close...")
else:
    a = 0
    for i in not_end:
        print(i,end=',')
        a += 1
        if a % 8 == 0: print()
