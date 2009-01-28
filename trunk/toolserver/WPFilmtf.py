#!/usr/bin/python
# -*- coding: utf-8  -*
 
#
# (C) Legoktm 2008-2009, MIT License
# 
 
import re, sys, time
import os
sys.path.append(os.environ['HOME'] + '/pyenwiki')
import wikipedia, pagegenerators, catlib

 
def process_article(page, tag):
		EditMsg = "Robot: Tagging {{Film|%s}}" %tag
		wikipedia.setAction(EditMsg)
		try:
			wikitext = page.get()
		except wikipedia.NoPage:
			page.put("{{Film|%s}}" %tag)
			return
		except wikipedia.IsRedirectPage:
			return
		if re.search(tag,wikitext,re.I):
			print "Skipping " + str(page)
			return
		# Fix Casing (Reduces the number of possible expressions)
		wikitext = re.compile(r'\{\{\s*(template:|)film', re.IGNORECASE).sub(r'{{Film', wikitext)
		state0 = wikitext
 
		# Add tf parameter
		wikitext = re.compile(r'\{\{\s*film(.*?)\}\}', re.IGNORECASE).sub(r'{{Film\1|%s}}' %tag, wikitext)
 
		wikipedia.showDiff(state0, wikitext)
 
		if (wikitext != state0):
			try:
				print 'Going to edit %s' %str(page)
				wikipedia.output(u'WRITE:	Adding %s bytes.' % str(len(wikitext)-len(state0)))
				page.put(wikitext)	
			except KeyboardInterrupt:
				sys.exit()
#			except:
#				wikipedia.output(u'ERROR:	Except raised while writing.')
 
def dogen(gen, tag):
	for page in gen:
		if not page.isTalkPage():
	        	page = page.toggleTalkPage()
		process_article(page, tag)
 
def docat(tag, cat2):
	site  = wikipedia.getSite()
	cat = catlib.Category(site, cat2)
	gen = pagegenerators.CategorizedPageGenerator(cat)
	dogen(gen, tag)
	wikipedia.output(u'\nFinished with Category:' + cat2 + '.\n')
	print 'Waiting 10 seconds'
	time.sleep(10)
 
 
def main():
 	
 	docat('American-task-force=yes','Lists of American films by year')
 	docat('Argentine-task-force=yes','Lists of Argentine films by year')
 	docat('British-task-force=yes','Lists of British films by year')
 	docat('French-task-force=yes','Lists of French films by year')
 	docat('Chinese-task-force=yes','Lists of Hong Kong films by year')
 	docat('Italian-task-force=yes','Lists of Italian films by year')
 	docat('Japanese-task-force=yes','Lists of Japanese films by year')
 	docat('Korean-task-force=yes','Lists of South Korean films by year')
 	docat('Spanish-task-force=yes','Lists of Spanish films by year')
 	
if __name__ == "__main__":
	try:
		main()
	finally:
		wikipedia.stopme()
