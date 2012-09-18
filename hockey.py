#!/usr/bin/python
# -*- coding: utf-8  -*-
"""

(C) Legoktm, 2008-2011

 Distributed under the terms of the MIT license.

__version__ = '$Id$'

This script creates stubs for NHL players and talk pages

You are responsible for all edits made using this script

You can find information about hockey players at http://hockeydb.com

TODO:
*Convert to hockey-reference website
*Incorporate persondata
*Taskforces on talk page (partially done)
*Former teams
*Career stats

NOTES:
*Approved for 50 edits trial (25 articles, 25 talk pages)
"""
import wikipedia, pagegenerators, catlib
from legoktm import *
from hockey2 import *
import webbrowser, shlex, re
#prepare for writing
name = raw_input("Player\'s name: ")
print "Writing article for " + name + "."
site = wikipedia.getSite()
if wikipedia.Page(site, name).exists() == True:
	print "Adding disambiguator \'(ice hockey)\'"
	realname = name + " (ice hockey)"
	print "Page will be created at " + realname
else:
	realname = name
hockeyref = hockeyref(name)
print "Opening hockey-reference page for " + name
#webbrowser.open("http://www.hockey-reference.com/players/" + hockeyref)
webbrowser.open("http://www.hockey-reference.com/player_search.cgi?search=" + name)
image = raw_input("Image for " + name + ".  Leave blank for none.")
imagebox = "{{Infobox Ice Hockey Player\n| image = " + image
image_caption = raw_input("Caption for [[Image:" + image + "]].  Leave blank for none.")
imagecaptbox = "\n| image_caption   = " + image_caption
positionr = raw_input("Does he play [c]enter, [l]eft wing, [r]ight wing, [d]efense, or [g]oalie? ")
if positionr == "c":
	position = "[[Centre (ice hockey)|Centre]]" 
elif positionr == "l":
	position = "[[Winger_(sport)#Ice_hockey|Left wing]]"
elif positionr == "r":
	position = "[[Winger_(sport)#Ice_hockey|Right wing]]"
elif positionr == "g":
	position = "[[Goaltender]]"
elif positionr == "d":
	position = "[[Defenceman (ice hockey)|Defence]]"
else:
	position = positionr
print name + " plays the position of ", position
posbox = "\n| position = " + position
shoots = raw_input("Does player shoot/catch [l]eft or [r]ight? ")
if shoots == "l":
	shoots = "Left"
elif shoots == "r":
	shoots = "Right"
if position == "[[Goaltender]]":
	catch_shoot = "catches"
else:
	catch_shoot = "shoots"
catshotbox = "\n| "+catch_shoot+"   = " + shoots
htft = raw_input("??? feet ")
htft = str(htft)
hftbox = "\n| height_ft       = " + htft
htin = raw_input("and inches ")
htin = str(htin)
hinbox = "\n| height_in       = " + htin
weight = raw_input("Weight in pounds: ")
weight = str(weight)
weibox = "\n| weight_lb       = " + weight
print name, " is ", htft, "ft, ", htin, "inches and weighs ", weight, " lbs."
nationraw = raw_input("Nationality is: (full country name, shortcuts: [can][usa][rus][swe][czech]) ")
if nationraw == "can":
	nation = "Canada"
elif nationraw == "usa":
	nation = "United States"
elif nationraw == "rus":
	nation = "Russia"
elif nationraw == "swe":
	nation = "Sweden"
elif nationraw == "czech":
	nation = "Czech Republic"
else:
	nationraw = nation
natbox = "\n| nationality     = " + nation
if nationraw == "usa":
	stubtag = "{{US-icehockey-bio-stub}}"
elif nationraw == "Finland":
	stubtag = "{{Finland-icehockey-bio-stub}}"
elif nationraw == "rus":
	stubtag = "{{Russia-icehockey-bio-stub}}"
elif nationraw == "czech":
	stubtag = "{{CzechRepublic-icehockey-bio-stub}}"
elif nationraw == "Slovakia":
	stubtag = "{{Slovakia-icehockey-bio-stub}}"
elif nationraw == "swe":
	stubtag = "{{Sweden-icehockey-bio-stub}}"
