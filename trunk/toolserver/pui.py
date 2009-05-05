#!usr/bin/python
# -*- coding: utf-8  -*
 
#
# (C) Legoktm 2008-2009, MIT License
# 
 
import re, sys, os
sys.path.append(os.environ['HOME'] + '/pywiki')
#sys.path.append('/Users/kman/projects/pywikibot')
import wiki
wiki.setUser('Legobot')
page = wiki.Page('Wikipedia:Possibly unfree images')
try:
	wikitext = state0 = page.get()
except wiki.IsRedirectPage:
	page = wiki.Page('Wikipedia:Possibly unfree files')
	wikitext = state0 = page.get()	
wikitext = re.compile(r'\n==New listings==', re.IGNORECASE).sub(r'\n*[[/{{subst:#time:Y F j|-14 days}}]]\n==New listings==', wikitext)
EditMsg = 'Adding new day to holding cell'
wiki.showDiff(state0, wikitext)
page.put(wikitext,EditMsg)
