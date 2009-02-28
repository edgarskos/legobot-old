#!usr/bin/python
# -*- coding: utf-8  -*
 
#
# (C) Legoktm 2008-2009, MIT License
# 
 
import re
sys.path.append(os.environ['HOME'] + '/pywiki')
import wiki
page = wiki.Page('Wikipedia:Possibly unfree images')
wikitext = state0 = page.get()
wikitext = re.compile(r'\n==New listings==', re.IGNORECASE).sub(r'\n*[[/{{subst:#time:Y F j|-14 days}}]]\n==New listings==', wikitext)
EditMsg = 'Adding new day to holding cell'
wiki.showDiff(state0, wikitext)
page.put(wikitext,EditMsg)