elif nationraw == "can":
	if positionr == "c":
		stubtag = "{{Canada-icehockey-centre-stub}}"
	elif positionr == "d":
		stubtag = "{{Canada-icehockey-defenceman-stub}}"
	elif positionr == "l" or positionr == "r":
		stubtag = "{{Canada-icehockey-winger-stub}}"
	elif positionr == "g":
		stubtag = "{{Canada-icehockey-goaltender-stub}}"
	else:
		stubtag = "{{Canada-icehockey-player-stub}}"
else:
	stubtag = "{{icehockey-bio-stub}}"
print "Using the stubtag of: " + stubtag
hockeycat = hockeycat(nationraw, positionr)
league = "[[National Hockey League]]"
leagueabbr = "[[National Hockey League|NHL]]"
leaguebox = "\n| league   = " + leagueabbr
team = raw_input(name + " plays for which team? ")
teamlink = wikilink(nhlshort(team))
formerteams = formerteams(formerteams)
ftbox = "| former_teams = " + formerteams
byear = raw_input("Born in what year: ")
bmonth = raw_input("Born in what month: ")
bday = raw_input("Born on what day: ")
dyear = raw_input("Died in which year: ")
if len(dyear) > 0:
	died = True
	dmonth = raw_input("Died in which month: ")
	dday = raw_input("Died in what day: ")
	dboxtemp = "\n| death_date = {{death date and age|" + dyear + "|" + dmonth + "|" + dday + "|" + byear + "|" + bmonth + "|" + bday + "|mf=y}}"
	print dboxtemp
	btemplate = "{{Birth date|" + str(byear) + "|" + str(bmonth) + "|" + str(bday) + "|mf=y}}"
else:
	died = False
	btemplate = "{{Birth date and age|" + str(byear) + "|" + str(bmonth) + "|" + str(bday) + "|mf=y}}"
	dboxtemp = ""
	dday = ""
	dmonthname = ""
bmonthtext = month(bmonth)
if len(dday) == 0:
	btext = "(born " + bmonthtext + " " + bday + ", " + byear + ") "
	
else:
	dmonthname = month(dmonth)
	btext = "(" + bmonthtext + " " + bday + ", " + byear + "–" + dmonthname + " " + dday + ", " + dyear + ") "
bvartext = bmonthtext + " " + bday + ", " + byear
print btemplate
namesplit = shlex.split(name)
if died == False:
	lifetime = "\n{{Lifetime|" + byear + "|LIVING|" + namesplit[1] + ", " + namesplit[0] + "}}\n"
else:	
	lifetime = "\n{{Lifetime|" + byear + "|" + dyear + "|" + namesplit[1] + ", " + namesplit[0] + "}}\n"
print lifetime
btempbox = "\n| birth_date      = " + btemplate + dboxtemp
bplace = raw_input("Born where: ")
pagecheck(bplace) #check if the place exists to wikilink
bbox = "\n|birth_place = " + bplace
draftnum = raw_input("Number drafted overall: ")
if len(draftnum) == 0:
	print "Player not drafted."
	draft = str(draftnum)
	draftcat = ""
	dbox = ""
	dftyear = ""
	dteam = ""
else:
	draft = str(draftnum) + "th overall"
	dbox = "\n| draft    = " + draft
	dftyear = raw_input("Drafted in what year: ")
	dftyear = str(dftyear)
	dyear = "\n| draft_year      = " + dftyear
	dftteam = raw_input("Drafted by what team: (use [p] if is team plays for now)")
	if dftteam == "p":
		dftteam = team
	dteam = "\n| draft_team      = " + dftteam
	draftcat = "\n[[Category:" + team + " draft picks]]"
cstart = raw_input("Career started in: ")
cstart = str(cstart)
cstbox = "\n| career_start    = " + cstart
cend = raw_input("Career ended in: (last year playing) ")
cend = str(cend)
if len(cend) != 0:
	playsnow = "who played"
	teambox = "\n| played_for = " + teamlink
else:
	playsnow = "that plays"
	teambox = "\n| team = " + teamlink
cenbox = "\n| career_end = " + cend + "\n}}\n"
hockeyrefnum = raw_input("Hockeyref id: ")
hockeyref = unicodify(hockeyrefnum)
#what article will contain
infobox = imagebox + imagecaptbox + posbox + catshotbox + hftbox + hinbox + weibox + natbox + leaguebox + teambox + ftbox + btempbox + dbox + dyear + dteam + bbox + cstbox + cenbox
text = "'''" + name + "''' " + btext + "is a [[Professional sports#Ice hockey|professional]] hockey player " + playsnow + " for the " + teamlink + " in the " + league + "."
if len(draftcat) != 0:
	categories = "[[Category:" + team + " players]]" + hockeycat
