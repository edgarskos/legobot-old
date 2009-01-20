#!usr/bin/python
# -*- coding: utf-8  -*
 
#
# (C) Legoktm 2008, MIT License
# 
 
import re, sys, os
sys.path.append(os.environ['HOME'] + '/pyenwiki')
import wikipedia
site = wikipedia.getSite()
page = wikipedia.Page(site, 'Wikipedia:Possibly unfree images')
wikitext = state0 = page.get()
wikitext = re.compile(r'\n==New listings==', re.IGNORECASE).sub(r'\n*[[/{{subst:#time:Y F j|-14 days}}]]\n==New listings==', wikitext)
EditMsg = 'Adding new day to holding cell'
wikipedia.showDiff(state0, wikitext)
wikipedia.setAction(EditMsg)
page.put(wikitext)