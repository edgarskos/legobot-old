#!/usr/bin/python
# -*- coding: utf-8  -*-
#
# (C) Compwhizii, Legoktm, 2008 
# Original code at [[User:John Bot II/Code]]
# Modified by Legoktm
#
# Distributed under the terms of the MIT license.
#
__version__ = '$Id: $'
#
 
import wikipedia, pagegenerators, catlib
import re
from wikipedia import Page
site = wikipedia.getSite()
def main():
	yearnumber = 1998
	yearset1 = yearnumber - 1
	if yearnumber >= 2000:
		yearset2 = yearnumber - 2000
	else:
		yearset2 = yearnumber - 1900
	if yearset2 < 10:
		yearset2 = "0" + str(yearset2)
	yearsetfinal = str(yearset1) + "–" + str(yearset2)
	loopsat = True # loop
	
	for arg in wikipedia.handleArgs():
		if arg.startswith('-year'):
			if len(arg) == 5:
				yearnumber = int(wikipedia.input('What year do you want to start at?'))
			elif len(arg) > 5:
				yearnumber = int(arg[6:])

	while loopsat == True: #start loop
		if yearnumber >= 2011:
			return
		listpage = wikipedia.Page(site, "DFB Cup " + yearsetfinal)
		if listpage.exists() == True:
			wikipedia.setAction("Making redirects per [[Wikipedia:Bot requests/Archive 22#DFB_Cups|Botreq]]")
			wikipedia.output("> The target for [[" + str(yearnumber) + " DFB Cup Final]] exists")
			rd = "#REDIRECT [[DFB Cup " + yearsetfinal + "#Final]]"
			p1 = wikipedia.Page(site, str(yearnumber) + " DFB Cup Final")
			pagelist = [p1]

			for i in pagelist:
				if i.exists() == False:
					wikipedia.output(">>Creating [[%s]]" % i.title() )
					i.put(rd)
				else:
					wikipedia.output(">>[[en:%s]] already exsists" % i.title() )
		else:
			wikipedia.output(">DFB Cup " + yearsetfinal + " does not exist")
		#Redefine values
		yearnumber = yearnumber + 1
		yearset1 = yearnumber - 1
		yearset2 = yearnumber - 1900
		if yearnumber >= 2000:
			yearset2 = yearnumber - 2000
		else:
			yearset2 = yearnumber - 1900
		if yearset2 < 10:
			yearset2 = "0" + str(yearset2)
			yearsetfinal = str(yearset1) + "-" + str(yearset2)
        if '<div class="usermessage">' in text: #check talk page for messages
			wikipedia.output(u'NOTE: You have unread messages on %s' % self)
			wikipedia.crash() #stop

	wikipedia.output("Done!")
	wikipage = "User:Legoktm/BOTFAQ/Code/redir.py"
	code = "redir.py"
	legoktm.upload(wikipage, code)
def update():
	scriptpage = Page(site, "User:Legoktm/BOTFAQ/Code/redir.py")
	text = file('redir.py').read()
	text = '<source lang="python">\n' + text + '</sou' + 'rce>' # Split to confuse MW parser
	if scriptpage.get() != text:
    		summary = 'Updating source'
    	scriptpage.put(text, summary)


if __name__ == "__main__":
    try:
		main()
#        	update()
    finally:
        wikipedia.stopme()
