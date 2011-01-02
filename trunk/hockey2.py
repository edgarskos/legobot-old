#!/usr/bin/python
# -*- coding: utf-8  -*-
"""

(C) Legoktm, 2008-2011

 Distributed under the terms of the MIT license.

__version__ = '$Id: $'

This script creates stubs for NHL players and talk pages

You are responsible for all edits made using this script

You can find information about hockey players at http://hockeydb.com
"""
from legoktm import *
import wikipedia
def hockeycat(nationraw, positionr):
	if nationraw == "can":
		if positionr == "c":
			hockeycat = "[[Category:Canadian ice hockey centres]]"
		elif positionr == "d":
			hockeycat = "[[Category:Canadian ice hockey defencemen]]"
		elif positionr == "g":
			hockeycat = "[[Category:Canadian ice hockey goaltenders]]"
		elif positionr == "l":
			hockeycat = "[[Category:Canadian ice hockey right wingers]]"
		elif positionr == "r":
			hockeycat = "[[Category:Canadian ice hockey left wingers]]"
		else:
			hockeycat = "[[Category:Canadian ice hockey players]]"
	elif nationraw == "usa":
		if positionr == "c":
			hockeycat = "[[Category:American ice hockey centres]]"
		elif positionr == "d":
			hockeycat = "[[Category:American ice hockey defencemen]]"
		elif positionr == "g":
			hockeycat = "[[Category:American ice hockey goaltenders]]"
		elif positionr == "l":
			hockeycat = "[[Category:American ice hockey right wingers]]"
		elif positionr == "r":
			hockeycat = "[[Category:American ice hockey left wingers]]"
		else:
			hockeycat = "[[Category:American ice hockey players]]"
	elif nationraw == "rus":
		hockeycat = "[[Category:Russian ice hockey players]]"
	elif nationraw == "czech":
		hockeycat = "[[Category:Czech ice hockey players]]"
	elif nationraw == "swe":
		hockeycat = "[[Category:Swedish ice hockey players]]"
	elif nationraw == "Finland":
		hockeycat = "[[Category:Finnish ice hockey players]]"
	elif nationraw == "Slovakia":
		hockeycat = "[[Category:Slovak ice hockey players]]"
	else:
		hockeycat = ""
	print "Using the category of: " + hockeycat
	hockeycat = "\n" + hockeycat
	return hockeycat

def persondata(name, bvartext, bplace, died, dmonthname, dday, dyear):
	import shlex
	namesplit = shlex.split(name)
	top = "\n<!-- Metadata: see [[Wikipedia:Persondata]] -->\n{{Persondata\n|NAME = " + namesplit[0] + " , " + namesplit[1] + "\n"
	descrip = "|SHORT DESCRIPTION = Professional ice hockey player"
	dbirth = "\n|DATE OF BIRTH     = " + bvartext
	pbirth = "\n|PLACE OF BIRTH    = " + bplace
	if died == True:
		ddeath = "\n|DATE OF DEATH     = " + dmonthname + " " + dday + ", " + dyear
	else:
		ddeath = "\n|DATE OF DEATH     = "
	fullpersondata = top + descrip + dbirth + pbirth + ddeath + "\n|PLACE OF DEATH = \n}}"
	return fullpersondata

def hockeyref(name):
	import shlex
	name = shlex.split(name)
	firstn = name[0]
	print firstn
	lastn = name[1]
	print lastn
	url = lastn[0] + "/" + lastn[0:4] + firstn[0:1]
	url = url.lower()
	return url

def hockeycat(nationraw, positionr):
	if nationraw == "can":
		if positionr == "c":
			hockeycat = "[[Category:Canadian ice hockey centres]]"
		elif positionr == "d":
			hockeycat = "[[Category:Canadian ice hockey defencemen]]"
		elif positionr == "g":
			hockeycat = "[[Category:Canadian ice hockey goaltenders]]"
		elif positionr == "l":
			hockeycat = "[[Category:Canadian ice hockey right wingers]]"
		elif positionr == "r":
			hockeycat = "[[Category:Canadian ice hockey left wingers]]"
		else:
			hockeycat = "[[Category:Canadian ice hockey players]]"
	elif nationraw == "usa":
		if positionr == "c":
			hockeycat = "[[Category:American ice hockey centres]]"
		elif positionr == "d":
			hockeycat = "[[Category:American ice hockey defencemen]]"
		elif positionr == "g":
			hockeycat = "[[Category:American ice hockey goaltenders]]"
		elif positionr == "l":
			hockeycat = "[[Category:American ice hockey right wingers]]"
		elif positionr == "r":
			hockeycat = "[[Category:American ice hockey left wingers]]"
		else:
			hockeycat = "[[Category:American ice hockey players]]"
	elif nationraw == "rus":
		hockeycat = "[[Category:Russian ice hockey players]]"
	elif nationraw == "czech":
		hockeycat = "[[Category:Czech ice hockey players]]"
	elif nationraw == "swe":
		hockeycat = "[[Category:Swedish ice hockey players]]"
	elif nationraw == "Finland":
		hockeycat = "[[Category:Finnish ice hockey players]]"
	elif nationraw == "Slovakia":
		hockeycat = "[[Category:Slovak ice hockey players]]"
	else:
		hockeycat = ""
	hockeycat = "\n" + hockeycat
	print "Using the category of: " + hockeycat
	return hockeycat

