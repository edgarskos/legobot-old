#!usr/bin/python
# -*- coding: utf-8  -*
 
#
# (C) Legoktm 2008, MIT License
# 
 
import re, sys
import os
import commonfixes #dispenser's common fixes
sys.path.append(os.environ['HOME'] + '/stuffs/pywiki/pylegoktm')
import wikipedia
site = wikipedia.getSite()
page = wikipedia.Page(site, 'User:Legoktm/Bot')
wikitext = page.get()
wikitext = re.compile(r'\n==New listings==', re.IGNORECASE).sub(r'\n*[[/{{subst:#time:Y F j|-14 days}}]]\n==New listings==', wikitext)
EditMsg = 'Adding new day to holding cell'
wikipedia.showDiff(page.get(), wikitext)
wikipedia.setAction(EditMsg)
page.put(wikitext)