else:
	categories = "\n[[Category:" + team + " players]]" + draftcat + hockeycat
persondatatemplate = persondata(name, bvartext, bplace, died, dmonthname, dday, dyear)
other = "==External links==\n* {{hockeyref|" + hockeyref + "|" + name + "}}\n\n" + persondatatemplate
fullcontent = infobox + "\n" + text + "\n" + other + categories + lifetime + stubtag
print fullcontent
#write it to wiki
wikipedia.setAction("Creating article on " + name + " (Trial [[Wikipedia:Bots/Requests for approval/Hockeybot|BRFA]])")
fullcontent = unicodify(fullcontent)
p1 = wikipedia.Page(site, realname)
if p1.exists() == False:
	wikipedia.output(">>Creating %s" % p1.title() )
	p1.put(fullcontent)
	wikipedia.output("Done with article!")
	if nationraw == "swe":
		tfs = "|Sweden-task-force= yes\n"
	else:
		tfs = ""
	if nationraw == "can":
		otherproj = "{{WPCANADA\n|class=Stub\n|importance=Low\n|sport=yes\n|nested=yes\n}}"
	elif nationraw == "usa":
		otherproj = "{{WikiProject United States\n|class=Stub\n|importance=Low\n|nested=yes\n}}"
	elif nationraw == "rus":
		otherproj = "{{WikiProject Russia\n|nested=yes\n|class=Stub\n|importance=Low\n}}"
	elif nationraw == "czech":
		otherproj = "{{WikiProject Czech Republic\n|class=Stub\n|importance=Low\n|nested=yes\n}}"
	elif nationraw == "swe":
		otherproj = "{{WPSweden\n|nested=yes\n|class=Stub\n|importance=Low\n}}"
	else:
		otherproj = ""
	otherproj = otherproj + "}}"


	talkpage = "{{WikiProjectBannerShell|1=\n{{ice hockey\n|class=stub\n|needs-photo=yes\n" + tfs + "|nested=yes\n}}\n{{WPBiography\n|living = yes \n|class = stub \n|priority = low \n|sports-work-group = yes\n|needs-photo = yes\n|nested=yes\n}}\n" + otherproj
	wikipedia.setAction("Creating talk page for " + name + " (Trial [[Wikipedia:Bots/Requests for approval/Hockeybot|BRFA]])")
	talkname = "Talk:" + realname
	p2 = wikipedia.Page(site, talkname)
	if p2.exists() == False:
    		wikipedia.output(">>Creating %s" % p2.title() )
		p2.put(talkpage)
	else:
		wikipedia.output(">>%s exists" % p2.title() )
	wikipedia.output("Done with talk page!")
	page = realname
	newtext = '*{{la|' + page + '}} was created at ~~~~~\n' 
	log = "User:Hockeybot/Log"
	logpage = Page(site, log)
	newtext = newtext + logpage.get()
	summary = 'Adding ' + page + ' to log'
	print summary
	logpage.put(newtext, summary)
	print "Done adding " + page + " to log."
	webbrowser.open("http://en.wikipedia.org/w/index.php?title=Special:RecentChangesLinked&limit=500&days=30&target=User%3AHockeybot%2FLog")
else:
	wikipedia.output(">>%s exists" % p1.title() )
#update code if necessary
scriptpage = wikipedia.Page(site, "User:Hockeybot/Code")
summary = 'Updating source code'
code1 = "hockey.py"
code2 = "hockey2.py"
text1 = file(code1).read()
text2 = file(code2).read()
toptext = '==Files==\n*hockey.py\n*hockey2.py\n*legoktm.py (Private)\n\n'
text = toptext + '==Code==\n{{collapse top|hockey.py}}\n<source lang="python">\n' + text1 + '\n</sou' + 'rce>\n{{collapse bottom}}\n{{collapse top|hockey2.py}}\n<source lang="python">\n' + text2 + '\n</sou' + 'rce>'
text = unicodify(text)
if scriptpage.get() != text:
    scriptpage.put(text, summary)
else:
	print 'No need to update code'
wikipedia.stopme()