def nhlshort(team):
	#easternconference
	if team == "njd":
		team = "New Jersy Devils"
	elif team == "nyi":
		team = "New York Islanders"
	elif team == "nyr":
		team = "New York Rangers"
	elif team == "ppf":
		team = "Philadelphia Flyers"
	elif team == "pit":
		team = "Pittsburgh Penguins"
	elif team == "bos":
		team = "Boston Bruins"
	elif team == "buf":
		team = "Buffalo Sabres"
	elif team == "mon":
		team = "Montreal Canadiens"
	elif team == "ott":
		team = "Ottawa Senators"
	elif team == "tor":
		team = "Toronto Maple Leafs"
	elif team == "atl":
		team = "Atlanta Thrashers"
	elif team == "car":
		team = "Carolina Hurricanes"
	elif team == "flor":
		team = "Florida Panthers"
	elif team == "tbl":
		team = "Tampa Bay Lightning"
	elif team == "wash":
		team = "Washington Capitals"
	#westernconference
	elif team == "chic":
		team = "Chicago Blackhawks"
	elif team == "cbj":
		team = "Columbus Blue Jackets"
	elif team == "drw":
		team = "Detroit Red Wings"
	elif team == "nash":
		team = "Nashville Predators"
	elif team == "stl":
		team = "St. Louis Blues"
	elif team == "cal":
		team = "Calgary Flames"
	elif team == "col":
		team = "Colorado Avalance"
	elif team == "edm":
		team = "Edmonton Oilers"
	elif team == "min":
		team = "Minnesota Wild"
	elif team == "van":
		team = "Vancouver Canucks"
	elif team == "ana":
		team = "Anaheim Ducks"
	elif team == "dal":
		team = "Dallas Stars"
	elif team == "lak":
		team = "Los Angeles Kings"
	elif team == "phx":
		team = "Phoenix Coyotes"
	elif team == "sjs":
		team = "San Jose Sharks"
	else:
		print 'You entered an invalid choice.'
		raise
	return team	
		
def formerteams(var):
	team1 = raw_input("What former teams did he play for? ")
	if len(team1) > 0:
		team1 = wikilink(nhlshort(team1))
		print team1
		yearnumber = input("Start year? ")
		yearnumber2 = input("End year? ")
		#code from http://en.wikipedia.org/wiki/User:Legoktm/BOTFAQ/Code/redir.py (C) Legoktm (MIT License)
		yearset1 = int(yearnumber)
		if yearnumber >= 2000: #if above 2000, then subtract by 2000, not 1900
			yearset2 = int(yearnumber) - 1900 + 1
		else:
			yearset3 = int(yearnumber) - 2000 + 1
			yearset2 = "0" + str(yearset3) #add preceding 0
		print yearset2
		yearset12 = int(yearnumber2)
		if yearnumber2 >= 2000: #if above 2000, then subtract by 2000, not 1900
			yearset22 = int(yearnumber2) - 1900 + 1
		else:
			yearset32 = int(yearnumber2) - 2000 + 1
			yearset22 = "0" + str(yearset32) #add preceding 0
			
		yearsettemp  = str(yearset1)  + "-" + str(yearset2)   + " NHL season|" + yearnumber 
		yearsettemp2 = str(yearset12) + "-" + str(yearset22) + " NHL season|" + yearnumber2
		yearsettemp  = wikilink(yearsettemp)
		yearsettemp2 = wikilink(yearsettemp2)
		var = team1 + " (" + yearsettemp + "-" + yearsettemp2 + ")<br />"
		print var
	else:
		var = ""
	return var
