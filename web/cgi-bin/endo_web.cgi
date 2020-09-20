#!/usr/bin/python3.6

import urllib.request
import xml.etree.ElementTree as ET
from copy import copy
from datetime import datetime
import time
import argparse
import cgi
import cgitb

cgitb.enable()
nt = datetime.utcnow().strftime('%Y-%m-%d at %H:%M:%S UTC')
out1 = '<html><head><meta charset="utf-8"><title>Merni\'s endorsement checker - output</title></head><body><h1>Endorsement checker: Output</h1><i>Report generated (start) on '+nt+'</i><hr>'
out2 = '<hr>If you get any errors, check your input and try again after a minute or so. If the error persists, contact me (see below).<br>If the web version of this script is buggy, very slow, etc. then download it from the GitHub link below and use it on your computer.<br>Script by <a href="http://www.nationstates.net">NationStates</a> user <a href="http://www.nationstates.net/merni">Merni</a>. <br>Source at <a href="http://www.github.com/merni-ns/nstools">Github</a>. <br>Send questions, suggestions, error reports etc. to me through NS telegram (preferred) or at merni at merni dot heliohost dot org.<br>Web site hosted for free by <a href="http://www.heliohost.org/">HelioHost</a><br><a href="../index.html">Home page</a></body></html>'
out = "_text"

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

useragent = "Merni's endo checking script: merni.heliohost.org"

# Variables to be received from the form via CGI are:
# region: the name of the region,
# chk = d : check endorsements of delegate
#     = n :                       a specific nation
# nname : the nation in case of n above
# output = f : for full output
#        = 8 : for condensed output

def getform() -> tuple : # returns (region, output, chk, [nname]) or None
	form = cgi.FieldStorage()
	if "region" not in form :
		print("<h2>Error</h2>Please enter a region and select the required options. (1)")
		return
	region = form.getvalue("region")
	chk = form.getvalue("chk", "d")
	output = form.getvalue("output","f")
	if chk == "n":
		if "nname" in form:
			nname = form.getvalue("nname")
			return (region, output, chk, nname)
		else:
			print("<h2>Error</h2>Your selected options require you to enter a nation name. (2)")
			return
	else:
		return (region, output, chk)

def get_region(region : str) -> set :
	regionnamef = region.casefold().replace(' ', '_')
	reg_url = 'https://www.nationstates.net/cgi-bin/api.cgi?region='+regionnamef+'&q=nations'
	reg_req = urllib.request.Request(reg_url,headers={'User-Agent':useragent})
	reg_req1 = urllib.request.urlopen(reg_req).read()
	reg_req2 = ET.fromstring(reg_req1)
	reg_d = dictify(reg_req2)
	reg_stl = reg_d['REGION']['NATIONS'][0][out]
	reg_l = reg_stl.split(':')
	return set(reg_l)

def get_reg_del(region : str) -> tuple : # returns tuple (set nations, str wad)
	regionnamef = region.casefold().replace(' ', '_')
	del_url = 'https://www.nationstates.net/cgi-bin/api.cgi?region='+regionnamef+'&q=delegate+nations'
	del_req = urllib.request.Request(del_url,headers={'User-Agent':useragent})
	del_req1 = urllib.request.urlopen(del_req).read()
	del_req2 = ET.fromstring(del_req1)
	del_d = dictify(del_req2)
	wadel = del_d['REGION']['DELEGATE'][0][out]
	reg_stl = del_d['REGION']['NATIONS'][0][out]
	reg_l = reg_stl.split(':')
	return (set(reg_l), wadel)
	
def get_endos(nation : str) -> set :
	den_url = 'https://www.nationstates.net/cgi-bin/api.cgi?nation='+nation+'&q=endorsements'
	den_req = urllib.request.Request(den_url,headers={'User-Agent':useragent})
	den_req1 = urllib.request.urlopen(den_req).read()
	den_req2 = ET.fromstring(den_req1)
	den_d = dictify(den_req2)
	den_stl = den_d['NATION']['ENDORSEMENTS'][0][out]
	den_l = den_stl.split(',')
	return set(den_l)

def get_wa() -> set :
	wa_url = "http://www.nationstates.net/cgi-bin/api.cgi?wa=1&q=members"
	wa_req = urllib.request.Request(wa_url,headers={'User-Agent':useragent})
	wa_req1 = urllib.request.urlopen(wa_req).read()
	wa_req2 = ET.fromstring(wa_req1)
	wa_d = dictify(wa_req2)
	wa_stl = wa_d['WA']['MEMBERS'][0][out]
	wa_l = wa_stl.split(',')
	return set(wa_l)

x = getform()
print("Content-Type: text/html")
print()
print(out1)
if x is not None:
	if x[2] == "d":
		reg, wad = get_reg_del(x[0])
		time.sleep(1) # very dumb ratelimit compliance
	elif x[2] == "n":
		wad = x[3].casefold().replace(' ','_')
		reg = get_region(x[0])
		time.sleep(1)
	endos = get_endos(wad)
	time.sleep(1)
	wa = get_wa()
	time.sleep(1)
	regwa = reg.intersection(wa)
	nend = regwa.difference(endos)
	nend = nend.difference({wad})
	resp = ""
	if x[1] == "8":
		i = 1
		for j in nend:
			resp += j + ', '
			if i % 8 == 0: resp += '<br>'
			i += 1
	else:
		resp += "<b>Region:</b> " + x[0] + "<br>"
		resp += "<b>Nations:</b> " + str(len(reg)) + "<br>"
		resp += "<b>WA nations:</b> " + str(len(regwa)) + "<br>"
		resp += "<b>Nation checked:</b> " + wad + "<br>"
		resp += "<b>Endorsements:</b> " + str(len(endos)) + "<br>"
		resp += "<b>Nations not endorsing:</b> " + str(len(nend)) + "<br>"
		resp += "<b>% endorsing:</b> " + str(len(endos)/(len(regwa)-1)) + "<br>"
		resp += "<h3>List of nations not endorsing: </h3>"
		resp += "<ol>"
		for i in nend:
			resp += "<li>" + i + "</li>"
		resp += "</ol>"
	# CGI headers and page header
	print(resp)
else:
	print("<h2>Error</h2>Unknown error in script. Please check your input. (3)")

print(out2)
