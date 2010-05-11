#!usr/bin/python
# -*- coding: utf-8  -*
 
#
# (C) Legoktm 2008-2010, MIT License
# 
 
import re, sys, os
import wikipedia as wiki
site=wiki.getSite()
page = wiki.Page(site,'Wikipedia:Possibly unfree files')
wikitext = re.compile(r'\n==New listings==', re.IGNORECASE).sub(r'\n*[[/{{subst:#time:Y F j|-14 days}}]]\n==New listings==', wikitext)
EditMsg = 'Adding new day to holding cell'
page.put(wikitext,EditMsg)
